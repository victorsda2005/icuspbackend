from django.db import models
from accounts.models import CustomUser

class IniciacaoCientifica(models.Model):
    professor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "professor"},
        related_name="iniciacoes"
    )

    titulo = models.CharField(max_length=200)
    area_pesquisa = models.CharField(max_length=200)
    duracao = models.CharField(max_length=100)
    numero_vagas = models.IntegerField()
    descricao = models.TextField()

    bolsa_disponivel = models.BooleanField(default=False)
    tipo_bolsa = models.CharField(max_length=100, blank=True, null=True)  # <-- novo campo

    tags = models.CharField(max_length=300)

    objetivos = models.TextField(blank=True, null=True)
    requisitos = models.TextField(blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo