<p align="center">
  <img src="assets/banner.png" alt="Banner do AutoRename">
</p>

<h1 align="center">AutoRename</h1>

<p align="center">
  <strong>Renomeação Inteligente de Arquivos</strong>
</p>

<p align="center">
  🇺🇸 <a href="README.md">English</a>
</p>

---

## Sobre

O AutoRename é uma ferramenta multiplataforma desenvolvida para automatizar tarefas repetitivas de renomeação de arquivos, extraindo informações diretamente do conteúdo dos documentos.

Em vez de depender apenas do nome original do arquivo, o AutoRename analisa o conteúdo do documento para gerar nomes de arquivos consistentes e significativos, reduzindo o trabalho manual e minimizando erros.

Criado originalmente para resolver fluxos reais de processamento de documentos, o projeto prioriza simplicidade, confiabilidade e eficiência.

A primeira versão pública é focada na renomeação automática de boletos em PDF, servindo como base para futuras expansões através de regras de extração configuráveis.

---

## ✨ Recursos

- 📄 Renomeação inteligente baseada no conteúdo do documento
- 🔍 Extração de informações de PDFs utilizando **pdfplumber**
- 📁 Geração automática de nomes de arquivos
- ⚡ Processamento rápido em lote
- 🛡️ Modo **Dry Run** para testes seguros
- 📝 Logs detalhados de execução
- ⚙️ Comportamento configurável através do `config.ini`
- 💻 Compatível com Windows e Linux
- 📦 Executáveis independentes (standalone)

---

## 📸 Capturas de tela

<p align="center">
<i>

As capturas de tela foram intencionalmente omitidas, pois a aplicação atualmente é utilizada com documentos reais e confidenciais.

Um conjunto de dados de demonstração e capturas públicas poderão ser adicionados em versões futuras.

</i>
</p>

---

## 🚀 Instalação

### Baixar o Executável

Baixe a versão mais recente na página de **Releases**.

### Executar a partir do código-fonte

Antes de executar a aplicação, edite o arquivo `config.ini` e configure a pasta que contém seus documentos PDF.

```bash
git clone https://github.com/Nid2002/AutoRename.git

cd AutoRename

pip install -r requirements.txt

python src/main.py
```

---

## 🛠️ Compilar a partir do código-fonte

O AutoRename utiliza **PyInstaller** para gerar executáveis independentes.

O executável será criado dentro da pasta `dist/`.

```bash
pyinstaller AutoRename.spec
```

---

## 🤝 Contribuindo

Contribuições, sugestões, relatos de bugs e solicitações de novas funcionalidades são sempre bem-vindos.

Sinta-se à vontade para abrir uma *Issue* ou enviar um *Pull Request*.

Se tiver ideias para melhorar o projeto, ficarei feliz em recebê-las.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

Consulte o arquivo **LICENSE** para mais detalhes.
