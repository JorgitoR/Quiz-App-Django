from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count


from django.views.generics import CreateView, ListView, UpdateView
from django.utils.decorators import method_decoratos

from .models import (Usuario, Examen, Categoria, Pregunta, Respuesta, 
					ExamenUsuario, ExamenTomado, RespuestaUsuario)


from .forms import PersonalRegistro, CategoriaForms
