# Configuración de Base de Datos con Docker

## Estado Actual
✅ **Configurado para PostgreSQL con Docker**  
❌ **Ya no usa SQLite (users/groups por defecto)**

## Para Usar tu Base de Datos Existente

### 1. Prepara tu archivo de base de datos
- Coloca tu dump SQL como: `database_dump.sql`
- O conéctate directamente a tu BD existente

### 2. Configura variables de entorno
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env con tus datos
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=tu_host_db
DB_PORT=tu_puerto
```

### 3. Opción A: Usar Docker con tu BD
```bash
# Inicia PostgreSQL con tu dump
docker-compose up db -d

# Espera a que la BD esté lista
# Tu dump se importará automáticamente si está en database_dump.sql

# Inicia Django
docker-compose up web
```

### 4. Opción B: Conectar a BD Externa
```bash
# Solo instala dependencias
pip install -r requirements.txt

# Configura .env con tus datos de BD existente
# Ejemplo:
DB_NAME=mi_sistema_apuestas
DB_USER=mi_usuario
DB_PASSWORD=mi_password
DB_HOST=mi-servidor-db.com
DB_PORT=5432

# Ejecuta migraciones (solo si es necesario)
python manage.py migrate

# Inicia servidor
python manage.py runserver
```

## Importante
- **No verás más Users/Groups por defecto** en Django Admin
- **Tus tablas existentes aparecerán** cuando registres los modelos
- **Admin sigue funcionando** pero con tus datos reales

## Para el Equipo de Desarrollo
```bash
# Clonar y configurar
git clone <repo>
cd "Sistema de Apuestas del Mundial"
cp .env.example .env
# Editar .env con datos de la BD

# Si usan Docker
docker-compose up

# Si conectan a BD externa directa
pip install -r requirements.txt
python manage.py runserver
```

## Verificar Conexión
```bash
# Probar conexión a BD
python manage.py dbshell
# Debería conectarse a tu PostgreSQL
```
