from django.db import models

# validators=[validate_phone_number]
"""endereco = Endereco.objects.create(
    rua="Rua A",
    numero_casa="123",
    complemento="Apto 101",
    bairro="Bairro X",
    cidade="Cidade Y",
    cep="12345-678",
)

entrega = Entrega.objects.create(
    nome_cliente="Fulano de Tal",
    telefone="(31) 99999-9999",
    numero_pedido="12345",
    hora_limite=datetime.datetime.now(),
    info_adicional="Deixar na portaria",
    endereco=endereco,
)"""
 

# Create your models here.


class Endereco(models.Model):
    rua = models.CharField(max_length=255, verbose_name="Rua")
    numero_casa = models.CharField(max_length=10, verbose_name="Nº")
    complemento = models.CharField(max_length=255, verbose_name="Complemento")
    bairro = models.CharField(max_length=255, verbose_name="Bairro")
    cidade = models.CharField(max_length=255, verbose_name="Cidade")
    cep = models.CharField(max_length=9, verbose_name="CEP")

    def __str__(self) -> str:
        return self.bairro

    class Meta:
        verbose_name_plural = "Enderecos"
        db_table = "enderecos"


class Entrega(models.Model):
    nome_cliente = models.CharField(max_length=255, verbose_name="Nome")
    telefone = models.CharField(max_length=11, verbose_name="Telefone")
    numero_pedido = models.CharField(
        max_length=25, verbose_name="Nº Pedido", null=True, blank=True
    )
    hora_limite = models.DateTimeField(
        verbose_name="Horário Limite", null=True, blank=True
    )
    info_adicional = models.TextField(
        verbose_name="Informações adicionais", null=True, blank=True
    )
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    valor_entrega = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.nome_cliente

    class Meta:
        verbose_name_plural = "Entregas"
        db_table = "entrega"
