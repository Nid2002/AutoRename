from config import DEBUG
from logger import logger


def debug(mensagem):
    if DEBUG:
        logger.info(f"DEBUG.......: {mensagem}")


def debug_secao(titulo):
    debug("")
    debug(f"===== {titulo.upper()} =====")
