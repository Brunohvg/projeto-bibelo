def ggerar_os(request, identificador):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
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

    # Estilos para o PDF
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_normal = styles["Normal"]

    # Título da Ordem de Serviço
    title = Paragraph("Ordem de Serviço", style_heading)
    elements.append(title)

    # Informações da Entrega
    customer_info = [
        Paragraph(f"<b>Nome do Cliente:</b> {entrega.nome_cliente}", style_normal),
        Paragraph(f"<b>Telefone:</b> {entrega.telefone}", style_normal),
        Paragraph(f"<b>Número do Pedido:</b> {entrega.numero_pedido}", style_normal),
    ]
    elements.extend(customer_info)

    # Endereço de Entrega
    address_info = [
        Paragraph(
            f"<b>Endereço:</b> {entrega.endereco.rua}, {entrega.endereco.numero_casa}",
            style_normal,
        ),
        Paragraph(f"<b>Complemento:</b> {entrega.endereco.complemento}", style_normal),
        Paragraph(f"<b>Bairro:</b> {entrega.endereco.bairro}", style_normal),
        Paragraph(f"<b>Cidade:</b> {entrega.endereco.cidade}", style_normal),
        Paragraph(f"<b>CEP:</b> {entrega.endereco.cep}", style_normal),
    ]
    elements.extend(address_info)

    # Informações Adicionais
    if entrega.info_adicional:
        additional_info = Paragraph(
            f"<b>Informações Adicionais:</b> {entrega.info_adicional}", style_normal
        )
        elements.append(additional_info)

    # Valor da Entrega
    if entrega.valor_entrega:
        value_info = [
            Paragraph(
                f"<b>Valor da Entrega:</b> R$ {entrega.valor_entrega:.2f}", style_normal
            )
        ]
        elements.extend(value_info)

    # Hora Limite
    if entrega.hora_limite:
        time_info = [
            Paragraph(f"<b>Entregar até:</b> {entrega.hora_limite}", style_normal)
        ]
        elements.extend(time_info)

    # Adicionar espaço em branco
    elements.append(Spacer(1, 12))

    # Criar o PDF
    doc.build(elements)

    return response
