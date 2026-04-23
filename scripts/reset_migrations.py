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

# Detectar directorio raíz del proyecto (donde está manage.py)
def get_project_root():
    """Encuentra el directorio raíz del proyecto buscando manage.py"""
    current = Path.cwd()
    # Buscar hacia arriba hasta encontrar manage.py
    for parent in [current] + list(current.parents):
        if (parent / "manage.py").exists():
            return parent
    # Si no se encuentra, usar el directorio actual
    return current

PROJECT_ROOT = get_project_root()

# Detectar Python del venv
def get_python_executable():
    """Encuentra el ejecutable de Python adecuado"""
    # Opción 1: Python del venv en el proyecto
    venv_python = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    
    # Opción 2: Python del venv en Linux/Mac
    venv_python_unix = PROJECT_ROOT / "venv" / "bin" / "python"
    if venv_python_unix.exists():
        return str(venv_python_unix)
    
    # Opción 3: Usar sys.executable como fallback
    return sys.executable

PYTHON_EXE = get_python_executable()

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
    backend_path = PROJECT_ROOT / "backend"
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
    errors = []
    
    for migrations_dir in migration_dirs:
        try:
            # Obtener lista de archivos antes de eliminar
            files_to_delete = []
            dirs_to_delete = []
            
            for file_path in migrations_dir.iterdir():
                if file_path.is_file() and file_path.name.endswith('.py'):
                    if file_path.name != '__init__.py':
                        files_to_delete.append(file_path)
                elif file_path.is_dir() and file_path.name == '__pycache__':
                    dirs_to_delete.append(file_path)
            
            # Eliminar archivos
            for file_path in files_to_delete:
                try:
                    file_path.unlink()
                    deleted.append(file_path)
                except Exception as e:
                    errors.append(f"Error al eliminar {file_path}: {e}")
            
            # Eliminar directorios __pycache__
            for dir_path in dirs_to_delete:
                try:
                    shutil.rmtree(dir_path)
                except Exception as e:
                    errors.append(f"Error al eliminar {dir_path}: {e}")
                    
        except Exception as e:
            errors.append(f"Error al procesar {migrations_dir}: {e}")
    
    if errors:
        print_color(Colors.YELLOW, f"   ⚠️  {len(errors)} errores durante la eliminación:")
        for error in errors[:5]:
            print(f"      - {error}")
    
    return deleted

def regenerate_migrations():
    """Regenera migraciones usando makemigrations"""
    manage_py = PROJECT_ROOT / "manage.py"
    
    print(f"   Ejecutando: {PYTHON_EXE} manage.py makemigrations")
    print(f"   Directorio: {PROJECT_ROOT}")
    
    try:
        result = subprocess.run(
            [PYTHON_EXE, str(manage_py), "makemigrations"],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=60  # Timeout de 60 segundos
        )
        return result
    except subprocess.TimeoutExpired:
        print_color(Colors.RED, "   ❌ Timeout: makemigrations tomó demasiado tiempo")
        return None
    except Exception as e:
        print_color(Colors.RED, f"   ❌ Error al ejecutar makemigrations: {e}")
        return None

def main():
    print_color(Colors.BLUE, "=" * 60)
    print_color(Colors.BLUE, "RESET DE MIGRACIONES DJANGO")
    print_color(Colors.BLUE, "=" * 60)
    print()
    
    # 0. Verificar entorno
    print_color(Colors.YELLOW, "0. Verificando entorno...")
    
    # Verificar que existe manage.py
    manage_py = PROJECT_ROOT / "manage.py"
    if not manage_py.exists():
        print_color(Colors.RED, "   ❌ No se encontró manage.py")
        print(f"   Buscado en: {manage_py}")
        return
    print(f"   ✅ manage.py encontrado")
    
    # Verificar que existe el venv
    venv_path = PROJECT_ROOT / "venv"
    if not venv_path.exists():
        print_color(Colors.RED, "   ❌ No se encontró el directorio venv/")
        print("   Crea el entorno virtual: python -m venv venv")
        return
    print(f"   ✅ Entorno virtual encontrado")
    
    # Verificar Python del venv
    if "venv" not in PYTHON_EXE:
        print_color(Colors.YELLOW, f"   ⚠️  Usando Python del sistema: {PYTHON_EXE}")
        print("   Se recomienda usar el Python del venv")
    else:
        print(f"   ✅ Usando Python del venv: {PYTHON_EXE}")
    
    print()
    
    # 1. Encontrar directorios de migraciones
    print_color(Colors.YELLOW, "1. Buscando directorios de migraciones...")
    migration_dirs = find_migration_dirs()
    if not migration_dirs:
        print_color(Colors.YELLOW, "   ⚠️  No se encontraron directorios de migraciones")
        return
        
    print(f"   Encontrados: {len(migration_dirs)} directorios")
    for d in migration_dirs:
        print(f"      - {d}")
    print()
    
    # Mostrar información de entorno
    print_color(Colors.BLUE, f"   Directorio raíz: {PROJECT_ROOT}")
    print_color(Colors.BLUE, f"   Python usado: {PYTHON_EXE}")
    print()
    
    # 2. Confirmar
    response = input("¿Eliminar y regenerar TODAS las migraciones? (yes/no): ")
    if response.lower() not in ['yes', 'y', 'si', 'sí']:
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
    
    if result is None:
        print_color(Colors.RED, "   ❌ No se pudo regenerar migraciones")
        return
    
    if result.returncode == 0:
        print_color(Colors.GREEN, "   ✅ Migraciones regeneradas exitosamente!")
        if result.stdout:
            print(result.stdout)
    else:
        print_color(Colors.RED, "   ❌ Error al regenerar migraciones:")
        if result.stderr:
            print(result.stderr)
        else:
            print("   Error desconocido (stderr vacío)")
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
    print('   git commit -m "chore: regenerar migraciones limpias"')
    print()
    
    # Mostrar comandos específicos para Windows
    print_color(Colors.BLUE, "=" * 60)
    print("Comandos para levantar el proyecto:")
    print()
    print_color(Colors.YELLOW, "   1. Iniciar PostgreSQL:")
    print("      docker-compose -f infrastructure/docker-compose.yml up -d")
    print()
    print_color(Colors.YELLOW, "   2. Aplicar migraciones:")
    print("      venv\\Scripts\\python.exe manage.py migrate --fake-initial")
    print()
    print_color(Colors.YELLOW, "   3. Iniciar Django:")
    print("      venv\\Scripts\\python.exe manage.py runserver")
    print()
    print_color(Colors.YELLOW, "   4. Iniciar React (en otra terminal):")
    print("      cd frontend && npm start")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_color(Colors.YELLOW, "\n⚠️  Operación cancelada por el usuario (Ctrl+C)")
        sys.exit(1)
    except Exception as e:
        print()
        print_color(Colors.RED, f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
