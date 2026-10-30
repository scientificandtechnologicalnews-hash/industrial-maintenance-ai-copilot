from django.contrib import admin

from .models import Averia, CasoResuelto, DocumentoRAG, Maquina


@admin.register(Maquina)
class MaquinaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "categoria", "ubicacion", "activa")
    list_filter = ("categoria", "activa")
    search_fields = ("codigo", "nombre", "marca", "modelo")


@admin.register(DocumentoRAG)
class DocumentoRAGAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "maquina", "fecha_actualizacion")
    list_filter = ("tipo", "maquina")
    search_fields = ("titulo", "contenido")


class CasoResueltoInline(admin.StackedInline):
    """Permite ver/editar el caso resuelto DESDE la propia avería en el admin."""
    model = CasoResuelto
    extra = 0


@admin.register(Averia)
class AveriaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "maquina", "tecnico", "prioridad", "estado", "fecha_apertura")
    list_filter = ("estado", "prioridad")
    search_fields = ("titulo", "descripcion_sintoma")
    inlines = [CasoResueltoInline]


@admin.register(CasoResuelto)
class CasoResueltoAdmin(admin.ModelAdmin):
    list_display = ("averia", "tecnico_valida", "fecha_validacion")
    search_fields = ("causa_raiz", "procedimiento_solucion")



# Register your models here.
