import os

import requests
from sqlalchemy.orm import Session

from app.models.partido import Partido
from app.models.seleccion import Seleccion
from app.schemas.partido import MarcadorUpdate, PartidoControlUpdate, PartidoCreate, PartidoMarcadorResponse, PartidoUpdate


DJANGO_WEBHOOK_URL = os.getenv("DJANGO_WEBHOOK_URL", "http://localhost:8000/api/partidos/marcador/webhook/")


def _notify_django(partido: Partido) -> None:
    """Notifica a Django cuando cambia el marcador de un partido."""
    if not DJANGO_WEBHOOK_URL:
        return
    try:
        payload = {
            "id_partido": partido.id_partido,
            "gol_local": partido.gol_local,
            "gol_visitante": partido.gol_visitante,
            "estado": partido.estado,
            "resultado": partido.resultado,
            "ganador_penales": partido.ganador_penales,
        }
        print(f"[WEBHOOK] Enviando notificación a Django: {DJANGO_WEBHOOK_URL}")
        print(f"[WEBHOOK] Payload: id_partido={partido.id_partido}, estado={partido.estado}, gol_local={partido.gol_local}, gol_visitante={partido.gol_visitante}")
        response = requests.post(
            DJANGO_WEBHOOK_URL,
            json=payload,
            timeout=3,
        )
        print(f"[WEBHOOK] Response status: {response.status_code}")
        print(f"[WEBHOOK] Response body: {response.text}")
    except Exception as e:
        print(f"[WEBHOOK] Error: {e}")
        pass  # No fallar si Django no está disponible


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
    _notify_django(partido)
    return partido


def controlar_partido(db: Session, partido: Partido, data: PartidoControlUpdate) -> Partido:
    """
    Controla el partido en vivo: iniciar, pausar, cambiar tiempo, agregar tiempo extra
    """
    payload = data.model_dump(exclude_unset=True)
    print(f"controlar_partido recibido: id_partido={partido.id_partido}, payload={payload}")
    
    # Finalizar partido - manejar primero para asegurar que no se sobrescriba
    if payload.get("estado") == "finalizado":
        print(f"Finalizando partido {partido.id_partido}")
        partido.estado = "finalizado"
        partido.partido_pausado = True
        partido.partido_iniciado = False
        # Generar resultado si no existe
        if not partido.resultado:
            partido.resultado = f"{partido.gol_local} - {partido.gol_visitante}"
    # Manejo especial para iniciar partido
    elif payload.get("partido_iniciado") == True and not partido.partido_iniciado:
        partido.estado = "en_juego"
        partido.partido_iniciado = True
        partido.partido_pausado = False
        partido.minuto_actual = 0
        partido.periodo_actual = "1T"
        partido.tiempo_extra_periodo = 0
    
    # Manejo especial para pausar partido
    if payload.get("partido_pausado") is not None:
        partido.partido_pausado = payload["partido_pausado"]
    
    # Actualizar otros campos (excepto estado que ya se manejó)
    for field, value in payload.items():
        if field not in ["partido_iniciado", "partido_pausado", "estado"]:
            setattr(partido, field, value)
    
    # Cambio de período
    if payload.get("periodo_actual") and payload["periodo_actual"] != partido.periodo_actual:
        partido.periodo_actual = payload["periodo_actual"]
        partido.minuto_actual = 0  # Reiniciar minuto al cambiar período
        partido.tiempo_extra_periodo = 0
    
    db.commit()
    db.refresh(partido)
    _notify_django(partido)
    return partido


def delete_partido(db: Session, partido: Partido) -> None:
    partido.soft_delete()
    db.commit()


def enrich_marcador(db: Session, partido: Partido) -> PartidoMarcadorResponse:
    local = get_seleccion_safe(db, partido.equipo_local)
    visitante = get_seleccion_safe(db, partido.equipo_visitante)
    
    if not local:
        print(f"No se encontró selección local para partido {partido.id_partido}: equipo_local={partido.equipo_local}")
    if not visitante:
        print(f"No se encontró selección visitante para partido {partido.id_partido}: equipo_visitante={partido.equipo_visitante}")
    
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
    if row:
        return SeleccionResponse.model_validate(row)
    else:
        print(f"Selección no encontrada: id_seleccion={id_seleccion}")
        return None
