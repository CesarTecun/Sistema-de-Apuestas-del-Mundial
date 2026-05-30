# Guía de Despliegue en Render con Neon

## Configuración Previa
Ya se han creado los archivos necesarios para el despliegue:
- ✅ `frontend/render.yaml` - Configuración del frontend React
- ✅ `backend/render.yaml` - Configuración del backend Django
- ✅ `marcador-service/render.yaml` - Configuración del servicio FastAPI
- ✅ `backend/Procfile` - Actualizado para Render (corrige ruta de manage.py)
- ✅ `marcador-service/Procfile` - Creado para Render

## Notas Importantes sobre la Configuración
- Las variables de entorno con `sync: false` deben configurarse manualmente en el dashboard de Render
- Las URLs de los servicios (backend-mundial.onrender.com, etc.) se generan después del despliegue
- El connection string de Neon debe configurarse manualmente como `DATABASE_URL`

## Pasos para Desplegar en Render

### 1. Preparar tu cuenta de Render
1. Crea una cuenta en [render.com](https://render.com)
2. Conecta tu repositorio de GitHub a Render

### 2. Configurar la Base de Datos Neon
1. Ve a tu proyecto en Neon
2. Copia tu connection string: `postgresql://neondb_owner:PASSWORD@HOST.neon.tech/neondb?sslmode=require`
3. Este string se usará como variable de entorno `DATABASE_URL` en cada servicio

### 3. Desplegar el Backend Django
1. En Render, crea un "New Web Service"
2. Selecciona tu repositorio de GitHub
3. Configura:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 4`
4. Agrega variables de entorno (manualmente en el dashboard de Render):
   - `DATABASE_URL`: Tu connection string de Neon
   - `SECRET_KEY`: Genera una clave secreta (o deja que Render la genere)
   - `DEBUG`: `false`
   - `ALLOWED_HOSTS`: La URL generada por Render (ej: `backend-mundial.onrender.com,localhost`)
   - `CORS_ALLOWED_ORIGINS`: La URL del frontend (se configurará después del despliegue)
5. Haz clic en "Create Web Service"
6. Copia la URL generada (ej: `https://backend-mundial.onrender.com`)

### 4. Desplegar el Marcador Service (FastAPI)
1. Crea otro "New Web Service"
2. Selecciona tu repositorio de GitHub
3. Configura:
   - **Root Directory**: `marcador-service`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Agrega variables de entorno (manualmente en el dashboard de Render):
   - `DATABASE_URL`: Tu connection string de Neon (el mismo que el backend)
   - `API_HOST`: `0.0.0.0`
   - `API_PORT`: `8001`
   - `CORS_ORIGINS`: Las URLs del frontend y backend (se configurarán después del despliegue)
   - `DJANGO_WEBHOOK_URL`: La URL del backend (se configurará después del despliegue)
5. Haz clic en "Create Web Service"
6. Copia la URL generada (ej: `https://marcador-service.onrender.com`)

### 5. Desplegar el Frontend React
1. Crea un "New Web Service"
2. Selecciona tu repositorio de GitHub
3. Configura:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `build`
4. Agrega variables de entorno (manualmente en el dashboard de Render):
   - `REACT_APP_API_URL`: URL del backend (ej: `https://backend-mundial.onrender.com`)
   - `REACT_APP_MARCADOR_URL`: URL del marcador service (ej: `https://marcador-service.onrender.com`)
5. Haz clic en "Create Web Service"

### 6. Configurar Variables de Entorno entre Servicios
Después de que los 3 servicios estén desplegados y tengas sus URLs:

1. **Backend Django**: Actualiza `CORS_ALLOWED_ORIGINS` con la URL del frontend
2. **Marcador Service**: Actualiza `CORS_ORIGINS` con las URLs del frontend y backend
3. **Marcador Service**: Actualiza `DJANGO_WEBHOOK_URL` con la URL del backend
4. **Frontend**: Configura `REACT_APP_API_URL` y `REACT_APP_MARCADOR_URL` con las URLs correspondientes

### 7. Verificar el Despliegue
1. Espera a que los 3 servicios estén en estado "Live"
2. Accede a la URL del frontend
3. Verifica que la aplicación funcione correctamente

## URLs de Producción (Ejemplo)
- Frontend: `https://frontend-mundial.onrender.com`
- Backend: `https://backend-mundial.onrender.com`
- Marcador Service: `https://marcador-service.onrender.com`

## Notas Importantes
- **Base de Datos**: No crees una base de datos en Render, usa tu Neon existente
- **Migraciones**: El backend ejecuta migraciones automáticamente al iniciar
- **CORS**: Asegúrate de que las URLs estén correctamente configuradas
- **Secret Key**: Genera una SECRET_KEY segura para producción
- **Tiempo de despliegue**: El primer despliegue puede tomar 5-10 minutos

## Solución de Problemas Comunes
- Si el backend falla: Revisa los logs en Render para ver errores de migración
- Si el frontend no conecta: Verifica las variables de entorno REACT_APP_*
- Si hay errores de CORS: Revisa las configuraciones de CORS en backend y marcador-service
- Si la BD no conecta: Verifica que el connection string de Neon sea correcto

## Actualizaciones Futuras
Para actualizar tu aplicación:
1. Haz push a GitHub
2. Render detectará los cambios y redeployará automáticamente
3. Si necesitas ejecutar migraciones manuales, usa el shell de Render
