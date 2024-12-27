# Usa una imagen base de PHP con Apache
FROM php:8.0-apache

# Actualiza el sistema y prepara las herramientas necesarias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    --no-install-recommends && \
    docker-php-ext-install pdo_pgsql pgsql && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /var/www/html

# Copia el código PHP al contenedor
COPY ./ /var/www/html/

# Asegúrate de que el archivo requirements.txt esté presente
# Instala las dependencias de Python
RUN if [ -f "requirements.txt" ]; then pip3 install -r requirements.txt; fi

# Cambia los permisos para el usuario del servidor web
RUN chown -R www-data:www-data /var/www/html

# Expone el puerto adecuado
EXPOSE 80

# Establece el comando por defecto para iniciar Apache
CMD ["apache2-foreground"]