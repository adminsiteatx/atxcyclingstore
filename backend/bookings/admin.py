from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "email",
        "telefone",
        "marcaBike",
        "modeloBike",
        "mensagem",
        "data",
    )

    search_fields = (
        "nome",
        "email",
        "marcaBike",
        "modeloBike",
    )

    list_filter = ("data",)