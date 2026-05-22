from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.seleccion import SeleccionResponse


class PartidoBase(BaseModel):
    horario: datetime
    equipo_local: int
    equipo_visitante: int
    fk_sede: int | None = None
    fk_id_fase: int | None = None
    fk_id_liga: int | None = None
    tipo_partido: str = "Regular"
    estado: str = "programado"


class PartidoCreate(PartidoBase):
    gol_local: int = 0
    gol_visitante: int = 0
    resultado: str | None = None
    ganador_penales: int | None = None


class PartidoUpdate(BaseModel):
    horario: datetime | None = None
    equipo_local: int | None = None
    equipo_visitante: int | None = None
    fk_sede: int | None = None
    fk_id_fase: int | None = None
    fk_id_liga: int | None = None
    gol_local: int | None = None
    gol_visitante: int | None = None
    ganador_penales: int | None = None
    tipo_partido: str | None = None
    resultado: str | None = None
    estado: str | None = None


class MarcadorUpdate(BaseModel):
    gol_local: int | None = None
    gol_visitante: int | None = None
    resultado: str | None = Field(None, max_length=50)
    estado: str | None = Field(None, max_length=20)
    ganador_penales: int | None = None
    faltas_local: int | None = None
    faltas_visitante: int | None = None


class PartidoControlUpdate(BaseModel):
    """Schema para controlar el partido en vivo"""
    estado: str | None = Field(None, max_length=20)  # programado, en_juego, finalizado
    minuto_actual: int | None = None
    periodo_actual: str | None = Field(None, max_length=20)  # 1T, 2T, ET1, ET2
    tiempo_extra_periodo: int | None = None
    partido_iniciado: bool | None = None
    partido_pausado: bool | None = None


class PartidoResponse(PartidoBase):
    model_config = ConfigDict(from_attributes=True)

    id_partido: int
    gol_local: int
    gol_visitante: int
    ganador_penales: int | None
    resultado: str | None
    status: bool
    resultado_display: str
    ganador: int | None
    # Campos de control del partido
    minuto_actual: int | None = None
    periodo_actual: str | None = None
    tiempo_extra_periodo: int | None = None
    partido_iniciado: bool | None = None
    partido_pausado: bool | None = None
    faltas_local: int | None = None
    faltas_visitante: int | None = None


class PartidoMarcadorResponse(PartidoResponse):
    equipo_local_detalle: SeleccionResponse | None = None
    equipo_visitante_detalle: SeleccionResponse | None = None
