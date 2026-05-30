from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.seleccion import SeleccionResponse


class PartidoBase(BaseModel):
    horario: datetime
    equipo_local: int
    equipo_visitante: int
    fk_sede: Optional[int] = None
    fk_id_fase: Optional[int] = None
    fk_id_liga: Optional[int] = None
    tipo_partido: str = "Regular"
    estado: str = "programado"


class PartidoCreate(PartidoBase):
    gol_local: int = 0
    gol_visitante: int = 0
    resultado: Optional[str] = None
    ganador_penales: Optional[int] = None


class PartidoUpdate(BaseModel):
    horario: Optional[datetime] = None
    equipo_local: Optional[int] = None
    equipo_visitante: Optional[int] = None
    fk_sede: Optional[int] = None
    fk_id_fase: Optional[int] = None
    fk_id_liga: Optional[int] = None
    gol_local: Optional[int] = None
    gol_visitante: Optional[int] = None
    ganador_penales: Optional[int] = None
    tipo_partido: Optional[str] = None
    resultado: Optional[str] = None
    estado: Optional[str] = None


class MarcadorUpdate(BaseModel):
    gol_local: Optional[int] = None
    gol_visitante: Optional[int] = None
    resultado: Optional[str] = Field(None, max_length=50)
    estado: Optional[str] = Field(None, max_length=20)
    ganador_penales: Optional[int] = None
    faltas_local: Optional[int] = None
    faltas_visitante: Optional[int] = None


class PartidoControlUpdate(BaseModel):
    """Schema para controlar el partido en vivo"""
    estado: Optional[str] = Field(None, max_length=20)  # programado, en_juego, finalizado
    minuto_actual: Optional[int] = None
    periodo_actual: Optional[str] = Field(None, max_length=20)  # 1T, 2T, ET1, ET2
    tiempo_extra_periodo: Optional[int] = None
    partido_iniciado: Optional[bool] = None
    partido_pausado: Optional[bool] = None


class PartidoResponse(PartidoBase):
    model_config = ConfigDict(from_attributes=True)

    id_partido: int
    gol_local: int
    gol_visitante: int
    ganador_penales: Optional[int]
    resultado: Optional[str]
    status: bool
    resultado_display: str
    ganador: Optional[int]
    # Campos de control del partido
    minuto_actual: Optional[int] = None
    periodo_actual: Optional[str] = None
    tiempo_extra_periodo: Optional[int] = None
    partido_iniciado: Optional[bool] = None
    partido_pausado: Optional[bool] = None
    faltas_local: Optional[int] = None
    faltas_visitante: Optional[int] = None


class PartidoMarcadorResponse(PartidoResponse):
    equipo_local_detalle: Optional[SeleccionResponse] = None
    equipo_visitante_detalle: Optional[SeleccionResponse] = None
