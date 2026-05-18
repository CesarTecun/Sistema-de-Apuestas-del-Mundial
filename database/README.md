# Base de Datos

## Roles de base de datos

El script `init-db.sql` crea dos roles de aplicación además del superusuario `postgres`.

### `quiniela_admin`

Rol para ejecutar la aplicación backend con permisos de escritura.

Permisos:

- `CONNECT` a la base de datos.
- `USAGE` sobre el schema `public`.
- `SELECT`, `INSERT`, `UPDATE`, `DELETE` sobre tablas.
- `USAGE`, `SELECT`, `UPDATE` sobre secuencias.
- `EXECUTE` sobre funciones.

Uso recomendado en `.env` para el backend:

```env
DB_USER=quiniela_admin
DB_PASSWORD=CAMBIAR_PASSWORD_ADMIN
```

### `quiniela_readonly`

Rol para consultas, reportes o revisión sin modificar datos.

Permisos:

- `CONNECT` a la base de datos.
- `USAGE` sobre el schema `public`.
- `SELECT` sobre tablas.
- `SELECT` sobre secuencias.

Uso recomendado para herramientas de consulta/reportes:

```env
DB_USER=quiniela_readonly
DB_PASSWORD=CAMBIAR_PASSWORD_READONLY
```

## Seguridad

Antes de usar la base fuera de desarrollo, cambiar las contraseñas temporales definidas en `init-db.sql`:

- `CAMBIAR_PASSWORD_ADMIN`
- `CAMBIAR_PASSWORD_READONLY`

El usuario `postgres` debe reservarse para administración de la base de datos, no para ejecutar la aplicación.
