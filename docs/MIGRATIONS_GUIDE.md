# Guía de Trabajo con Migraciones en Equipo

## El Problema

Cuando varios desarrolladores trabajan en Django, las migraciones pueden causar conflictos:
- Dos devs crean migración `0002` al mismo tiempo
- Merge conflicts en archivos de migración
- Dependencias circulares entre migraciones
- Migraciones que aplican cambios inconsistentes

## Nuestra Solución: Estrategia "Squash & Reset"

### Reglas del Equipo

#### 1. NUNCA commitees migraciones en desarrollo activo

Durante el desarrollo de una feature:
- Crea migraciones localmente para probar
- NO hagas `git add` de archivos en `*/migrations/0*.py`
- Solo commitea el código, no las migraciones

#### 2. UN responsable de migraciones

Designamos a **un solo desarrollador** (rotativo) que:
- Antes de cada release, genera TODAS las migraciones limpias
- Resuelve conflictos de modelo
- Commitea las migraciones finales

#### 3. Workflow diario

```bash
# Al empezar a trabajar
git pull origin main

# Si hay nuevas migraciones:
venv\Scripts\python.exe manage.py migrate

# Trabaja en tu código...
# Si necesitas migrar para probar:
venv\Scripts\python.exe manage.py makemigrations
venv\Scripts\python.exe manage.py migrate

# Al hacer commit - SOLO código, NO migraciones
git add backend/tuapp/models.py  # ✅
git add backend/tuapp/migrations/  # ❌ NO!
```

#### 4. Reset de migraciones semanal/release

Antes de cada release importante:

```bash
# 1. Todos deben tener su código commiteado y pusheado

# 2. El responsable de migraciones ejecuta:
python scripts/reset_migrations.py

# 3. Esto genera migraciones limpias desde cero

# 4. Push a main

git add backend/*/migrations/0*.py
git commit -m "chore: regenerate clean migrations for vX.Y.Z"
```

## Archivos a Ignorar

Las migraciones **en desarrollo** se ignoran:
- `backend/*/migrations/0*.py` (excepto las que ya están en main)

Las migraciones **oficiales** se mantienen:
- Solo las generadas por el responsable de migraciones

## Resolución de Conflictos

### Si tienes conflicto de migraciones:

```bash
# Opción 1: Reset completo (recomendado)
python scripts/reset_migrations.py

# Opción 2: Solo tus migraciones
cd backend/tuapp
rm -rf migrations/0*.py
venv\Scripts\python.exe manage.py makemigrations
```

### Si la BD está inconsistente:

```bash
# Borrar contenedor y recrear
docker-compose -f infrastructure/docker-compose.yml down -v
docker-compose -f infrastructure/docker-compose.yml up -d

# Regenerar todo
python scripts/reset_migrations.py
venv\Scripts\python.exe manage.py migrate
```

## Comandos Útiles

```bash
# Ver estado de migraciones
venv\Scripts\python.exe manage.py showmigrations

# Ver qué migraciones faltan
venv\Scripts\python.exe manage.py migrate --plan

# Faker una migración (si la tabla ya existe)
venv\Scripts\python.exe manage.py migrate --fake app_name migration_name

# Deshacer migraciones
venv\Scripts\python.exe manage.py migrate app_name zero
```

## Checklist antes de Push

- [ ] Mis modelos están actualizados
- [ ] NO incluí archivos de migración en el commit
- [ ] El código funciona con las migraciones actuales en main
- [ ] Si cambié modelos, avisé al equipo

## Responsables de Migraciones (Rotativo)

| Sprint | Responsable |
|--------|-------------|
| 1      | @dev1       |
| 2      | @dev2       |
| 3      | @dev3       |

El responsable del sprint actual debe:
1. Generar migraciones limpias antes del release
2. Resolver conflictos entre modelos de diferentes devs
3. Asegurar que todas las migraciones aplican correctamente
