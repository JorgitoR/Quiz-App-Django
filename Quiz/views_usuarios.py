from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.db.models import Count


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import CreateView, ListView, UpdateView

from .models import (Usuario, Examen, Categoria, Pregunta, Respuesta, 
					ExamenUsuario, ExamenTomado, RespuestaUsuario)


from .forms import PersonalRegistro, CategoriaForms, TomarQuizForm

class PersonalRegistro(CreateView):
	model = Usuario
	form_class = PersonalRegistro
	template_name= 'registro/formulario.html'

	def get_context_data(self, **kwargs):
		kwargs['tipo_usuario'] = "Persona"
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		usuario = form.save()
		login(self.request, usuario)
		return redirect('ListaExamenes')


class ActualizarInteres(UpdateView):
	model = ExamenUsuario
	form_class = CategoriaForms
	template_name = 'tablero/personal/categoria_form.html'

	def get_object(self):
		return self.request.user.examenusuario

	def form_valid(self, form):
		messages.success(self.request, 'Categoria actualizado correctamente')
		return super().form_valid(form)


class ListaExamenes(ListView):
	model = Examen
	ordering = ('nombre',)
	context_object_name = 'examenes'
	template_name = 'tablero/personal/lista_quiz.html'

	def get_queryset(self):
		estudiante = self.request.user.examenusuario
		categoria = estudiante.categorias.values_list('pk', flat=True)
		examen_tomado = estudiante.examenes.values_list('pk', flat=True)
		queryset = Examen.objects.filter(categoria__in=categoria) \
				.exclude(pk__in=examen_tomado) \
				.annotate(preguntas__count=Count('preguntas')) \
				.filter(preguntas__count__gt=0)
		return queryset


class ExamenTomado(ListView):
	model = ExamenTomado
	context_object_name = 'examen_tomado'
	template_name = 'tablero/personal/lista_examen_tomado.html'


	def get_queryset(self):
		queryset = self.request.user.examenusuario.examen_tomado \
			.select_related('examen', 'examen__categoria') \
			.order_by('examen__nombre')
		return queryset



def  jugar(request, quiz):
	quiz = get_object_or_404(Examen, pk=quiz)
	estudiante = request.user.examenusuario

	if estudiante.examenes.filter(pk=quiz).exists():
		return render(request, 'tablero/personal/jugar.html')


	total_preguntas = estudiante.examenes.preguntas.count()
	preguntas_sin_responder = estudiante.get_preguntas_sin_respuestas(quiz)
	total_preguntas_sin_responder = preguntas_sin_responder.count()
	barra_de_progreso = 100 - round(((total_preguntas_sin_responder - 1) / total_preguntas)*100)

	pregunta = preguntas_sin_responder.first()

	if request.method == 'POST':
		form = TomarQuizForm(pregunta=pregunta, data=request.POST)
		if form.is_valid():
			with transaction.atomic():
				instance = form.save(commit=False)
				instance.quizuser = estudiante
				instance.save()

				if estudiante.get_preguntas_sin_respuestas(quiz):
					return redirect('jugar', pk)
				else:
					respuesta_correcta = estudiante.respuesa_examen.filter(respuesta__pregunta__examen=quiz, respuesta__correcta=True).count()
					puntaje = round((respuesta__correcta / total_preguntas) * 100)
					ExamenTomado.objects.create(quizuser=estudiante, examen=quiz, puntaje=puntaje)
					if puntaje < 50.0:
						messages.warning(request, 'Mejor suerte la proxima vez! Tu puntaje para el Quiz %s  fue %s' %(quiz.nombre, puntaje))
					else:
						messages.success(request, 'Felicitaciones! Tu puntaje para el Quiz %s  fue %s' %(quiz.nombre, puntaje))

					return redirect('ListaExamenes')

	else:
		form = TomarQuizForm(pregunta=pregunta)

	context = {

	}

	return render(request, 'tablero/personal/jugar.html', context)



