from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from projects.models import IniciacaoCientifica
from projects.serializers import IniciacaoListSerializer
from rest_framework import permissions

from .serializers import (
    AlunoSignupSerializer,
    ProfessorSignupSerializer
)

# ----------------------------------------
#               SIGNUP ALUNO
# ----------------------------------------
class SignupAluno(APIView):
    def post(self, request):
        serializer = AlunoSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "matricula": user.matricula,
                    "curso": user.curso,
                },
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=201)

        return Response(serializer.errors, status=400)


# ----------------------------------------
#            SIGNUP PROFESSOR
# ----------------------------------------
class SignupProfessor(APIView):
    def post(self, request):
        serializer = ProfessorSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "departamento": user.departamento,
                    "areas_pesquisa": user.areas_pesquisa,
                    "biografia": user.biografia
                },
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=201)

        return Response(serializer.errors, status=400)


# ----------------------------------------
#                  LOGIN
# ----------------------------------------
class LoginView(APIView):
    def post(self, request):

        login = request.data.get("username")
        password = request.data.get("password")

        # 1. Tenta autenticar usando username normalmente
        user = authenticate(username=login, password=password)

        # 2. Se falhar, tenta autenticar usando o email
        if user is None:
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user_obj = User.objects.filter(email=login).first()
                if user_obj:
                    user = authenticate(username=user_obj.username, password=password)
            except:
                pass

        if user is None:
            return Response({"error": "Credenciais inválidas"}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=200)

class GetProfessorById(APIView):
    # permite GET sem autenticação, mas requer autenticação para métodos de escrita
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, professor_id):
        professor = get_object_or_404(CustomUser, id=professor_id, role="professor")
        ics = IniciacaoCientifica.objects.filter(professor=professor)
        ic_serializer = IniciacaoListSerializer(ics, many=True)

        return Response({
            "id": professor.id,
            "username": professor.username,
            "email": professor.email,
            "departamento": professor.departamento,
            "areas_pesquisa": professor.areas_pesquisa,
            "iniciacoes": ic_serializer.data,
            "biografia": professor.biografia
        }, status=status.HTTP_200_OK)

    def _update_professor_from_data(self, professor, data):
        # Atualiza somente os campos enviados (comportamento PATCH)
        if 'departamento' in data:
            professor.departamento = data.get('departamento')
        if 'areas_pesquisa' in data:
            professor.areas_pesquisa = data.get('areas_pesquisa')
        if 'biografia' in data:
            professor.biografia = data.get('biografia')
        # se quiser validar outros campos, faça aqui
        professor.save()
        return professor

    def patch(self, request, professor_id):
        # requer autenticação por conta de permission_classes
        professor = get_object_or_404(CustomUser, id=professor_id, role="professor")

        # somente o dono do perfil (ou superuser) pode editar
        if not request.user.is_authenticated:
            return Response({"detail": "Autenticação necessária."}, status=status.HTTP_401_UNAUTHORIZED)

        if request.user != professor and not request.user.is_superuser:
            return Response({"detail": "Você só pode editar seu próprio perfil."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        try:
            professor = self._update_professor_from_data(professor, data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # responder com o objeto atualizado (mesma estrutura do GET)
        ics = IniciacaoCientifica.objects.filter(professor=professor)
        ic_serializer = IniciacaoListSerializer(ics, many=True)

        return Response({
            "id": professor.id,
            "username": professor.username,
            "email": professor.email,
            "departamento": professor.departamento,
            "areas_pesquisa": professor.areas_pesquisa,
            "iniciacoes": ic_serializer.data,
            "biografia": professor.biografia
        }, status=status.HTTP_200_OK)

    # Opcional: tratar PUT como alias de PATCH (se preferir PUT full replace, implemente validação)
    def put(self, request, professor_id):
        return self.patch(request, professor_id)