# Guia de Contribuição

Ficamos muito felizes com o seu interesse em contribuir para este projeto! Para garantir um ambiente colaborativo e organizado, criamos este guia com os passos e padrões que seguimos.

## 🚀 Começando

### 1. Configure o Ambiente de Desenvolvimento

Para começar, você precisará configurar seu ambiente local. Siga os passos abaixo:

1.  **Fork e Clone o Repositório**:
    *   Faça um **fork** deste repositório para a sua conta do GitHub.
    *   Clone o seu fork localmente:
        ```bash
        git clone https://github.com/SEU-USUARIO/cpf-serverless-python.git
        cd cpf-serverless-python
        ```

2.  **Instale as Ferramentas e Dependências**:
    *   Este projeto utiliza `pyenv` para gerenciar a versão do Python e `poetry` para as dependências. Certifique-se de que ambos estão instalados.
    *   Instale a versão correta do Python e as dependências do projeto:
        ```bash
        pyenv install $(cat .python-version)
        poetry install
        ```

3.  **Execute a Aplicação Localmente**:
    *   Para iniciar o ambiente local do Azure Functions, execute:
        ```bash
        func start
        ```
    *   O endpoint estará disponível em `http://localhost:7071/api/validate-cpf`.

### 2. Estratégia de Branches

Utilizamos um padrão simples para a nomenclatura de branches, baseado no tipo de alteração que você está fazendo. Isso nos ajuda a manter o repositório organizado.

*   **features**: `feature/nome-da-feature` (ex: `feature/add-cnpj-validation`)
*   **bug fixes**: `fix/descricao-do-bug` (ex: `fix/adjust-rate-limiter`)
*   **documentação**: `docs/tema-da-documentacao` (ex: `docs/update-readme`)
*   **outras tarefas**: `chore/descricao-da-tarefa` (ex: `chore/update-dependencies`)

### 3. Fluxo de Trabalho para Contribuições

1.  **Crie uma nova branch** a partir da `main`, seguindo a convenção de nomenclatura descrita acima.
    ```bash
    git checkout -b feature/sua-nova-feature
    ```

2.  **Faça suas alterações** no código.

3.  **Valide suas alterações localmente** antes de fazer o commit. Temos um script que roda todas as verifições de uma só vez (formatação, linting e testes):
    ```bash
    ./scripts/run-checks.sh
    ```

4.  **Faça o commit das suas alterações**. É muito importante que suas mensagens de commit sigam a nossa **Convenção de Commits**. Veja o documento [COMMIT_CONVENTION.md](COMMIT_CONVENTION.md) para mais detalhes.
    ```bash
    git commit -m "feat: Adiciona nova funcionalidade X"
    ```

5.  **Envie suas alterações** para o seu fork:
    ```bash
    git push origin feature/sua-nova-feature
    ```

6.  **Abra um Pull Request (PR)** no repositório original, com a `main` como branch de destino. Preencha o template do PR com as informações solicitadas.

### 4. Revisão e Merge

*   Seu PR será revisado por um dos mantenedores do projeto. Fique atento a possíveis feedbacks ou pedidos de alteração.
*   Após a aprovação, seu PR será integrado à branch `main` utilizando o método **"Squash and Merge"**. Isso agrupa todos os commits do seu PR em um único commit, mantendo o histórico da `main` limpo e organizado.

Agradecemos novamente pela sua contribuição!
