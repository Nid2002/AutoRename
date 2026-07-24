from dataclasses import dataclass


@dataclass
class Boleto:

    condominio: str | None = None
    bloco: str | None = None
    unidade: str | None = None
    vencimento: str | None = None

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

        partes = [self.condominio]

        if self.bloco:
            partes.append(self.bloco)

        partes.append(self.unidade)
        partes.append(self.vencimento)

        return " - ".join(partes) + ".pdf"

    def __str__(self):

        partes = [
            f"condominio='{self.condominio}'",
        ]

        if self.bloco:
            partes.append(f"bloco='{self.bloco}'")

        partes.append(f"unidade='{self.unidade}'")
        partes.append(f"vencimento='{self.vencimento}'")

        return "Boleto(" + ", ".join(partes) + ")"
