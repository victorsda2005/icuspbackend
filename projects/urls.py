from django.urls import path
from .views import CriarIniciacaoCientificaView, ListaIniciacoesView, MinhasIniciacoesView, DetalheIniciacaoView
from .views import (
    CriarIniciacaoCientificaView, 
    ListaIniciacoesView, 
    MinhasIniciacoesView, 
    DetalheIniciacaoView, 
    DemonstrarInteresseView,
    ListaInteressadosView,
    ListarInteressesAlunoView,
    RemoverInteresseView,
    BuscarIniciacoesView,
    EditarIniciacaoView,
    ExcluirIniciacaoView,
    ICListarMensagensView,
    ICEnviarMensagemView,
    ICDetalheMensagemView,
)

urlpatterns = [
    #criação de ics
    path('iniciacao/criar/', CriarIniciacaoCientificaView.as_view()),
    path('iniciacao/listar/', ListaIniciacoesView.as_view(), name='listar-iniciacoes'),
    path('iniciacao/minhas/', MinhasIniciacoesView.as_view(), name='minhas-iniciacoes'),
    path('iniciacao/<int:id>/', DetalheIniciacaoView.as_view(), name='detalhe-iniciacao'),
    # URLs para Messagens
    path('mensagem/listar/', ICListarMensagensView.as_view(), name='listar-mensagens'),
    path('mensagem/criar/', ICEnviarMensagemView.as_view(), name='enviar-mensagens'),
    path('mensagem/ler/<int:pk>/', ICDetalheMensagemView.as_view(), name='ler-mensagens'),
    #declarar interesse
    path("iniciacao/interesse/", DemonstrarInteresseView.as_view(), name="interesse-ic"),
    path("iniciacao/<int:id>/interessados/", ListaInteressadosView.as_view()),
    path("iniciacao/interesse/listar/", ListarInteressesAlunoView.as_view()),
    path("iniciacao/interesse/remover/<int:pk>/", RemoverInteresseView.as_view()),
    #busca de ics
    path("iniciacao/buscar/", BuscarIniciacoesView.as_view()),
    path("iniciacao/<int:pk>/editar/", EditarIniciacaoView.as_view()),
    path("iniciacao/<int:pk>/excluir/", ExcluirIniciacaoView.as_view()),
]
