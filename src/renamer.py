from pathlib import Path

from config import DRY_RUN

from debug import debug


class Renamer:

    def renomear(self, caminho_pdf, boleto):
        """
        Renomeia o PDF utilizando os dados do boleto.
        Retorna o novo caminho do arquivo ou None em caso de erro.
        """

        if not boleto.completo:

            debug("Renomeação cancelada: boleto incompleto.")

            return None

        caminho_pdf = Path(caminho_pdf)

        novo_caminho = caminho_pdf.with_name(
            boleto.nome_arquivo
        )

        debug(f"Nome gerado.....: {novo_caminho.name}")

        if DRY_RUN:

            print()
            print("=== DRY RUN ===")
            print(caminho_pdf.name)
            print("↓")
            print(novo_caminho.name)

            return novo_caminho

        try:

            caminho_pdf.rename(novo_caminho)

            debug(f"Arquivo renomeado: {novo_caminho.name}")

            return novo_caminho

        except Exception as erro:

            debug(f"Falha ao renomear: {erro}")

            return None
