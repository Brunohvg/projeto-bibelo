from django.shortcuts import render, get_object_or_404
from .models import Endereco, Entrega
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from .models import Endereco, Entrega
from .forms import FormularioEndereco, FormularioEntrega
from api_external.api_funcitions import (
    buscar_endereco,
    consultar_valor_correio,
    consultar_valor_motoboy,
)
from fpdf import FPDF
from api_external.create_pdf import ggerar_os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def home(request):
    return render(request, "FreteApp/home.html")


def cotar(request):
    if request.method == "POST":
        return handle_post_request(request)
    else:
        return render(request, "FreteApp/cotacao.html", status=200)


def handle_post_request(request):
    cep = request.POST.get("cep")
    peso = request.POST.get("peso")

    if cep and peso:
        return handle_valid_data(cep, peso, request)
    else:
        return handle_invalid_data(request)


def handle_valid_data(cep, peso, request):
    try:
        endereco = buscar_endereco(cep)
        if endereco["logradouro"]:
            endereco = buscar_endereco(cep)
    except:
        messages.error(
            request, "Erro ao processar o cep ou cep invalido favor tentar novamente"
        )
        return render(request, "FreteApp/cotacao.html", status=401)
    if endereco:
        conteudo_inicial = {
            "rua": endereco["logradouro"],
            "bairro": endereco["bairro"],
            "cidade": endereco["localidade"],
            "cep": endereco["cep"],
        }
    valores_correio = consultar_valor_correio(cep=cep, peso=peso)
    valor_motoboy = consultar_valor_motoboy(cep=cep)
    formulario_endereco = FormularioEndereco(initial=conteudo_inicial)
    formulario_entrega = FormularioEntrega(
        initial={"hora_limite": "12:00", "valor_entrega": valor_motoboy}
    )
    if endereco.get("cep"):
        endereco_info = {
            "cep": endereco["cep"],
            "logradouro": endereco["logradouro"],
            "complemento": endereco["complemento"],
            "bairro": endereco["bairro"],
            "localidade": endereco["localidade"],
            "uf": endereco["uf"],
            "erro": "cep digitado errado",
            "valor_sedex": valores_correio["servicos"]["04162"]["Valor"],
            "valor_pac": valores_correio["servicos"]["04669"]["Valor"],
            "tempo_sedex": valores_correio["servicos"]["04162"]["PrazoEntrega"],
            "tempo_pac": valores_correio["servicos"]["04669"]["PrazoEntrega"],
            "valor_boy": valor_motoboy,
            "formulario_endereco": formulario_endereco,
            "formulario_entrega": formulario_entrega,
        }

        return render(
            request,
            "FreteApp/cotacao.html",
            context=endereco_info,
            status=200,
        )
    else:
        return render(
            request,
            "FreteApp/cotacao.html",
            context={"endereco": "O cep informado é inválido ou não existe"},
            status=400,
        )


def handle_invalid_data(request):
    return render(
        request,
        "FreteApp/cotacao.html",
        context={"endereco": "Dados inválidos fornecidos"},
        status=400,
    )


def handle_formulario_cotacao(request):
    hora_limite_str = request.POST.get("hora_limite")
    endereco = Endereco.objects.create(
        rua=request.POST.get("rua"),
        numero_casa=request.POST.get("numero_casa"),
        complemento=request.POST.get("complemento"),
        bairro=request.POST.get("bairro"),
        cidade=request.POST.get("cidade"),
        cep=request.POST.get("cep"),
    )

    entrega = (
        Entrega.objects.create(
            nome_cliente=request.POST.get("nome_cliente"),
            telefone=request.POST.get("telefone"),
            numero_pedido=request.POST.get("numero_pedido"),
            criado=timezone.now(),
            hora_limite=hora_limite_str,
            info_adicional=request.POST.get("info_adicional"),
            endereco=endereco,
            valor_entrega=request.POST.get("valor_entrega"),
        ),
    )

    messages.success(request, "Entrega criada com sucesso")

    todas_entregas = Entrega.objects.all()
    t_entregas = {
        "todas_entregas": todas_entregas,
    }

    return render(request, "FreteApp/listar_cotacoes.html", context=t_entregas)


def listar_cotacoes(request):
    todas_entregas = Entrega.objects.all()
    t_entregas = {
        "todas_entregas": todas_entregas,
    }
    if request.method == "POST":
        return handle_formulario_cotacao(request)

    return render(request, "FreteApp/listar_cotacoes.html", context=t_entregas)


def cotacao(request, identificador):
    entrega = get_object_or_404(Entrega, identificador=identificador)

    entrega = {"entrega": entrega}
    return render(request, "FreteApp/visualizar_cotacao.html", entrega)


def gerar_os(request, identificador):
    return ggerar_os(request, identificador=identificador)


from django.shortcuts import get_object_or_404


def delete(request, identificador):
    # Certifique-se de que 'Entrega' é o modelo correto que você deseja excluir
    entrega = get_object_or_404(Entrega, identificador=identificador)
    entrega.delete()
    # Redirecionar ou retornar uma resposta apropriada após a exclusão
    return HttpResponseRedirect("/algum_url_apropriado/")
