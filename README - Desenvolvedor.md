# AutoRename Phoenix

**Versão:** 1.0.0  
**Codename:** Phoenix

AutoRename Phoenix é uma ferramenta desenvolvida para renomear automaticamente boletos de faturas condominais em PDF utilizando informações extraídas do próprio documento.

O objetivo é eliminar o trabalho manual de renomeação, padronizando os arquivos de forma rápida e confiável.

---

## Recursos

- Extração automática do condomínio
- Extração automática do bloco (quando existir)
- Extração automática da unidade
- Extração automática do vencimento
- Sistema de aliases para nomes de condomínios
- Configuração externa via `config.ini`
- Modo DEBUG para diagnóstico
- Geração automática de logs
- Compatível com Windows

---

## Estrutura do projeto

```
AutoRename/
│
├── src/
├── config.py
├── config.ini
├── README.md
├── build.bat
├── AutoRename.spec
└── icon.ico
```

---

## Tecnologias

- Python 3.12
- pdfplumber
- pathlib
- configparser
- PyInstaller

---

## Como executar durante o desenvolvimento

```bash
python src/main.py
```

---

## Gerando o executável

Execute:

```bash
build.bat
```

Ao finalizar será criada automaticamente a pasta:

```
Release/
```

pronta para distribuição.

---

## Estrutura da Release

```
Release/

AutoRename.exe

config.ini

Entrada/

Logs/

README.txt
```

---

## Configuração

Todas as configurações ficam em:

```
config.ini
```

Não é necessário recompilar o programa para alterar:

- pastas
- aliases
- debug
- dry-run

---

## Logs

Todos os processamentos ficam registrados em:

```
Logs/autorename.log
```

Quando o DEBUG estiver habilitado também serão registradas todas as etapas da extração.

---

## Licença

Uso interno.

---

## Autor

Nicolas Alves Oliveira

AutoRename Phoenix © 2026
