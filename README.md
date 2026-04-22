# Sistema de Apuestas del Mundial 2026

## Stack Tecnológico
- **Backend**: Python + Django + Django REST Framework
- **Frontend**: React + Node.js
- **Base de Datos**: PostgreSQL (recomendado)

## Estructura del Proyecto
```
Sistema de Apuestas del Mundial/
|-- backend/              # Proyecto Django
|   |-- manage.py
|   |-- backend/          # Configuración principal
|   |-- autenticacion/    # App de autenticación
|   |-- usuarios/         # App de usuarios
|   |-- ligas/            # App de ligas
|   |-- partidos/         # App de partidos
|   |-- pronosticos/      # App de pronósticos
|   |-- posiciones/       # App de rankings
|   |-- premios/          # App de premios
|   |-- historialganador/ # App de historial
|   `-- correos/          # App de correos (futuro)
|-- frontend/             # Proyecto React
|   |-- src/
|   |   |-- config/       # Configuración centralizada
|   |   |-- contextos/    # Contextos de React
|   |   |-- hooks/        # Hooks personalizados
|   |   |-- componentes/  # Componentes reutilizables
|   |   |-- paginas/      # Páginas principales
|   |   |-- servicios/    # Servicios de API
|   |   `-- estilos/      # Estilos globales
|   |-- public/
|   `-- package.json
|-- database/             # Scripts y archivos de base de datos
|   |-- init-db.sql       # Script de inicialización de BD
|   |-- migrations/       # Migraciones manuales
|   `-- backups/          # Respaldos de BD
|-- infrastructure/       # Configuración de infraestructura
|   |-- docker-compose.yml # Configuración Docker
|   |-- Dockerfile        # Imagen Docker
|   `-- nginx/            # Configuración nginx (futuro)
|-- config/               # Configuración centralizada
|   `-- .env.example     # Ejemplo de variables de entorno
|-- requirements.txt      # Dependencias Python
`-- README.md

## Instalación para Desarrollo

### Prerrequisitos
- Python 3.10+
- Node.js 18+
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd "Sistema de Apuestas del Mundial"
```

2. **Instalar dependencias del Backend**
```bash
pip install -r requirements.txt
```

3. **Instalar dependencias del Frontend**
```bash
cd frontend
npm install
cd ..
```

### Ejecutar en Desarrollo

1. **Backend (Django)**
```bash
python manage.py migrate
python manage.py runserver
```
El backend correrá en: http://localhost:8000

2. **Frontend (React)**
```bash
cd frontend
npm start
```
El frontend correrá en: http://localhost:3000

## Configuración de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:
```bash
cp config/.env.example .env
```

Editar el archivo `.env` con tus configuraciones:
```
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=quiniela
DB_USER=postgres
DB_PASSWORD=PASSWORD
DB_HOST=localhost
DB_PORT=5432
```

## Ejecutar con Docker

### Iniciar base de datos PostgreSQL
```bash
cd infrastructure
docker-compose up -d
```

### Detener base de datos
```bash
cd infrastructure
docker-compose down
```

## Flujo de Trabajo con Git

1. Cada desarrollador crea su rama: `git checkout -b feature/nueva-funcionalidad`
2. Realiza cambios y commitea: `git add . && git commit -m "Descripción del cambio"`
3. Sube al repositorio: `git push origin feature/nueva-funcionalidad`
4. Crea Pull Request para revisión

## Notas Importantes
- Este proyecto está diseñado para ser desarrollado por equipos
- Mantener la estructura de carpetas tal como está
- Seguir las convenciones de nomenclatura de Django y React
