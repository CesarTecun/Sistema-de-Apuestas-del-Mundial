# Generated manually on 2026-05-20
# Pobla selecciones faltantes y 36 partidos del calendario del Mundial 2026.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0008_fix_estado_partido'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                -- ============================================================
                -- 1. SELECCIONES FALTANTES
                -- ============================================================
                INSERT INTO seleccion (id_seleccion, pais, bandera, codigo_iso, status)
                VALUES
                    (50, 'México', 'mexico.png', 'MEX', true),
                    (51, 'Canadá', 'canada.png', 'CAN', true),
                    (52, 'Estados Unidos', 'usa.png', 'USA', true),
                    (53, 'Curazao', 'curazao.png', 'CUW', true)
                ON CONFLICT (id_seleccion) DO NOTHING;

                -- ============================================================
                -- 2. PARTIDOS MUNDIAL 2026 (36 partidos)
                -- Solo columnas que existen en el modelo Django
                -- ============================================================
                INSERT INTO partido (
                    id_partido, horario, equipo_local, equipo_visitante,
                    fk_sede, gol_local, gol_visitante, tipo_partido,
                    resultado, estado_partido, status
                )
                VALUES
                    -- Jueves 11 de junio
                    (43, '2026-06-11 13:00:00-06', 50, 39, 1, 0, 0, 'Regular', NULL, 'programado', true),
                    (44, '2026-06-11 20:00:00-06', 34, 40, 3, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Viernes 12 de junio
                    (45, '2026-06-12 13:00:00-06', 51, 15, 5, 0, 0, 'Regular', NULL, 'programado', true),
                    (46, '2026-06-12 19:00:00-06', 52, 11, 9, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Sábado 13 de junio
                    (47, '2026-06-13 13:00:00-06', 35, 27, 15, 0, 0, 'Regular', NULL, 'programado', true),
                    (48, '2026-06-13 16:00:00-06', 8, 41, 6, 0, 0, 'Regular', NULL, 'programado', true),
                    (49, '2026-06-13 19:00:00-06', 5, 24, 11, 0, 0, 'Regular', NULL, 'programado', true),
                    (50, '2026-06-13 22:00:00-06', 29, 28, 4, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Domingo 14 de junio
                    (51, '2026-06-14 11:00:00-06', 20, 53, 12, 0, 0, 'Regular', NULL, 'programado', true),
                    (52, '2026-06-14 14:00:00-06', 21, 32, 7, 0, 0, 'Regular', NULL, 'programado', true),
                    (53, '2026-06-14 17:00:00-06', 42, 10, 14, 0, 0, 'Regular', NULL, 'programado', true),
                    (54, '2026-06-14 20:00:00-06', 26, 43, 2, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Lunes 15 de junio
                    (55, '2026-06-15 10:00:00-06', 25, 44, 8, 0, 0, 'Regular', NULL, 'programado', true),
                    (56, '2026-06-15 13:00:00-06', 14, 45, 16, 0, 0, 'Regular', NULL, 'programado', true),
                    (57, '2026-06-15 16:00:00-06', 36, 12, 10, 0, 0, 'Regular', NULL, 'programado', true),
                    (58, '2026-06-15 19:00:00-06', 31, 38, 9, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Martes 16 de junio
                    (59, '2026-06-16 13:00:00-06', 19, 46, 6, 0, 0, 'Regular', NULL, 'programado', true),
                    (60, '2026-06-16 16:00:00-06', 30, 22, 11, 0, 0, 'Regular', NULL, 'programado', true),
                    (61, '2026-06-16 19:00:00-06', 7, 47, 13, 0, 0, 'Regular', NULL, 'programado', true),
                    (62, '2026-06-16 22:00:00-06', 13, 33, 15, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Miércoles 17 de junio
                    (63, '2026-06-17 11:00:00-06', 23, 48, 12, 0, 0, 'Regular', NULL, 'programado', true),
                    (64, '2026-06-17 14:00:00-06', 18, 16, 7, 0, 0, 'Regular', NULL, 'programado', true),
                    (65, '2026-06-17 17:00:00-06', 49, 6, 5, 0, 0, 'Regular', NULL, 'programado', true),
                    (66, '2026-06-17 20:00:00-06', 37, 9, 1, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Jueves 18 de junio
                    (67, '2026-06-18 10:00:00-06', 40, 39, 8, 0, 0, 'Regular', NULL, 'programado', true),
                    (68, '2026-06-18 13:00:00-06', 27, 15, 9, 0, 0, 'Regular', NULL, 'programado', true),
                    (69, '2026-06-18 16:00:00-06', 51, 35, 4, 0, 0, 'Regular', NULL, 'programado', true),
                    (70, '2026-06-18 19:00:00-06', 50, 34, 3, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Viernes 19 de junio
                    (71, '2026-06-19 13:00:00-06', 52, 29, 16, 0, 0, 'Regular', NULL, 'programado', true),
                    (72, '2026-06-19 16:00:00-06', 24, 41, 11, 0, 0, 'Regular', NULL, 'programado', true),
                    (73, '2026-06-19 18:30:00-06', 8, 5, 14, 0, 0, 'Regular', NULL, 'programado', true),
                    (74, '2026-06-19 21:00:00-06', 28, 11, 15, 0, 0, 'Regular', NULL, 'programado', true),

                    -- Sábado 20 de junio
                    (75, '2026-06-20 11:00:00-06', 21, 26, 12, 0, 0, 'Regular', NULL, 'programado', true),
                    (76, '2026-06-20 14:00:00-06', 20, 42, 5, 0, 0, 'Regular', NULL, 'programado', true),
                    (77, '2026-06-20 18:00:00-06', 10, 53, 13, 0, 0, 'Regular', NULL, 'programado', true),
                    (78, '2026-06-20 22:00:00-06', 43, 32, 2, 0, 0, 'Regular', NULL, 'programado', true)

                ON CONFLICT (id_partido) DO NOTHING;
            """,
            reverse_sql="""
                DELETE FROM partido WHERE id_partido BETWEEN 43 AND 78;
                DELETE FROM seleccion WHERE id_seleccion IN (50, 51, 52, 53);
            """,
        ),
    ]
