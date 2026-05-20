from pydantic import BaseModel, ConfigDict, Field


class SeleccionBase(BaseModel):
    pais: str = Field(..., max_length=100)
    bandera: str | None = Field(None, max_length=255)
    fk_id_fase_inicial: int | None = None


class SeleccionCreate(SeleccionBase):
    pass


class SeleccionUpdate(BaseModel):
    pais: str | None = Field(None, max_length=100)
    bandera: str | None = Field(None, max_length=255)
    fk_id_fase_inicial: int | None = None


class SeleccionResponse(SeleccionBase):
    model_config = ConfigDict(from_attributes=True)

    id_seleccion: int
    status: bool
