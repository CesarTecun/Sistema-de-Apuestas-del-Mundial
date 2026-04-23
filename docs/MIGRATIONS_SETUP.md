# Configuración de Migraciones para el Equipo

## Setup Inicial (Una sola vez por desarrollador)

### 1. Configurar Git Hooks

```bash
# En la raíz del proyecto
git config core.hooksPath .githooks

# En Windows (PowerShell):
git config core.hooksPath .githooks
```

Esto activa el pre-commit hook que evitará commitear migraciones accidentalmente.

### 2. Verificar que todo funciona

```bash
# Probar el check de migraciones
python scripts/check_migrations.py

# Probar el reset de migraciones
python scripts/reset_migrations.py
```

## Workflow Diario

### Al empezar a trabajar

```bash
# 1. Actualizar código
git pull origin main

# 2. Verificar estado de migraciones
python scripts/check_migrations.py

# 3. Si hay migraciones nuevas, aplicarlas
python manage.py migrate

# 4. Verificar que todo funciona
python manage.py check
```

### Durante el desarrollo

```bash
# Trabajas en tu código...

# Si necesitas crear migraciones para probar:
python manage.py makemigrations
python manage.py migrate

# Pero NO las commitees!
# El pre-commit hook te avisará si lo intentas
```

### Al hacer commit

```bash
# Agregar solo archivos de código (NO migraciones)
git add backend/tuapp/models.py
git add backend/tuapp/views.py
# etc...

# El pre-commit hook verificará automáticamente
git commit -m "feat: agrega campo X al modelo Y"

# Si el hook rechaza tu commit por migraciones:
git reset HEAD backend/*/migrations/0*.py  # Quitarlas del staging
git commit -m "feat: agrega campo X al modelo Y"  # Reintentar
```

### Al hacer push

```bash
# Asegurarte de que no hay migraciones sin commitear
python scripts/check_migrations.py

# Si todo está bien:
git push origin tu-branch
```

## Responsable de Migraciones (Rotativo)

### Antes de cada release/sprint:

```bash
# 1. Coordinar con el equipo que nadie tenga cambios pendientes

# 2. Ejecutar reset de migraciones
python scripts/reset_migrations.py

# 3. Aplicar migraciones limpias (opción C - reset completo)
docker-compose -f infrastructure/docker-compose.yml down -v
docker-compose -f infrastructure/docker-compose.yml up -d
python manage.py migrate

# 4. Crear superusuario de prueba
python manage.py shell -c "from backend.usuarios.models import Usuario; u = Usuario(email='admin@example.com', primer_nombre='Admin', primer_apellido='User', fk_rol=1); u.set_password('admin123'); u.save()"

# 5. Probar que todo funciona
python manage.py check
python manage.py runserver  # Probar en navegador

# 6. Commitear migraciones
# ⚠️ Temporalmente desactivar el hook:
git commit --no-verify -m "chore: regenerate clean migrations for vX.Y.Z"

# 7. Push a main
git push origin main

# 8. Avisar al equipo que actualicen
```

## Solución de Problemas

### "relation X does not exist"

```bash
# Las migraciones y la BD están desincronizadas

# Opción A - Reset completo (pierdes datos locales):
docker-compose -f infrastructure/docker-compose.yml down -v
docker-compose -f infrastructure/docker-compose.yml up -d
python manage.py migrate

# Opción B - Solo rehacer migraciones:
python scripts/reset_migrations.py
python manage.py migrate --fake-initial
```

### "Conflicting migrations detected"

```bash
# Dos desarrolladores crearon la misma migración

# Solución:
python scripts/reset_migrations.py
python manage.py migrate
```

### "No changes detected" pero sí hay cambios

```bash
# Posiblemente el cache de migraciones está corrupto

# Solución:
find backend -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find backend -path "*/migrations/*.pyc" -delete 2>/dev/null
python manage.py makemigrations
```

### Pre-commit hook muy estricto

```bash
# Si necesitas forzar un commit con migraciones (solo responsable):
git commit --no-verify -m "chore: migrate"
```

## Comandos Útiles

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Ver plan de migraciones
python manage.py migrate --plan

# Deshacer migraciones de una app
python manage.py migrate ligas zero

# Deshacer última migración
python manage.py migrate ligas 0001

# Faker una migración (si la tabla ya existe)
python manage.py migrate --fake ligas 0002

# Crear migración vacía para data migrations
python manage.py makemigrations --empty ligas
```

## Checklist para Cada Developer

- [ ] Configuré los git hooks (`git config core.hooksPath .githooks`)
- [ ] Leí la guía de migraciones (`docs/MIGRATIONS_GUIDE.md`)
- [ ] Entiendo que NO debo commitear migraciones
- [ ] Sé quién es el responsable de migraciones este sprint
- [ ] Ejecuté `python scripts/check_migrations.py` y todo está OK
