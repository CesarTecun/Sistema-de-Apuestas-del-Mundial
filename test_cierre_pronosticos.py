"""
Script para probar el cierre automático de pronósticos 15 min antes.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from django.utils import timezone
from datetime import timedelta
from backend.partidos.models import Partido
from backend.pronosticos.models import Pronostico
from backend.pronosticos.views import _validar_ventana_pronostico
from rest_framework.exceptions import ValidationError

print("=" * 60)
print("PRUEBA 1: CIERRE AUTOMATICO 15 MINUTOS ANTES")
print("=" * 60)

# Tomar el primer partido disponible
partido = Partido.objects.filter(status=True).first()
if not partido:
    print("ERROR: No hay partidos en la base de datos.")
    sys.exit(1)

print(f"\nPartido seleccionado: ID={partido.id_partido}, Horario={partido.horario}")
print(f"Horario actual: {timezone.now()}")

# Caso A: Horario normal (futuro) -> Debería permitir
print("\n--- CASO A: Partido con horario futuro (debe permitir) ---")
try:
    _validar_ventana_pronostico(partido.id_partido)
    print("OK: Pronóstico PERMITIDO (ventana abierta)")
except ValidationError as e:
    print(f"ERROR INESPERADO: {e.detail}")

# Caso B: Simular que falta 10 minutos para el partido -> Debería rechazar
print("\n--- CASO B: Partido a 10 minutos de iniciar (debe rechazar) ---")
horario_original = partido.horario
partido.horario = timezone.now() + timedelta(minutes=10)
partido.save(update_fields=['horario'])

try:
    _validar_ventana_pronostico(partido.id_partido)
    print("ERROR: Pronóstico fue PERMITIDO (debería haberse cerrado)")
except ValidationError as e:
    print(f"OK: Pronóstico RECHAZADO - {e.detail['detail']}")

# Restaurar horario
partido.horario = horario_original
partido.save(update_fields=['horario'])

# Caso C: Simular que el partido ya inició -> Debería rechazar
print("\n--- CASO C: Partido ya iniciado (debe rechazar) ---")
partido.horario = timezone.now() - timedelta(minutes=5)
partido.save(update_fields=['horario'])

try:
    _validar_ventana_pronostico(partido.id_partido)
    print("ERROR: Pronóstico fue PERMITIDO (debería haberse cerrado)")
except ValidationError as e:
    print(f"OK: Pronóstico RECHAZADO - {e.detail['detail']}")

# Restaurar horario original
partido.horario = horario_original
partido.save(update_fields=['horario'])

print("\n" + "=" * 60)
print("Prueba de cierre automático completada.")
print("=" * 60)
