from django.contrib import admin, messages
from django.utils import timezone

from backend.usuarios.models import Usuario
from .models import Liga, Invitacion, ParticipanteLiga, SolicitudParticipacion
from .emails import enviar_correo_invitacion


def contar_participantes_activos(liga_id: int) -> int:
    return ParticipanteLiga.objects.filter(
        fk_id_liga=liga_id,
        estado_participacion='Activo'
    ).count()


def hay_cupo_disponible(liga: Liga) -> bool:
    if liga.cupo_maximo is None:
        return True
    return contar_participantes_activos(liga.id_liga) < liga.cupo_maximo


def agregar_participante_a_liga(liga: Liga, usuario_id: int) -> ParticipanteLiga:
    participante, _ = ParticipanteLiga.objects.get_or_create(
        fk_id_liga=liga.id_liga,
        fk_id_usuario=usuario_id,
        defaults={'estado_participacion': 'Activo'}
    )
    participante.estado_participacion = 'Activo'
    participante.save(update_fields=['estado_participacion'])
    return participante


@admin.register(Liga)
class LigaAdmin(admin.ModelAdmin):
    list_display = ('id_liga', 'nombre_liga', 'fk_administrador', 'monto_total_recaudado', 'estado', 'tipo_liga')
    list_filter = ('estado', 'tipo_liga')
    search_fields = ('nombre_liga',)
    readonly_fields = ('id_liga',)
    ordering = ('id_liga',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_liga', 'fk_administrador')
        }),
        ('Detalles de la Liga', {
            'fields': ('monto_total_recaudado', 'estado', 'tipo_liga')
        }),
    )


@admin.register(Invitacion)
class InvitacionAdmin(admin.ModelAdmin):
    list_display = ('id_invitacion', 'fk_id_liga', 'email_invitado', 'estado_invitacion', 'codigo_invitacion', 'fecha_invitacion')
    list_filter = ('estado_invitacion', 'fecha_invitacion')
    search_fields = ('email_invitado', 'codigo_invitacion', 'mensaje_invitacion')
    readonly_fields = ('id_invitacion', 'codigo_invitacion', 'fecha_invitacion')
    ordering = ('-fecha_invitacion',)
    
    fieldsets = (
        ('Información de la Invitación', {
            'fields': ('id_invitacion', 'codigo_invitacion', 'fk_id_liga', 'email_invitado')
        }),
        ('Participantes', {
            'fields': ('fk_id_usuario_invitado', 'fk_id_usuario_administrador')
        }),
        ('Estado y Mensaje', {
            'fields': ('estado_invitacion', 'mensaje_invitacion', 'fecha_invitacion')
        }),
    )
    
    actions = ['enviar_invitacion_email', 'aceptar_invitaciones']
    
    @admin.action(description='Enviar invitación por correo')
    def enviar_invitacion_email(self, request, queryset):
        """Acción para enviar invitaciones seleccionadas por correo"""
        enviadas = 0
        errores = 0
        
        for invitacion in queryset.filter(estado_invitacion='Pendiente'):
            if invitacion.email_invitado:
                try:
                    enviar_correo_invitacion(invitacion)
                    enviadas += 1
                except Exception as e:
                    errores += 1
                    self.message_user(
                        request,
                        f"Error al enviar a {invitacion.email_invitado}: {str(e)}",
                        messages.ERROR
                    )
        
        if enviadas > 0:
            self.message_user(
                request,
                f'{enviadas} invitación(es) enviada(s) por correo.',
                messages.SUCCESS
            )
        
        if errores > 0:
            self.message_user(
                request,
                f'{errores} invitación(es) no pudieron ser enviadas.',
                messages.WARNING
            )
        
        if enviadas == 0 and errores == 0:
            self.message_user(
                request,
                'No se encontraron invitaciones pendientes con email para enviar.',
                messages.INFO
            )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change and obj.email_invitado and obj.estado_invitacion == 'Pendiente':
            try:
                enviar_correo_invitacion(obj)
                self.message_user(
                    request,
                    f'Correo enviado a {obj.email_invitado}',
                    messages.SUCCESS
                )
            except Exception as exc:
                self.message_user(
                    request,
                    f'No se pudo enviar correo a {obj.email_invitado}: {exc}',
                    messages.ERROR
                )

    @admin.action(description='Aceptar invitaciones seleccionadas')
    def aceptar_invitaciones(self, request, queryset):
        aceptadas = sin_usuario = sin_cupo = ya_gestionadas = 0

        for invitacion in queryset:
            if invitacion.estado_invitacion != 'Pendiente':
                ya_gestionadas += 1
                continue

            usuario_id = invitacion.fk_id_usuario_invitado

            if not usuario_id and invitacion.email_invitado:
                try:
                    usuario = Usuario.objects.get(email__iexact=invitacion.email_invitado)
                    usuario_id = usuario.id_usuario
                except Usuario.DoesNotExist:
                    sin_usuario += 1
                    continue

            if not usuario_id:
                sin_usuario += 1
                continue

            try:
                liga = Liga.objects.get(id_liga=invitacion.fk_id_liga)
            except Liga.DoesNotExist:
                continue

            if not hay_cupo_disponible(liga):
                sin_cupo += 1
                continue

            agregar_participante_a_liga(liga, usuario_id)
            invitacion.estado_invitacion = 'Aceptada'
            invitacion.save(update_fields=['estado_invitacion'])
            aceptadas += 1

        if aceptadas:
            self.message_user(request, f'{aceptadas} invitación(es) aceptada(s).', messages.SUCCESS)
        if sin_usuario:
            self.message_user(request, f'{sin_usuario} invitación(es) sin usuario asociado.', messages.WARNING)
        if sin_cupo:
            self.message_user(request, f'{sin_cupo} invitación(es) sin cupo disponible.', messages.WARNING)
        if ya_gestionadas:
            self.message_user(request, f'{ya_gestionadas} ya estaban gestionadas.', messages.INFO)


@admin.register(SolicitudParticipacion)
class SolicitudParticipacionAdmin(admin.ModelAdmin):
    list_display = (
        'id_solicitud', 'liga', 'usuario', 'estado',
        'email_contacto', 'fecha_solicitud', 'fecha_respuesta'
    )
    list_filter = ('estado', 'liga')
    search_fields = ('liga__nombre_liga', 'usuario__email', 'email_contacto')
    readonly_fields = ('fecha_solicitud', 'fecha_respuesta')
    ordering = ('-fecha_solicitud',)
    actions = ['aprobar_solicitudes', 'rechazar_solicitudes']
    exclude = ('email_contacto', 'respuesta_admin', 'respondido_por')

    def _registrar_respuesta(self, solicitud: SolicitudParticipacion, estado: str, respuesta: str, user):
        solicitud.estado = estado
        solicitud.fecha_respuesta = timezone.now()
        solicitud.respondido_por = getattr(user, 'id_usuario', None) or getattr(user, 'id', None)
        if respuesta:
            solicitud.respuesta_admin = respuesta
        solicitud.save(update_fields=['estado', 'fecha_respuesta', 'respondido_por', 'respuesta_admin'])

    @admin.action(description='Aprobar solicitudes seleccionadas')
    def aprobar_solicitudes(self, request, queryset):
        aprobadas = sin_cupo = sin_usuario = ya_gestionadas = 0

        for solicitud in queryset.select_related('liga', 'usuario'):
            if solicitud.estado != 'Pendiente':
                ya_gestionadas += 1
                continue

            if not solicitud.usuario_id:
                sin_usuario += 1
                continue

            if not hay_cupo_disponible(solicitud.liga):
                sin_cupo += 1
                continue

            agregar_participante_a_liga(solicitud.liga, solicitud.usuario_id)
            self._registrar_respuesta(
                solicitud,
                'Aprobada',
                solicitud.respuesta_admin or 'Aprobada desde administrador',
                request.user
            )
            aprobadas += 1

        if aprobadas:
            self.message_user(request, f'{aprobadas} solicitud(es) aprobada(s).', messages.SUCCESS)
        if sin_cupo:
            self.message_user(request, f'{sin_cupo} sin cupo disponible.', messages.WARNING)
        if sin_usuario:
            self.message_user(request, f'{sin_usuario} sin usuario asociado.', messages.WARNING)
        if ya_gestionadas:
            self.message_user(request, f'{ya_gestionadas} ya estaban gestionadas.', messages.INFO)

    @admin.action(description='Rechazar solicitudes seleccionadas')
    def rechazar_solicitudes(self, request, queryset):
        rechazadas = ya_gestionadas = 0

        for solicitud in queryset:
            if solicitud.estado != 'Pendiente':
                ya_gestionadas += 1
                continue

            self._registrar_respuesta(
                solicitud,
                'Rechazada',
                solicitud.respuesta_admin or 'Rechazada desde administrador',
                request.user
            )
            rechazadas += 1

        if rechazadas:
            self.message_user(request, f'{rechazadas} solicitud(es) rechazada(s).', messages.SUCCESS)
        if ya_gestionadas:
            self.message_user(request, f'{ya_gestionadas} ya estaban gestionadas.', messages.INFO)
