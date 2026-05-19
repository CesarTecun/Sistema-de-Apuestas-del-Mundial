# Base de Datos

> **Nota:** El esquema de la base de datos ahora es gestionado exclusivamente por las migraciones de Django. El archivo `init-db.sql` ha sido renombrado a `init-db.sql.backup` y ya no se ejecuta automáticamente.

## Roles de base de datos

Si necesitas crear roles personalizados, hazlo manualmente en PostgreSQL o mediante migraciones/data migrations de Django.

### `quiniela_admin` (ejemplo)

Rol para ejecutar la aplicación backend con permisos de escritura.

Uso recomendado en `.env` para el backend:

```env
DB_USER=quiniela_admin
DB_PASSWORD=CAMBIAR_PASSWORD_ADMIN
```

### `quiniela_readonly` (ejemplo)

Rol para consultas, reportes o revisión sin modificar datos.

Uso recomendado para herramientas de consulta/reportes:

```env
DB_USER=quiniela_readonly
DB_PASSWORD=CAMBIAR_PASSWORD_READONLY
```

## Seguridad

El usuario `postgres` debe reservarse para administración de la base de datos, no para ejecutar la aplicación.
