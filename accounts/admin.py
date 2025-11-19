from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # O que aparece na lista de usuários no admin
    list_display = (
        "username", "email", "role",
        "is_staff", "is_active"
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    # Seções exibidas ao editar um usuário
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informações pessoais", {
            "fields": (
                "first_name", "last_name", "email", "role",
                "matricula", "curso",
                "departamento", "areas_pesquisa",
            )
        }),
        ("Permissões", {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions",
            )
        }),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )

    # Seção exibida ao criar um usuário no admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "role",
                "password1", "password2",
                "matricula", "curso",
                "departamento", "areas_pesquisa",
                "is_active", "is_staff", "is_superuser",
            ),
        }),
    )

    search_fields = ("username", "email", "role")
    ordering = ("id",)


