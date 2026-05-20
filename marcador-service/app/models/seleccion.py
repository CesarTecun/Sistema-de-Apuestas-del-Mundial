from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import SoftDeleteMixin


class Seleccion(SoftDeleteMixin, Base):
    """
    Réplica del modelo Seleccion (tabla seleccion) del proyecto principal.
    """

    __tablename__ = "seleccion"

    id_seleccion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pais: Mapped[str] = mapped_column(String(100), nullable=False)
    bandera: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fk_id_fase_inicial: Mapped[int | None] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Seleccion {self.id_seleccion}: {self.pais}>"
