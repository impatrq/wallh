from django.shortcuts import render
from .models import Paciente, Sensores

# Create your views here.


def index(request):
    return render(request, "pacientes/index.html", {
        "pacientes": Paciente.objects.all(),
        "sensores": Sensores.objects.all()
    })
