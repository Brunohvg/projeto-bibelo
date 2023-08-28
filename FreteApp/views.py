from django.shortcuts import render
from api_external.api_funcitions import (
    buscar_endereco,
    consultar_valor_correio,
    consultar_valor_motoboy,
)
from .form import FormularioEndereco, FormularioEntrega


def home(request):
    return render(request, "FreteApp/home.html")


def cotacao(request):
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
    endereco = buscar_endereco(cep)
    valores_correio = consultar_valor_correio(cep=cep, peso=peso)
    valor_motoboy = consultar_valor_motoboy(cep=cep)
    formulario_endereco = FormularioEndereco()
    formulario_entrega = FormularioEntrega()
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
