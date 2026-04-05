from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .gmail_service import send_email

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

        booking = Booking.objects.create(

            nome=request.POST.get("nome"),
            email=request.POST.get("email"),
            telefone=request.POST.get("telefone"),
            servico=request.POST.get("servico"),
            modelo_bike=request.POST.get("modelo_bike"),
            mensagem=request.POST.get("mensagem"),
            data=request.POST.get("data"),
            estado="pendente"

        )

        try:

            # EMAIL ADMIN
            subject_admin = "Nova marcação – ATX Cycling Store"

            html_admin = f"""
            <h2>Nova marcação recebida</h2>

            <p><strong>Nome:</strong> {booking.nome}</p>
            <p><strong>Email:</strong> {booking.email}</p>
            <p><strong>Telefone:</strong> {booking.telefone}</p>

            <p><strong>Serviço:</strong> {booking.servico}</p>
            <p><strong>Bicicleta:</strong> {booking.modelo_bike}</p>

            <p><strong>Data:</strong> {booking.data}</p>

            <p><strong>Mensagem:</strong><br>
            {booking.mensagem}
            </p>
            """

            send_email(
                "adminsiteatx@gmail.com",
                subject_admin,
                html_admin
            )

            # EMAIL CLIENTE

            subject_client = "Confirmação da sua marcação – ATX Cycling Store"

            html_client = f"""
            <div style="font-family:Arial;padding:25px;background:#f5f5f5">

            <div style="
            max-width:520px;
            margin:auto;
            background:white;
            padding:30px;
            border-radius:12px;
            box-shadow:0 4px 18px rgba(0,0,0,0.08);
            ">

            <h2 style="margin-bottom:20px;color:#002a4d">
            Confirmação da sua marcação
            </h2>

            <p>
            Olá <strong>{booking.nome}</strong>,
            </p>

            <p>
            Recebemos o seu pedido de marcação com sucesso.
            </p>

            <div style="
            margin:25px 0;
            padding:18px;
            border-radius:8px;
            background:#f8fafc;
            border:1px solid #e6e6e6;
            ">

            <p><strong>Serviço:</strong> {booking.servico}</p>

            <p><strong>Bicicleta:</strong> {booking.modelo_bike}</p>

            <p><strong>Data pretendida:</strong> {booking.data}</p>

            <p><strong>Mensagem:</strong><br>
            <span style="color:#555">
            {booking.mensagem}
            </span>
            </p>

            </div>

            <p>
            Entraremos em contacto brevemente para confirmar a disponibilidade.
            </p>

            <p>
            Obrigado pela confiança.
            </p>

            <hr style="margin:30px 0">

            <div style="text-align:center">

            <p style="
            margin-bottom:8px;
            font-weight:600;
            color:#002a4d
            ">
            ATX Cycling Store
            </p>

            <img
            src="https://raw.githubusercontent.com/adminsiteatx/atxcyclingstore/main/images/atx.png"
            width="120"
            style="opacity:0.9"
            />

            <p style="
            font-size:13px;
            color:#888;
            margin-top:15px
            ">
            Oficina certificada Shimano Service Center
            </p>

            </div>

            </div>

            </div>
            """

            send_email(
                booking.email,
                subject_client,
                html_client
            )

        except Exception as e:

            print("ERRO EMAIL ADMIN:", e)

        return redirect("/painel")

    return render(request, "nova_marcacao.html")
