from django.urls import path
from .views import SignupAluno, SignupProfessor, LoginView, GetProfessorById


urlpatterns = [
    path("signup/aluno/", SignupAluno.as_view(), name="signup_aluno"),
    path("signup/professor/", SignupProfessor.as_view(), name="signup_professor"),
    path("login/", LoginView.as_view(), name="login"),
    path('professor/<int:professor_id>/', GetProfessorById.as_view(), name='get_professor_by_id'),
]
