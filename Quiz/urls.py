from django.urls import path

from .views import (
				inicio,
				AdminRegistro, 
				ListaExamen, 
				CrearExamen,
				ActualizarExamen,
				ExamenResultado

		)

urlpatterns = [
	
	path('', inicio, name='inicio'),
	path('registro_admin', AdminRegistro.as_view(), name='AdminRegistro'),
	path('lista_examen', ListaExamen.as_view(), name='ListaExamen'),
	path('crear_examen', CrearExamen.as_view(), name='CrearExamen'),

	path('actualizar_examen/<int:pk>', ActualizarExamen.as_view(), name='ActualizarExamen')

	path('examen/<int:pk>/resultado', ExamenResultado.as_view(), name='ExamenResultado')


]