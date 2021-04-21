from django.urls import path

from .views import (
				inicio,
				AdminRegistro, 
				ListaExamen, 
				CrearExamen,
				ActualizarExamen,
				ExamenResultado,

				add_preguntas,
				add_respuestas

		)


from .views_usuarios import (

			PersonalRegistro,
			ActualizarInteres,
			ListaExamenes,
			ExamenTomado,
			jugar

		)


urlpatterns = [
	
	path('', inicio, name='inicio'),
	path('registro_admin', AdminRegistro.as_view(), name='AdminRegistro'),
	path('lista_examen', ListaExamen.as_view(), name='ListaExamen'),
	path('crear_examen', CrearExamen.as_view(), name='CrearExamen'),

	path('actualizar_examen/<int:pk>', ActualizarExamen.as_view(), name='ActualizarExamen'),

	path('examen/<int:pk>/resultado', ExamenResultado.as_view(), name='ExamenResultado'),


	path('examen/<int:pk>/add_preguntas', add_preguntas, name='add_preguntas'),
	path('examen/<int:examen_id>/pregunta/<int:pregunta_id>/', add_respuestas, name='add_respuestas'),



	#########ESTUIANTE############

	path('registro_estudiante', PersonalRegistro.as_view(), name='PersonalRegistro'),
	path('ActualizarInteres', ActualizarInteres.as_view(), name='ActualizarInteres'),
	path('ListaExamenes', ListaExamenes.as_view(), name='ListaExamenes'),
	path('ExamenTomado', ExamenTomado.as_view(), name='ExamenTomado'),
	path('jugar/examen/<int:quiz_id>/', jugar, name='jugar'),



]