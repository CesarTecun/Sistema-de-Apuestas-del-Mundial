#!/bin/bash
# Script de inicio para Railway
# Ejecuta migraciones y luego inicia el servidor

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Iniciando servidor con gunicorn..."
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --threads 4 --timeout 120
