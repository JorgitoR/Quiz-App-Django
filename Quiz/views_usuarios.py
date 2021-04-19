from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generics import CreateView, ListView, UpdateView
from django.utils.decorators import method_decoratos

from .models import (Usuario, Examen, Categoria, Pregunta, Respuesta, 
					ExamenUsuario, ExamenTomado, RespuestaUsuario)


from .forms import PersonalRegistro, CategoriaForms

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
		return redirect('')


class ActualizarInteres(UpdateView):
	model = ExamenUsuario
	form_class = CategoriaForms
	template_name = 'tablero/personal/categoria_form.html'

	def get_object(self):
		return self.request.user.examenusuario

	def form_valid(self, form):
		messages.success(self.request, 'Categoria actualizado correctamente')
		return super().form_valid(form)
		