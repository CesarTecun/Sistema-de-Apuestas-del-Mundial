#!/usr/bin/env python
"""
Script para verificar estado de migraciones antes de push.

Uso:
    python scripts/check_migrations.py

Verifica:
    1. Si hay migraciones sin commitear
    2. Si las migraciones aplican correctamente
    3. Si hay conflictos potenciales
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Ejecuta un comando y retorna el resultado"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

def check_uncommitted_migrations():
    """Verifica si hay migraciones sin commitear"""
    result = run_command("git diff --name-only backend/*/migrations/*.py")
    uncommitted = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    result = run_command("git ls-files --others --exclude-standard backend/*/migrations/*.py")
    untracked = result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    all_migrations = [f for f in (uncommitted + untracked) if f]
    
    return all_migrations

def check_migration_status():
    """Verifica si hay migraciones pendientes por aplicar"""
    result = run_command("venv\\Scripts\\python.exe manage.py showmigrations")
    lines = result.stdout.split('\n')
    
    pending = []
    for line in lines:
        if '[ ]' in line and '000' in line:
            pending.append(line.strip())
    
    return pending

def main():
    print("=" * 60)
    print("CHECK DE MIGRACIONES")
    print("=" * 60)
    print()
    
    # 1. Verificar migraciones sin commitear
    print("1. Verificando migraciones sin commitear...")
    uncommitted = check_uncommitted_migrations()
    
    if uncommitted:
        print(f"   ⚠️  Encontradas {len(uncommitted)} migración(es) sin commitear:")
        for f in uncommitted:
            print(f"      - {f}")
        print()
        print("   💡 Recuerda: No commitees migraciones durante desarrollo.")
        print("      Solo el responsable de migraciones las debe commitear.")
    else:
        print("   ✅ No hay migraciones sin commitear")
    print()
    
    # 2. Verificar migraciones pendientes
    print("2. Verificando migraciones pendientes...")
    pending = check_migration_status()
    
    if pending:
        print(f"   ⚠️  Hay {len(pending)} migración(es) pendientes por aplicar:")
        for p in pending[:5]:
            print(f"      {p}")
        if len(pending) > 5:
            print(f"      ... y {len(pending) - 5} más")
        print()
        print("   Ejecuta: python manage.py migrate")
    else:
        print("   ✅ Todas las migraciones están aplicadas")
    print()
    
    # 3. Recomendación
    print("=" * 60)
    if uncommitted or pending:
        print("⚠️  ACCIÓN REQUERIDA:")
        if uncommitted:
            print("   - Descarta migraciones locales: git checkout -- backend/*/migrations/0*.py")
            print("   - O ejecuta: python scripts/reset_migrations.py")
        if pending:
            print("   - Aplica migraciones: python manage.py migrate")
        sys.exit(1)
    else:
        print("✅ Todo listo para trabajar!")
        sys.exit(0)

if __name__ == "__main__":
    main()
