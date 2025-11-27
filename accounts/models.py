from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÖØ-öø-ÿ ]+$',
        message="O nome de usuário deve conter apenas letras, acentos e espaços."
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": "Já existe um usuário com este nome.",
        },
    )

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
    biografia = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


