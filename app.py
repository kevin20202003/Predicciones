from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/ejecutar_predicciones', methods=['POST'])
def ejecutar_predicciones():
    try:
        # Llamar al script de predicciones directamente
        result = subprocess.run(['python3', 'predicciones.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return f"Predicciones ejecutadas correctamente. {result.stdout}", 200
        else:
            return f"Error al ejecutar el script: {result.stderr}", 500
    except Exception as e:
        return f"Error interno: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
