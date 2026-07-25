"""
config.py

Responsável por:

- Localizar o projeto
- Carregar o config.ini
- Disponibilizar as configurações para o restante da aplicação
"""

from configparser import ConfigParser
from pathlib import Path
import sys

# ==========================================================
# Informações da aplicação
# ==========================================================

APP_NAME = "AutoRename"
APP_VERSION = "1.0.1"
APP_AUTHOR = "Nic0las"

# ==========================================================
# Estrutura do projeto
# ==========================================================

#
# Diretório raiz da aplicação
#
# Desenvolvimento:
#   AutoRename/
#       config.ini
#       src/
#
# Executável:
#   AutoRename.exe
#   config.ini
#

if getattr(sys, "frozen", False):

    ROOT_DIR = Path(sys.executable).resolve().parent

else:

    ROOT_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = ROOT_DIR / "config.ini"

# ==========================================================
# Validação
# ==========================================================

if not CONFIG_FILE.exists():
    raise FileNotFoundError(
        f"Arquivo de configuração não encontrado:\n{CONFIG_FILE}"
    )

# ==========================================================
# Leitura do config.ini
# ==========================================================

config = ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")

# ==========================================================
# Funções auxiliares
# ==========================================================

def carregar_lista(secao: str) -> list[str]:
    """
    Retorna todos os valores de uma seção do config.ini.
    """

    return [
        valor.strip()
        for valor in config[secao].values()
    ]


def caminho_config(chave: str) -> Path:
    """
    Retorna um caminho baseado na seção [GERAL].

    - Caminhos relativos são interpretados a partir da raiz do projeto.
    - Caminhos absolutos são utilizados exatamente como informados.
    """

    caminho = Path(config["GERAL"][chave]).expanduser()

    if caminho.is_absolute():
        return caminho.resolve()

    return (ROOT_DIR / caminho).resolve()
# ==========================================================
# Diretórios da aplicação
# ==========================================================

PASTA_ENTRADA = caminho_config("PASTA_ENTRADA")
PASTA_LOGS = caminho_config("PASTA_LOGS")

# Arquivo de log

LOG_FILE = PASTA_LOGS / "autorename.log"

# Cria automaticamente as pastas

PASTA_ENTRADA.mkdir(
    parents=True,
    exist_ok=True,
)

PASTA_LOGS.mkdir(
    parents=True,
    exist_ok=True,
)

# ==========================================================
# Configurações gerais
# ==========================================================

DRY_RUN = config.getboolean(
    "GERAL",
    "DRY_RUN",
)

DEBUG = config.getboolean(
    "GERAL",
    "DEBUG",
    fallback=False,
)

# ==========================================================
# Configurações do Extrator
# ==========================================================

PREFIXOS_CONDOMINIO = carregar_lista(
    "CONDOMINIOS"
)

# Alias de condomínios (opcional)

if config.has_section("ALIAS_CONDOMINIOS"):

    ALIAS_CONDOMINIOS = {
        chave.upper(): valor.strip()
        for chave, valor in config["ALIAS_CONDOMINIOS"].items()
    }

else:

    ALIAS_CONDOMINIOS = {}

TIPOS_UNIDADE = carregar_lista(
    "UNIDADES"
)

#
# Tipos de bloco
#

if config.has_section("BLOCOS"):

    TIPOS_BLOCO = {
        valor.strip().upper()
        for valor in config["BLOCOS"].values()
    }

else:

    TIPOS_BLOCO = {
        "BL",
        "BLOCO",
        "CS",
        "TE",
    }

PALAVRAS_PARADA_CONDOMINIO = [
    palavra.strip()
    for palavra in config["FILTROS"]["PALAVRAS_PARADA"].split(",")

]

# Delimitadores que indicam o fim das informações da unidade

if config.has_section("DELIMITADORES_UNIDADE"):

    DELIMITADORES_UNIDADE = {
        valor.strip().upper()
        for valor in config["DELIMITADORES_UNIDADE"].values()
    }

else:

    # Valores padrão (compatibilidade)

    DELIMITADORES_UNIDADE = {
        "ID",
        "CPF",
        "CNPJ",
        "CEP",
        "RUA",
        "AV",
        "AVENIDA",
        "Nº",
        "NUMERO",
        "BANCO",
        "PIX",
    }
