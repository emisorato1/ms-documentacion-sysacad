# Usamos Python 3.12-bookworm (similar a SYSACAD para compatibilidad con WeasyPrint)
FROM python:3.12.10-bookworm

ENV FLASK_CONTEXT=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Agregamos el entorno virtual al PATH
ENV PATH="/home/flaskapp/.venv/bin:$PATH"

# 1. Copiamos 'uv' directamente desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Creamos el usuario
RUN useradd --create-home --home-dir /home/flaskapp flaskapp

# Instalamos dependencias del sistema (incluyendo las de WeasyPrint como en SYSACAD)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-psycopg2 \
    curl \
    # Dependencias runtime para WeasyPrint/GTK/Cairo/Pango
    libglib2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libpangoft2-1.0-0 \
    libffi-dev shared-mime-info \
    libxml2 libxslt1.1 \
    libjpeg62-turbo zlib1g \
    libfreetype6 libharfbuzz0b libfribidi0 \
    fonts-liberation fonts-dejavu fonts-freefont-ttf \
    libcairo-gobject2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/flaskapp

# Cambiamos al usuario no-root
USER flaskapp

# 2. Copiamos archivos de dependencias CON PERMISOS para el usuario flaskapp
COPY --chown=flaskapp:flaskapp ./pyproject.toml ./uv.lock ./

# Ejecutamos uv sync
RUN uv sync

# 3. Copiamos el código de la aplicación
COPY --chown=flaskapp:flaskapp ./app ./app
COPY --chown=flaskapp:flaskapp ./wsgi.py .
COPY --chown=flaskapp:flaskapp ./app.py .

# Variables de entorno
ENV VIRTUAL_ENV="/home/flaskapp/.venv"

EXPOSE 5000

CMD ["granian", "--port", "5000", "--host", "0.0.0.0", "--http", "auto", "--workers", "4", "--blocking-threads", "4", "--backlog", "2048", "--interface", "wsgi", "wsgi:app"]