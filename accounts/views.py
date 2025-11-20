from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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
