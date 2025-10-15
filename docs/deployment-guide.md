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

## Checklist de Deploy

- [x] **Testes passam com Poetry**
- [x] **requirements.txt atualizado**
- [x] **Secret AZURE_CREDENTIALS configurado no GitHub**
- [x] **app-name no workflow preenchido corretamente**
- [x] **Configurações sensíveis (Key/API Secrets) só no portal Azure**

