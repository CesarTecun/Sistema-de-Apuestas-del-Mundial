"""
Carga inicial de selecciones (Mundial 2026), misma lista que
backend/partidos/migrations/0002_seed_selecciones.py del proyecto principal.
"""
from app.database import SessionLocal, engine, Base
from app.models.seleccion import Seleccion

PAISES_MUNDIAL_2026 = [
    "Canadá", "México", "Estados Unidos", "Curazao", "Haití", "Panamá",
    "Argentina", "Brasil", "Colombia", "Ecuador", "Paraguay", "Uruguay",
    "Austria", "Bélgica", "Bosnia y Herzegovina", "Croacia", "Chequia",
    "Inglaterra", "Francia", "Alemania", "Países Bajos", "Noruega",
    "Portugal", "Escocia", "España", "Suecia", "Suiza", "Turquía",
    "Australia", "Irak", "Irán", "Japón", "Jordania", "Corea del Sur",
    "Catar", "Arabia Saudita", "Uzbekistán", "Nueva Zelanda",
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for nombre in PAISES_MUNDIAL_2026:
            existe = db.query(Seleccion).filter(Seleccion.pais == nombre).first()
            if not existe:
                db.add(Seleccion(pais=nombre))
        db.commit()
        total = db.query(Seleccion).filter(Seleccion.status.is_(True)).count()
        print(f"Seed completado: {total} selecciones activas.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
