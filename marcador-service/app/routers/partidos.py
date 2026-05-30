from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.partido import (
    MarcadorUpdate,
    PartidoControlUpdate,
    PartidoCreate,
    PartidoMarcadorResponse,
    PartidoResponse,
    PartidoUpdate,
)
from app.services import partido_service

router = APIRouter(prefix="/partidos", tags=["Partidos / Marcador"])


@router.get("/", response_model=list[PartidoResponse])
def listar_partidos(
    estado: Optional[str] = Query(None, description="programado | en_juego | finalizado"),
    fk_id_liga: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return partido_service.list_partidos(db, estado=estado, fk_id_liga=fk_id_liga)


@router.get("/en-vivo", response_model=list[PartidoMarcadorResponse])
def partidos_en_vivo(db: Session = Depends(get_db)):
    partidos = partido_service.list_partidos(db, estado="en_juego")
    return partido_service.enrich_marcador_list(db, partidos)


@router.get("/todos", response_model=list[PartidoMarcadorResponse])
def todos_partidos(db: Session = Depends(get_db)):
    """Obtiene todos los partidos para el marcador (sin filtrar por estado)"""
    partidos = partido_service.list_partidos(db)
    return partido_service.enrich_marcador_list(db, partidos)


@router.get("/por-equipo", response_model=list[PartidoResponse])
def partidos_por_equipo(equipo_id: int = Query(...), db: Session = Depends(get_db)):
    return partido_service.partidos_por_equipo(db, equipo_id)


@router.get("/{id_partido}", response_model=PartidoMarcadorResponse)
def obtener_partido(id_partido: int, db: Session = Depends(get_db)):
    partido = partido_service.get_partido(db, id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_service.enrich_marcador_single(db, partido)


@router.post("/", response_model=PartidoResponse, status_code=201)
def crear_partido(data: PartidoCreate, db: Session = Depends(get_db)):
    try:
        return partido_service.create_partido(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/{id_partido}", response_model=PartidoResponse)
def actualizar_partido(id_partido: int, data: PartidoUpdate, db: Session = Depends(get_db)):
    partido = partido_service.get_partido(db, id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_service.update_partido(db, partido, data)


@router.patch("/{id_partido}/marcador", response_model=PartidoMarcadorResponse)
def actualizar_marcador(id_partido: int, data: MarcadorUpdate, db: Session = Depends(get_db)):
    """Equivalente a actualizar-resultado del backend principal."""
    partido = partido_service.get_partido(db, id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    partido = partido_service.actualizar_marcador(db, partido, data)
    return partido_service.enrich_marcador_single(db, partido)


@router.delete("/{id_partido}", status_code=204)
def eliminar_partido(id_partido: int, db: Session = Depends(get_db)):
    partido = partido_service.get_partido(db, id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    partido_service.delete_partido(db, partido)


@router.patch("/{id_partido}/control", response_model=PartidoMarcadorResponse)
def controlar_partido(id_partido: int, data: PartidoControlUpdate, db: Session = Depends(get_db)):
    """
    Controla el partido en vivo: iniciar, pausar, cambiar tiempo, agregar tiempo extra
    """
    print(f"Router controlar_partido: id_partido={id_partido}, data={data}")
    partido = partido_service.get_partido(db, id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    partido = partido_service.controlar_partido(db, partido, data)
    return partido_service.enrich_marcador_single(db, partido)
