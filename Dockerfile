# ─────────────────────────────────────────────────────────────────
# Dockerfile: Imagen base para la aplicación y las pruebas
# Usa Python 3.12 slim para reducir el tamaño de la imagen
# ─────────────────────────────────────────────────────────────────

# Usar Bookworm (Debian 12) explícitamente.
# python:3.12-slim sin tag puede resolverse a Trixie (Debian 13) donde
# los paquetes de fuentes que Playwright necesita (ttf-unifont, ttf-ubuntu-font-family)
# ya no existen, causando un error en el build.
FROM python:3.12-slim-bookworm

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para Playwright y psycopg2
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar las dependencias de Python primero
# (esto aprovecha el caché de capas de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar los navegadores de Playwright para las pruebas E2E
RUN playwright install --with-deps chromium

# Copiar el resto del código fuente al contenedor
COPY . .

# Exponer el puerto donde correrá la aplicación FastAPI
EXPOSE 8000

# Comando por defecto: arrancar el servidor de la API
CMD ["uvicorn", "src.interfaz.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
