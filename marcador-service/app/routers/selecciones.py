from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.seleccion import SeleccionCreate, SeleccionResponse, SeleccionUpdate
from app.services import seleccion_service

router = APIRouter(prefix="/selecciones", tags=["Selecciones"])


@router.get("/", response_model=list[SeleccionResponse])
def listar_selecciones(
    include_deleted: bool = Query(False),
    db: Session = Depends(get_db),
):
    return seleccion_service.list_selecciones(db, include_deleted=include_deleted)


@router.get("/{id_seleccion}", response_model=SeleccionResponse)
def obtener_seleccion(id_seleccion: int, db: Session = Depends(get_db)):
    seleccion = seleccion_service.get_seleccion(db, id_seleccion)
    if not seleccion:
        raise HTTPException(status_code=404, detail="Selección no encontrada")
    return seleccion


@router.post("/", response_model=SeleccionResponse, status_code=201)
def crear_seleccion(data: SeleccionCreate, db: Session = Depends(get_db)):
    return seleccion_service.create_seleccion(db, data)


@router.patch("/{id_seleccion}", response_model=SeleccionResponse)
def actualizar_seleccion(id_seleccion: int, data: SeleccionUpdate, db: Session = Depends(get_db)):
    seleccion = seleccion_service.get_seleccion(db, id_seleccion)
    if not seleccion:
        raise HTTPException(status_code=404, detail="Selección no encontrada")
    return seleccion_service.update_seleccion(db, seleccion, data)


@router.delete("/{id_seleccion}", status_code=204)
def eliminar_seleccion(id_seleccion: int, db: Session = Depends(get_db)):
    seleccion = seleccion_service.get_seleccion(db, id_seleccion)
    if not seleccion:
        raise HTTPException(status_code=404, detail="Selección no encontrada")
    seleccion_service.delete_seleccion(db, seleccion)


@router.post("/{id_seleccion}/restore", response_model=SeleccionResponse)
def restaurar_seleccion(id_seleccion: int, db: Session = Depends(get_db)):
    seleccion = seleccion_service.restore_seleccion(db, id_seleccion)
    if not seleccion:
        raise HTTPException(status_code=404, detail="Selección no encontrada")
    return seleccion
