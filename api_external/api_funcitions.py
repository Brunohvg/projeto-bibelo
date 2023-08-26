import requests
from decouple import config

"""
07083e9b894d791c4a8191442cf4747b
B515296DB6444A61C4A4B5CDCEF1846A3FF58D2D
"""

api_key = config("KEY_CORREIO")
api_borzo = config("TOKEN_BORZO")


def buscar_endereco(cep):
    VIACEP_URL = "https://viacep.com.br/ws/{}/json/"
    CEP_INVALIDO_MSG = "O CEP: {}, é inválido ou não foi encontrado."
    ERRO_REQUISICAO_MSG = "Erro na requisição: {}"
    """
    Busca informações de endereço usando um CEP.

    :param cep: O CEP a ser consultado.
    :return: Um dicionário com os dados do endereço ou uma mensagem de erro.

    cep = "99999-9999"
    endereco = buscar_endereco(cep)
    print(endereco)


    """
    try:
        response = requests.get(url=VIACEP_URL.format(cep))
        response.raise_for_status()  # Lança uma exceção se houver um erro de HTTP

        data = response.json()
        if "erro" in data:
            return {"response_erro": CEP_INVALIDO_MSG.format(cep)}

        return data
    except requests.exceptions.RequestException as e:
        return {"response_erro": ERRO_REQUISICAO_MSG.format(e)}


def consultar_valor_correio(cep, peso):
    url_sgpweb = f"https://www.sgpweb.com.br/novo/api/consulta-precos-prazos?chave_integracao={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "cep_origem": "30170-130",
        "cep_destino": cep,
        "peso": peso,
        "comprimento": "",
        "altura": "",
        "largura": "",
        "servicos": ["04162", "04669"],
    }
    try:
        # Construir a URL ou payload para a consulta à API externa
        # Fazer a requisição usando requests.get() ou requests.post()
        response = requests.post(url_sgpweb, json=payload, headers=headers)
        response.raise_for_status()  # Lidar com erros HTTP

        data = response.json()

        sedex_erro = data["servicos"]["04162"]["Erro"]
        pac_erro = data["servicos"]["04669"]["Erro"]

        if sedex_erro and pac_erro != "0":
            return data["servicos"]["04669"]["MsgErro"]

        # Processar e retornar os dados obtidos da API
        return data

    except requests.exceptions.RequestException as e:
        # Lidar com erros de requisição, como timeouts, conexão falha, etc.
        # Pode retornar uma mensagem de erro, logar o erro, etc.
        print("Erro na requisição:", e)
        return {"erro": "Ocorreu um erro na consulta à API externa."}


def consultar_valor_motoboy(cep):
    url_borzo = (
        "https://robotapitest-br.borzodelivery.com/api/business/1.4/calculate-order"
    )
    header = {
        "X-DV-Auth-Token": api_borzo,
        "Content-Type": "application/json",
    }
    data = {
        "matter": "Documents",
        "points": [{"address": "30170-130"}, {"address": cep}],
    }

    try:
        response = requests.post(url_borzo, headers=header, json=data)
        response.raise_for_status()  # Lidar com erros HTTP
        response = response.json()

        valor_boy = int(float(response["order"]["payment_amount"]))

        if valor_boy <= 18:
            valor = "18,00"
            return valor

        else:
            return response["order"]["payment_amount"]

    except requests.exceptions.RequestException as e:
        # Lidar com erros de requisição, como timeouts, conexão falha, etc.
        # Pode retornar uma mensagem de erro, logar o erro, etc.
        print("Erro na requisição:", e)
        return {"erro": "Ocorreu um erro na consulta à API externa."}


print(consultar_valor_motoboy(54))
