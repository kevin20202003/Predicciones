# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Crea un entorno virtual y activa el entorno
RUN python3 -m venv /venv

# Establece la variable de entorno para usar el entorno virtual
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copia el código y archivos necesarios al contenedor
COPY ./ /app/

# Instala las dependencias dentro del entorno virtual
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto adecuado (si deseas que sea accesible por HTTP)
EXPOSE 5000

# Establece el comando para ejecutar el script Python
CMD ["python3", "predicciones.py"]
