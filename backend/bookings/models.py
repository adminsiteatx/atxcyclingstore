from django.db import models


class Booking(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    servico = models.CharField(max_length=100)
    modelo_bike = models.CharField(max_length=100, blank=True)
    mensagem = models.TextField()
    data = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="pendente")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
