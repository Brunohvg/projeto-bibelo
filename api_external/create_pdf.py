from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import get_object_or_404
from FreteApp.models import Entrega  # Importe o modelo Entrega do seu aplicativo Django

def criar_pedido_entrega(request, identificador):
    # Recupere a entrega que deseja imprimir
    entrega = get_object_or_404(Entrega, id=identificador)

    # Configurar o tamanho da página
    doc = SimpleDocTemplate(f"pedido_entrega_{identificador}.pdf", pagesize=letter)

    # Lista para armazenar elementos do PDF
    elements = []

    # Estilos para o PDF
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_normal = styles["Normal"]

    # Título do Pedido de Entrega
    title = Paragraph("Pedido de Entrega", style_heading)
    elements.append(title)

    # Informações do Cliente
    customer_info = [
        Paragraph(f"<b>Nome:</b> {entrega.nome_cliente}", style_normal),
        Paragraph(f"<b>Telefone:</b> {entrega.telefone}", style_normal),
        Paragraph(f"<b>Número do Pedido:</b> {entrega.numero_pedido}", style_normal),
    ]
    elements.extend(customer_info)

    # Endereço de Entrega
    address_info = [
        Paragraph(f"<b>Endereço:</b> {entrega.endereco.rua}, {entrega.endereco.numero_casa}", style_normal),
        Paragraph(f"<b>Complemento:</b> {entrega.endereco.complemento}", style_normal),
        Paragraph(f"<b>Bairro:</b> {entrega.endereco.bairro}", style_normal),
        Paragraph(f"<b>Cidade:</b> {entrega.endereco.cidade}", style_normal),
        Paragraph(f"<b>CEP:</b> {entrega.endereco.cep}", style_normal),
    ]
    elements.extend(address_info)

    # Informações Adicionais
    if entrega.info_adicional:
        additional_info = Paragraph(f"<b>Informações Adicionais:</b> {entrega.info_adicional}", style_normal)
        elements.append(additional_info)

    # Valor da Entrega
    if entrega.valor_entrega:
        value_info = [Paragraph(f"<b>Valor da Entrega:</b> R$ {entrega.valor_entrega:.2f}", style_normal)]
        elements.extend(value_info)

    # Hora Limite
    if entrega.hora_limite:
        time_info = [Paragraph(f"<b>Entregar até:</b> {entrega.hora_limite.strftime('%H:%M')}", style_normal)]
        elements.extend(time_info)

    # Adicionar espaço em branco
    elements.append(Spacer(1, 12))

    # Criar o PDF
    doc.build(elements)

# Exemplo de uso: Passe o ID da entrega que deseja imprimir
criar_pedido_entrega(45)  # Substitua pelo ID da entrega desejada


"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Dados fictícios de um pedido de entrega
pedido_de_entrega = {
    "nome_cliente": "Cliente Exemplo",
    "telefone": "(123) 456-7890",
    "numero_pedido": "PED12345",
    "endereco": {
        "rua": "Rua da Entrega",
        "numero_casa": "123",
        "complemento": "Apto 4B",
        "bairro": "Bairro da Entrega",
        "cidade": "Cidade da Entrega",
        "cep": "12345-678",
    },
    "info_adicional": "Instruções especiais para a entrega.",
    "valor_entrega": 25.50,
    "hora_limite": "14:30",
}

# Configurar o tamanho da página
doc = SimpleDocTemplate("pedido_entrega.pdf", pagesize=letter)

# Lista para armazenar elementos do PDF
elements = []

# Estilos para o PDF
styles = getSampleStyleSheet()
style_heading = styles["Heading1"]
style_normal = styles["Normal"]

# Título do Pedido de Entrega
title = Paragraph("Pedido de Entrega", style_heading)
elements.append(title)

# Informações do Cliente
customer_info = [
    Paragraph(f"<b>Nome:</b> {pedido_de_entrega['nome_cliente']}", style_normal),
    Paragraph(f"<b>Telefone:</b> {pedido_de_entrega['telefone']}", style_normal),
    Paragraph(f"<b>Número do Pedido:</b> {pedido_de_entrega['numero_pedido']}", style_normal),
]
elements.extend(customer_info)

# Endereço de Entrega
endereco_entrega = pedido_de_entrega['endereco']
address_info = [
    Paragraph(f"<b>Endereço:</b> {endereco_entrega['rua']}, {endereco_entrega['numero_casa']}", style_normal),
    Paragraph(f"<b>Complemento:</b> {endereco_entrega['complemento']}", style_normal),
    Paragraph(f"<b>Bairro:</b> {endereco_entrega['bairro']}", style_normal),
    Paragraph(f"<b>Cidade:</b> {endereco_entrega['cidade']}", style_normal),
    Paragraph(f"<b>CEP:</b> {endereco_entrega['cep']}", style_normal),
]
elements.extend(address_info)

# Informações Adicionais
if pedido_de_entrega["info_adicional"]:
    additional_info = Paragraph(f"<b>Informações Adicionais:</b> {pedido_de_entrega['info_adicional']}", style_normal)
    elements.append(additional_info)

# Valor da Entrega
if pedido_de_entrega["valor_entrega"]:
    value_info = [Paragraph(f"<b>Valor da Entrega:</b> R$ {pedido_de_entrega['valor_entrega']:.2f}", style_normal)]
    elements.extend(value_info)

# Hora Limite
if pedido_de_entrega["hora_limite"]:
    time_info = [Paragraph(f"<b>Entregar até:</b> {pedido_de_entrega['hora_limite']}", style_normal)]
    elements.extend(time_info)

# Adicionar espaço em branco
elements.append(Spacer(1, 12))

# Criar o PDF
doc.build(elements)

"""