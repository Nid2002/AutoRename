import logging

from datetime import datetime

from constants import (
    APP_NOME,
    APP_VERSAO,
)

from config import (
    PASTA_LOGS,
    LOG_FILE,
    DEBUG,
)

logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8",
)

logger = logging.getLogger("AutoRename")

# ======================================================
# Inicialização do Log
# ======================================================

def iniciar_log():

    logger.info("=" * 60)
    logger.info(APP_NOME)
    logger.info(f"Versão.....: {APP_VERSAO}")
    logger.info(
        f"Iniciado em: {datetime.now():%d/%m/%Y %H:%M:%S}"
    )
    logger.info("=" * 60)
    logger.info("")

def finalizar_log():

    logger.info("")
    logger.info("=" * 60)
    logger.info("Fim da execução")
    logger.info("=" * 60)

# ======================================================
# Funções de DEBUG
# ======================================================

def debug(texto):

    if DEBUG:
        logger.info(texto)


def debug_secao(titulo):

    if DEBUG:

        logger.info("")
        logger.info("-" * 60)
        logger.info(titulo)
        logger.info("-" * 60)

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


