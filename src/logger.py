"""
=============================================================
AutoRename Phoenix
Versão : 1.0.0
Autor  : Nicolas Alves Oliveira
Ano    : 2026
=============================================================

"""


import logging

from config import (
    PASTA_LOGS,
    LOG_FILE,
    DEBUG,
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
)

logger = logging.getLogger("AutoRename")


# ======================================================
# Compatibilidade
# ======================================================

def registrar_sucesso(original, novo):
    logger.info(f"{original} -> {novo}")


def registrar_erro(arquivo, erro):
    logger.error(f"{arquivo} | {erro}")


def registrar_info(mensagem):
    logger.info(mensagem)


def registrar_excecao(arquivo):
    logger.exception(f"Erro inesperado ao processar {arquivo}")


def registrar_ignorado(arquivo):
    logger.info(f"Ignorado: {arquivo}")


# ======================================================
# Novo logger detalhado
# ======================================================

def registrar_processamento(
    arquivo,
    boleto,
    status,
    motivo=None,
    novo_nome=None,
):

    logger.info("=" * 60)

    logger.info(f"Arquivo.....: {arquivo}")

    logger.info(
        f"Condomínio..: {boleto.condominio or 'NÃO ENCONTRADO'}"
    )

    logger.info(
        f"Bloco.......: {boleto.bloco or '-'}"
    )

    logger.info(
        f"Unidade.....: {boleto.unidade or 'NÃO ENCONTRADA'}"
    )

    logger.info(
        f"Vencimento..: {boleto.vencimento or 'NÃO ENCONTRADO'}"
    )

    if novo_nome:

        logger.info(
            f"Novo Nome...: {novo_nome}"
        )

    logger.info(
        f"Status......: {status}"
    )

    if motivo:

        logger.info(
            f"Motivo......: {motivo}"
        )

    logger.info("=" * 60)

    #
    # Informações extras para DEBUG
    #

    if DEBUG:

        logger.info(
            "DEBUG.......: Processamento concluído."
        )

        logger.info("")
