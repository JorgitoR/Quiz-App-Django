from django.db import models

from django.contrib.auth.models import AbstractUser

from django.utils.html import escape, mark_safe


class Usuario(AbstractUser):
	admin =  models.BooleanField(default=False)
	personal = models.BooleanField(default=False)


class Categoria(models.Model):
	nombre = models.CharField(max_length=100)
	color = models.CharField(max_length=7, default='#007bff')


	def __str__(self):
		return self.nombre

class Examen(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='examen')
	nombre = models.TextField(verbose_name='Nombre del Examen')
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='examen')

	def __str__(self):
		return self.nombre


class Pregunta(models.Model):
	RESPUESTA_CORRECTA = 1

	examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='preguntas')
	texto = models.TextField(verbose_name='Texto de la pregunta')


	def __str__(self):
		return self.texto


class Respuesta(models.Model):
	MAX_RESPUESTA_COUNT = 4
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuesta')
	texto = models.CharField(max_length=250, verbose_name='Respesta')
	correcta = models.BooleanField(verbose_name='Respuesta correcta', default=False, null=False)

	def __str__(self):
		return self.texto

class ExamenUsuario(models.Model):
	usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
	examenes = models.ManyToManyField(Examen, through='ExamenTomado')
	categorias = models.ManyToManyField(Categoria, related_name='categorias')

	def get_preguntas_sin_respuestas(self, examen):
		preguntas_respondidas = self.examen_tomado \
			.filter(respuesta__pregunta__examen=examen) \
			.values_list('respuesta__pregunta__pk', flat=True)



class ExamenTomado(models.Model):
	quizUser = models.ForeignKey(ExamenUsuario, on_delete=models.CASCADE, related_name='examen_tomado')
	examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='examen_tomado')
	puntaje = models.FloatField()
	fecha  = models.DateTimeField(auto_now_add=True)	

class RespuestaUsuario(models.Model):
	quizUser = models.ForeignKey(ExamenUsuario, on_delete=models.CASCADE, related_name='respuesa_examen')
	respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
