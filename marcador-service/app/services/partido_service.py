from sqlalchemy.orm import Session

from app.models.partido import Partido
from app.models.seleccion import Seleccion
from app.schemas.partido import MarcadorUpdate, PartidoCreate, PartidoMarcadorResponse, PartidoUpdate


def _ensure_seleccion_exists(db: Session, id_seleccion: int) -> bool:
    return (
        db.query(Seleccion)
        .filter(Seleccion.id_seleccion == id_seleccion, Seleccion.status.is_(True))
        .first()
        is not None
    )


def list_partidos(db: Session, estado: str | None = None, fk_id_liga: int | None = None) -> list[Partido]:
    query = db.query(Partido).filter(Partido.status.is_(True))
    if estado:
        query = query.filter(Partido.estado == estado)
    if fk_id_liga is not None:
        query = query.filter(Partido.fk_id_liga == fk_id_liga)
    return query.order_by(Partido.horario).all()


def get_partido(db: Session, id_partido: int) -> Partido | None:
    return (
        db.query(Partido)
        .filter(Partido.id_partido == id_partido, Partido.status.is_(True))
        .first()
    )


def partidos_por_equipo(db: Session, equipo_id: int) -> list[Partido]:
    return (
        db.query(Partido)
        .filter(
            Partido.status.is_(True),
            (Partido.equipo_local == equipo_id) | (Partido.equipo_visitante == equipo_id),
        )
        .order_by(Partido.horario)
        .all()
    )


def create_partido(db: Session, data: PartidoCreate) -> Partido:
    if not _ensure_seleccion_exists(db, data.equipo_local):
        raise ValueError(f"Selección local {data.equipo_local} no existe")
    if not _ensure_seleccion_exists(db, data.equipo_visitante):
        raise ValueError(f"Selección visitante {data.equipo_visitante} no existe")

    partido = Partido(**data.model_dump())
    if not partido.resultado and (partido.gol_local or partido.gol_visitante):
        partido.resultado = f"{partido.gol_local} - {partido.gol_visitante}"
    db.add(partido)
    db.commit()
    db.refresh(partido)
    return partido


def update_partido(db: Session, partido: Partido, data: PartidoUpdate) -> Partido:
    payload = data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        setattr(partido, field, value)
    if "gol_local" in payload or "gol_visitante" in payload:
        if partido.resultado is None:
            partido.resultado = f"{partido.gol_local} - {partido.gol_visitante}"
    db.commit()
    db.refresh(partido)
    return partido


def actualizar_marcador(db: Session, partido: Partido, data: MarcadorUpdate) -> Partido:
    payload = data.model_dump(exclude_unset=True)
    for field, value in payload.items():
        setattr(partido, field, value)

    if partido.gol_local is not None and partido.gol_visitante is not None:
        if partido.resultado is None:
            partido.resultado = f"{partido.gol_local} - {partido.gol_visitante}"

    if partido.estado == "programado" and (partido.gol_local > 0 or partido.gol_visitante > 0):
        partido.estado = "en_juego"

    db.commit()
    db.refresh(partido)
    return partido


def delete_partido(db: Session, partido: Partido) -> None:
    partido.soft_delete()
    db.commit()


def enrich_marcador(db: Session, partido: Partido) -> PartidoMarcadorResponse:
    local = get_seleccion_safe(db, partido.equipo_local)
    visitante = get_seleccion_safe(db, partido.equipo_visitante)
    base = PartidoMarcadorResponse.model_validate(partido)
    return base.model_copy(
        update={
            "equipo_local_detalle": local,
            "equipo_visitante_detalle": visitante,
        }
    )


def get_seleccion_safe(db: Session, id_seleccion: int):
    from app.schemas.seleccion import SeleccionResponse

    row = (
        db.query(Seleccion)
        .filter(Seleccion.id_seleccion == id_seleccion, Seleccion.status.is_(True))
        .first()
    )
    return SeleccionResponse.model_validate(row) if row else None
