#!/bin/bash

# Script de inicio para Docker + Django
# Uso: ./scripts/docker_start.sh

echo "Iniciando entorno Docker para Sistema de Apuestas del Mundial..."
echo "=" * 60

# 1. Iniciar Docker Compose
echo "Iniciando contenedores Docker..."
cd infrastructure
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "Error iniciando Docker Compose"
    exit 1
fi

echo "Contenedores iniciados"

# 2. Esperar a que PostgreSQL esté listo
echo "Esperando a que PostgreSQL esté listo..."
sleep 10

# 3. Ejecutar script de configuración
echo "Configurando Django..."
cd ..
python scripts/docker_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Entorno listo"
    echo ""
    echo "Para iniciar el servidor de desarrollo:"
    echo "   python manage.py runserver"
    echo ""
    echo "Acceso:"
    echo "   Frontend: http://localhost:3000"
    echo "   Admin: http://localhost:8000/admin (admin/admin123)"
else
    echo "Error en la configuración"
    exit 1
fi
