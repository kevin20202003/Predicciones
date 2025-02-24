from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/ejecutar_predicciones', methods=['GET'])
def ejecutar_predicciones():
    try:
        # Ejecutar el script predicciones.py
        result = subprocess.run(['python3', 'predicciones.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return "Predicciones ejecutadas correctamente", 200
        else:
            return f"Error al ejecutar el script: {result.stderr}", 500
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
