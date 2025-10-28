# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    Flask==3.1.2 \
    gunicorn==23.0.0 \
    blinker==1.9.0 \
    click==8.3.0 \
    itsdangerous==2.2.0 \
    Jinja2==3.1.6 \
    MarkupSafe==3.0.3 \
    packaging==25.0 \
    Werkzeug==3.1.3

# Copy project files
COPY . /app

# Expose Flask’s internal port
EXPOSE 8000

# Initialize DB automatically if missing, then run gunicorn
CMD bash -c '\
  if [ ! -f "instance/liendans.sqlite" ]; then \
    echo "[INIT] Creating database..."; \
    flask --app liendans init-db; \
  fi && \
  exec gunicorn -b 0.0.0.0:8000 liendans.wsgi:app'

