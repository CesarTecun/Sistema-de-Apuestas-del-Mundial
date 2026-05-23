from django.db import migrations


def seed_selecciones_v2(apps, schema_editor):
    """Inserta las selecciones del Mundial 2026 con banderas e ISO."""
    Seleccion = apps.get_model('partidos', 'Seleccion')

    PAIS_DATA = {
        'Alemania': ('https://flagcdn.com/de.svg', 'DEU'),
        'Arabia Saudita': ('https://flagcdn.com/sa.svg', 'SAU'),
        'Argelia': ('https://flagcdn.com/dz.svg', 'DZA'),
        'Argentina': ('https://flagcdn.com/ar.svg', 'ARG'),
        'Australia': ('https://flagcdn.com/au.svg', 'AUS'),
        'Austria': ('https://flagcdn.com/at.svg', 'AUT'),
        'Bélgica': ('https://flagcdn.com/be.svg', 'BEL'),
        'Bosnia y Herzegovina': ('https://flagcdn.com/ba.svg', 'BIH'),
        'Brasil': ('https://flagcdn.com/br.svg', 'BRA'),
        'Cabo Verde': ('https://flagcdn.com/cv.svg', 'CPV'),
        'Canadá': ('https://flagcdn.com/ca.svg', 'CAN'),
        'Catar': ('https://flagcdn.com/qa.svg', 'QAT'),
        'Colombia': ('https://flagcdn.com/co.svg', 'COL'),
        'Corea del Sur': ('https://flagcdn.com/kr.svg', 'KOR'),
        'Costa de Marfil': ('https://flagcdn.com/ci.svg', 'CIV'),
        'Croacia': ('https://flagcdn.com/hr.svg', 'HRV'),
        'Curazao': ('https://flagcdn.com/cw.svg', 'CUW'),
        'Ecuador': ('https://flagcdn.com/ec.svg', 'ECU'),
        'Egipto': ('https://flagcdn.com/eg.svg', 'EGY'),
        'Escocia': ('https://flagcdn.com/gb-sct.svg', 'SCO'),
        'España': ('https://flagcdn.com/es.svg', 'ESP'),
        'Estados Unidos': ('https://flagcdn.com/us.svg', 'USA'),
        'Francia': ('https://flagcdn.com/fr.svg', 'FRA'),
        'Ghana': ('https://flagcdn.com/gh.svg', 'GHA'),
        'Haití': ('https://flagcdn.com/ht.svg', 'HTI'),
        'Inglaterra': ('https://flagcdn.com/gb-eng.svg', 'ENG'),
        'Irak': ('https://flagcdn.com/iq.svg', 'IRQ'),
        'Irán': ('https://flagcdn.com/ir.svg', 'IRN'),
        'Japón': ('https://flagcdn.com/jp.svg', 'JPN'),
        'Jordania': ('https://flagcdn.com/jo.svg', 'JOR'),
        'Marruecos': ('https://flagcdn.com/ma.svg', 'MAR'),
        'México': ('https://flagcdn.com/mx.svg', 'MEX'),
        'Noruega': ('https://flagcdn.com/no.svg', 'NOR'),
        'Nueva Zelanda': ('https://flagcdn.com/nz.svg', 'NZL'),
        'Países Bajos': ('https://flagcdn.com/nl.svg', 'NLD'),
        'Panamá': ('https://flagcdn.com/pa.svg', 'PAN'),
        'Paraguay': ('https://flagcdn.com/py.svg', 'PRY'),
        'Portugal': ('https://flagcdn.com/pt.svg', 'PRT'),
        'República Checa': ('https://flagcdn.com/cz.svg', 'CZE'),
        'República Democrática del Congo': ('https://flagcdn.com/cd.svg', 'COD'),
        'Senegal': ('https://flagcdn.com/sn.svg', 'SEN'),
        'Sudáfrica': ('https://flagcdn.com/za.svg', 'ZAF'),
        'Suecia': ('https://flagcdn.com/se.svg', 'SWE'),
        'Suiza': ('https://flagcdn.com/ch.svg', 'CHE'),
        'Túnez': ('https://flagcdn.com/tn.svg', 'TUN'),
        'Turquía': ('https://flagcdn.com/tr.svg', 'TUR'),
        'Uruguay': ('https://flagcdn.com/uy.svg', 'URY'),
        'Uzbekistán': ('https://flagcdn.com/uz.svg', 'UZB'),
    }

    for pais, (bandera, iso) in PAIS_DATA.items():
        Seleccion.objects.get_or_create(
            pais=pais,
            defaults={
                'bandera': bandera,
                'codigo_iso': iso,
                'status': True,
            }
        )


def reverse_seed(apps, schema_editor):
    """Elimina las selecciones insertadas."""
    Seleccion = apps.get_model('partidos', 'Seleccion')
    paises = [
        'Alemania', 'Arabia Saudita', 'Argelia', 'Argentina', 'Australia',
        'Austria', 'Bélgica', 'Bosnia y Herzegovina', 'Brasil', 'Cabo Verde',
        'Canadá', 'Catar', 'Colombia', 'Corea del Sur', 'Costa de Marfil',
        'Croacia', 'Curazao', 'Ecuador', 'Egipto', 'Escocia', 'España',
        'Estados Unidos', 'Francia', 'Ghana', 'Haití', 'Inglaterra', 'Irak',
        'Irán', 'Japón', 'Jordania', 'Marruecos', 'México', 'Noruega',
        'Nueva Zelanda', 'Países Bajos', 'Panamá', 'Paraguay', 'Portugal',
        'República Checa', 'República Democrática del Congo', 'Senegal',
        'Sudáfrica', 'Suecia', 'Suiza', 'Túnez', 'Turquía', 'Uruguay',
        'Uzbekistán',
    ]
    Seleccion.objects.filter(pais__in=paises).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('partidos', '0013_clear_seleccion_jugador_partido'),
    ]

    operations = [
        migrations.RunPython(seed_selecciones_v2, reverse_seed),
    ]
