from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/ejecutar_predicciones', methods=['GET'])
def ejecutar_predicciones():
    try:
        # Ejecutar el script en segundo plano
        subprocess.Popen(['python3', 'predicciones.py'])
        return "Predicciones están siendo procesadas en segundo plano.", 200
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
