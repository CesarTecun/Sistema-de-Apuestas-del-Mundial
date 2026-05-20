from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import SoftDeleteMixin


class Partido(SoftDeleteMixin, Base):
    """
    Réplica del modelo Partido (tabla partido) orientado al marcador en vivo.
    equipo_local / equipo_visitante referencian id_seleccion.
    """

    __tablename__ = "partido"

    id_partido: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    horario: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    equipo_local: Mapped[int] = mapped_column(Integer, nullable=False)
    equipo_visitante: Mapped[int] = mapped_column(Integer, nullable=False)
    fk_sede: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fk_id_fase: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fk_id_liga: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    gol_local: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gol_visitante: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ganador_penales: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tipo_partido: Mapped[str] = mapped_column(String(50), default="Regular", nullable=False)
    resultado: Mapped[str | None] = mapped_column(String(50), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="programado", nullable=False)

    @property
    def resultado_display(self) -> str:
        if self.resultado:
            return self.resultado
        return f"{self.gol_local} - {self.gol_visitante}"

    @property
    def ganador(self) -> int | None:
        if self.gol_local > self.gol_visitante:
            return self.equipo_local
        if self.gol_visitante > self.gol_local:
            return self.equipo_visitante
        if self.ganador_penales is not None:
            return self.ganador_penales
        return None
