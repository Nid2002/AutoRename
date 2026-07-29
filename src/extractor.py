# extracto.py

import re
import pdfplumber

from config import (
    PREFIXOS_CONDOMINIO,
    TIPOS_UNIDADE,
    TIPOS_BLOCO,
    ALIAS_CONDOMINIOS,
    DELIMITADORES_UNIDADE,
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

    #
    # Linhas extraídas do documento
    #

    debug_secao("Linhas Extraídas")

    for i, linha in enumerate(linhas, start=1):

        linha = linha.strip()

        if linha:
            debug(f"[{i:02}] {linha}")

    #
    # Processamento das linhas
    #

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

                debug(f"✓ Condomínio encontrado: {condominio}")

        # --------------------------
        # BLOCO / UNIDADE
        # --------------------------

        if dados.unidade is None:

            resultado = detectar_unidade(linha)

            if resultado:

                bloco, unidade = resultado

                dados.bloco = bloco
                dados.unidade = unidade

                debug(f"✓ Bloco encontrado.....: {bloco or '-'}")
                debug(f"✓ Unidade encontrada...: {unidade}")

        #
        # Já encontrou tudo que depende da leitura linha a linha
        #

        if dados.condominio and dados.unidade:
            break

    #
    # Tipo do documento
    #

    dados.tipo_documento = detectar_tipo_documento(texto)

    debug(f"✓ Tipo documento.....: {dados.tipo_documento}")

    

    #
    # VENCIMENTO
    #

    dados.vencimento = detectar_vencimento(texto)

    if dados.vencimento:

        debug(f"✓ Vencimento encontrado: {dados.vencimento}")

    else:

        debug("⚠ Vencimento não encontrado.")

    #
    # Resumo da extração
    #

    debug_secao("Resumo da Extração")

    debug(f"Tipo Documento.: {dados.tipo_documento}")
    debug(f"Condomínio.....: {dados.condominio or '-'}")
    debug(f"Bloco..........: {dados.bloco or '-'}")
    debug(f"Unidade........: {dados.unidade or '-'}")
    debug(f"Vencimento.....: {dados.vencimento or '-'}")

    if dados.nome_arquivo:
        debug(f"Nome Final.....: {dados.nome_arquivo}")

    return dados

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def _normalizar_token(token):
    """
    Remove pontuação das extremidades e converte para maiúsculas.
    """

    return token.strip(" ,.;:-_/\\()[]{}").upper()

def _eh_inicio_bloco(token):
    """
    Verifica se o token pode iniciar
    um identificador de bloco.
    """

    return token.upper() in TIPOS_BLOCO

def _token_eh_bloco(token):

    token = _normalizar_token(token)

    return _eh_inicio_bloco(token)

def _coletar_contexto_unidade(partes, indice_tipo):
    """
    Coleta o contexto da unidade.

    Retorna um dicionário contendo os tokens
    antes e depois do tipo da unidade.
    """

    antes = []

    for token in partes[:indice_tipo]:

        token_normalizado = _normalizar_token(token)

        if token_normalizado:
            antes.append(token_normalizado)

    depois = []

    for token in partes[indice_tipo + 1:]:

        token_normalizado = _normalizar_token(token)

        if token_normalizado in DELIMITADORES_UNIDADE:
            break

        if token_normalizado:
            depois.append(token_normalizado)

    return {
        "antes": antes,
        "depois": depois,
    }

def _interpretar_bloco(antes, depois, indice_unidade):

    bloco_tokens = []

    #
    # Tokens antes do tipo de unidade
    #
    if antes:
        bloco_tokens.extend(antes)

    #
    # Tokens entre o tipo da unidade e o número
    #
    if indice_unidade > 0:
        bloco_tokens.extend(depois[:indice_unidade])

    if not bloco_tokens:
        return None

#
# Um único número antes da unidade
# representa o bloco.
#
    if len(bloco_tokens) == 1:

        if bloco_tokens[0].isdigit():
            return bloco_tokens[0]
        
        if _token_eh_bloco(bloco_tokens[0]):
            return bloco_tokens[0]

        return None
#
# Múltiplos tokens somente são aceitos
# quando iniciam com um identificador
# de bloco.
#
    if not _token_eh_bloco(bloco_tokens[0]):
        return None

    bloco = " ".join(bloco_tokens).strip()

    return bloco

def _interpretar_tokens_unidade(contexto):

    antes = contexto["antes"]
    depois = contexto["depois"]

    indice_unidade = None

    for i in range(len(depois) - 1, -1, -1):

        if depois[i].isdigit():

            indice_unidade = i
            break

    if indice_unidade is None:
        return None

    unidade = depois[indice_unidade]

    bloco = _interpretar_bloco(
        antes,
        depois,
        indice_unidade,
    )

    return bloco, unidade

def normalizar_nome_condominio(nome):
    """
    Remove informações que não fazem parte do nome do condomínio.
    """

    nome = nome.strip()

    #
    # Remove número isolado no início
    #

    nome = re.sub(r"^\d+\s+", "", nome)

    #
    # Remove número isolado no final (ex.: número da página)
    #

    nome = re.sub(r"\s+\d+$", "", nome)

    #
    # Remove tudo após "ID:"
    #

    nome = re.sub(
        r"\s+ID:.*$",
        "",
        nome,
        flags=re.IGNORECASE,
    )

    #
    # Normaliza espaços
    #

    nome = " ".join(nome.split())

    return nome
# ======================================================
# CONDOMÍNIO
# ======================================================
def normalizar_condominio(nome):

    nome = nome.replace("*", "")

    nome = " ".join(nome.split())

    return nome.strip()

def detectar_condominio(linha):

    linha_maiuscula = linha.upper()

    #
    # Primeira tentativa
    #

    for prefixo in PREFIXOS_CONDOMINIO:

        if linha_maiuscula.startswith(prefixo.upper()):

            debug_secao("Condomínio")

            debug(f"Linha..........: {linha}")
            debug(f"Prefixo........: {prefixo}")

            condominio = limpar_nome_condominio(linha)

            debug(f"Resultado......: {condominio}")

            return condominio

    #
    # Segunda tentativa
    #

    match = re.search(
        r"SACADOR/AVALISTA:\s*(.+)",
        linha,
        flags=re.IGNORECASE,
    )

    if match:

        debug_secao("Condomínio")

        debug(f"Linha..........: {linha}")
        debug("Origem.........: SACADOR/AVALISTA")

        condominio = limpar_nome_condominio(
            match.group(1)
        )

        debug(f"Resultado......: {condominio}")

        return condominio

    return None

#====================================================

def limpar_nome_condominio(nome):

    nome = normalizar_condominio(nome)

    #
    # Remove todos os prefixos conhecidos
    #

    while True:

        alterado = False

        for prefixo in PREFIXOS_CONDOMINIO:

            novo_nome = re.sub(
                rf"^{re.escape(prefixo)}\s*",
                "",
                nome,
                flags=re.IGNORECASE,
            )

            if novo_nome != nome:

                debug(f"Removido........: {prefixo}")

                nome = novo_nome
                alterado = True

        if not alterado:
            break

    nome = " ".join(nome.split()).strip()

    nome = normalizar_nome_condominio(nome)

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

        if palavra.upper() not in TIPOS_UNIDADE:
            continue

        debug_secao("Unidade")

        contexto = _coletar_contexto_unidade(partes, i)

        resultado = _interpretar_tokens_unidade(contexto)

        if resultado is None:
            return None

        bloco, unidade = resultado

        debug(f"Linha..........: {linha}")
        debug(f"Partes.........: {partes}")
        debug(f"Tipo...........: {palavra}")
        debug(f"Antes..........: {contexto['antes']}")
        debug(f"Depois.........: {contexto['depois']}")
        debug(f"Bloco..........: {bloco or '-'}")
        debug(f"Unidade........: {unidade}")

        return bloco, unidade

    return None

# ======================================================
# VENCIMENTO
# ======================================================

def detectar_vencimento(texto):

    debug_secao("Vencimento")

    #
    # Primeira tentativa
    #

    resultado = re.search(
        r"Vencimento\s*(\d{2}/\d{2}/\d{4})",
        texto,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if resultado:

        data = resultado.group(1).replace("/", ".")

        debug("Origem.........: Vencimento imediato")
        debug(f"Data...........: {data}")

        return data

    #
    # Segunda tentativa
    #
    resultado = re.search(
        r"Vencimento.*?(\d{2}/\d{2}/\d{4})",
        texto,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if resultado:

        data = resultado.group(1).replace("/", ".")

        debug("Origem.........: Vencimento (fallback)")
        debug(f"Data...........: {data}")

        return data

    debug("Resultado......: Não encontrado")

    return None

#===========================
# Detectar tipo de documento
#===========================

def detectar_tipo_documento(texto):

    debug_secao("Tipo do Documento")

    #
    # NOVA VIA DE ACORDO
    #

    resultado = re.search(
        r"Final\s+da\s+Parcela\s+de\s+acordo\s+de\s+\d{2}/\d{2}/\d{4}",
        texto,
        flags=re.IGNORECASE,
    )

    if resultado:

        debug("Origem.........: Final da Parcela de Acordo")
        debug("Resultado......: NV - AC")

        return "NV - AC"

    #
    # ACORDO
    #

    resultado = re.search(
        r"PARCELA\s+(\d+)\s+DE\s+(\d+)",
        texto,
        flags=re.IGNORECASE,
    )

    if resultado:

        parcela = int(resultado.group(1))
        total = int(resultado.group(2))

        tipo = f"AC {parcela}-{total}"

        debug("Origem.........: Parcela de Acordo")
        debug(f"Resultado......: {tipo}")

        return tipo

    #
    # NOVA VIA DE TAXA
    #

    resultado = re.search(
        r"Final\s+da\s+Taxa\s+de\s+(\d{2})/(\d{2})/\d{4}",
        texto,
        flags=re.IGNORECASE,
    )

    if resultado:

        dia = resultado.group(1)
        mes = resultado.group(2)

        tipo = f"NV TAXA {dia}.{mes}"

        debug("Origem.........: Final da Taxa")
        debug(f"Resultado......: {tipo}")

        return tipo

    #
    # PADRÃO
    #

    debug("Origem.........: Padrão")
    debug("Resultado......: 2° VIA")

    return "2° VIA"
