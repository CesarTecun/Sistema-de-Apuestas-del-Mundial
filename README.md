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

## Pruebas

```bash
# Backend
python manage.py test

# Frontend
npm run lint
npm test
```

Hay pruebas adicionales para lógica de pronósticos en `test_cierre_pronosticos.py`.

---

## Flujo de trabajo recomendado

1. Crear rama desde `main`: `git checkout -b feature/mi-cambio`.
2. Realizar cambios y asegurarse de que backend/frontend compilen.
3. Ejecutar `scripts/check_migrations.py` para prevenir migraciones accidentales.
4. `git commit`, `git push` y abrir Pull Request.

---

## Recursos adicionales

- Documentación del microservicio marcador: [marcador-service/README.md](marcador-service/README.md)
- Guías de migraciones: `docs/MIGRATIONS_GUIDE.md` y `docs/MIGRATIONS_SETUP.md`
- Scripts y utilidades: revisar el directorio `scripts/`

---

¿Necesitas ayuda? Revisa los archivos mencionados o abre un issue describiendo el contexto. ¡Bienvenido al proyecto!
