import re


PADRAO_ARQUIVO_RENOMEADO = re.compile(
    r"""
    ^
    .+
    \s-\s

    (?:
        [^-]+
        \s-\s
    )?

    [^-]+

    \s-\s

    \d{2}\.\d{2}\.\d{4}

    \.pdf$
    """,
    re.VERBOSE | re.IGNORECASE,
)


def arquivo_ja_renomeado(nome_arquivo: str) -> bool:
    """
    Verifica se o nome do arquivo segue o padrão gerado
    pelo AutoRename.

    Exemplos aceitos:

    BELLE VILLE - 201 - 10.06.2026.pdf

    CAÇADORES - B2 - 013 - 10.06.2026.pdf
    """

    return bool(
        PADRAO_ARQUIVO_RENOMEADO.match(nome_arquivo)
    )
