from datetime import datetime, timedelta
from cnab import gerar_arquivo

empresa = {
    "nome": "EMPRESA a",
    "codigo": "22",
    "sequencial": 1
}

boletos = []


def menu():
    print("1 - Adicionar boleto")
    print("2 - Gerar arquivo remessa")
    print("3 - Sair")


def adicionar_boleto():
    try:
        nome = input("Nome / Razão Social: ")
        cpf_cnpj = input("CPF / CNPJ (somente números): ")
        endereco = input("Endereço: ")

        valor = float(input("Valor do boleto: "))
        juros = float(input("Juros por dia: "))
        multa = float(input("Multa (%): "))

        print("\nOcorrência:")
        print("1 - Registro")
        print("2 - Baixa")
        print("6 - Prorrogação")
        ocorrencia = int(input("Escolha: "))

        boleto = {
            "agencia": 1234,
            "digito_agencia": "0",
            "razao": 12345,
            "conta": 1234567,
            "digito_conta": "0",
            "carteira": 9,
            "controle": f"CTRL{len(boletos)+1}",
            "multa": multa,
            "identificacao_titulo": len(boletos) + 1,
            "rateio_credito": "",
            "ocorrencia": ocorrencia,
            "documento": 1,
            "vencimento": datetime.now() + timedelta(days=30),
            "valor": valor,
            "juros_dia": juros,
            "data_limite": datetime.now(),
            "valor_desconto": 0,
            "cpf_cnpj": cpf_cnpj,
            "nome": nome,
            "endereco": endereco,
            "cep": 80000,
            "sufixo_cep": 000,
            "especie": 1
        }

        boletos.append(boleto)

        print("\nBoleto adicionado com sucesso!")

    except Exception as e:
        print(f"\nErro: {e}")


def gerar_remessa():
    try:
        if not boletos:
            print("\nNenhum boleto cadastrado.")
            return

        cnab, df = gerar_arquivo(empresa, boletos)

        with open("remessa.txt", "w") as f:
            f.write(cnab)

        with open("remessa.rem", "w") as f:
            f.write(cnab)

        df.to_csv("log.csv", index=False)

        print("\nArquivo gerado")

    except Exception as e:
        print(f"\nErro: {e}")
