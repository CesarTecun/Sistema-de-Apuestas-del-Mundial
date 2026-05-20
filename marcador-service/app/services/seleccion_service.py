from sqlalchemy.orm import Session

from app.models.seleccion import Seleccion
from app.schemas.seleccion import SeleccionCreate, SeleccionUpdate


def list_selecciones(db: Session, include_deleted: bool = False) -> list[Seleccion]:
    query = db.query(Seleccion)
    if not include_deleted:
        query = query.filter(Seleccion.status.is_(True))
    return query.order_by(Seleccion.pais).all()


def get_seleccion(db: Session, id_seleccion: int) -> Seleccion | None:
    return (
        db.query(Seleccion)
        .filter(Seleccion.id_seleccion == id_seleccion, Seleccion.status.is_(True))
        .first()
    )


def create_seleccion(db: Session, data: SeleccionCreate) -> Seleccion:
    seleccion = Seleccion(**data.model_dump())
    db.add(seleccion)
    db.commit()
    db.refresh(seleccion)
    return seleccion


def update_seleccion(db: Session, seleccion: Seleccion, data: SeleccionUpdate) -> Seleccion:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(seleccion, field, value)
    db.commit()
    db.refresh(seleccion)
    return seleccion


def delete_seleccion(db: Session, seleccion: Seleccion) -> None:
    seleccion.soft_delete()
    db.commit()


def restore_seleccion(db: Session, id_seleccion: int) -> Seleccion | None:
    seleccion = db.query(Seleccion).filter(Seleccion.id_seleccion == id_seleccion).first()
    if not seleccion:
        return None
    seleccion.restore()
    db.commit()
    db.refresh(seleccion)
    return seleccion
