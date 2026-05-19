# Base de Datos

> **Nota:** El esquema de la base de datos ahora es gestionado exclusivamente por las migraciones de Django. El archivo `init-db.sql` ha sido renombrado a `init-db.sql.backup` y ya no se ejecuta automáticamente.

## Roles de base de datos

El archivo `roles.sql` define dos roles principales para cumplir con el requisito de **separación de roles** (principio de mínimo privilegio):

### `quiniela_app`

Rol de aplicación para el backend Django. Tiene permisos DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) pero **NO tiene permisos DDL** (`CREATE`, `DROP`, `ALTER`).

```env
DB_USER=quiniela_app
DB_PASSWORD=CAMBIAR_PASSWORD_APP
```

### `quiniela_readonly`

Rol de solo lectura para reportes y dashboards. Únicamente `SELECT`.

```env
DB_USER=quiniela_readonly
DB_PASSWORD=CAMBIAR_PASSWORD_READONLY
```

### Crear roles

```bash
psql -U postgres -d quiniela -f database/roles.sql
```

> **Importante:** Cambiar las contraseñas temporales antes de usar en producción.

## Seguridad

- El usuario `postgres` debe reservarse para administración de la base de datos, no para ejecutar la aplicación.
- El backend debe conectarse con `quiniela_app` (sin permisos DDL).
