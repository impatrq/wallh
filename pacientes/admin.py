from django.contrib import admin
from .models import Paciente, Sensores
# Register your models here.
admin.site.register(Sensores)
admin.site.register(Paciente)
