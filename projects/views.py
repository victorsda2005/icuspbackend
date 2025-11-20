from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .serializers import IniciacaoCientificaSerializer, MessageSerializer
from .models import IniciacaoCientifica, Message
from .permissions import IsProfessor, IsOwnerOrReadOnly
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

class CriarIniciacaoCientificaView(generics.CreateAPIView):
    queryset = IniciacaoCientifica.objects.all()
    serializer_class = IniciacaoCientificaSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)

class ListaIniciacoesView(ListAPIView):
    queryset = IniciacaoCientifica.objects.all()
    serializer_class = IniciacaoCientificaSerializer
    permission_classes = [AllowAny]

class MinhasIniciacoesView(ListAPIView):
    serializer_class = IniciacaoCientificaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IniciacaoCientifica.objects.filter(professor=self.request.user)
    
class DetalheIniciacaoView(RetrieveAPIView):
    queryset = IniciacaoCientifica.objects.all()
    serializer_class = IniciacaoCientificaSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

class MessageViewSet(viewsets.ModelViewSet):
    """
    Endpoints para CRUD de Message.
    - GET /messages/?post=<id>  -> lista mensagens do post
    - POST /messages/           -> cria mensagem (request.user será autor)
    """
    queryset = Message.objects.select_related("autor").all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        post_id = self.request.query_params.get("post") or self.kwargs.get("post_pk")
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)