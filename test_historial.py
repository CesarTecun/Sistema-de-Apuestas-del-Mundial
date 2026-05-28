"""
Script para probar el endpoint de historial y capturar el error exacto.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from backend.pronosticos.models import Pronostico
from backend.partidos.models import Partido, Seleccion
from backend.posiciones.models import Ranking
from backend.ligas.models import Liga

try:
    # Simular el usuario con id=1 (ajusta si tu usuario tiene otro id)
    usuario_id = 1
    pronosticos = Pronostico.objects.filter(fk_id_usuario=usuario_id, status=True)
    print(f"Pronósticos encontrados: {pronosticos.count()}")

    partido_ids = {p.fk_id_partido for p in pronosticos}
    print(f"IDs de partidos: {partido_ids}")

    partidos = {p.id_partido: p for p in Partido.objects.filter(id_partido__in=partido_ids)}
    print(f"Partidos encontrados: {len(partidos)}")

    selecciones = {s.id_seleccion: s for s in Seleccion.objects.all()}
    print(f"Selecciones encontradas: {len(selecciones)}")

    ligas_ids = {p.fk_id_liga for p in pronosticos}
    print(f"IDs de ligas: {ligas_ids}")

    ligas = {l.id_liga: l for l in Liga.objects.filter(id_liga__in=ligas_ids)}
    print(f"Ligas encontradas: {len(ligas)}")

    rankings = {r.fk_id_liga: r for r in Ranking.objects.filter(fk_id_usuario=usuario_id, fk_id_liga__in=ligas_ids)}
    print(f"Rankings encontrados: {len(rankings)}")

    print("\n--- Todo OK, construyendo respuesta ---")

except Exception as e:
    import traceback
    print("\n=== ERROR ===")
    traceback.print_exc()
