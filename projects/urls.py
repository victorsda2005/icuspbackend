from django.urls import path
from .views import (
    CriarIniciacaoCientificaView, 
    ListaIniciacoesView, 
    MinhasIniciacoesView, 
    DetalheIniciacaoView, 
    DemonstrarInteresseView,
    ListaInteressadosView,
    ListarInteressesAlunoView,
    RemoverInteresseView
)

urlpatterns = [
    path('iniciacao/criar/', CriarIniciacaoCientificaView.as_view()),
    path('iniciacao/listar/', ListaIniciacoesView.as_view(), name='listar-iniciacoes'),
    path('iniciacao/minhas/', MinhasIniciacoesView.as_view(), name='minhas-iniciacoes'),
    path('iniciacao/<int:id>/', DetalheIniciacaoView.as_view(), name='detalhe-iniciacao'),
    path("iniciacao/interesse/", DemonstrarInteresseView.as_view(), name="interesse-ic"),
    path("iniciacao/<int:id>/interessados/", ListaInteressadosView.as_view()),
    path("iniciacao/interesse/listar/", ListarInteressesAlunoView.as_view()),
    path("iniciacao/interesse/remover/<int:pk>/", RemoverInteresseView.as_view()),
]