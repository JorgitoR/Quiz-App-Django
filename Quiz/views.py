from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import (CreateView, ListView, 
							DeleteView, DetailView, UpdateView)

from .forms import AdminRegistro, PersonalRegistro
from django.forms import inlineformset_factory
from .models import (Usuario, Examen, Categoria, Pregunta, Respuesta, 
					ExamenUsuario, ExamenTomado, RespuestaUsuario)


from django.contrib import messages
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.db.models import Avg, Count


def inicio(request):
	if request.user.is_authenticated:
		if request.user.admin:
			return redirect('ListaExamen')
		else:
			return redirect('')

	return render(request, 'inicio.html')

class AdminRegistro(CreateView):
	model = Usuario
	form_class = AdminRegistro
	template_name = "registro/admin_registro.html"

	def get_context_data(self, **kwargs):
		kwargs['tipo_usuario'] = 'Admin'
		return super().get_context_data(**kwargs)


	def form_valid(self, form):
		usuario = form.save()
		login(self.request, usuario)
		return redirect('ListaExamen')


class ListaExamen(ListView):
	model = Examen
	ordering = ('nombre', )
	context_object_name = 'examenes'
	template_name = 'tablero/admin/lista_examen.html'

	def get_queryset(self):
		queryset = self.request.user.examen \
			.select_related('categoria') \
			.annotate(preguntas_count=Count('preguntas', distinct=True)) \
			.annotate(tomados_count=Count('examen_tomado', distinct=True))
		return queryset

@method_decorator([login_required], name='dispatch')
class CrearExamen(CreateView):
	model = Examen
	fields = ('nombre', 'categoria',)
	template_name = 'tablero/admin/crear_examen.html'

	def form_valid(self, form):
		examen = form.save(commit=False)
		examen.usuario = self.request.user
		examen.save()
		messages.success(self.request, 'El examen fue creado exitosamente! Sigue adelante, agrega las preguntas')
		return redirect('ActualizarExamen', examen.pk)


@method_decorator([login_required], name='dispatch')
class ActualizarExamen(UpdateView):
	model = Examen
	fields = ('nombre', 'categoria', )
	context_object_name='examen'
	template_name = 'tablero/admin/actualizar_examen.html'

	def get_context_data(self, **kwargs):
		print(self.get_object())
		kwargs['preguntas'] = self.get_object().preguntas.annotate(respuesta_count=Count('respuesta'))
		return super().get_context_data(**kwargs)


	def get_queryset(self):
		'''
		Este metodo es un gestion de permiso a nivel de objeto  implicito 
		Esta View solo  emparejara los ids de los examenes existentes 
		pertenecientes al usuaio loggeado

		'''

		return self.request.user.examen.all()

	def get_success_url(self):
		return reverse('ActualizarExamen', kwargs={'pk': self.object.pk})


@method_decorator([login_required], name='dispatch')
class ExamenEliminar(DeleteView):
	model = Examen
	context_object_name = 'examen'
	template_name = 'tablero/admin/eliminar_examen.html'
	success_url = reverse_lazy('ListaExamen')

	def delete(self, request, *args, **kwargs):
		examen = self.get_object()
		print(examen)
		messages.success(request, 'El examen %s fue eliminado con exito!' %examen.nombre)
		return super().delete(request, *args, **kwargs)

	def get_queryset(self):
		return self.request.user.examen.all()



@method_decorator([login_required], name='dispatch')
class ExamenResultado(DeleteView):
	model = Examen
	context_object_name = 'examen'
	template_name = 'tablero/admin/examen_resultado.html'

	def get_context_data(self, **kwargs):
		examen = self.get_object()
		examenes_tomados = examen.examen_tomado.select_related('quizuser__usuario').order_by('nombre')
		total_examenes_tomados = examen_tomado.count()
		examen_puntaje = examen.examen_tomado.aggregate(average_score=Avg('puntaje'))

		dicionario_extra = {

			'examenes_tomados': examenes_tomados,
			'total_examenes_tomados':total_examenes_tomados,
			'examen_puntaje':examen_puntaje

		}

		kwargs.update(dicionario_extra)
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		return self.request.user.examen.all()


@login_required
def add_preguntas(request, pk):

	quiz = get_object_or_404(Examen, pk=pk)

	if request.method == 'POST':
		form = AddPreguntaForm(request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.examen= quiz
			instance.save()
			messages.success(request, 'Ahora debes agregar las opciones de respuestas a la pregunta')
			return redirect('addRespuestas', quiz.pk, instance.pk)

	else:
		form = AddPreguntaForm()

	context = {
		'form':form,
		'quiz':quiz
	}

	return render(request, '', context)



def add_respuestas(request, examen_id, pregunta_id):

	quiz = get_object_or_404(Examen, pk=examen_id)
	pregunta = get_object_or_404(Pregunta, pk=pregunta_id, examen=quiz)

	RespuestaFormSet = inlineformset_factory(

		Pregunta,
		

	)