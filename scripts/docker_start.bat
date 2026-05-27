@echo off
REM Script de inicio para Docker + Django (Windows)
REM Uso: scripts\docker_start.bat

echo Iniciando entorno Docker para Sistema de Apuestas del Mundial...
echo ============================================================

REM 1. Iniciar Docker Compose
echo Iniciando contenedores Docker...
cd infrastructure
docker-compose up -d

if %errorlevel% neq 0 (
    echo Error iniciando Docker Compose
    pause
    exit /b 1
)

echo Contenedores iniciados

REM 2. Esperar a que PostgreSQL esté listo
echo Esperando a que PostgreSQL esté listo...
timeout /t 10 /nobreak > nul

REM 3. Ejecutar script de configuración
echo Configurando Django...
cd ..
python scripts\docker_setup.py

if %errorlevel% equ 0 (
    echo.
    echo Entorno listo
    echo.
    echo Para iniciar el servidor de desarrollo:
    echo    python manage.py runserver
    echo.
    echo Acceso:
    echo    Frontend: http://localhost:3000
    echo    Admin: http://localhost:8000/admin (admin/admin123)
) else (
    echo Error en la configuración
    pause
    exit /b 1
)

pause
