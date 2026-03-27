from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "email",
        "telemovel",
        "marca_bicicleta",
        "modelo_bicicleta",
        "mensagem",
        "data",
    )

    search_fields = ("nome", "email", "marca_bicicleta", "modelo_bicicleta")

    list_filter = ("data",)