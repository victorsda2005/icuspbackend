# chat/serializers.py
from rest_framework import serializers
from .models import DirectMessage

class DirectMessageSerializer(serializers.ModelSerializer):
    remetente_username = serializers.CharField(source='remetente.username', read_only=True)
    destinatario_username = serializers.CharField(source='destinatario.username', read_only=True)
    remetente_role = serializers.CharField(source='remetente.role', read_only=True)
    destinatario_role = serializers.CharField(source='destinatario.role', read_only=True)

    class Meta:
        model = DirectMessage
        fields = [
            'id',
            'remetente', 
            'remetente_username',
            'remetente_role',
            'destinatario', 
            'destinatario_username', 
            'destinatario_role',
            'texto', 
            'criado_em'
        ]
        read_only_fields = ['id', 'remetente', 'criado_em']

    def validate(self, data):
        """
        Validação para a API REST
        """
        request = self.context.get('request')
        destinatario = data.get('destinatario')
        
        if request and request.method == 'POST':
            # Garante que o remetente é o usuário logado
            if request.user != data.get('remetente', request.user):
                raise serializers.ValidationError({
                    "remetente": "Você só pode enviar mensagens como você mesmo."
                })
            
            # Valida que destinatário existe
            if not destinatario:
                raise serializers.ValidationError({
                    "destinatario": "Destinatário é obrigatório."
                })
            
            # Valida que não é mensagem para si mesmo
            if request.user == destinatario:
                raise serializers.ValidationError({
                    "destinatario": "Você não pode enviar mensagens para si mesmo."
                })
            
            # Valida que é entre professor e aluno
            if request.user.role == destinatario.role:
                raise serializers.ValidationError({
                    "destinatario": "Chat só é permitido entre professor e aluno."
                })
            
            # Garante que um é professor e outro é aluno
            roles = {request.user.role, destinatario.role}
            if not ('professor' in roles and 'aluno' in roles):
                raise serializers.ValidationError({
                    "destinatario": "Chat deve ser entre um professor e um aluno."
                })

        return data

    def create(self, validated_data):
        """
        Sobrescreve o create para garantir que o remetente é o usuário logado
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['remetente'] = request.user
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Customiza a representação dos dados na resposta
        """
        representation = super().to_representation(instance)
        
        # Formata a data para algo mais legível
        representation['criado_em'] = instance.criado_em.strftime('%d/%m/%Y %H:%M')
        
        return representation