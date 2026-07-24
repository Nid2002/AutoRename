"""
=============================================================
AutoRename Phoenix
Versão : 1.0.0
Autor  : Nicolas Alves Oliveira
Ano    : 2026
=============================================================

"""


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
APP_VERSION = "1.0.0"
APP_AUTHOR = "Nic0las"

# ==========================================================
# Estrutura do projeto
# ==========================================================

#
# Quando executado pelo PyInstaller (--onefile),
# o executável fica em dist/ e o config.ini deve
# estar na mesma pasta do .exe.
#
if getattr(sys, "frozen", False):

    ROOT_DIR = Path(sys.executable).resolve().parent

#
# Execução normal pelo Python
#
else:

    BASE_DIR = Path(__file__).resolve().parent

    # Assume que config.py está dentro de src/
    ROOT_DIR = BASE_DIR.parent

    # Compatibilidade caso o projeto esteja sem a pasta src/
    if not (ROOT_DIR / "config.ini").exists():
        ROOT_DIR = BASE_DIR

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
    Retorna um caminho absoluto baseado na seção [GERAL].
    """

    return ROOT_DIR / config["GERAL"][chave]


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

TIPOS_BLOCO = carregar_lista(
    "BLOCOS"
)

PALAVRAS_PARADA_CONDOMINIO = [
    palavra.strip()
    for palavra in config["FILTROS"]["PALAVRAS_PARADA"].split(",")
]
