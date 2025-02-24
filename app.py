from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/ejecutar_predicciones', methods=['GET'])
def ejecutar_predicciones():
    try:
        # Definir la ruta completa del script si es necesario
        script_path = os.path.join(os.getcwd(), 'predicciones.py')  # Asegúrate de que la ruta sea correcta
        
        # Ejecutar el script predicciones.py
        result = subprocess.run(['python3', script_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            return "Predicciones ejecutadas correctamente", 200
        else:
            return f"Error al ejecutar el script: {result.stderr}", 500
    except Exception as e:
        return f"Error inesperado: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
