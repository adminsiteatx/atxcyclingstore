from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Booking


def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:

            login(request, user)

            return redirect("/painel")

    return render(request, "admin_login.html")


@login_required(login_url="/login-admin")
def painel(request):

    pendentes = Booking.objects.filter(estado="pendente").order_by("-created_at")

    concluidos = Booking.objects.filter(estado="concluido").order_by("-created_at")

    return render(request, "painel.html", {

        "pendentes": pendentes,
        "concluidos": concluidos

    })


def admin_logout(request):

    logout(request)

    return redirect("/login-admin")

from django.shortcuts import get_object_or_404
from .models import Booking


@login_required(login_url="/login-admin")
def booking_detail(request, id):

    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":

        booking.estado = "concluido"
        booking.save()

        return redirect("/painel")

    return render(request, "booking_detail.html", {

        "booking": booking

    })

@login_required(login_url="/login-admin")
def nova_marcacao(request):

    if request.method == "POST":

        Booking.objects.create(

            nome=request.POST.get("nome"),

            email=request.POST.get("email"),

            telefone=request.POST.get("telefone"),

            servico=request.POST.get("servico"),

            modelo_bike=request.POST.get("modelo_bike"),

            mensagem=request.POST.get("mensagem"),

            data=request.POST.get("data"),

            estado="pendente"

        )

        return redirect("/painel")

    return render(request, "nova_marcacao.html")