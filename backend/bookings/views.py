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

            </div>
            
            <p><strong>Mensagem do cliente:</strong></p>
            
            <div style="
            background:#fff;
            border-left:4px solid #002a4d;
            padding:15px;
            margin-top:10px;
            border-radius:6px;
            ">
            
            {booking.mensagem}
            
            </div>

            """

            send_email(

                "adminsiteatx@gmail.com",
                subject_admin,
                html_admin

            )

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
            src="https://atxcyclingstore.vercel.app/public/atx.png"
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
