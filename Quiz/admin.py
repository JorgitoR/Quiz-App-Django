from django.contrib import admin

from .models import Categoria,  Examen, Pregunta
from .models import Respuesta, ExamenUsuario, ExamenTomado, RespuestaUsuario


class RespuestaInline(admin.TabularInline):
	model = Respuesta
	can_delete=False
	max_num = Respuesta.MAX_RESPUESTA_COUNT
	min_num = Respuesta.MAX_RESPUESTA_COUNT


class PreguntaAdmin(admin.ModelAdmin):
	model = Pregunta
	inlines = (RespuestaInline, )
	list_display = ['texto']
	search_fields = ['texto']



admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ExamenUsuario)
admin.site.register(ExamenTomado)
admin.site.register(Examen)
admin.site.register(Categoria)