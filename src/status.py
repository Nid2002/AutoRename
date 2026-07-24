from enum import Enum, auto


class ResultadoProcessamento(Enum):
    RENOMEADO = auto()
    IGNORADO = auto()
    ERRO = auto()
