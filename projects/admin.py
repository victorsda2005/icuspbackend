from django.contrib import admin
from .models import IniciacaoCientifica


@admin.register(IniciacaoCientifica)
class IniciacaoCientificaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "area_pesquisa",
        "duracao",
        "numero_vagas",
        "bolsa_disponivel",
        "professor",
    )

    list_filter = (
        "area_pesquisa",
        "bolsa_disponivel",
        "professor",
    )

    search_fields = (
        "titulo",
        "area_pesquisa",
        "descricao",
        "tags",
    )

    readonly_fields = ("criado_em",)

    fieldsets = (
        ("Informações da Iniciação Científica", {
            "fields": (
                "titulo",
                "area_pesquisa",
                "duracao",
                "numero_vagas",
                "descricao",
                "tags",
                "professor",
            )
        }),
        ("Informações sobre Bolsa", {
            "fields": (
                "bolsa_disponivel",
                "tipo_bolsa",
            )
        }),
        ("Campos Opcionais", {
            "fields": (
                "objetivos",
                "requisitos",
            )
        }),
        ("Metadados", {
            "fields": ("criado_em",),
        }),
    )
