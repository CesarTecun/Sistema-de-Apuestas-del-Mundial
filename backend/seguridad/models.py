from django.db import models
from django.utils import timezone


class VulnerabilidadInyeccion(models.Model):
    """A01 - Inyeccion: Detecta puntos de entrada para SQL/NoSQL/OS injection."""
    endpoint = models.CharField(max_length=255)
    metodo = models.CharField(max_length=10)
    parametro = models.CharField(max_length=100, blank=True)
    tipo_inyeccion = models.CharField(
        max_length=20,
        choices=[('SQL', 'SQL'), ('NoSQL', 'NoSQL'), ('OS', 'OS'), ('LDAP', 'LDAP')],
        default='SQL'
    )
    payload = models.TextField(blank=True, help_text="Payload de prueba utilizado")
    resultado = models.CharField(
        max_length=20,
        choices=[('Limpio', 'Limpio'), ('Sospechoso', 'Sospechoso'), ('Vulnerable', 'Vulnerable')],
        default='Limpio'
    )
    observacion = models.TextField(blank=True)
    fecha_escaneo = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vulnerabilidad_inyeccion'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Vulnerabilidad Inyeccion (A01)'
        verbose_name_plural = 'Vulnerabilidades Inyeccion (A01)'

    def __str__(self):
        return f"{self.endpoint} - {self.tipo_inyeccion} ({self.resultado})"


class FallaAutenticacion(models.Model):
    """A02 - Autenticacion interrumpida: Detecta fallas en login, sesiones y tokens."""
    modulo = models.CharField(max_length=100)
    problema = models.CharField(max_length=255)
    severidad = models.CharField(
        max_length=20,
        choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta'), ('Critica', 'Critica')],
        default='Baja'
    )
    recomendacion = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Mitigado', 'Mitigado'), ('En revisión', 'En revisión')],
        default='Pendiente'
    )
    fecha_deteccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'falla_autenticacion'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Falla Autenticacion (A02)'
        verbose_name_plural = 'Fallas Autenticacion (A02)'

    def __str__(self):
        return f"{self.modulo} - {self.problema}"


class ExposicionDatos(models.Model):
    """A03 - Exposicion de datos confidenciales: Datos sensibles expuestos."""
    origen = models.CharField(max_length=255)
    tipo_dato = models.CharField(max_length=50, help_text="Ej: contraseña, token, PII, tarjeta")
    exposicion = models.TextField(blank=True)
    riesgo = models.CharField(
        max_length=20,
        choices=[('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto'), ('Critico', 'Critico')],
        default='Bajo'
    )
    recomendacion = models.TextField(blank=True)
    fecha_deteccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exposicion_datos'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Exposicion Datos (A03)'
        verbose_name_plural = 'Exposiciones Datos (A03)'

    def __str__(self):
        return f"{self.origen} - {self.tipo_dato}"


class VulnerabilidadXXE(models.Model):
    """A04 - Entidades externas XML (XXE): Detecta parsers XML vulnerables."""
    endpoint = models.CharField(max_length=255)
    parser = models.CharField(max_length=50, help_text="Ej: xml.etree, lxml, DOMParser")
    permite_dtd = models.BooleanField(default=False)
    permite_entities = models.BooleanField(default=False)
    resultado = models.CharField(
        max_length=20,
        choices=[('Seguro', 'Seguro'), ('Sospechoso', 'Sospechoso'), ('Vulnerable', 'Vulnerable')],
        default='Seguro'
    )
    observacion = models.TextField(blank=True)
    fecha_escaneo = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vulnerabilidad_xxe'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Vulnerabilidad XXE (A04)'
        verbose_name_plural = 'Vulnerabilidades XXE (A04)'

    def __str__(self):
        return f"{self.endpoint} - {self.parser} ({self.resultado})"


class AuditoriaAcceso(models.Model):
    """A05 - Control de Acceso Roto: Auditoria de endpoints y permisos."""
    endpoint = models.CharField(max_length=255)
    metodo = models.CharField(max_length=10)
    requiere_auth = models.BooleanField(default=True)
    auth_configurado = models.BooleanField(default=False)
    riesgo = models.CharField(
        max_length=20,
        choices=[('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto'), ('Critico', 'Critico')],
        default='Bajo'
    )
    observacion = models.TextField(blank=True)
    fecha_escaneo = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auditoria_acceso'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Auditoria de Acceso (A05)'
        verbose_name_plural = 'Auditorias de Acceso (A05)'

    def __str__(self):
        return f"{self.endpoint} ({self.riesgo})"


class ConfiguracionSeguridad(models.Model):
    """A06 - Configuraciones Incorrectas de Seguridad."""
    nombre = models.CharField(max_length=100, unique=True)
    valor_actual = models.TextField()
    valor_recomendado = models.TextField()
    estado = models.CharField(
        max_length=20,
        choices=[('OK', 'OK'), ('Advertencia', 'Advertencia'), ('Critico', 'Critico')],
        default='OK'
    )
    descripcion = models.TextField(blank=True)
    fecha_verificacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'configuracion_seguridad'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Configuracion Seguridad (A06)'
        verbose_name_plural = 'Configuraciones Seguridad (A06)'

    def __str__(self):
        return f"{self.nombre} ({self.estado})"


class VulnerabilidadXSS(models.Model):
    """A07 - XSS: Registro de vectores y pruebas de reflexion."""
    vector = models.TextField(help_text="Payload XSS probado")
    endpoint = models.CharField(max_length=255)
    parametros = models.TextField(blank=True)
    resultado = models.CharField(
        max_length=20,
        choices=[('Limpio', 'Limpio'), ('Sospechoso', 'Sospechoso'), ('Vulnerable', 'Vulnerable')],
        default='Limpio'
    )
    detalle = models.TextField(blank=True)
    fecha_prueba = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vulnerabilidad_xss'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Vulnerabilidad XSS (A07)'
        verbose_name_plural = 'Vulnerabilidades XSS (A07)'

    def __str__(self):
        return f"{self.endpoint} - {self.resultado}"


class IntentoDeserializacion(models.Model):
    """A08 - Desserializacion Insegura: Intentos de deserializacion no segura."""
    origen = models.CharField(max_length=255)
    tipo_dato = models.CharField(max_length=50, help_text="Ej: JSON, XML, Pickle, YAML")
    contenido_muestra = models.TextField(blank=True)
    permitido = models.BooleanField(default=True)
    riesgo = models.CharField(
        max_length=20,
        choices=[('Bajo', 'Bajo'), ('Medio', 'Medio'), ('Alto', 'Alto')],
        default='Bajo'
    )
    recomendacion = models.TextField(blank=True)
    fecha_deteccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'intento_deserializacion'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Intento Deserializacion (A08)'
        verbose_name_plural = 'Intentos Deserializacion (A08)'

    def __str__(self):
        return f"{self.tipo_dato} ({self.riesgo})"


class ComponenteVulnerable(models.Model):
    """A09 - Componentes con Vulnerabilidades Conocidas."""
    nombre = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    cve_id = models.CharField(max_length=50, blank=True, null=True)
    severidad = models.CharField(
        max_length=20,
        choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta'), ('Critica', 'Critica')],
        default='Baja'
    )
    descripcion = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Mitigado', 'Mitigado'), ('Aceptado', 'Aceptado')],
        default='Pendiente'
    )
    fecha_deteccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'componente_vulnerable'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Componente Vulnerable (A09)'
        verbose_name_plural = 'Componentes Vulnerables (A09)'

    def __str__(self):
        return f"{self.nombre} {self.version} ({self.severidad})"


class PanelOWASP(models.Model):
    """Panel central de control OWASP."""
    nombre = models.CharField(max_length=50, default='Panel OWASP')
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'panel_owasp'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Panel OWASP'
        verbose_name_plural = 'Panel OWASP'

    def __str__(self):
        return self.nombre


class RegistroMonitoreo(models.Model):
    """A10 - Registro y Monitoreo Insuficientes."""
    evento = models.CharField(max_length=255)
    nivel = models.CharField(
        max_length=20,
        choices=[('INFO', 'INFO'), ('WARNING', 'WARNING'), ('ERROR', 'ERROR'), ('CRITICAL', 'CRITICAL')],
        default='INFO'
    )
    usuario = models.CharField(max_length=100, blank=True)
    ip_address = models.CharField(max_length=45, blank=True)
    detalle = models.TextField(blank=True)
    fecha_evento = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_monitoreo'
        managed = True
        app_label = 'seguridad'
        verbose_name = 'Registro Monitoreo (A10)'
        verbose_name_plural = 'Registros Monitoreo (A10)'

    def __str__(self):
        return f"{self.evento} [{self.nivel}]"
