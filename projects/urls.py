from django.urls import path
from .views import CriarIniciacaoCientificaView, ListaIniciacoesView, MinhasIniciacoesView, DetalheIniciacaoView, MessageViewSet

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
]
