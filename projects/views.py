from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import IniciacaoCientificaSerializer
from .models import IniciacaoCientifica
from .permissions import IsProfessor
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