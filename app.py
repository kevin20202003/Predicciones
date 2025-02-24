from flask import Flask, request
from celery import Celery

app = Flask(__name__)

# Configuración de Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def ejecutar_predicciones_task():
    # Llamar al script de predicciones
    result = subprocess.run(['python3', 'predicciones.py'], capture_output=True, text=True)
    return result.stdout

@app.route('/ejecutar_predicciones', methods=['POST'])
def ejecutar_predicciones():
    task = ejecutar_predicciones_task.apply_async()
    return f'Predicciones en proceso... ID de tarea: {task.id}'

if __name__ == "__main__":
    app.run(debug=True)
