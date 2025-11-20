from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import IniciacaoCientificaSerializer
from .permissions import IsProfessor
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import InteresseIC, IniciacaoCientifica
from .serializers import InteresseICSerializer, AlunoInteressadoSerializer, IniciacaoListSerializer
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