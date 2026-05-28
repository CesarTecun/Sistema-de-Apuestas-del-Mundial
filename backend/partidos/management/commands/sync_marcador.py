"""
Comando de Django para sincronizar datos con el microservicio marcador.

Uso:
    python manage.py sync_marcador --verify           # Solo verificar estado
    python manage.py sync_marcador --sync-selecciones # Sincronizar selecciones
    python manage.py sync_marcador --sync-partidos    # Sincronizar partidos
    python manage.py sync_marcador --all              # Sincronizar todo
"""

from django.core.management.base import BaseCommand
from backend.partidos.models import Seleccion, Partido
from backend.marcador_client import marcador_client, MarcadorClientError


class Command(BaseCommand):
    help = 'Sincroniza selecciones y partidos con el microservicio marcador'

    # Mismo mapa de selecciones que en seed.py del marcador-service
    # + selecciones adicionales que no clasificaron al Mundial 2026
    SELECCIONES_MUNDIAL_2026 = {
        "Canadá": "CAN",
        "México": "MEX",
        "Estados Unidos": "USA",
        "Curazao": "CUW",
        "Haití": "HTI",
        "Panamá": "PAN",
        "Argentina": "ARG",
        "Brasil": "BRA",
        "Colombia": "COL",
        "Ecuador": "ECU",
        "Paraguay": "PRY",
        "Uruguay": "URY",
        "Austria": "AUT",
        "Bélgica": "BEL",
        "Bosnia y Herzegovina": "BIH",
        "Croacia": "HRV",
        "Chequia": "CZE",
        "Inglaterra": "ENG",
        "Francia": "FRA",
        "Alemania": "DEU",
        "Países Bajos": "NLD",
        "Noruega": "NOR",
        "Portugal": "PRT",
        "Escocia": "SCO",
        "España": "ESP",
        "Suecia": "SWE",
        "Suiza": "CHE",
        "Turquía": "TUR",
        "Australia": "AUS",
        "Irak": "IRQ",
        "Irán": "IRN",
        "Japón": "JPN",
        "Jordania": "JOR",
        "Corea del Sur": "KOR",
        "Catar": "QAT",
        "Arabia Saudita": "SAU",
        "Uzbekistán": "UZB",
        "Nueva Zelanda": "NZL",
        # Selecciones adicionales (no clasificaron al Mundial 2026)
        "Sudáfrica": "ZAF",
        "Marruecos": "MAR",
        "Senegal": "SEN",
        "Chile": "CHL",
        "Ucrania": "UKR",
        "Egipto": "EGY",
        "Perú": "PER",
        "Túnez": "TUN",
        "Gales": "WAL",
        "Jamaica": "JAM",
        "Costa de Marfil": "CIV",
        "Venezuela": "VEN",
        "Polonia": "POL",
        "Argelia": "DZA",
        "Ghana": "GHA",
        "Dinamarca": "DNK",
        "Serbia": "SRB",
        "Nigeria": "NGA",
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Solo verificar estado sin sincronizar',
        )
        parser.add_argument(
            '--sync-selecciones',
            action='store_true',
            help='Sincronizar selecciones con el marcador',
        )
        parser.add_argument(
            '--sync-partidos',
            action='store_true',
            help='Sincronizar partidos con el marcador',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Sincronizar selecciones y partidos',
        )
        parser.add_argument(
            '--fix-iso',
            action='store_true',
            help='Asignar codigo_iso faltantes basándose en el nombre del país',
        )

    def handle(self, *args, **options):
        verify_only = options['verify']
        sync_selecciones = options['sync_selecciones']
        sync_partidos = options['sync_partidos']
        sync_all = options['all']
        fix_iso = options['fix_iso']

        self.stdout.write(self.style.SUCCESS('=== SINCRONIZACIÓN CON MARCADOR-SERVICE ===\n'))

        # 1. Verificar estado de selecciones
        self._verificar_selecciones()

        if fix_iso:
            self._fix_codigo_iso()

        if verify_only:
            self.stdout.write(self.style.WARNING('\nModo verificación: no se sincronizará nada.'))
            return

        # 2. Sincronizar según opciones
        if sync_all or sync_selecciones:
            self._sincronizar_selecciones()

        if sync_all or sync_partidos:
            self._sincronizar_partidos()

        if not (sync_all or sync_selecciones or sync_partidos):
            self.stdout.write(self.style.WARNING('\nNo se especificó ninguna acción de sincronización.'))
            self.stdout.write(self.style.WARNING('Usa --sync-selecciones, --sync-partidos o --all'))

    def _verificar_selecciones(self):
        """Verifica el estado de las selecciones en Django."""
        total = Seleccion.objects.count()
        con_iso = Seleccion.objects.exclude(codigo_iso__isnull=True).exclude(codigo_iso='').count()
        sin_iso = total - con_iso

        self.stdout.write(f'Selecciones en Django: {total}')
        self.stdout.write(f'Con codigo_iso: {con_iso}')
        self.stdout.write(f'Sin codigo_iso: {sin_iso}')

        if sin_iso > 0:
            self.stdout.write(self.style.WARNING(f'⚠️  {sin_iso} selecciones sin codigo_iso:'))
            sin_iso_list = Seleccion.objects.filter(codigo_iso__isnull=True) | Seleccion.objects.filter(codigo_iso='')
            for s in sin_iso_list:
                self.stdout.write(f'  - ID: {s.id_seleccion:2d} | País: {s.pais}')
        else:
            self.stdout.write(self.style.SUCCESS('✅ Todas las selecciones tienen codigo_iso'))

    def _fix_codigo_iso(self):
        """Asigna codigo_iso faltantes basándose en el nombre del país."""
        self.stdout.write('\n--- ASIGNANDO CODIGO_ISO FALTANTES ---')

        sin_iso = Seleccion.objects.filter(codigo_iso__isnull=True) | Seleccion.objects.filter(codigo_iso='')
        actualizados = 0

        for seleccion in sin_iso:
            # Buscar codigo_iso basándose en el nombre del país
            codigo_iso = self.SELECCIONES_MUNDIAL_2026.get(seleccion.pais)
            if codigo_iso:
                seleccion.codigo_iso = codigo_iso
                seleccion.save(update_fields=['codigo_iso'])
                self.stdout.write(self.style.SUCCESS(f'✅ {seleccion.pais} -> {codigo_iso}'))
                actualizados += 1
            else:
                self.stdout.write(self.style.WARNING(f'⚠️  No se encontró codigo_iso para: {seleccion.pais}'))

        self.stdout.write(f'\nTotal actualizados: {actualizados}/{sin_iso.count()}')

    def _sincronizar_selecciones(self):
        """Sincroniza todas las selecciones con el marcador-service."""
        self.stdout.write('\n--- SINCRONIZANDO SELECCIONES ---')

        selecciones = Seleccion.objects.exclude(codigo_iso__isnull=True).exclude(codigo_iso='')
        total = selecciones.count()
        exitosos = 0
        fallidos = 0

        for seleccion in selecciones:
            payload = {
                "id_seleccion": seleccion.id_seleccion,
                "pais": seleccion.pais,
                "bandera": seleccion.bandera,
                "fk_id_fase_inicial": seleccion.fk_id_fase_inicial,
                "codigo_iso": seleccion.codigo_iso,
                "status": seleccion.status,
            }
            try:
                marcador_client.sync_seleccion(payload)
                self.stdout.write(f'✅ {seleccion.pais} (ID: {seleccion.id_seleccion})')
                exitosos += 1
            except MarcadorClientError as e:
                self.stdout.write(self.style.ERROR(f'❌ {seleccion.pais}: {e}'))
                fallidos += 1

        self.stdout.write(f'\nSelecciones sincronizadas: {exitosos}/{total}')
        if fallidos > 0:
            self.stdout.write(self.style.ERROR(f'Fallidos: {fallidos}'))

    def _sincronizar_partidos(self):
        """Sincroniza todos los partidos con el marcador-service."""
        self.stdout.write('\n--- SINCRONIZANDO PARTIDOS ---')

        partidos = Partido.objects.all()
        total = partidos.count()
        exitosos = 0
        fallidos = 0

        for partido in partidos:
            payload = {
                "id_partido": partido.id_partido,
                "horario": partido.horario.isoformat() if partido.horario else None,
                "equipo_local": partido.equipo_local,
                "equipo_visitante": partido.equipo_visitante,
                "fk_sede": partido.fk_sede,
                "fk_id_fase": partido.fk_id_fase,
                "fk_id_liga": partido.fk_id_liga,
                "gol_local": partido.gol_local,
                "gol_visitante": partido.gol_visitante,
                "ganador_penales": partido.ganador_penales,
                "tipo_partido": partido.tipo_partido,
                "resultado": partido.resultado,
                "estado": partido.estado_partido,
                "status": partido.status,
            }
            try:
                marcador_client.sync_partido(payload)
                self.stdout.write(f'✅ Partido {partido.id_partido}')
                exitosos += 1
            except MarcadorClientError as e:
                self.stdout.write(self.style.ERROR(f'❌ Partido {partido.id_partido}: {e}'))
                fallidos += 1

        self.stdout.write(f'\nPartidos sincronizados: {exitosos}/{total}')
        if fallidos > 0:
            self.stdout.write(self.style.ERROR(f'Fallidos: {fallidos}'))
