# Microservicio Marcador de Fútbol

Servicio **independiente** del monolito Django. Tiene su propia base PostgreSQL (contenedor aparte) y replica el modelo de equipos **`Seleccion`** y partidos **`Partido`** del proyecto principal.

## Arquitectura

```
marcador-service/
├── app/
│   ├── models/          # seleccion, partido (mismo esquema conceptual)
│   ├── schemas/         # DTOs Pydantic
│   ├── routers/         # API REST
│   ├── services/        # Lógica de negocio
│   ├── seed.py          # 37 selecciones Mundial 2026
│   └── main.py
├── alembic/             # Migraciones SQL
├── docker-compose.yml   # Postgres :5433 + API :8001
└── Dockerfile
```

| Recurso | Proyecto principal | Microservicio |
|---------|-------------------|---------------|
| Puerto DB | 5432 (`quiniela`) | **5433** (`marcador_db`) |
| Puerto API | 8000 (Django) | **8001** (FastAPI) |
| Contenedor DB | `postgres-db` | `marcador-postgres` |

## Inicio rápido con Docker

```bash
cd marcador-service
copy .env.example .env
docker compose up -d --build
```

- API: http://localhost:8001/docs
- Health: http://localhost:8001/health

## Desarrollo local (sin Docker para la API)

```bash
cd marcador-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# Solo base de datos
docker compose up -d marcador-postgres

alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --port 8001
```

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/selecciones/` | Listar equipos |
| POST | `/api/selecciones/` | Crear selección |
| GET | `/api/partidos/` | Listar partidos |
| GET | `/api/partidos/en-vivo` | Marcadores en juego (con banderas/país) |
| PATCH | `/api/partidos/{id}/marcador` | Actualizar goles (como `actualizar-resultado`) |
| GET | `/api/partidos/por-equipo?equipo_id=` | Partidos de un equipo |

### Ejemplo: actualizar marcador

```bash
curl -X PATCH http://localhost:8001/api/partidos/1/marcador \
  -H "Content-Type: application/json" \
  -d "{\"gol_local\": 2, \"gol_visitante\": 1, \"estado\": \"en_juego\"}"
```

## Integración con el proyecto principal

Este servicio **no comparte base de datos** con la quiniela. Los `id_seleccion` pueden diferir entre ambos sistemas. Para sincronizar en el futuro puedes:

1. Exponer un endpoint de sincronización por `pais` (nombre único).
2. O consumir eventos cuando cambie el marcador y propagar al Django vía webhook.

El contrato de datos (campos de `Seleccion` y `Partido`) está alineado con `backend/partidos/models.py`.
