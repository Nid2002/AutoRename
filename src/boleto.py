from dataclasses import dataclass
import re


def sanitizar_nome_arquivo(nome: str) -> str:

    nome = re.sub(r'[<>:"/\\|?*]', "", nome)

    return " ".join(nome.split())


@dataclass
class Boleto:

    condominio: str | None = None
    bloco: str | None = None
    unidade: str | None = None
    vencimento: str | None = None
    tipo_documento: str | None = None

    @property
    def completo(self):

        return all([
            self.condominio,
            self.unidade,
            self.vencimento,
        ])

    @property
    def nome_arquivo(self):

        if not self.completo:
            return None

        partes = []

        if self.tipo_documento:
            partes.append(self.tipo_documento)

        partes.append(self.condominio)

        if self.bloco:
            partes.append(self.bloco)

        partes.append(self.unidade)
        partes.append(self.vencimento)

        nome = " - ".join(partes) + ".pdf"

        return sanitizar_nome_arquivo(nome)

    def __str__(self):

        partes = [
            f"condominio='{self.condominio}'",
        ]

        if self.bloco:
            partes.append(f"bloco='{self.bloco}'")

        partes.append(f"unidade='{self.unidade}'")
        partes.append(f"vencimento='{self.vencimento}'")

        if self.tipo_documento:
            partes.append(f"tipo_documento='{self.tipo_documento}'")

        return "Boleto(" + ", ".join(partes) + ")"
