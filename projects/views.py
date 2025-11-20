from rest_framework import generics, viewsets,permissions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .serializers import IniciacaoCientificaSerializer, MessageSerializer
from .models import IniciacaoCientifica, Message
from .permissions import IsProfessor, IsOwnerOrReadOnly
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import InteresseIC, IniciacaoCientifica
from .serializers import InteresseICSerializer, AlunoInteressadoSerializer, IniciacaoListSerializer, IniciacaoUpdateSerializer
from accounts.models import CustomUser

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


class DemonstrarInteresseView(generics.CreateAPIView):
    serializer_class = InteresseICSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        # Apenas alunos podem demonstrar interesse
        if user.role != "aluno":
            raise PermissionDenied("Somente alunos podem demonstrar interesse.")

        iniciacao_id = self.request.data.get("iniciacao")

        if not IniciacaoCientifica.objects.filter(id=iniciacao_id).exists():
            raise ValidationError("Iniciação Científica não encontrada.")

        # Evitar duplicação
        if InteresseIC.objects.filter(aluno=user, iniciacao_id=iniciacao_id).exists():
            raise ValidationError("Você já demonstrou interesse nesta iniciação.")

        serializer.save(aluno=user)

class ListaInteressadosView(generics.ListAPIView):
    serializer_class = AlunoInteressadoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        iniciacao_id = self.kwargs["id"]

        ic = IniciacaoCientifica.objects.get(id=iniciacao_id)

        if user.role != "professor":
            raise PermissionDenied("Apenas professores podem ver interessados.")

        if ic.professor != user:
            raise PermissionDenied("Você só pode ver interessados das suas próprias iniciações.")

        return CustomUser.objects.filter(interesses__iniciacao=ic)
    
class ListarInteressesAlunoView(generics.ListAPIView):
    serializer_class = IniciacaoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role != "aluno":
            raise PermissionDenied("Somente alunos podem listar seus interesses.")

        return IniciacaoCientifica.objects.filter(interessados__aluno=user)
    
class RemoverInteresseView(generics.DestroyAPIView):
    queryset = InteresseIC.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        interesse = self.get_object()

        if request.user != interesse.aluno:
            raise PermissionDenied("Você só pode remover seus próprios interesses.")

        interesse.delete()
        return Response({"detail": "Interesse removido com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    
class BuscarIniciacoesView(generics.ListAPIView):
    serializer_class = IniciacaoListSerializer
    queryset = IniciacaoCientifica.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()

        titulo = self.request.query_params.get("titulo")
        area = self.request.query_params.get("area")
        tags = self.request.query_params.get("tags")
        bolsa = self.request.query_params.get("bolsa")
        professor = self.request.query_params.get("professor")
        duracao = self.request.query_params.get("duracao")

        if titulo:
            qs = qs.filter(titulo__icontains=titulo)

        if area:
            qs = qs.filter(area_pesquisa__icontains=area)

        if tags:
            qs = qs.filter(tags__icontains=tags)

        if bolsa is not None:
            if bolsa.lower() == "true":
                qs = qs.filter(bolsa_disponivel=True)
            elif bolsa.lower() == "false":
                qs = qs.filter(bolsa_disponivel=False)

        if professor:
            qs = qs.filter(professor__username__icontains=professor)

        if duracao:
            qs = qs.filter(duracao__icontains=duracao)

        return qs

class EditarIniciacaoView(generics.UpdateAPIView):
    queryset = IniciacaoCientifica.objects.all()
    serializer_class = IniciacaoUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        user = self.request.user
        ic = self.get_object()

        if user.role != "professor":
            raise PermissionDenied("Somente professores podem editar iniciações científicas.")

        if ic.professor != user:
            raise PermissionDenied("Você só pode editar iniciações criadas por você.")

        serializer.save()

class ExcluirIniciacaoView(generics.DestroyAPIView):
    queryset = IniciacaoCientifica.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role != "professor":
            raise PermissionDenied("Somente professores podem excluir iniciações científicas.")

        if instance.professor != user:
            raise PermissionDenied("Você só pode excluir iniciações criadas por você.")

        instance.delete()