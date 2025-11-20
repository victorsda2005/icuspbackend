from django.db import models
from django.conf import settings
# from accounts.models import CustomUser

class DirectMessage(models.Model):
    """
    Mensagem direta entre professor e aluno
    """
    remetente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensagens_enviadas'
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mensagens_recebidas'
    )
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']
        indexes = [
            models.Index(fields=['remetente', 'destinatario']),
            models.Index(fields=['criado_em']),
        ]

    def __str__(self):
        return f"{self.remetente} -> {self.destinatario}: {self.texto[:30]}"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Valida que é entre professor e aluno
        if self.remetente.role == self.destinatario.role:
            raise ValidationError("Chat só é permitido entre professor e aluno")
        
        # Garante que um seja professor e outro aluno
        roles = {self.remetente.role, self.destinatario.role}
        if not ('professor' in roles and 'aluno' in roles):
            raise ValidationError("Chat deve ser entre um professor e um aluno")