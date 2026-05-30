from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Boolean
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
    fk_sede: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fk_id_fase: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fk_id_liga: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    gol_local: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gol_visitante: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ganador_penales: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tipo_partido: Mapped[str] = mapped_column(String(50), default="Regular", nullable=False)
    resultado: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="programado", nullable=False)
    
    # Campos para control de partido en vivo
    minuto_actual: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    periodo_actual: Mapped[str] = mapped_column(String(20), default="1T", nullable=True)  # 1T, 2T, ET1, ET2
    tiempo_extra_periodo: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    partido_iniciado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    partido_pausado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    faltas_local: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
    faltas_visitante: Mapped[int] = mapped_column(Integer, default=0, nullable=True)

    @property
    def resultado_display(self) -> str:
        if self.resultado:
            return self.resultado
        return f"{self.gol_local} - {self.gol_visitante}"

    @property
    def ganador(self) -> Optional[int]:
        if self.gol_local > self.gol_visitante:
            return self.equipo_local
        if self.gol_visitante > self.gol_local:
            return self.equipo_visitante
        if self.ganador_penales is not None:
            return self.ganador_penales
        return None
