# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by *Keep a Changelog*, and this project follows Semantic Versioning.

---

# [1.0.1] - 2026-07-31

## 🇧🇷 Português

## ✨ Novidades

- Adicionado o tipo do documento ao nome final do arquivo.
- Suporte para boletos de acordo (`AC X-Y`).
- Suporte para novas vias de acordo (`NV - AC`).
- Suporte para novas vias de taxa (`NV TAXA DD.MM`).

## 🚀 Melhorias

- Refatoração completa da normalização do nome do condomínio.
- Remoção sucessiva de prefixos como `CONDOMINIO`, `COND.`, `RES.` e similares.
- Sanitização do nome dos arquivos gerados para maior compatibilidade com o Windows.
- Suporte para blocos identificados por uma única letra (ex.: `A`, `B`, `C`).
- Melhor organização interna do código.
- Logs de depuração mais detalhados para facilitar manutenção e diagnóstico.

## 🛠 Correções

- Aprimorada a identificação de blocos e unidades em diferentes layouts.
- Adicionado um mecanismo de fallback para localizar o bloco quando não identificado na leitura principal.
- Preservado o formato original de blocos alfanuméricos (ex.: `06-CO`) no nome do arquivo.
- Melhor compatibilidade com diferentes modelos de boletos em PDF.

---

## 🇺🇸 English

## ✨ New Features

- Added document type identification to generated filenames.
- Added support for agreement payment slips (`AC X-Y`).
- Added support for agreement replacement slips (`NV - AC`).
- Added support for fee replacement slips (`NV TAXA DD.MM`).

## 🚀 Improvements

- Refactored condominium name normalization.
- Improved sequential removal of condominium prefixes (`CONDOMINIO`, `COND.`, `RES.`, etc.).
- Sanitized generated filenames for better Windows compatibility.
- Added support for single-letter block identifiers (e.g. `A`, `B`, `C`).
- Better internal code organization.
- Enhanced debug logging for easier maintenance and troubleshooting.

## 🛠 Fixes

- Improved block and unit detection across different payment slip layouts.
- Added a fallback mechanism to recover block information when not found during the primary extraction.
- Preserved the original formatting of alphanumeric block identifiers (e.g. `06-CO`) in generated filenames.
- Better compatibility with multiple PDF formats.

========================
## [1.0.0] - 2026-07-25

### Added

- Initial public release
- Intelligent document-based file renaming
- Batch processing support
- Dry Run mode
- Configurable application behavior
- Detailed execution logs
- Windows support
- Linux support
- Standalone executables
- English documentation
- Portuguese documentation
- MIT License

### Documentation

- Added bilingual documentation (English and Portuguese)
- Added project banner
- Improved repository organization

---
