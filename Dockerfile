# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el código y archivos necesarios al contenedor
COPY ./ /app/

# Asegúrate de que el archivo requirements.txt esté presente
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto adecuado (si deseas que sea accesible por HTTP)
EXPOSE 5000

# Establece el comando para ejecutar el script Python
CMD ["python3", "predicciones.py"]
