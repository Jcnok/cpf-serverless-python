# Microsserviço Serverless para Validação de CPF – Azure Functions (Python)

Repositório para desenvolvimento de microsserviço serverless destinado à validação de CPF, utilizando **Azure Functions** e ambiente Python moderno.

---

## 🚀 Visão Geral

- Projeto desenvolvido em **Python 3.8+** (preferencialmente gerenciado com `pyenv`)
- Gerenciamento de dependências com **Poetry**
- Infraestrutura preparada para **Azure Functions Core Tools**
- Estrutura modular e escalável, seguindo boas práticas de separação de responsabilidades

---

## 🗂️ Estrutura do Projeto

```
├── src/
│   ├── functions/
│   │   └── cpf_validation/
│   │       ├── __init__.py
│   │       └── function_app.py
│   ├── core/
│   │   ├── validators/
│   │   ├── models/
│   │   └── utils/
│   └── config/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── .github/
│   └── workflows/
├── scripts/
└── requirements.txt
```
- **src/**: Código principal da aplicação
- **tests/**: Testes unitários e de integração
- **docs/**: Documentação técnica e de produto
- **.github/workflows/**: Automação CI/CD (actions, workflows)
- **scripts/**: Utilitários e ferramentas auxiliares
- **requirements.txt**: Alternativa para ambientes sem Poetry

---

## ⚙️ Como Rodar o Projeto

1. **Clone o repositório:**
   ```
   git clone https://github.com/Jcnok/cpf-serverless-python.git
   cd cpf-serverless-python
   ```

2. **Configure o ambiente Python:**
   - Recomenda-se usar `pyenv` para gerenciar versões do Python

3. **Instale as dependências:**
   ```
   poetry install --no-root
   ```

4. **Ative o ambiente virtual:**
   ```
   poetry shell
   ```

---

## 🧪 Checks, Testes e Qualidade

- **Rodar testes automatizados:**
  ```
  poetry run pytest
  ```

- **Checar estilo de código (Black):**
  ```
  poetry run black --check .
  ```

- **Linting (Flake8):**
  ```
  poetry run flake8 .
  ```

- **Type Checking (Mypy):**
  ```
  poetry run mypy .
  ```

---

## 📝 Documentação e Contribuição

- Para instruções completas de setup, convenções e guidelines de contribuição, consulte o arquivo [CONTRIBUTING.md](./CONTRIBUTING.md).
- Toda nova contribuição deve ser precedida de testes, checagem de qualidade e Pull Request vinculado à issue correspondente.

---

## ☁️ Deploy Serverless (Azure)

- Em breve: Guia detalhado de deploy utilizando Azure Functions Core Tools e workflows de CI/CD no GitHub Actions.

---

## 📚 Referências

- [Documentação Azure Functions](https://docs.microsoft.com/azure/azure-functions/)
- [Documentação Poetry](https://python-poetry.org/docs/)
- [Validador CPF/CNPJ](https://pypi.org/project/cpf-cnpj-validator/)

---

## 👤 Autor
- **Julio Okuda**  
  [LinkedIn](https://www.linkedin.com/in/julio-okuda/) • [GitHub](https://github.com/Jcnok)

---

> Para dúvidas, contribuições ou sugestões, abra uma Issue ou consulte o arquivo de contribuição!
```
