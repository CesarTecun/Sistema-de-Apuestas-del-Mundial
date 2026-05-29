# Sistema de Apuestas del Mundial 2026

Aplicación full-stack para administrar quinielas y marcadores del Mundial 2026:

- API REST con **Django 5.2 + DRF** para autenticación, ligas, pronósticos, posiciones y premios.
- **Frontend React 18** para la experiencia de usuarios finales y administradores.
- **Microservicio marcador (FastAPI + PostgreSQL)** independiente para sincronizar resultados en tiempo real.

---

## Arquitectura

| Módulo | Descripción |
| --- | --- |
| `backend/` | Proyecto Django con apps para usuarios, ligas, partidos, pronósticos, posiciones, historial, premios y seguridad. Incluye JWT, tracking de sesiones, ratelimiting y servicios auxiliares. |
| `frontend/` | SPA React con contextos, hooks personalizados y componentes reutilizables agrupados por páginas. |
| `marcador-service/` | Microservicio FastAPI que expone endpoints para registrar marcadores y publica webhooks al backend. Usa su propio Postgres (puerto 5433). |
| `infrastructure/` | Docker Compose, Dockerfile y configuración de nginx para despliegues. |
| `database/` | Scripts para roles, backups y utilidades (p.ej. marcar migraciones como aplicadas). |
| `scripts/` | Automatizaciones para levantar Docker, crear usuarios admin y validar migraciones. |

Estructura general:

```
Sistema de Apuestas del Mundial/
├── backend/
├── frontend/
├── marcador-service/
├── config/
├── database/
├── infrastructure/
├── scripts/
└── README.md
```

---

## Prerrequisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (local o remoto)
- Docker y Docker Compose (opcional, para la configuración automatizada)

---

## Configuración inicial

1. **Clonar y entrar al directorio**
   ```bash
   git clone <url>
   cd Sistema-de-Apuestas-del-Mundial
   ```

2. **Backend**
   ```bash
   python -m venv venv311
   venv311\Scripts\activate  # o source venv311/bin/activate
   pip install -r requirements.txt
   ```

3. **Frontend**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Variables de entorno**
   ```bash
   copy config\.env.example .env   # Windows
   # o
   cp config/.env.example .env
   ```
   Ajusta los valores principales:
   ```env
   DEBUG=True
   SECRET_KEY=tu-clave
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=quiniela
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   FRONTEND_URL=http://localhost:3000
   MARCADOR_SERVICE_URL=http://localhost:8001
   ```

5. **Base de datos**
   - Crea la base `quiniela` en PostgreSQL.
   - Ejecuta `python manage.py migrate` para generar el esquema (o usa los scripts de `database/` si restauras un dump existente y solo deseas "fijar" migraciones).

---

## Ejecución en desarrollo

| Servicio | Comando | URL |
| --- | --- | --- |
| Backend | `python manage.py runserver` | http://localhost:8000 |
| Frontend | `cd frontend && npm start` | http://localhost:3000 |
| Microservicio marcador | `cd marcador-service && uvicorn app.main:app --reload --port 8001` | http://localhost:8001 |

Para el microservicio asegúrate de tener su `.env` y Postgres (puerto 5433 por defecto) listos. Sus detalles están en `marcador-service/README.md`.

---

## Ejecución con Docker (opcional)

1. Levanta la infraestructura base (PostgreSQL contenedorizado, etc.):
   ```bash
   docker-compose -f infrastructure/docker-compose.yml up -d
   ```

2. Corre el script de configuración para esperar la BD, aplicar migraciones y crear el superusuario `admin/admin123`:
   ```bash
   python scripts/docker_setup.py
   ```

3. Scripts de conveniencia:
   - Windows: `scripts\docker_start.bat`
   - Linux/Mac: `./scripts/docker_start.sh`

---

## Scripts relevantes

| Script | Descripción |
| --- | --- |
| `scripts/check_migrations.py` | Detecta migraciones pendientes o sin commitear. |
| `scripts/create_admin.py` | Crea un usuario admin en la base actual. |
| `database/fake_migrations.py` | Marca migraciones como aplicadas cuando se restauró un dump. |
| `scripts/docker_setup.py` | Automatiza la configuración del backend dentro de Docker. |

---

## Despliegue en Railway

Este proyecto está configurado para desplegar el backend y frontend en Railway, conectándose a bases de datos PostgreSQL existentes (NO se despliegan nuevas BDs en Railway).

### Prerrequisitos

- Cuenta en Railway (https://railway.app)
- Bases de datos PostgreSQL existentes (principal y microservicio marcador)
- Repositorio en GitHub conectado a Railway

### Configuración del Backend

1. **Variables de entorno en Railway**
   - Crea un nuevo proyecto en Railway desde tu repositorio GitHub
   - Agrega un servicio "Python" para el backend
   - Configura las siguientes variables de entorno en el dashboard de Railway:

   ```env
   # Database (PostgreSQL existente)
   DB_NAME=quiniela
   DB_USER=tu_usuario
   DB_PASSWORD=tu_password
   DB_HOST=tu_host_postgresql
   DB_PORT=5432
   DB_SSLMODE=require

   # Django Settings
   DEBUG=False
   SECRET_KEY=tu-secret-key-seguro
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Frontend URL (para CORS)
   FRONTEND_URL=https://tu-frontend-url.railway.app

   # Microservicio Marcador
   MARCADOR_SERVICE_URL=http://tu-marcador-service-url
   MARCADOR_SERVICE_TIMEOUT=30

   # Email (opcional)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=tu_email@gmail.com
   EMAIL_HOST_PASSWORD=tu_contraseña_aplicacion
   ```

2. **Archivos creados para Railway**
   - `backend/Procfile` - Configura el comando de inicio
   - `backend/start.sh` - Ejecuta migraciones antes de iniciar el servidor
   - `requirements.txt` - Incluye gunicorn y whitenoise para producción

### Configuración del Frontend

1. **Variables de entorno en Railway**
   - Agrega un servicio "Node.js" para el frontend
   - Configura la variable de entorno:

   ```env
   REACT_APP_API_URL=https://tu-backend-url.railway.app
   ```

2. **Archivos creados para Railway**
   - `frontend/Procfile` - Configura el build y servidor estático
   - `frontend/package.json` - Incluye `serve` para servir el build

### Archivos de configuración

- `railway.json` - Configuración general del proyecto en Railway
- `.env.example.railway` - Plantilla de variables de entorno para Railway

### Pasos de despliegue

1. **Conectar repositorio a Railway**
   - En Railway, selecciona "New Project" → "Deploy from GitHub repo"
   - Selecciona tu repositorio

2. **Desplegar el backend**
   - Railway detectará automáticamente el directorio `backend/`
   - Configura las variables de entorno mencionadas
   - El despliegue ejecutará automáticamente las migraciones

3. **Desplegar el frontend**
   - Agrega un nuevo servicio "Node.js" al proyecto
   - Configura el directorio raíz en `frontend/`
   - Configura `REACT_APP_API_URL` con la URL del backend
   - El despliegue construirá y servirá la aplicación React

4. **Obtener URLs de Railway**
   - Después del despliegue, Railway proporcionará URLs como:
     - Backend: `https://backend-name.railway.app`
     - Frontend: `https://frontend-name.railway.app`
   - Actualiza las variables de entorno con estas URLs

### Notas importantes

- **Bases de datos**: Las BDs principal y del microservicio marcador NO se despliegan en Railway. Usa bases de datos existentes (Neon, Railway PostgreSQL, o tu propio servidor).
- **Migraciones**: Se ejecutan automáticamente durante el despliegue del backend.
- **Archivos estáticos**: Whitenoise sirve los archivos estáticos del backend.
- **CORS**: Configurado dinámicamente desde `FRONTEND_URL`.

---



