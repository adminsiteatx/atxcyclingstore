from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "email",
        "telefone",
        "servico",
        "modelo_bike",
        "mensagem",
        "data",
        "estado",
        "created_at",
    )

    search_fields = (
        "nome",
        "email",
        "telefone",
        "modelo_bike",
    )

    list_filter = (
        "servico",
        "estado",
        "created_at",
    )

    ordering = ("-created_at",)