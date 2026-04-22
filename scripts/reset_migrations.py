#!/usr/bin/env python
"""
Script para regenerar migraciones limpias.

Uso:
    python scripts/reset_migrations.py

Esto:
    1. Elimina todas las migraciones existentes (excepto __init__.py)
    2. Regenera migraciones desde cero basadas en los modelos actuales
    3. Muestra instrucciones para aplicarlas
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Colores para output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_color(color, message):
    print(f"{color}{message}{Colors.END}")

def find_migration_dirs():
    """Encuentra todos los directorios de migraciones en backend/"""
    backend_path = Path("backend")
    migration_dirs = []
    
    for app_dir in backend_path.iterdir():
        if app_dir.is_dir():
            migrations_dir = app_dir / "migrations"
            if migrations_dir.exists():
                migration_dirs.append(migrations_dir)
    
    return migration_dirs

def delete_migrations(migration_dirs):
    """Elimina todos los archivos de migración excepto __init__.py"""
    deleted = []
    
    for migrations_dir in migration_dirs:
        for file_path in migrations_dir.iterdir():
            if file_path.is_file() and file_path.name.endswith('.py'):
                if file_path.name != '__init__.py':
                    file_path.unlink()
                    deleted.append(file_path)
            elif file_path.is_dir() and file_path.name == '__pycache__':
                shutil.rmtree(file_path)
    
    return deleted

def regenerate_migrations():
    """Regenera migraciones usando makemigrations"""
    result = subprocess.run(
        [sys.executable, "manage.py", "makemigrations"],
        capture_output=True,
        text=True
    )
    return result

def main():
    print_color(Colors.BLUE, "=" * 60)
    print_color(Colors.BLUE, "RESET DE MIGRACIONES DJANGO")
    print_color(Colors.BLUE, "=" * 60)
    print()
    
    # 1. Encontrar directorios de migraciones
    print_color(Colors.YELLOW, "1. Buscando directorios de migraciones...")
    migration_dirs = find_migration_dirs()
    print(f"   Encontrados: {len(migration_dirs)} directorios")
    for d in migration_dirs:
        print(f"      - {d}")
    print()
    
    # 2. Confirmar
    response = input("¿Eliminar y regenerar TODAS las migraciones? (yes/no): ")
    if response.lower() != 'yes':
        print_color(Colors.YELLOW, "Operación cancelada.")
        return
    
    # 3. Eliminar migraciones existentes
    print_color(Colors.YELLOW, "2. Eliminando migraciones existentes...")
    deleted = delete_migrations(migration_dirs)
    print(f"   Eliminados: {len(deleted)} archivos")
    for f in deleted[:10]:  # Mostrar solo los primeros 10
        print(f"      - {f.name}")
    if len(deleted) > 10:
        print(f"      ... y {len(deleted) - 10} más")
    print()
    
    # 4. Regenerar migraciones
    print_color(Colors.YELLOW, "3. Regenerando migraciones...")
    result = regenerate_migrations()
    
    if result.returncode == 0:
        print_color(Colors.GREEN, "   ✅ Migraciones regeneradas exitosamente!")
        if result.stdout:
            print(result.stdout)
    else:
        print_color(Colors.RED, "   ❌ Error al regenerar migraciones:")
        print(result.stderr)
        return
    
    print()
    print_color(Colors.BLUE, "=" * 60)
    print_color(Colors.GREEN, "INSTRUCCIONES SIGUIENTES:")
    print_color(Colors.BLUE, "=" * 60)
    print()
    print("Para aplicar las nuevas migraciones:")
    print()
    print_color(Colors.YELLOW, "   Opción A - Si la BD está limpia:")
    print("      docker-compose -f infrastructure/docker-compose.yml up -d")
    print("      python manage.py migrate")
    print()
    print_color(Colors.YELLOW, "   Opción B - Si la BD tiene datos (preservar):")
    print("      python manage.py migrate --fake-initial")
    print()
    print_color(Colors.YELLOW, "   Opción C - Reset completo (perder datos):")
    print("      docker-compose -f infrastructure/docker-compose.yml down -v")
    print("      docker-compose -f infrastructure/docker-compose.yml up -d")
    print("      python manage.py migrate")
    print()
    print_color(Colors.BLUE, "=" * 60)
    print("Para commitear las migraciones (solo el responsable):")
    print()
    print("   git add backend/*/migrations/0*.py")
    print('   git commit -m "chore: regenerate clean migrations"')
    print()

if __name__ == "__main__":
    main()
