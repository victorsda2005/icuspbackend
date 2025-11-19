from django.urls import path
from .views import CriarIniciacaoCientificaView, ListaIniciacoesView, MinhasIniciacoesView, DetalheIniciacaoView

urlpatterns = [
    path('iniciacao/criar/', CriarIniciacaoCientificaView.as_view()),
    path('iniciacao/listar/', ListaIniciacoesView.as_view(), name='listar-iniciacoes'),
    path('iniciacao/minhas/', MinhasIniciacoesView.as_view(), name='minhas-iniciacoes'),
    path('iniciacao/<int:id>/', DetalheIniciacaoView.as_view(), name='detalhe-iniciacao'),
]