# extractor.py

import re
import pdfplumber

from config import (
    PREFIXOS_CONDOMINIO,
    TIPOS_UNIDADE,
    ALIAS_CONDOMINIOS,
)

from boleto import Boleto

from debug import (
    debug,
    debug_secao,
)

# ======================================================
# EXTRAI TODO O TEXTO DO PDF
# ======================================================

def extrair_texto(caminho_pdf):

    debug_secao("Leitura do PDF")
    debug(f"Arquivo.........: {caminho_pdf}")

    texto = ""

    with pdfplumber.open(caminho_pdf) as pdf:

        for pagina in pdf.pages:

            conteudo = pagina.extract_text()

            if conteudo:
                texto += conteudo + "\n"

    debug("Leitura concluída.")

    return texto


# ======================================================
# EXTRAI TODAS AS INFORMAÇÕES
# ======================================================

def extrair_dados(texto):

    dados = Boleto()

    linhas = texto.splitlines()

    for linha in linhas:

        linha = linha.strip()

        if not linha:
            continue

        # --------------------------
        # CONDOMÍNIO
        # --------------------------

        if dados.condominio is None:

            condominio = detectar_condominio(linha)

            if condominio:
                dados.condominio = condominio

        # --------------------------
        # BLOCO / UNIDADE
        # --------------------------

        if dados.unidade is None:

            resultado = detectar_unidade(linha)

            if resultado:

                bloco, unidade = resultado

                dados.bloco = bloco
                dados.unidade = unidade

        #
        # Já encontrou tudo que depende da leitura linha a linha
        #

        if dados.condominio and dados.unidade:
            break

    #
    # VENCIMENTO
    #

    dados.vencimento = detectar_vencimento(texto)

    #
    # Resumo da extração
    #

    debug_secao("Resumo da Extração")

    debug(f"Condomínio.....: {dados.condominio or '-'}")
    debug(f"Bloco..........: {dados.bloco or '-'}")
    debug(f"Unidade........: {dados.unidade or '-'}")
    debug(f"Vencimento.....: {dados.vencimento or '-'}")

    return dados


# ======================================================
# CONDOMÍNIO
# ======================================================

def detectar_condominio(linha):

    linha_maiuscula = linha.upper()

    for prefixo in PREFIXOS_CONDOMINIO:

        if linha_maiuscula.startswith(prefixo.upper()):

            debug_secao("Condomínio")

            debug(f"Linha..........: {linha}")
            debug(f"Prefixo........: {prefixo}")

            condominio = limpar_nome_condominio(linha)

            debug(f"Resultado......: {condominio}")

            return condominio

    return None


def limpar_nome_condominio(nome):

    nome_original = nome

    #
    # Remove prefixos
    #

    for prefixo in PREFIXOS_CONDOMINIO:

        nome = re.sub(
            rf"^{re.escape(prefixo)}\s*",
            "",
            nome,
            flags=re.IGNORECASE,
        )

    nome = " ".join(nome.split()).strip()

    debug(f"Após limpeza...: {nome}")

    #
    # Alias
    #

    nome_maiusculo = nome.upper()

    for texto, alias in ALIAS_CONDOMINIOS.items():

        if texto in nome_maiusculo:

            debug(f"Alias..........: {nome} -> {alias}")

            return alias

    debug("Alias..........: Nenhum")

    return nome


# ======================================================
# BLOCO / UNIDADE
# ======================================================

def detectar_unidade(linha):

    partes = linha.split()

    for i, palavra in enumerate(partes):

        if palavra.upper() in TIPOS_UNIDADE:

            debug_secao("Unidade")

            bloco = None
            unidade = None

            if i > 0:
                bloco = partes[i - 1]

            if i + 1 < len(partes):
                unidade = partes[i + 1]

            debug(f"Linha..........: {linha}")
            debug(f"Tipo...........: {palavra}")
            debug(f"Bloco..........: {bloco or '-'}")
            debug(f"Unidade........: {unidade}")

            return bloco, unidade

    return None


# ======================================================
# VENCIMENTO
# ======================================================

def detectar_vencimento(texto):

    debug_secao("Vencimento")

    resultado = re.search(
        r"Vencimento\s*(\d{2}/\d{2}/\d{4})",
        texto,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if resultado:

        data = resultado.group(1).replace("/", ".")

        debug(f"Data...........: {data}")

        return data

    debug("Resultado......: Não encontrado")

    return None
