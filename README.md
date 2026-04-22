# Gerador de Remessa CNAB 400 - Bradesco

Projeto em Python para geração de arquivos de remessa no padrão CNAB 400 (Banco Bradesco)

## Funcionalidades

- Interface via terminal (CMD)
- Geração de arquivo CNAB (.REM e .TXT)
- Exportação de dados em CSV
- Validação de layout (400 caracteres por linha)

## Como configurar o ambiente

### 1. Clonar o projeto

git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

### 2. Criar ambiente virtual (recomendado)

python -m venv venv
venv\Scripts\activate

### 3. Instalar dependências

pip install -r requirements.txt

## Como executar

python main.py

## Interface

===== GERADOR CNAB 400 =====  
1 - Adicionar boleto  
2 - Gerar arquivo remessa  
3 - Sair  

## Arquivos gerados

- remessa.rem → Arquivo CNAB padrão bancário  
- remessa.txt → Backup do arquivo  
- boletos.csv → Dados dos boletos  

## Regras do CNAB

- Cada linha deve ter exatamente 400 caracteres  
- Datas no formato DDMMAA  
- Valores em centavos (sem vírgula)  
- Campos numéricos com zeros à esquerda  
- Campos texto com espaços à direita  

## Banco

- Banco: Bradesco  
- Código: 237  
- Layout: CNAB 400  

## Autor

Projeto desenvolvido para automação de cobrança via CNAB.
