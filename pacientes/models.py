from django.db import models

# Create your models here.


class Paciente(models.Model):
    nombre_apellido = models.CharField(max_length=90)
    fecha_ingreso = models.DateField(auto_now_add=True)
    dni = models.CharField(max_length=8)
    afecciones = models.CharField(max_length=250)
    

    def __str__(self):
        return f"{self.id}: {self.nombre_apellido}"


class Sensores(models.Model):
    paciente = models.ForeignKey(Paciente, null=True, on_delete=models.CASCADE)
    fiebre = models.CharField(max_length=2)
    pulso = models.IntegerField()
    oxigeno = models.CharField(max_length=30)
    fecha_medidas = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Fiebre: {self.fiebre}\nPRbpm: {self.pulso}\n%SpO2: {self.oxigeno}"
