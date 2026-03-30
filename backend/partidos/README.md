# Módulo de Partidos - Sistema de Apuestas del Mundial 2026

## Descripción
Este módulo gestiona los partidos del sistema de apuestas, permitiendo crear, administrar y controlar los resultados de los encuentros deportivos.

## Funcionalidades

### Modelo Partido
- **id_partido**: Identificador único (AutoField)
- **horario**: Fecha y hora del partido (DateTimeField)
- **equipo_local**: ID del equipo local (IntegerField)
- **equipo_visitante**: ID del equipo visitante (IntegerField)
- **fk_sede**: ID de la sede (IntegerField, nullable)
- **fk_id_fase**: ID de la fase (IntegerField, nullable)
- **gol_local**: Goles del equipo local (IntegerField, default=0)
- **gol_visitante**: Goles del equipo visitante (IntegerField, default=0)
- **ganador_penales**: Ganador por penales (IntegerField, nullable)
- **tipo_partido**: Tipo de partido (CharField, default='Regular')
- **resultado**: Resultado del partido (CharField, nullable)

### Propiedades del Modelo
- **resultado_display**: Retorna el marcador formateado "X - Y"
- **ganador**: Determina automáticamente el ganador según goles o penales

### Endpoints de la API

#### CRUD Completo de Partidos
- `GET /api/partidos/api/partidos/` - Listar todos los partidos
- `POST /api/partidos/api/partidos/` - Crear nuevo partido
- `GET /api/partidos/api/partidos/{id}/` - Obtener partido específico
- `PATCH /api/partidos/api/partidos/{id}/` - Actualizar partido
- `DELETE /api/partidos/api/partidos/{id}/` - Eliminar partido

#### Endpoints Especiales
- `GET /api/partidos/api/partidos/por-liga/?liga_id={id}` - Obtener partidos por liga
- `GET /api/partidos/api/partidos/por-equipo/?equipo_id={id}` - Obtener partidos por equipo
- `POST /api/partidos/api/partidos/{id}/actualizar-resultado/` - Actualizar resultado de partido

### Admin de Django
El módulo incluye una interfaz administrativa completa con:
- Listado de partidos con filtros por tipo y fase
- Búsqueda por equipos
- Campos de solo lectura para ID
- Fieldsets organizados por categorías
- Protección contra modificación de equipos después de crear

## Ejemplos de Uso

### Crear un Partido
```json
POST /api/partidos/api/partidos/
{
    "horario": "2026-06-15T14:00:00Z",
    "equipo_local": 1,
    "equipo_visitante": 2,
    "fk_sede": 1,
    "fk_id_fase": 1,
    "gol_local": 0,
    "gol_visitante": 0,
    "tipo_partido": "Regular"
}
```

### Actualizar Resultado
```json
POST /api/partidos/api/partidos/1/actualizar-resultado/
{
    "gol_local": 2,
    "gol_visitante": 1,
    "resultado": "Local 2-1 Visitante"
}
```

### Obtener Partidos por Liga
```
GET /api/partidos/api/partidos/por-liga/?liga_id=1
```

### Obtener Partidos por Equipo
```
GET /api/partidos/api/partidos/por-equipo/?equipo_id=1
```

## Validaciones
- Los goles no pueden ser negativos
- Todos los campos requeridos deben estar presentes
- El horario debe ser una fecha válida

## Pruebas
El módulo incluye pruebas completas:
- Pruebas del modelo y propiedades
- Pruebas de la API (CRUD completo)
- Pruebas de validaciones
- Pruebas de endpoints especiales

Ejecutar pruebas:
```bash
python manage.py test partidos
```

## Relaciones Futuras
- Conectar con modelo de Equipos
- Conectar con modelo de Sedes
- Conectar con modelo de Fases
- Integrar con sistema de pronósticos

## Notas Importantes
- La tabla `partido` ya existe en la base de datos
- Django está configurado como `managed = False` para no alterar la estructura existente
- Todos los endpoints requieren autenticación
- El modelo incluye propiedades útiles para cálculos automáticos
