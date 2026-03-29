from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Booking
from django.core.mail import EmailMultiAlternatives


@csrf_exempt
def create_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            booking = Booking.objects.create(
                nome=data.get("nome"),
                email=data.get("email"),
                telefone=data.get("telefone"),
                servico=data.get("servico"),
                modelo_bike=data.get("modelo_bike"),
                mensagem=data.get("mensagem"),
                data=data.get("data"),
            )

            subject = "Nova marcação - ATX Cycling Store"

            text_content = f"""
            Nova marcação recebida:

            Nome: {booking.nome}
            Email: {booking.email}
            Telefone: {booking.telefone}
            Serviço: {booking.servico}
            Data: {booking.data}
            Mensagem: {booking.mensagem}
            """

            html_content = f"""
            <div style="font-family: Arial; padding:20px;">
                <h2 style="color:#0A2540;">Nova marcação recebida</h2>
                <p><strong>Nome:</strong> {booking.nome}</p>
                <p><strong>Email:</strong> {booking.email}</p>
                <p><strong>Telefone:</strong> {booking.telefone}</p>
                <p><strong>Serviço:</strong> {booking.servico}</p>
                <p><strong>Bicicleta:</strong> {booking.modelo_bike}</p>
                <p><strong>Data:</strong> {booking.data}</p>
                <p><strong>Mensagem:</strong><br>{booking.mensagem}</p>
                <hr>
                <p style="color:gray;">ATX Cycling Store</p>
            </div>
            """

            email = EmailMultiAlternatives(
                subject,
                text_content,
                "adminsiteatx@gmail.com",
                ["adminsiteatx@gmail.com"]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            # EMAIL PARA O CLIENTE
            subject_client = "Confirmação de marcação - ATX Cycling Store"

            text_client = f"""
            Olá {booking.nome},

            Recebemos o seu pedido de marcação.

            Resumo do pedido:

            Serviço: {booking.servico}
            Bicicleta: {booking.modelo_bike}
            Data pretendida: {booking.data}

            Mensagem enviada:
            {booking.mensagem}

            Entraremos em contacto em breve para confirmar a disponibilidade.

            Obrigado,
            ATX Cycling Store
            """

            html_client = f"""
            <div style="font-family: Arial; padding:30px; background:#f5f7fa;">
                <div style="max-width:500px; margin:auto; background:white; padding:25px; border-radius:8px;">

                    <h2 style="color:#0A2540;">Confirmação de marcação</h2>

                    <p>Olá <strong>{booking.nome}</strong>,</p>

                    <p>Recebemos o seu pedido de marcação com o seguinte detalhe:</p>

                    <div style="background:#f0f4f8; padding:15px; border-radius:6px;">

                        <p><strong>Serviço:</strong> {booking.servico}</p>

                        <p><strong>Bicicleta:</strong> {booking.modelo_bike}</p>

                        <p><strong>Data pretendida:</strong> {booking.data}</p>

                        <p><strong>Mensagem:</strong><br>
                        {booking.mensagem}</p>

                    </div>

                    <p style="margin-top:20px;">
                    Entraremos em contacto em breve para confirmar a disponibilidade.
                    </p>

                    <hr style="margin:25px 0;">

                    <p style="font-size:12px; color:#777;">
                    ATX Cycling Store<br>
                    Oficina especializada em manutenção de bicicletas
                    </p>

                </div>
            </div>
            """

            email_client = EmailMultiAlternatives(
                subject_client,
                text_client,
                "adminsiteatx@gmail.com",
                [booking.email]
            )

            email_client.attach_alternative(html_client, "text/html")
            email_client.send()

            return JsonResponse({"success": True})

        except Exception as e:
            print("ERRO:", e)  # 👈 isto ajuda a debug no terminal
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método inválido"}, status=400)
