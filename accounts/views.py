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

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

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
