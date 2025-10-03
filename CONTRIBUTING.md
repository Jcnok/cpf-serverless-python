# Guia de Contribuição – cpf-serverless-python

Bem-vindo! Este documento orienta sobre como configurar o ambiente, adotar convenções e contribuir com qualidade para este projeto.

---

## 🛠️ Setup do Ambiente

- **Instale as dependências:**
poetry install --no-root


- **Ative o ambiente virtual Poetry:**
poetry shell


- **Verifique a versão do Python:**
python --version



## ⚙️ Ferramentas e Dependências

- **Dependências base:**  
- `azure-functions`
- `azure-functions-worker`
- `pydantic`
- `cpf-cnpj-validator`

- **Dependências de desenvolvimento:**  
- `pytest` (testes)
- `black` (formatação de código)
- `flake8` (linter)
- `mypy` (type checking)
- `pytest-cov` (cobertura de testes)

## 📝 Checks de Qualidade

Execute antes de abrir PR:

- **Testes:**  
poetry run pytest


- **Formatação Black:**  
poetry run black --check .


- **Lint:**  
poetry run flake8 .


- **Type Check:**  
poetry run mypy .



## 🧹 Observações Importantes

- O projeto possui `.flake8` configurado para ignorar pastas ocultas/ambiente virtual.
- Use sempre `poetry install --no-root` caso não deseje instalar o projeto como pacote Python.
- Mantenha o código na pasta principal do projeto (ex: `src/` ou `cpf_serverless_python/`, conforme padrão).

## 🚀 Fluxo para Pull Requests

1. Crie uma branch referente à issue (ex: `hotfix/22-complementa-dependencias`)
2. Faça commits claros e objetivos (ex: `"feat: validação de CPF"`)
3. Execute todos os checks de qualidade antes de abrir o PR
4. Relacione o PR à Issue correspondente e documente comandos/evidências no PR

## 💡 Dúvidas ou Sugestões?

Contribua ou peça mentoria!  
Contate o responsável pelo repositório ou abra uma discussão na aba "Issues".

---

**Bons commits e bons PRs!**