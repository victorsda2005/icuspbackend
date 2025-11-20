from django.urls import path
from .views import CriarIniciacaoCientificaView, ListaIniciacoesView, MinhasIniciacoesView, DetalheIniciacaoView, MessageViewSet
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
    ExcluirIniciacaoView
)

urlpatterns = [
    path('iniciacao/criar/', CriarIniciacaoCientificaView.as_view()),
    path('iniciacao/listar/', ListaIniciacoesView.as_view(), name='listar-iniciacoes'),
    path('iniciacao/minhas/', MinhasIniciacoesView.as_view(), name='minhas-iniciacoes'),
    path('iniciacao/<int:id>/', DetalheIniciacaoView.as_view(), name='detalhe-iniciacao'),
    # URLs para MessageViewSet
    path('messages/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='message-list'),
    
    path('messages/<int:pk>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='message-detail'),
    path("iniciacao/interesse/", DemonstrarInteresseView.as_view(), name="interesse-ic"),
    path("iniciacao/<int:id>/interessados/", ListaInteressadosView.as_view()),
    path("iniciacao/interesse/listar/", ListarInteressesAlunoView.as_view()),
    path("iniciacao/interesse/remover/<int:pk>/", RemoverInteresseView.as_view()),
    path("iniciacao/buscar/", BuscarIniciacoesView.as_view()),
    path("iniciacao/<int:pk>/editar/", EditarIniciacaoView.as_view()),
    path("iniciacao/<int:pk>/excluir/", ExcluirIniciacaoView.as_view()),
]
