from django.conf import settings
from django.db import models


class Maquina(models.Model):
    """Equipo físico de la planta: PLC, motor, robot, sensor..."""

    class Categoria(models.TextChoices):
        ACCIONAMIENTO = "ACC", "Accionamientos (motores, variadores)"
        CONTROL = "CTL", "Control (PLC)"
        SENSORIZACION = "SEN", "Sensorización y lectura"
        TRANSPORTE = "TRA", "Transporte y clasificación"
        ROBOTICA = "ROB", "Robótica y almacenes automáticos"
        NEUMATICA = "NEU", "Neumática y servicios"
        OTROS = "OTR", "Otros"

    nombre = models.CharField(max_length=120)
    marca = models.CharField(max_length=80, blank=True)
    modelo = models.CharField(max_length=80, blank=True)
    codigo = models.CharField(max_length=30, unique=True)
    categoria = models.CharField(max_length=3, choices=Categoria.choices, default=Categoria.OTROS)
    ubicacion = models.CharField(max_length=120, blank=True)
    manual_url = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["codigo"]
        verbose_name = "máquina"
        verbose_name_plural = "máquinas"

    def __str__(self):
        return f"{self.nombre} [{self.codigo}]"




class DocumentoRAG(models.Model):
    """Conocimiento técnico: manuales, esquemas o fallos conocidos."""

    class Tipo(models.TextChoices):
        FALLO = "FP", "Fallo y solución"
        MANUAL = "MT", "Manual técnico"
        ESQUEMA = "EE", "Esquema eléctrico"

    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=2, choices=Tipo.choices)
    # null=True además de blank=True: un documento puede no pertenecer a
    # ninguna máquina concreta (p. ej. una norma de seguridad general).
    maquina = models.ForeignKey(
        Maquina, on_delete=models.CASCADE, related_name="documentos",
        null=True, blank=True,
    )
    contenido = models.TextField(help_text="Texto del documento, usado para la búsqueda.")
    # Opcional a propósito: un caso resuelto puede generar un documento de
    # texto sin archivo físico adjunto (lección aprendida del proyecto anterior).
    archivo = models.FileField(upload_to="documentos/", blank=True)
    fuente_url = models.URLField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["maquina", "titulo"]
        verbose_name = "documento"
        verbose_name_plural = "documentos"

    def __str__(self):
        return self.titulo


class Averia(models.Model):
    """Avería registrada por un técnico sobre una máquina."""

    class Estado(models.TextChoices):
        ABIERTA = "AB", "Abierta"
        EN_CURSO = "EC", "En curso"
        RESUELTA = "RE", "Resuelta"

    class Prioridad(models.TextChoices):
        BAJA = "B", "Baja"
        MEDIA = "M", "Media"
        ALTA = "A", "Alta"

    # PROTECT: no se puede borrar una máquina con averías registradas;
    # el historial de averías no debe desaparecer nunca.
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT, related_name="averias")
    # El técnico SIEMPRE lo asigna el servidor (request.user), nunca el
    # formulario. Lección de seguridad del proyecto anterior.
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="averias",
    )
    titulo = models.CharField(max_length=200)
    descripcion_sintoma = models.TextField()
    acciones_realizadas = models.TextField(blank=True)
    notas_adicionales = models.TextField(blank=True)
    prioridad = models.CharField(max_length=1, choices=Prioridad.choices, default=Prioridad.MEDIA)
    estado = models.CharField(max_length=2, choices=Estado.choices, default=Estado.ABIERTA)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_apertura"]
        verbose_name = "avería"
        verbose_name_plural = "averías"

    def __str__(self):
        return f"{self.titulo} ({self.maquina.codigo})"


class CasoResuelto(models.Model):
    """Conocimiento verificado: la causa raíz y la solución confirmadas de una avería."""

    # OneToOneField: relación 1 a 1. Una avería genera como mucho un caso
    # resuelto, y un caso resuelto pertenece exactamente a una avería.
    averia = models.OneToOneField(Averia, on_delete=models.CASCADE, related_name="caso_resuelto")
    causa_raiz = models.TextField()
    procedimiento_solucion = models.TextField()
    tiempo_reparacion_horas = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Horas que tardó la reparación, si se conoce.",
    )
    lecciones_aprendidas = models.TextField(blank=True)
    tecnico_valida = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="casos_validados",
    )
    fecha_validacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_validacion"]
        verbose_name = "caso resuelto"
        verbose_name_plural = "casos resueltos"

    def __str__(self):
        return f"Caso resuelto: {self.averia.titulo}"


# Create your models here.
