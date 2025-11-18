from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # Campos do aluno
    matricula = models.CharField(max_length=50, null=True, blank=True)
    curso = models.CharField(max_length=100, null=True, blank=True)

    # Campos do professor
    departamento = models.CharField(max_length=100, null=True, blank=True)
    areas_pesquisa = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


