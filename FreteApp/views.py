from django.shortcuts import render
from api_external.api_funcitions import buscar_endereco


def home(request):
    if request.method == "POST":
        cep = request.POST.get("cep")
        if cep:
            endereco = buscar_endereco(cep)

            if endereco.get("cep"):
                endereco_info = {
                    "cep": endereco["cep"],
                    "logradouro": endereco["logradouro"],
                    "complemento": endereco["complemento"],
                    "bairro": endereco["bairro"],
                    "localidade": endereco["localidade"],
                    "uf": endereco["uf"],
                    "erro": "cep digitado errado",
                }
                return render(
                    request,
                    "FreteApp/cotacao.html",
                    context={"endereco": endereco_info},
                    status=200,
                )

            """
            retornar erro caso o cep seja errado 
            """
            return render(
                request,
                "FreteApp/cotacao.html",
                context={"endereco": f"O cep informado é invalido ou não existe"},
                status=400,
            )

    return render(request, "FreteApp/cotacao.html", status=200)
