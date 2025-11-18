from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password


# -------------------------------------------------------
#        SERIALIZER DO ALUNO
# -------------------------------------------------------
class AlunoSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "email",
            "password", "password2",
            "matricula", "curso",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role="aluno",
            matricula=validated_data.get("matricula"),
            curso=validated_data.get("curso"),
        )
        return user


# -------------------------------------------------------
#        SERIALIZER DO PROFESSOR
# -------------------------------------------------------
class ProfessorSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "email",
            "password", "password2",
            "departamento", "areas_pesquisa",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            role="professor",
            departamento=validated_data.get("departamento"),
            areas_pesquisa=validated_data.get("areas_pesquisa"),
        )
        return user
