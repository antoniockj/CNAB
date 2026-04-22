from datetime import datetime
import pandas as pd

#Deixa letras no padrão
def alfanumerico(texto, tamanho):
    return str(texto).upper().ljust(tamanho)[:tamanho]

#Deixa numeros no padrão
def numerico(num, tamanho):
    return str(num).zfill(tamanho)[:tamanho]

#Transformar numeros quebrados em int
def formatar_valor(valor, tamanho):
    return str(int(float(valor) * 100)).zfill(tamanho)

def gerar_header(empresa_nome, codigo_empresa, sequencial):
    hoje = datetime.now().strftime("%d%m%y")

    header = ""
    header += "0" #Identificação Registro
    header += "1" #Identificação Arquivo de Remessa
    header += "REMESSA" #Literal REMESSA
    header += "01" #Cod de Serviço
    header += alfanumerico("COBRANCA", 15) #Literal Serviço
    header += alfanumerico( codigo_empresa, 20) #Cod da Empresa
    header += alfanumerico(empresa_nome, 30) #Nome da Empresa
    header += "237" #Número do Bradesco na Câmara de Compensação
    header += alfanumerico("BRADESCO", 15) # Nome do Banco por Extenso
    header += hoje #Data
    header += " " * 8 #Branco
    header += "MX" #Identificação do sistema
    header += numerico(sequencial, 7) #Nº Seqüencial de Remessa
    header += " " * 277 #Branco
    header += numerico(1, 6) #Nº Seqüencial do Registro de Um em Um

    if len(header) != 400:
        raise ValueError(f"Linha inválida: {len(header)} caracteres")

    return header

def gerar_detalhe(dados, seq):
    hoje = datetime.now().strftime("%d%m%y")

    linha = ""
    linha += "1" #Identificação do Registro
    linha += numerico(dados["agencia"], 5) #Agencia de Debito
    linha += alfanumerico(dados["digito_agencia"], 1) #Digito da Agencia
    linha += numerico(dados["razao"], 5) #Razao da Conta
    linha += numerico(dados["conta"], 7) #Conta
    linha += alfanumerico(dados["digito_conta"], 1) #Digito da Conta
    linha += "0" + numerico(dados["carteira"], 3) + numerico(dados["agencia"], 5) + numerico(dados["conta"], 7) + alfanumerico(dados["digito_conta"], 1) #Conta Pagadora
    linha += alfanumerico(dados["controle"], 25) #N° Controle do participante
    linha += "237" #Cod do Banco
    linha += "2" if dados["multa"] > 0 else "0" #0 (sem multa) 2 (com multa)
    linha += numerico(int(dados["multa"] * 100), 4) #0 (preencher com zeros) 2 (preencher com percentual da multa com 2 casa decimais
    linha += numerico(dados["identificacao_titulo"], 11) # Identificação do Título no Banco voltar
    linha += "0" #Voltar
    linha += "0" * 10  #Desconto Bonificação por dia
    linha += "2"  # 1 banco emite boleto 2 cliente emite boleto
    linha += "N" #Ident. se emite Boleto para Débito Automático
    linha += " " * 10 #Brancos
    linha += "R" if dados["rateio_credito"] == "R" else " " #R se a empresa contratou o serviço de rateio
    linha += "2" #1 = emite aviso, e assume o endereço do Pagador constante do Arquivo-Remessa; 2 = não emite aviso;
    linha += " " * 2 #quantidade de parcelas para pagamento, se a Empresa contratou o serviço Pagamento Parcial, caso não, informar Branco.
    linha += numerico(dados["ocorrencia"], 2) #Cod de ocorrencia
    linha += alfanumerico(dados["documento"], 10) #N do doc
    linha += dados["vencimento"].strftime("%d%m%y") #Data vencimento
    linha += formatar_valor(dados["valor"], 13)
    linha += "0" * 3 #Banco encarregado pela cobrança
    linha += "0" * 5 #Agencia depositaria
    linha += numerico(dados["especie"], 2)  # espécie de titulo
    linha += "N" #indentificação
    linha += hoje #Data de emissão
    linha += "00" #1 instrução (Não interesse)
    linha += "00" #2 instrução (Não interesse)
    linha += formatar_valor(dados["juros_dia"], 13) #Valor a ser cobrado por dia de atraso
    linha += dados["data_limite"].strftime("%d%m%y") #Data Limite P/Concessão de Desconto
    linha += numerico(dados["valor_desconto"], 13) #Valor do desconto
    linha += "0" * 13 #Valor do IOF
    linha += "0" * 13 #Valor do abatimento
    linha += "01" if len(dados["cpf_cnpj"]) == 11 else "02" #01 cpf 02 cnpj
    linha += numerico(dados["cpf_cnpj"], 14) #cpf ou cnpj
    linha += alfanumerico(dados["nome"], 40) #nome do pagador
    linha += alfanumerico(dados["endereco"], 40) #endereço do pagador
    linha += " " * 12 #1 mensagem
    linha += numerico(dados["cep"], 5) #CEP pagador
    linha += numerico(dados["sufixo_cep"], 3) #Sufixo do Cep
    linha += " " * 60 #Sacador/Avalista ou 2ª Mensagem
    linha += numerico(seq, 6) #N sequencial do registro

    if len(linha) != 400:
        raise ValueError(f"Linha inválida: {len(linha)} caracteres")

    return linha

def gerar_trailer(seq):
    trailer = "9" #Indetificação Registro
    trailer += " " * 393 #Branco
    trailer += numerico(seq, 6) #N sequencial do registro

    if len(trailer) != 400:
        raise ValueError(f"Linha inválida: {len(trailer)} caracteres")

    return trailer

def gerar_arquivo(empresa, lista_boletos):
    linhas = []
    log = []

    linhas.append(gerar_header(
        empresa["nome"],
        empresa["codigo"],
        empresa["sequencial"]
    ))

    seq = 2

    for boleto in lista_boletos:
        linhas.append(gerar_detalhe(boleto, seq))

        log.append({
            "nome": boleto["nome"],
            "cpf_cnpj": boleto["cpf_cnpj"],
            "endereco": boleto["endereco"],
            "valor": boleto["valor"],
            "juros_dia": boleto["juros_dia"],
            "multa": boleto["multa"],
            "ocorrencia": boleto["ocorrencia"],
            "data_vencimento": boleto["vencimento"].strftime("%d/%m/%Y"),
            "sequencial": seq
        })

        seq += 1

    linhas.append(gerar_trailer(seq))

    cnab = "\n".join(linhas)

    df = pd.DataFrame(log)

    return cnab, df