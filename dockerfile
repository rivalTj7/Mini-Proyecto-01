# ==============================================================================
# Dockerfile para Análisis de Videojuegos
# ==============================================================================
# Imagen base: Python 3.11 slim (ligera y eficiente)
FROM python:3.11-slim

# Información del mantenedor
LABEL maintainer="estudiante@proyecto.com"
LABEL description="Análisis de Videojuegos - Mini Proyecto Python"
LABEL version="1.0"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para matplotlib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY analisis_videojuegos.py .

# Crear directorio para datos y resultados
RUN mkdir -p /app/data /app/output

# Volúmenes para persistencia de datos
VOLUME ["/app/data", "/app/output"]

# Puerto para Jupyter (opcional, por si quieres usar notebooks)
EXPOSE 8888

# Comando por defecto: ejecutar el análisis
CMD ["python", "analisis_videojuegos.py"]