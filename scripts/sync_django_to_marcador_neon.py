"""
Script para sincronizar datos de Django (base general) al microservicio marcador en Neon.
Replica las tablas 'seleccion' y 'partido' con sus IDs originales.
"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Base de datos Django (base general)
DJANGO_DB = "postgresql://neondb_owner:npg_pQrLmJXlZ78I@ep-falling-cherry-aqc89mqe.c-8.us-east-1.aws.neon.tech:5432/quiniela?sslmode=require"

# Base de datos del microservicio marcador en Neon (proyecto 'tablero')
MARCADOR_DB = "postgresql://neondb_owner:npg_eZ7sPF3fGglv@ep-small-poetry-aqil41c7.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require"


def sync_selecciones():
    source = psycopg2.connect(DJANGO_DB)
    target = psycopg2.connect(MARCADOR_DB)

    cur_src = source.cursor(cursor_factory=RealDictCursor)
    cur_tgt = target.cursor()

    # Leer selecciones de Django
    cur_src.execute(
        "SELECT id_seleccion, pais, bandera, fk_id_fase_inicial, codigo_iso, status, deleted_at "
        "FROM seleccion WHERE status = true OR status IS NULL"
    )
    selecciones = cur_src.fetchall()

    # Insertar/actualizar en marcador
    for s in selecciones:
        cur_tgt.execute(
            """
            INSERT INTO seleccion (id_seleccion, pais, bandera, fk_id_fase_inicial, codigo_iso, status, deleted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id_seleccion) DO UPDATE SET
                pais = EXCLUDED.pais,
                bandera = EXCLUDED.bandera,
                fk_id_fase_inicial = EXCLUDED.fk_id_fase_inicial,
                codigo_iso = EXCLUDED.codigo_iso,
                status = EXCLUDED.status,
                deleted_at = EXCLUDED.deleted_at
            """,
            (s['id_seleccion'], s['pais'], s['bandera'], s['fk_id_fase_inicial'],
             s['codigo_iso'], s.get('status', True), s['deleted_at'])
        )

    target.commit()
    print(f"Sincronizadas {len(selecciones)} selecciones")

    cur_src.close()
    cur_tgt.close()
    source.close()
    target.close()


def sync_partidos():
    source = psycopg2.connect(DJANGO_DB)
    target = psycopg2.connect(MARCADOR_DB)

    cur_src = source.cursor(cursor_factory=RealDictCursor)
    cur_tgt = target.cursor()

    # Leer partidos de Django
    cur_src.execute(
        "SELECT id_partido, horario, equipo_local, equipo_visitante, fk_sede, fk_id_fase, fk_id_liga, "
        "gol_local, gol_visitante, ganador_penales, tipo_partido, resultado, estado_partido AS estado, "
        "status, deleted_at FROM partido WHERE status = true OR status IS NULL"
    )
    partidos = cur_src.fetchall()

    # Insertar/actualizar en marcador
    for p in partidos:
        cur_tgt.execute(
            """
            INSERT INTO partido (
                id_partido, horario, equipo_local, equipo_visitante, fk_sede, fk_id_fase, fk_id_liga,
                gol_local, gol_visitante, ganador_penales, tipo_partido, resultado, estado,
                status, deleted_at,
                minuto_actual, periodo_actual, tiempo_extra_periodo, partido_iniciado, partido_pausado,
                faltas_local, faltas_visitante
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                0, '1T', 0, false, false, 0, 0
            )
            ON CONFLICT (id_partido) DO UPDATE SET
                horario = EXCLUDED.horario,
                equipo_local = EXCLUDED.equipo_local,
                equipo_visitante = EXCLUDED.equipo_visitante,
                fk_sede = EXCLUDED.fk_sede,
                fk_id_fase = EXCLUDED.fk_id_fase,
                fk_id_liga = EXCLUDED.fk_id_liga,
                gol_local = EXCLUDED.gol_local,
                gol_visitante = EXCLUDED.gol_visitante,
                ganador_penales = EXCLUDED.ganador_penales,
                tipo_partido = EXCLUDED.tipo_partido,
                resultado = EXCLUDED.resultado,
                estado = EXCLUDED.estado,
                status = EXCLUDED.status,
                deleted_at = EXCLUDED.deleted_at
            """,
            (p['id_partido'], p['horario'], p['equipo_local'], p['equipo_visitante'],
             p['fk_sede'], p['fk_id_fase'], p['fk_id_liga'],
             p['gol_local'], p['gol_visitante'], p['ganador_penales'],
             p['tipo_partido'], p['resultado'], p['estado'],
             p.get('status', True), p['deleted_at'])
        )

    target.commit()
    print(f"Sincronizados {len(partidos)} partidos")

    cur_src.close()
    cur_tgt.close()
    source.close()
    target.close()


if __name__ == "__main__":
    sync_selecciones()
    sync_partidos()
    print("Sincronizacion completada exitosamente.")
