"""
Router de sincronización para recibir datos del backend Django.
Permite que Django replique selecciones y partidos con sus IDs originales.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.seleccion import Seleccion
from app.models.partido import Partido

router = APIRouter(prefix="/sync", tags=["Sincronización"])


@router.post("/selecciones/")
def sync_seleccion(data: dict, db: Session = Depends(get_db)):
    """
    Upsert de selección desde Django.
    Busca por codigo_iso; si no existe, la crea (respetando id_seleccion si viene).
    """
    codigo_iso = data.get("codigo_iso")
    if not codigo_iso:
        raise HTTPException(status_code=400, detail="codigo_iso es requerido")

    seleccion = (
        db.query(Seleccion)
        .filter(Seleccion.codigo_iso == codigo_iso)
        .first()
    )

    if seleccion:
        seleccion.pais = data.get("pais", seleccion.pais)
        seleccion.bandera = data.get("bandera", seleccion.bandera)
        seleccion.fk_id_fase_inicial = data.get("fk_id_fase_inicial", seleccion.fk_id_fase_inicial)
        seleccion.status = data.get("status", seleccion.status)
        db.commit()
        db.refresh(seleccion)
        return {"action": "updated", "seleccion": seleccion.id_seleccion}

    nueva = Seleccion(
        id_seleccion=data.get("id_seleccion"),
        pais=data["pais"],
        bandera=data.get("bandera"),
        fk_id_fase_inicial=data.get("fk_id_fase_inicial"),
        codigo_iso=codigo_iso,
        status=data.get("status", True),
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"action": "created", "seleccion": nueva.id_seleccion}


@router.post("/partidos/")
def sync_partido(data: dict, db: Session = Depends(get_db)):
    """
    Upsert de partido desde Django.
    Busca por id_partido; si existe actualiza, si no lo crea con ID explícito.
    """
    id_partido = data.get("id_partido")
    if not id_partido:
        raise HTTPException(status_code=400, detail="id_partido es requerido")

    partido = (
        db.query(Partido)
        .filter(Partido.id_partido == id_partido)
        .first()
    )

    if partido:
        for campo in [
            "horario", "equipo_local", "equipo_visitante", "fk_sede",
            "fk_id_fase", "fk_id_liga", "gol_local", "gol_visitante",
            "ganador_penales", "tipo_partido", "resultado", "estado", "status",
        ]:
            if campo in data:
                setattr(partido, campo, data[campo])
        db.commit()
        db.refresh(partido)
        return {"action": "updated", "partido": partido.id_partido}

    nuevo = Partido(
        id_partido=id_partido,
        horario=data["horario"],
        equipo_local=data["equipo_local"],
        equipo_visitante=data["equipo_visitante"],
        fk_sede=data.get("fk_sede"),
        fk_id_fase=data.get("fk_id_fase"),
        fk_id_liga=data.get("fk_id_liga"),
        gol_local=data.get("gol_local", 0),
        gol_visitante=data.get("gol_visitante", 0),
        ganador_penales=data.get("ganador_penales"),
        tipo_partido=data.get("tipo_partido", "Regular"),
        resultado=data.get("resultado"),
        estado=data.get("estado", "programado"),
        status=data.get("status", True),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"action": "created", "partido": nuevo.id_partido}
