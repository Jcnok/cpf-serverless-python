# Guia de Deploy Automatizado

Este documento explica o processo de **deploy CI/CD** da aplicação de validação de CPF para Azure Functions, usando autenticação profissional via Service Principal (`secrets.AZURE_CREDENTIALS`) e GitHub Actions.

***

## Visão Geral do Pipeline

O deploy é realizado automaticamente por um **workflow do GitHub Actions** definido em `.github/workflows/deploy.yml`.  
A pipeline executa testes automatizados (com Poetry) e publica a aplicação na Azure Functions usando o `requirements.txt`, **apenas se todos os testes passarem**.

***

## Funcionamento do Workflow

- **Testes:** Executados com Poetry antes de qualquer deploy.
- **Deploy:** Usando o Action oficial do Azure, autenticado via Service Principal configurado em `AZURE_CREDENTIALS`.

### Resumo das Etapas

1. **`test`**
   - Instala dependências com Poetry
   - Roda toda a suíte de testes

2. **`deploy`**
   - Autentica via Azure Service Principal (`secrets.AZURE_CREDENTIALS`)
   - Publica o conteúdo do projeto para o Azure Functions usando `requirements.txt`

***

## Autenticação: Gerando o Service Principal e Configurando o Secret

### 1. Criar Service Principal no Azure

Execute no terminal:
```bash
az ad sp create-for-rbac --name "github-actions-deploy-cpf-func" --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.Web/sites/<FUNCTION_APP_NAME> \
  --sdk-auth
```
**Substitua:**
- `<SUBSCRIPTION_ID>` pelo ID da sua assinatura Azure
- `<RESOURCE_GROUP>` pelo grupo de recursos
- `<FUNCTION_APP_NAME>` pelo nome da sua Function App

O comando irá gerar um JSON `AZURE_CREDENTIALS` similar a:
```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  "activeDirectoryEndpointUrl": "...",
  "resourceManagerEndpointUrl": "...",
  "activeDirectoryGraphResourceId": "...",
  "sqlManagementEndpointUrl": "...",
  "galleryEndpointUrl": "...",
  "managementEndpointUrl": "..."
}
```

### 2. Adicionar o Secret no GitHub

1. No repositório, acesse **Settings > Secrets and variables > Actions**
2. Clique em **New repository secret**
3. Nomeie como `AZURE_CREDENTIALS`
4. Cole o JSON gerado no campo de valor
5. Salve

***

## Configuração do Workflow (`.github/workflows/deploy.yml`)

Exemplo de workflow enxuto para seu cenário:

```yaml
name: CI/CD Azure Functions (Poetry + requirements.txt)

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout código
        uses: actions/checkout@v3
      - name: Instalar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Instalar Poetry
        run: curl -sSL https://install.python-poetry.org | python3 -
      - name: Instalar dependências
        run: poetry install --no-interaction --no-root
      - name: Rodar testes
        run: poetry run pytest --cov=src --cov-fail-under=90

  deploy:
    if: github.ref == 'refs/heads/master'
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout código
        uses: actions/checkout@v3
      - name: Login Azure (Service Principal)
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Deploy para Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: 'cpf-function-seunome2025' # Nome exato da sua Function App!
          package: '.'
```

***

## Observações Importantes

- O build remoto do Azure Functions **usa o requirements.txt** para instalar todas as dependências.
- Mantenha o requirements.txt sempre atualizado (gere via Poetry se o projeto evoluir).
- Secrets nunca devem ser versionados ou expostos no repositório!
- O Service Principal deve ter permissão mínima necessária (usando escopo do resource group ou especificamente da Function App).

***

Aqui está o modelo atualizado para seu `docs/deployment-guide.md`, já incluindo toda a explicação sobre o parâmetro `WEBSITE_RUN_FROM_PACKAGE` — pronto para copiar e colar:

***

# Guia de Deploy Automatizado

Este documento explica, em detalhes, o processo de deploy CI/CD deste microsserviço serverless para validação de CPF na Azure Functions, incluindo autenticação via Service Principal e o tratamento do parâmetro `WEBSITE_RUN_FROM_PACKAGE`.

***

## Visão Geral do Pipeline

O deploy é realizado via workflow no GitHub Actions, responsável por executar os testes automatizados (usando Poetry) e, em seguida, publicar na Azure Functions usando o arquivo `requirements.txt`, somente quando os testes passam.

- **Autenticação:** Service Principal configurado como `AZURE_CREDENTIALS`
- **Deploy:** Action oficial do Azure Functions, utiliza `requirements.txt` para instalar dependências

***

## Funcionamento do Workflow

### 1. Teste

- Instala dependências com Poetry (`poetry install --no-root`)
- Roda testes (`poetry run pytest ...`)

### 2. Deploy

- Faz login na Azure via Service Principal
- Realiza o deploy da aplicação com `requirements.txt` pelo action oficial

Exemplo resumido do workflow:

```yaml
jobs:
  test:
    ...
    - run: poetry install --no-root
    - run: poetry run pytest --cov=src --cov-fail-under=90
  deploy:
    ...
    - uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    - uses: Azure/functions-action@v1
      with:
        app-name: 'cpf-function-seunome2025'
        package: '.'
```

***

## Atenção sobre `WEBSITE_RUN_FROM_PACKAGE`

Durante o deploy via GitHub Actions/Azure CLI, o parâmetro `WEBSITE_RUN_FROM_PACKAGE` é ativado por padrão.

**O que significa:**

- O app roda diretamente de um pacote ZIP — sistema de arquivos em **modo somente leitura**.
- Não é possível editar código ou arquivos pelo portal Azure.

**Implicações:**

- Todas as atualizações devem ser feitas via novo deploy.
- Garante integridade e segurança (sem risco de alterações pós-deploy).
- Fica fácil realizar rollback e controle de versão.

**Edição rápido via portal:**

- Se for necessário editar arquivos pelo portal Azure (ex: hotfix ou teste pontual), remova temporariamente o parâmetro `WEBSITE_RUN_FROM_PACKAGE`:
  - No portal Azure:  
    - Acesse Function App > Configuração > Configurações do aplicativo.
    - Localize `WEBSITE_RUN_FROM_PACKAGE` e remova.
    - Salve as alterações.
  - Ou via CLI:
    ```bash
    az functionapp config appsettings delete \
      --name cpf-function-seunome2025 \
      --resource-group meu-resource-group \
      --setting-names WEBSITE_RUN_FROM_PACKAGE
    ```
- **Atenção:** Ao publicar novamente via CI/CD/pipeline, o parâmetro será restaurado e a Function voltará ao modo somente leitura.

***

## Checklist de Deploy

- [x] Testes passam com Poetry
- [x] requirements.txt atualizado na raiz
- [x] Secret AZURE_CREDENTIALS configurado
- [x] Nome correto do app no workflow
- [x] Variáveis sensíveis só configuradas via portal Azure
- [x] Entendimento do modo de leitura do pacote (`WEBSITE_RUN_FROM_PACKAGE`)

***
