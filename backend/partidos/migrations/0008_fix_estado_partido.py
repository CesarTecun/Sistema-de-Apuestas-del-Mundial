# Generated manually on 2026-05-20
# Corrige duplicidad: hace el modelo usar la columna existente estado_partido.
# Funciona tanto en BD nueva (renombra estado->estado_partido) como en BD existente.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0007_add_standings_fields'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='partido',
                    name='estado',
                ),
                migrations.AddField(
                    model_name='partido',
                    name='estado_partido',
                    field=models.CharField(
                        choices=[
                            ('programado', 'Programado'),
                            ('en_juego', 'En juego'),
                            ('finalizado', 'Finalizado'),
                            ('suspendido', 'Suspendido'),
                        ],
                        db_column='estado_partido',
                        default='programado',
                        max_length=20,
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        DO $$
                        BEGIN
                            -- En BD nueva: estado existe pero estado_partido no -> renombrar
                            IF EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='partido' AND column_name='estado'
                            ) AND NOT EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='partido' AND column_name='estado_partido'
                            ) THEN
                                ALTER TABLE partido RENAME COLUMN estado TO estado_partido;
                            END IF;

                            -- En BD existente: hay columna duplicada estado -> eliminarla
                            IF EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='partido' AND column_name='estado'
                            ) AND EXISTS (
                                SELECT 1 FROM information_schema.columns
                                WHERE table_name='partido' AND column_name='estado_partido'
                            ) THEN
                                ALTER TABLE partido DROP COLUMN estado;
                            END IF;

                            -- Normalizar valores antiguos (Finalizado -> finalizado, etc.)
                            UPDATE partido
                            SET estado_partido = CASE estado_partido
                                WHEN 'Finalizado' THEN 'finalizado'
                                WHEN 'No_Iniciado' THEN 'programado'
                                WHEN 'En_Juego' THEN 'en_juego'
                                WHEN 'Suspendido' THEN 'suspendido'
                                ELSE COALESCE(estado_partido, 'programado')
                            END
                            WHERE estado_partido NOT IN ('programado','en_juego','finalizado','suspendido');
                        END $$;
                    """,
                    reverse_sql="""
                        ALTER TABLE partido ADD COLUMN IF NOT EXISTS estado varchar(20) DEFAULT 'programado';
                    """,
                ),
            ],
        ),
    ]
