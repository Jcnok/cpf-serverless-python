Aqui está o modelo revisado e ajustado para o arquivo `CONTRIBUTING.md`, atualizado conforme as práticas do seu projeto e as mudanças recentes:

***

# Guia de Contribuição – cpf-serverless-python

Bem-vindo! Este documento orienta como configurar o ambiente local, seguir convenções e contribuir com qualidade para este microsserviço serverless para validação de CPF em Azure Functions.

***

## 🛠️ Setup do Ambiente

### Pré-requisitos

Antes de iniciar o desenvolvimento, garanta que estas ferramentas estejam instaladas:

- **Python 3.12**
- **Poetry** (gerenciamento de dependências)
- **Azure CLI** (para deploy e gerenciamento no Azure)
- **Azure Functions Core Tools** (execução local de Functions)
- Opcional: **pyenv** (para gerenciar múltiplas versões Python)

Para instruções detalhadas de instalação e setup, consulte o README do projeto.

***

### Instalação das Dependências

```bash
poetry install --no-root
poetry shell
python --version
```

***

### Validação do Ambiente Azure

Após configurar as ferramentas Azure, valide a instalação:

```bash
az --version
func --version
az account show
```

***

### Estrutura do Projeto

- Suas funções devem estar organizadas na pasta `cpf_validation/` na raiz do projeto.
- Siga os padrões descritos no README e mantenha clareza na estrutura, nomenclatura e separação de módulos.

***

## ⚙️ Dependências e Ferramentas

- Principais: `azure-functions`, `pydantic`, `pycpfcnpj`
- Dev: `pytest`, `pytest-cov`, `black`, `flake8`, `mypy`

As dependências de produção devem estar sempre no `requirements.txt` (atualizado via poetry export quando necessário).  
As dependências de desenvolvimento vão no `pyproject.toml`.

***

## 📝 Checks de Qualidade (antes do PR)

Execute antes de abrir Pull Request:

- Testes unitários
  ```bash
  poetry run pytest
  ```
- Formatação Black
  ```bash
  poetry run black --check .
  ```
- Lint Flake8
  ```bash
  poetry run flake8 .
  ```
- Type Check Mypy
  ```bash
  poetry run mypy .
  ```

Para rodar todos de uma vez (exemplo):
```bash
poetry run black --check . && poetry run flake8 . && poetry run mypy . && poetry run pytest
```

***

## 🚀 Fluxo para Pull Requests

1. Crie uma branch específica da issue (ex: `feat/validacao-cpf`)
2. Faça commits claros e siga convenções de mensagem (vide abaixo)
3. Execute todos os checks de qualidade antes do PR
4. Relacione o PR à Issue correspondente, explique as alterações, adicione evidências/prints se relevante
5. Aguarde revisão e responda feedbacks

### Convenção de Commits

Utilize [Conventional Commits](https://www.conventionalcommits.org/) para clareza:

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alteração na documentação
- `test:` Novos testes
- `refactor:` Refatoração
- `ci:` Mudanças no CI/CD
- `chore:` Tarefas de manutenção

***

## 🧙 Observações Importantes

- Faça sempre os testes automatizados; o workflow do GitHub Actions irá impedir deploy caso algo falhe.
- Use sempre `poetry install --no-root` para instalar dependências (não empacotar).
- O deploy é feito automaticamente via CI/CD (usando `requirements.txt`), basta manter o arquivo atualizado.
- Segredos ou variáveis sensíveis devem ser configurados **exclusivamente no portal Azure**, nunca no código ou no repositório.

***

## 📚 Recursos Úteis

- [Documentação do Azure Functions (Python)](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Poetry Docs](https://python-poetry.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black](https://black.readthedocs.io/)
- [Flake8](https://flake8.pycqa.org/)
- [pytest](https://docs.pytest.org/en/stable/)
- [pycpfcnpj](https://pypi.org/project/pycpfcnpj/)

***

## 💡 Dúvidas ou Sugestões?

Abra uma *Issue*, um *Pull Request* ou discuta na aba Discussions.

**Contribua! Bom código e bons PRs!**

[1](https://github.com/Jcnok/cpf-serverless-python)