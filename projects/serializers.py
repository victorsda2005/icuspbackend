from rest_framework import serializers
<<<<<<< HEAD
from .models import IniciacaoCientifica, Message
=======
from .models import IniciacaoCientifica
from .models import InteresseIC
from accounts.models import CustomUser
>>>>>>> 57be28e8da60aea77a54af8af214cabc588cfaea

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



# Serializer para mensagens do post / chat simples
class MessageSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("autor", "criado_em", "atualizado_em")

    def validate(self, data):
        texto = data.get('texto')
        if not texto or not texto.strip():
            raise serializers.ValidationError({"texto": "O texto da mensagem não pode ficar vazio."})
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["autor"] = request.user
        return super().create(validated_data)
    
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
