from django.urls import path
from .views import SignupAluno, SignupProfessor, LoginView

urlpatterns = [
    path("signup/aluno/", SignupAluno.as_view(), name="signup_aluno"),
    path("signup/professor/", SignupProfessor.as_view(), name="signup_professor"),
    path("login/", LoginView.as_view(), name="login"),
]
