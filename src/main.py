# main.py

from boleto import Boleto

from config import PASTA_ENTRADA

from constants import (
    APP_NOME,
    APP_VERSAO,
    EXTENSAO_PDF,
    SEPARADOR,
)

from status import ResultadoProcessamento

from extractor import (
    extrair_texto,
    extrair_dados,
)

from renamer import Renamer

from validator import arquivo_ja_renomeado

from logger import (
    iniciar_log,
    finalizar_log,
    registrar_info,
    registrar_processamento,
    registrar_ignorado,
    registrar_excecao,
)

renamer = Renamer()


# ======================================================
# PROCESSA UM ÚNICO PDF
# ======================================================

def processar_pdf(pdf):
    """
    Processa um único PDF.
    """

    if arquivo_ja_renomeado(pdf.name):

        registrar_ignorado(pdf.name)

        return ResultadoProcessamento.IGNORADO

    boleto = None

    try:

        #
        # Extração
        #

        texto = extrair_texto(pdf)

        boleto = extrair_dados(texto)

        #
        # Renomeação
        #

        novo_pdf = renamer.renomear(pdf, boleto)

        #
        # Não conseguiu renomear
        #

        if novo_pdf is None:

            registrar_processamento(
                arquivo=pdf.name,
                boleto=boleto,
                status="ERRO",
                motivo="Falha ao renomear o arquivo.",
            )

            return ResultadoProcessamento.ERRO

        #
        # Sucesso
        #

        registrar_processamento(
            arquivo=pdf.name,
            boleto=boleto,
            status="RENOMEADO",
            novo_nome=novo_pdf.name,
        )

        return ResultadoProcessamento.RENOMEADO

    #
    # Arquivo aberto por outro programa
    #

    except PermissionError:

        registrar_processamento(
            arquivo=pdf.name,
            boleto=boleto or Boleto(),
            status="ERRO",
            motivo="O arquivo está aberto em outro programa.",
        )

        return ResultadoProcessamento.ERRO

    #
    # Qualquer outro erro inesperado
    #

    except Exception as erro:

        registrar_processamento(
            arquivo=pdf.name,
            boleto=boleto or Boleto(),
            status="EXCEÇÃO",
            motivo=str(erro),
        )

        registrar_excecao(pdf.name)

        return ResultadoProcessamento.ERRO


# ======================================================
# PROGRAMA PRINCIPAL
# ======================================================

def main():

    iniciar_log()

    arquivos = sorted(
        PASTA_ENTRADA.glob(EXTENSAO_PDF)
    )

    if not arquivos:
        print("Nenhum PDF encontrado.")
        
        registrar_info("Nenhum PDF encontrado.")

        finalizar_log()

        return

    total = len(arquivos)

    renomeados = 0
    ignorados = 0
    erros = 0

    for pdf in arquivos:

        resultado = processar_pdf(pdf)

        if resultado == ResultadoProcessamento.RENOMEADO:
            renomeados += 1

        elif resultado == ResultadoProcessamento.IGNORADO:
            ignorados += 1

        elif resultado == ResultadoProcessamento.ERRO:
            erros += 1

    resumo = (
        f"\n{SEPARADOR}\n"
        "RESUMO DA EXECUÇÃO\n"
        f"{SEPARADOR}\n"
        f"PDFs encontrados : {total}\n"
        f"Renomeados       : {renomeados}\n"
        f"Ignorados        : {ignorados}\n"
        f"Erros            : {erros}\n"
        f"{SEPARADOR}"
    )

    print(resumo)

    registrar_info(resumo)

    finalizar_log()


if __name__ == "__main__":
    main()
