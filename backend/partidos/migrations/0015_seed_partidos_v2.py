import datetime
from django.db import migrations


def seed_partidos(apps, schema_editor):
    """Inserta los 36 partidos de fase de grupos del Mundial 2026."""
    Seleccion = apps.get_model('partidos', 'Seleccion')
    Partido = apps.get_model('partidos', 'Partido')

    def sel_id(pais):
        return Seleccion.objects.get(pais=pais).id_seleccion

    cst = datetime.timezone(datetime.timedelta(hours=-6))

    PARTIDOS = [
        # Jueves 11 de junio
        ('2026-06-11 13:00', 'México', 'Sudáfrica', 1),
        ('2026-06-11 20:00', 'Corea del Sur', 'República Checa', 3),
        # Viernes 12 de junio
        ('2026-06-12 13:00', 'Canadá', 'Bosnia y Herzegovina', 5),
        ('2026-06-12 19:00', 'Estados Unidos', 'Paraguay', 9),
        # Sábado 13 de junio
        ('2026-06-13 13:00', 'Catar', 'Suiza', 15),
        ('2026-06-13 16:00', 'Brasil', 'Marruecos', 6),
        ('2026-06-13 19:00', 'Haití', 'Escocia', 11),
        ('2026-06-13 22:00', 'Australia', 'Turquía', 4),
        # Domingo 14 de junio
        ('2026-06-14 11:00', 'Alemania', 'Curazao', 12),
        ('2026-06-14 14:00', 'Países Bajos', 'Japón', 7),
        ('2026-06-14 17:00', 'Costa de Marfil', 'Ecuador', 14),
        ('2026-06-14 20:00', 'Suecia', 'Túnez', 2),
        # Lunes 15 de junio
        ('2026-06-15 10:00', 'España', 'Cabo Verde', 8),
        ('2026-06-15 13:00', 'Bélgica', 'Egipto', 16),
        ('2026-06-15 16:00', 'Arabia Saudita', 'Uruguay', 10),
        ('2026-06-15 19:00', 'Irán', 'Nueva Zelanda', 9),
        # Martes 16 de junio
        ('2026-06-16 13:00', 'Francia', 'Senegal', 6),
        ('2026-06-16 16:00', 'Irak', 'Noruega', 11),
        ('2026-06-16 19:00', 'Argentina', 'Argelia', 13),
        ('2026-06-16 22:00', 'Austria', 'Jordania', 15),
        # Miércoles 17 de junio
        ('2026-06-17 11:00', 'Portugal', 'República Democrática del Congo', 12),
        ('2026-06-17 14:00', 'Inglaterra', 'Croacia', 7),
        ('2026-06-17 17:00', 'Ghana', 'Panamá', 5),
        ('2026-06-17 20:00', 'Uzbekistán', 'Colombia', 1),
        # Jueves 18 de junio
        ('2026-06-18 10:00', 'República Checa', 'Sudáfrica', 8),
        ('2026-06-18 13:00', 'Suiza', 'Bosnia y Herzegovina', 9),
        ('2026-06-18 16:00', 'Canadá', 'Catar', 4),
        ('2026-06-18 19:00', 'México', 'Corea del Sur', 3),
        # Viernes 19 de junio
        ('2026-06-19 13:00', 'Estados Unidos', 'Australia', 16),
        ('2026-06-19 16:00', 'Escocia', 'Marruecos', 11),
        ('2026-06-19 18:30', 'Brasil', 'Haití', 14),
        ('2026-06-19 21:00', 'Turquía', 'Paraguay', 15),
        # Sábado 20 de junio
        ('2026-06-20 11:00', 'Países Bajos', 'Suecia', 12),
        ('2026-06-20 14:00', 'Alemania', 'Costa de Marfil', 5),
        ('2026-06-20 18:00', 'Ecuador', 'Curazao', 13),
        ('2026-06-20 22:00', 'Túnez', 'Japón', 2),
    ]

    partidos_objs = []
    for fecha_hora, local, visitante, sede in PARTIDOS:
        dt = datetime.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M').replace(tzinfo=cst)
        partidos_objs.append(Partido(
            horario=dt,
            equipo_local=sel_id(local),
            equipo_visitante=sel_id(visitante),
            fk_sede=sede,
            gol_local=0,
            gol_visitante=0,
            tipo_partido='Regular',
            resultado=None,
            estado_partido='programado',
            status=True,
        ))

    Partido.objects.bulk_create(partidos_objs, batch_size=500)
    print(f"Insertados {len(partidos_objs)} partidos.")


def reverse_seed(apps, schema_editor):
    """Elimina los partidos de fase de grupos insertados."""
    Partido = apps.get_model('partidos', 'Partido')
    cst = datetime.timezone(datetime.timedelta(hours=-6))
    inicio = datetime.datetime(2026, 6, 11, 0, 0, tzinfo=cst)
    fin = datetime.datetime(2026, 6, 21, 0, 0, tzinfo=cst)
    Partido.objects.filter(horario__gte=inicio, horario__lt=fin).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0014_seed_selecciones_v2'),
    ]

    operations = [
        migrations.RunPython(seed_partidos, reverse_seed),
    ]
