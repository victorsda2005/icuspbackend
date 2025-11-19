from rest_framework import serializers
from .models import IniciacaoCientifica

class IniciacaoCientificaSerializer(serializers.ModelSerializer):
    class Meta:
        model = IniciacaoCientifica
        fields = "__all__"
        read_only_fields = ("professor", "criado_em")

    def validate(self, data):
        # Se bolsa_disponivel é True → tipo_bolsa é obrigatório
        if data.get("bolsa_disponivel") and not data.get("tipo_bolsa"):
            raise serializers.ValidationError({
                "tipo_bolsa": "O campo 'tipo_bolsa' é obrigatório quando 'bolsa_disponivel' é verdadeiro."
            })

        # Se bolsa_disponivel é False → tipo_bolsa deve ser nulo
        if not data.get("bolsa_disponivel"):
            data["tipo_bolsa"] = None

        return data