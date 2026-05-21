from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/health")
def health():
    return {"status": "ok", "service": "marcador"}
