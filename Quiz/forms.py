from django import forms
from .models import (Usuario, Examen, Categoria, Pregunta, Respuesta, 
					ExamenUsuario, ExamenTomado, RespuestaUsuario)


from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ValidationError


class AdminRegistro(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = Usuario

	def save(self, commit=True):
		usuario = super().save(commit=False)
		usuario.admin = True
		if commit:
			usuario.save()
		return usuario


class PersonalRegistro(UserCreationForm):

	dependencias = forms.ModelMultipleChoiceField(

		queryset = Categoria.objects.all(),
		widget = forms.CheckboxSelectMultiple,
		required=True
	)

	class Meta(UserCreationForm.Meta):
		model = Usuario


	def save(self):
		usuario = super().save(commit=False)
		usuario.personal = True
		usuario.save()

		examenUsuario = ExamenUsuario.objects.create(usuario=usuario)
		examenUsuario.categorias.add(*self.cleaned_data.get('dependencias'))
		return usuario

