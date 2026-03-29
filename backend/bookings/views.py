from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Booking
from .gmail_service import send_email


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


            subject_admin = "Nova marcação - ATX Cycling Store"

            html_admin = f"""

            <div style="font-family: Arial; padding:20px;">

                <h2>Nova marcação recebida</h2>

                <p><strong>Nome:</strong> {booking.nome}</p>

                <p><strong>Email:</strong> {booking.email}</p>

                <p><strong>Telefone:</strong> {booking.telefone}</p>

                <p><strong>Serviço:</strong> {booking.servico}</p>

                <p><strong>Bicicleta:</strong> {booking.modelo_bike}</p>

                <p><strong>Data:</strong> {booking.data}</p>

                <p><strong>Mensagem:</strong><br>{booking.mensagem}</p>

            </div>

            """


            send_email(

                "adminsiteatx@gmail.com",
                subject_admin,
                html_admin

            )


            subject_client = "Confirmação de marcação - ATX Cycling Store"

            html_client = f"""

            <div style="font-family: Arial; padding:20px;">

                <h2>Confirmação de marcação</h2>

                <p>Olá {booking.nome},</p>

                <p>Recebemos o seu pedido com os seguintes dados:</p>

                <ul>

                    <li><strong>Serviço:</strong> {booking.servico}</li>

                    <li><strong>Bicicleta:</strong> {booking.modelo_bike}</li>

                    <li><strong>Data:</strong> {booking.data}</li>

                </ul>

                <p>Entraremos em contacto em breve.</p>

                <p>ATX Cycling Store</p>

            </div>

            """


            send_email(

                booking.email,
                subject_client,
                html_client

            )


            return JsonResponse({"success": True})


        except Exception as e:

            print("ERRO EMAIL:", e)

            return JsonResponse(

                {"error": str(e)},
                status=500

            )


    return JsonResponse(

        {"error": "Método inválido"},
        status=400

    )