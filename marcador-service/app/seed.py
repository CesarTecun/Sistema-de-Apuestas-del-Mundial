"""
Carga inicial de selecciones (Mundial 2026), misma lista que
backend/partidos/migrations/0002_seed_selecciones.py del proyecto principal.
codigo_iso actúa como clave natural compartida entre Django y el microservicio.
"""
from app.database import SessionLocal, engine, Base
from app.models.seleccion import Seleccion

SELECCIONES_MUNDIAL_2026 = [
    {"pais": "Canadá", "codigo_iso": "CAN"},
    {"pais": "México", "codigo_iso": "MEX"},
    {"pais": "Estados Unidos", "codigo_iso": "USA"},
    {"pais": "Curazao", "codigo_iso": "CUW"},
    {"pais": "Haití", "codigo_iso": "HTI"},
    {"pais": "Panamá", "codigo_iso": "PAN"},
    {"pais": "Argentina", "codigo_iso": "ARG"},
    {"pais": "Brasil", "codigo_iso": "BRA"},
    {"pais": "Colombia", "codigo_iso": "COL"},
    {"pais": "Ecuador", "codigo_iso": "ECU"},
    {"pais": "Paraguay", "codigo_iso": "PRY"},
    {"pais": "Uruguay", "codigo_iso": "URY"},
    {"pais": "Austria", "codigo_iso": "AUT"},
    {"pais": "Bélgica", "codigo_iso": "BEL"},
    {"pais": "Bosnia y Herzegovina", "codigo_iso": "BIH"},
    {"pais": "Croacia", "codigo_iso": "HRV"},
    {"pais": "Chequia", "codigo_iso": "CZE"},
    {"pais": "Inglaterra", "codigo_iso": "ENG"},
    {"pais": "Francia", "codigo_iso": "FRA"},
    {"pais": "Alemania", "codigo_iso": "DEU"},
    {"pais": "Países Bajos", "codigo_iso": "NLD"},
    {"pais": "Noruega", "codigo_iso": "NOR"},
    {"pais": "Portugal", "codigo_iso": "PRT"},
    {"pais": "Escocia", "codigo_iso": "SCO"},
    {"pais": "España", "codigo_iso": "ESP"},
    {"pais": "Suecia", "codigo_iso": "SWE"},
    {"pais": "Suiza", "codigo_iso": "CHE"},
    {"pais": "Turquía", "codigo_iso": "TUR"},
    {"pais": "Australia", "codigo_iso": "AUS"},
    {"pais": "Irak", "codigo_iso": "IRQ"},
    {"pais": "Irán", "codigo_iso": "IRN"},
    {"pais": "Japón", "codigo_iso": "JPN"},
    {"pais": "Jordania", "codigo_iso": "JOR"},
    {"pais": "Corea del Sur", "codigo_iso": "KOR"},
    {"pais": "Catar", "codigo_iso": "QAT"},
    {"pais": "Arabia Saudita", "codigo_iso": "SAU"},
    {"pais": "Uzbekistán", "codigo_iso": "UZB"},
    {"pais": "Nueva Zelanda", "codigo_iso": "NZL"},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for item in SELECCIONES_MUNDIAL_2026:
            existe = db.query(Seleccion).filter(Seleccion.pais == item["pais"]).first()
            if not existe:
                db.add(Seleccion(pais=item["pais"], codigo_iso=item["codigo_iso"]))
            else:
                if not existe.codigo_iso:
                    existe.codigo_iso = item["codigo_iso"]
        db.commit()
        total = db.query(Seleccion).filter(Seleccion.status.is_(True)).count()
        print(f"Seed completado: {total} selecciones activas.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
