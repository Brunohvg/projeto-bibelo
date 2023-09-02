from django.db import models


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
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    numero_pedido = models.CharField(
        max_length=25, verbose_name="Nº Pedido", null=True, blank=True
    )
    criado = models.DateTimeField(verbose_name="Entrega Criada", null=True, blank=True)
    hora_limite = models.TimeField(verbose_name="Entregar até", null=True, blank=True)

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
