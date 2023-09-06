def ggerar_os(request, identificador):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    from FreteApp.models import Entrega

    # Obtenha o objeto de entrega com base no identificador
    entrega = get_object_or_404(Entrega, identificador=identificador)

    # Configurar o tamanho da página
    response = HttpResponse(content_type="application/pdf")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="ordem_de_servico_{identificador}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Lista para armazenar elementos do PDF
    elements = []

    # Crie um estilo personalizado com um tamanho de fonte diferente
    custom_style = ParagraphStyle(
        'CustomStyle',  # Nome do estilo
        # Pode ser 'Normal' ou outro estilo base
        parent=getSampleStyleSheet()['Normal'],
        fontSize=12,  # Tamanho da fonte desejado em pontos
    )

    # Estilos para o PDF
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_normal = styles["Normal"]

    # Título da Ordem de Serviço
    title = Paragraph("Ordem de Entrega - Motoboy", style_heading)
    elements.append(title)
    elements.append(Spacer(1, 24))

    # Informações da Entrega
    customer_info = [
        Paragraph(
            f"<b>Nome do Cliente:</b> {entrega.nome_cliente}", custom_style),
        Paragraph(f"<b>Telefone:</b> {entrega.telefone}", custom_style),
        Paragraph(
            f"<b>Número do Pedido:</b> {entrega.numero_pedido}", custom_style),
    ]

    custmer_info_space = []

    for paragraph in customer_info:
        custmer_info_space.append(paragraph)
        custmer_info_space.append(Spacer(1, 5))

    elements.extend(custmer_info_space)

    # Endereço de Entrega
    address_info = [
        Paragraph(
            f"<b>Endereço:</b> {entrega.endereco.rua}, {entrega.endereco.numero_casa} - {entrega.endereco.bairro} - {entrega.endereco.cidade} - {entrega.endereco.complemento}",
            custom_style,
        ),
        Paragraph(f"<b>CEP:</b> {entrega.endereco.cep}", custom_style),
    ]

    address_elements = []

    for paragraph in address_info:
        address_elements.append(paragraph)
        # Adiciona um espaço de 5 pontos entre os parágrafos
        address_elements.append(Spacer(1, 5))

    elements.extend(address_elements)

    # Informações Adicionais
    if entrega.info_adicional:
        additional_info = Paragraph(
            f"<b>Informações Adicionais:</b> {entrega.info_adicional}", custom_style
        )
        elements.append(additional_info)

    # Valor da Entrega
    if entrega.valor_entrega:
        value_info = [
            Paragraph(
                f"<b>Valor da Entrega:</b> R$ {entrega.valor_entrega:.2f}", custom_style
            )
        ]
        elements.extend(value_info)

    # Hora Limite
    if not entrega.hora_limite:
        time_info = [
            Paragraph(
                f"<b>Entregar até:</b> {entrega.hora_limite}", custom_style)
        ]
        elements.extend(time_info)

    # Adicionar espaço em branco
    elements.append(Spacer(1, 12))

    # Criar o PDF
    doc.build(elements)

    return response
