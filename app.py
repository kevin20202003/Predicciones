import logging
from flask import Flask
import subprocess

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/ejecutar_predicciones', methods=['GET'])
def ejecutar_predicciones():
    try:
        # Ejecutar el script y capturar errores
        result = subprocess.run(['python3', 'predicciones.py'], capture_output=True, text=True)
        if result.returncode == 0:
            app.logger.info("Predicciones ejecutadas correctamente")
            return f"Predicciones ejecutadas correctamente: {result.stdout}", 200
        else:
            app.logger.error(f"Error al ejecutar el script: {result.stderr}")
            return f"Error al ejecutar el script: {result.stderr}", 500
    except Exception as e:
        app.logger.error(f"Error interno: {str(e)}")
        return f"Error interno: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
