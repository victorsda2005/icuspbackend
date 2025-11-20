# chat/views.py
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import DirectMessage
from .serializers import DirectMessageSerializer

class ListarMensagensView(generics.ListAPIView):
    """
    Lista todas as mensagens do usuário logado (tanto enviadas quanto recebidas)
    Pode filtrar por conversa com um usuário específico usando query parameter
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.request.query_params.get('usuario')
        
        # Base query: mensagens onde o usuário é remetente OU destinatário
        queryset = DirectMessage.objects.filter(
            Q(remetente=user) | Q(destinatario=user)
        ).select_related('remetente', 'destinatario')
        
        # Filtra por conversa com usuário específico
        if other_user_id:
            queryset = queryset.filter(
                Q(remetente=user, destinatario_id=other_user_id) |
                Q(remetente_id=other_user_id, destinatario=user)
            )
        
        return queryset.order_by('criado_em')

class EnviarMensagemView(generics.CreateAPIView):
    """
    Envia uma nova mensagem
    O remetente é automaticamente definido como o usuário logado
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Garante que a validação do serializer seja executada
        serializer.save()

class DetalheMensagemView(generics.RetrieveAPIView):
    """
    Visualiza os detalhes de uma mensagem específica
    Apenas se o usuário logado for remetente ou destinatário
    """
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            Q(remetente=user) | Q(destinatario=user)
        ).select_related('remetente', 'destinatario')

#quase ctz q houje chapação de IA nesse trecho
# class ListarConversasView(generics.ListAPIView):
#     """
#     Lista todas as conversas do usuário (última mensagem de cada conversa)
#     """
#     serializer_class = DirectMessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
        
#         # Pega os IDs de todos os usuários com quem o usuário atual conversou
#         from django.db.models import Max, OuterRef, Subquery
        
#         # Subquery para pegar a última mensagem de cada conversa
#         ultimas_mensagens = DirectMessage.objects.filter(
#             Q(remetente=user) | Q(destinatario=user)
#         ).values('remetente', 'destinatario').annotate(
#             ultima_msg_id=Max('id')
#         ).values('ultima_msg_id')
        
#         # Retorna as últimas mensagens de cada conversa
#         return DirectMessage.objects.filter(
#             id__in=Subquery(ultimas_mensagens)
#         ).select_related('remetente', 'destinatario').order_by('-criado_em')