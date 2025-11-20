from rest_framework import serializers
from .models import IniciacaoCientifica
from .models import InteresseIC
from accounts.models import CustomUser

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
    
class InteresseICSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteresseIC
        fields = ["id", "aluno", "iniciacao", "criado_em"]
        read_only_fields = ["aluno", "criado_em"]

class AlunoInteressadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "matricula", "curso"]

class IniciacaoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IniciacaoCientifica
        fields = ["id", "titulo", "area_pesquisa", "professor", "criado_em"]