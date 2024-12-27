import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from sqlalchemy import create_engine
import time
import logging

# Configuración de logging
logging.basicConfig(filename='predicciones.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de conexión con SQLAlchemy
db_uri = "mysql+mysqlconnector://u636023223_sensorwatch:SensorWatch99@mysql.hostinger.com/u636023223_invernadero"
engine = create_engine(db_uri)

def obtener_datos(tabla):
    """Obtiene los datos históricos desde la base de datos."""
    try:
        query = f"SELECT * FROM {tabla}"
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        logging.error(f"Error al obtener datos de la tabla {tabla}: {e}")
        raise

def entrenar_y_predecir(tabla, variables, horizonte, columna_fecha):
    """Entrena un modelo y predice valores futuros."""
    datos = obtener_datos(tabla)
    for columna in variables + [columna_fecha]:
        if columna not in datos.columns:
            raise ValueError(f"La columna '{columna}' no existe en la tabla '{tabla}'")

    datos[columna_fecha] = pd.to_datetime(datos[columna_fecha])
    datos = datos.sort_values(columna_fecha)

    X = datos[variables].values
    y = datos[variables].shift(-1).fillna(0).values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    joblib.dump(modelo, f"modelo_{tabla}.pkl")

    ultimos_datos = datos[variables].iloc[-horizonte:].values
    predicciones = modelo.predict(ultimos_datos)

    fechas_futuras = [pd.Timestamp.now().replace(microsecond=0) + pd.Timedelta(days=i) for i in range(1, horizonte + 1)]

    predicciones_df = pd.DataFrame(predicciones, columns=variables)
    predicciones_df[columna_fecha] = fechas_futuras

    return predicciones_df

def guardar_predicciones(tabla, predicciones, columna_fecha):
    """Guarda las predicciones en la base de datos."""
    tabla_predicciones = f"{tabla}_predicciones"
    with engine.connect() as conn:
        try:
            predicciones.to_sql(tabla_predicciones, con=conn, if_exists='append', index=False)
            logging.info(f"Predicciones guardadas exitosamente en la tabla {tabla_predicciones}.")
        except Exception as e:
            logging.error(f"Error al guardar predicciones en la tabla {tabla_predicciones}: {e}")
            raise

# Ciclo principal con sincronización de tareas
while True:
    try:
        # Procesar predicciones para todas las tablas
        tareas = [
            ('datos_suelo', ['temperatura', 'humedad', 'PH'], 7, 'created_at', 6 * 3600),  # Cada 6 horas
            ('datos_ambiente', ['temperatura_amb', 'humedad_amb', 'lux'], 7, 'created_at', 6 * 3600),  # Cada 6 horas
            ('datos_meteorologicos', ['temp', 'humidity', 'pressure', 'wind_speed'], 30, 'date', 12 * 3600)  # Cada 12 horas
        ]
        for tabla, variables, horizonte, columna_fecha, intervalo in tareas:
            predicciones = entrenar_y_predecir(tabla, variables, horizonte, columna_fecha)
            guardar_predicciones(tabla, predicciones, columna_fecha)
            logging.info(f"Predicciones de la tabla {tabla} actualizadas.")
        logging.info("Todas las tareas completadas. Esperando 6 horas...")
        time.sleep(6 * 3600)  # Esperar 6 horas antes de la siguiente iteración
    except Exception as e:
        logging.error(f"Error en el ciclo principal: {e}")
        logging.info("Reintentando en 1 hora...")
        time.sleep(3600)  # Esperar 1 hora en caso de error
