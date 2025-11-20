from django.urls import path
from .views import (
    ListarMensagensView,
    EnviarMensagemView, 
    DetalheMensagemView,
)

urlpatterns = [
    # Listar todas as mensagens (com filtro opcional por usuário)
    path('chat/listar/', ListarMensagensView.as_view(), name='listar-mensagens'),
    
    # Enviar nova mensagem
    path('chat/enviar/', EnviarMensagemView.as_view(), name='enviar-mensagem'),
    
    # Visualizar detalhes de uma mensagem específica
    path('chat/mensagem/<int:id>/', DetalheMensagemView.as_view(), name='detalhe-mensagem'),
]