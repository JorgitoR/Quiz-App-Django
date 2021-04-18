from django import forms
from .models import (Usuario, Examen, Categoria, Pregunta, Respuesta, 
					ExamenUsuario, ExamenTomado, RespuestaUsuario)


from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ValidationError



class AddPreguntaForm(forms.ModelForm):
	class Meta:
		model = Pregunta
		fields = [
			'texto'
		]

class CategoriaForms(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = [
			"nombre",
		]
		widget = {
			'nombre':forms.CheckboxSelectMultiple
		}

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



class BaseRespuestasInlinesFormSet(forms.BaseInlineFormSet):
	def clean(self):
		super().clean()

		respuestas_correcta_respondida = False
		for form in self.forms:
			if not form.cleaned_data.get('DELETE', False):
				if form.cleaned_data.get('correcta', False):
					respuestas_correcta_respondida = True
					break

		if not respuestas_correcta_respondida:
			raise ValidationError('Marca al menos una respuesta Correcta', code='sin_respuesta')
