from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import Base, engine
from app.routers import partidos, selecciones, sync


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Marcador de Fútbol",
    description="Microservicio independiente de marcador en vivo. Modelo de equipos alineado con Seleccion del proyecto principal.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(selecciones.router, prefix="/api")
app.include_router(partidos.router, prefix="/api")
app.include_router(sync.router, prefix="/api")

# Montar archivos estáticos
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/health")
def health():
    return {"status": "ok", "service": "marcador"}


@app.get("/api/ping-db/")
def ping_db():
    """
    Endpoint para mantener el compute de Neon activo.
    Ejecuta SELECT 1 para evitar scale-to-zero (cold-start).
    """
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "db": "reachable"}


@app.get("/")
def read_root():
    return FileResponse(str(static_dir / "index.html"))
