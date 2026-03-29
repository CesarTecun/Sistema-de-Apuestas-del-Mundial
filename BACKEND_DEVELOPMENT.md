# Guía de Desarrollo Backend - Sin Frontend

## Herramientas Disponibles para Testing

### 1. Django Admin Panel
**URL:** http://127.0.0.1:8000/admin/
**Usuario:** admin
**Contraseña:** admin123

**Funcionalidades:**
- Gestión de usuarios y grupos
- CRUD de todos los modelos
- Interface web para probar datos
- No requiere frontend

### 2. Django REST Framework Browsable API
**URL:** http://127.0.0.1:8000/api/
**Autenticación:** Session (login via admin) o Basic Auth

**Funcionalidades:**
- Interface web para probar endpoints
- Formularios HTML para POST/PUT
- Visualización de respuestas JSON
- Documentación automática de APIs

### 3. Django Shell
```bash
python manage.py shell
```

**Ejemplos de uso:**
```python
# Crear usuarios de prueba
from django.contrib.auth.models import User
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Probar modelos (cuando los creen)
from mi_app.models import Liga
liga = Liga.objects.create(nombre='Liga Test', administrador=user)
```

### 4. Django Management Commands
```bash
# Crear datos de prueba
python manage.py shell < create_test_data.py

# Verificar migraciones
python manage.py showmigrations

# Probar endpoints con curl
curl -X GET http://127.0.0.1:8000/api/usuarios/
curl -X POST -H "Content-Type: application/json" -d '{"nombre":"test"}' http://127.0.0.1:8000/api/ligas/
```

## Flujo de Trabajo para Desarrollo Backend

1. **Crear modelos en su app Django**
2. **Registrar en admin.py** para gestión visual
3. **Crear serializers** para API endpoints
4. **Crear ViewSets** para CRUD automático
5. **Probar en /admin/** para datos
6. **Probar en /api/** para endpoints REST

## URLs Importantes
- Admin: http://127.0.0.1:8000/admin/
- API Browser: http://127.0.0.1:8000/api/
- API Root: http://127.0.0.1:8000/api-auth/login/

## Notas para el Equipo Backend
- No necesitan instalar React ni Node.js
- Solo necesitan Python y las dependencias en requirements.txt
- Pueden probar toda la lógica de negocio sin frontend
- Los datos creados persisten en db.sqlite3 (no subir a Git)
