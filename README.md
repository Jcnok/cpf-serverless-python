# Microsserviço Serverless para Validação de CPF – Azure Functions (Python)

[![CI/CD Status](https://github.com/Jcnok/cpf-serverless-python/actions/workflows/deploy.yml/badge.svg)](https://github.com/Jcnok/cpf-serverless-python/actions/workflows/deploy.yml)

Microsserviço serverless para validação de CPF via Azure Functions (Python). Com estrutura moderna, dependências por Poetry ou requirements.txt, testes automatizados, CI/CD e deploy fácil no Azure.

***

## 🚀 Visão Geral

Este projeto oferece um microsserviço serverless robusto e escalável para a validação de CPFs brasileiros, construído com Python 3.12 e implantado no ambiente do Azure Functions. Ele foi projetado com foco em boas práticas de engenharia de software, incluindo uma arquitetura modular, gerenciamento de dependências com Poetry, e um pipeline de CI/CD totalmente automatizado com GitHub Actions, que garante a qualidade e a integridade do código a cada alteração.

## ✨ Funcionalidades

- **Validação de CPF**: O endpoint principal valida CPFs com e sem formatação, utilizando a biblioteca `pycpfcnpj` para garantir a precisão.
- **Rate Limiting**: Um limitador de requisições baseado em IP previne abusos, garantindo a disponibilidade do serviço (10 requisições por minuto).
- **Tratamento de Erros Estruturado**: Respostas de erro claras e consistentes para requisições malformadas, CPFs inválidos e outros cenários de falha.
- **CI/CD Automatizado**: O pipeline de integração contínua executa testes, verifica a formatação do código e faz o deploy automaticamente para o Azure a cada push na branch `main`.
- **Cobertura de Testes**: O projeto mantém uma cobertura de testes de 100%, assegurando a confiabilidade da lógica de negócios.

***

## 🗂️ Estrutura do Projeto

| Arquivo/Diretório | Descrição |
|---|---|
| `cpf_validation/` | Contém o código-fonte da Azure Function. O `__init__.py` é o ponto de entrada da função, e o `function.json` define seus gatilhos e bindings. |
| `src/core/` | Abriga a lógica de negócios e os componentes compartilhados da aplicação. |
| `src/core/models/` | Modelos de dados Pydantic (`http_models.py`) que garantem a validação e a consistência das requisições e respostas. |
| `src/core/utils/` | Módulos utilitários, como o logger (`logger.py`) e o limitador de requisições (`rate_limiter.py`). |
| `tests/` | Contém os testes automatizados. Os testes unitários ficam em `tests/unit`. |
| `.github/workflows/` | Arquivos de workflow do GitHub Actions para o pipeline de CI/CD. |
| `pyproject.toml` | Arquivo de configuração do Poetry, que gerencia as dependências do projeto e as configurações de ferramentas como o `pytest`. |
| `host.json` | Arquivo de configuração do host do Azure Functions, onde são definidas configurações globais como `logging` e `functionTimeout`. |
| `requirements.txt` | Lista de dependências de produção, gerada a partir do `poetry.lock`, utilizada pelo Azure Functions durante o deploy. |

***

## ⚙️ Execução Local

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Jcnok/cpf-serverless-python.git
   cd cpf-serverless-python
   ```

2. **Configure o ambiente Python**
   ```bash
   pip install -r requirements.txt
   # ou
   poetry install
   ```

3. **Rode o Azure Functions local**
   ```bash
   func start
   ```
   O endpoint estará disponível:
   ```
   http://localhost:7071/api/validate-cpf
   ```

***

## 🧪 Teste do Endpoint

**Via cURL/local:**
```bash
curl -X POST http://localhost:7071/api/validate-cpf \
  -H "Content-Type: application/json" \
  -d '{"cpf": "11144477735"}'
```

**Via Postman/Insomnia:**
- Método: POST
- URL: http://localhost:7071/api/validate-cpf
- Body (JSON):
  ```json
  {
    "cpf": "11144477735"
  }
  ```

***

## 📝 Deploy para Azure Functions

1. **Autentique**
   ```bash
   az login
   ```

2. **Crie recursos**
   ```bash
   az group create --name meu-grupo-cpf --location brazilsouth

   az storage account create --name cpfstorageSEUNOME2025 --location brazilsouth --resource-group meu-grupo-cpf --sku Standard_LRS
   
   az functionapp create --resource-group meu-grupo-cpf --consumption-plan-location brazilsouth --name cpf-function-seunome2025 --storage-account cpfstorageSEUNOME2025 --runtime python --runtime-version 3.12 --functions-version 4 --os-type Linux
   ```

3. **Deploy**
   ```bash
   func azure functionapp publish cpf-function-seunome2025 --python
   ```

***

## 🌐 Testes no Azure

> O endpoint público estará em  
> `https://cpf-function-seunome2025.azurewebsites.net/api/validate-cpf`

### **Via portal Azure**
- Teste na aba "Funções" > "Testar/Executar"
- Certifique-se de que CORS esteja habilitado (veja [abaixo])

### **Via cURL/Postman (CLOUD):**
Atenção: O endpoint **exige key** (authLevel padrão):

1. No portal Azure, copie a Function Key (aba "Gerenciar chave" na função).
2. Use:
   ```bash
   curl -X POST "https://cpf-function-seunome2025.azurewebsites.net/api/validate-cpf?code=SUA_CHAVE_AQUI" \
     -H "Content-Type: application/json" \
     -d '{"cpf": "11144477735"}'
   ```
3. Se quiser acesso público **(não recomendado para produção):**
   - Edite `authLevel` em `function.json` para `"anonymous"`
   - Faça o redeploy.

***

## 🔒 CORS no Azure

Se precisar testar pelo portal Azure (UI):
```bash
az functionapp cors add --name cpf-function-seunome2025 --resource-group meu-grupo-cpf --allowed-origins https://portal.azure.com
```
Ou configure via portal Azure > "Configurações" > "CORS" adicionando o domínio.

***

## 🧰 Troubleshooting

- **Erro 401:** Requisição precisa de function key. Adicione `?code=SUA_CHAVE`.
- **Erro de import (`ModuleNotFoundError: src`)**  
  Garanta que no início de `cpf_validation/__init__.py` tenha:
  ```python
  import sys, os
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
  ```
- **Deploy enviando arquivos desnecessários:**  
  Utilize `.funcignore` com:
  ```
  .flake8
  .python-version
  README.md
  README-bk.md
  pyproject.toml
  poetry.lock
  .coverage
  oryx-manifest.toml
  tests/
  ```
- **Função não aparece após deploy:**  
  Certifique-se de que está rodando/publishing na raiz (`cpf-serverless-python`), com a pasta da função presente na raiz.

- **Payload inválido:**  
  Sempre envie:
  ```json
  { "cpf": "11144477735" }
  ```
  no corpo da requisição.

  ### Atenção sobre modo somente leitura (`WEBSITE_RUN_FROM_PACKAGE`)

Após deploy via CI/CD (GitHub Actions, Azure CLI) o Azure Functions ativa o parâmetro `WEBSITE_RUN_FROM_PACKAGE`, e o aplicativo roda diretamente de um pacote ZIP — ficando em **modo somente leitura**.

- **Não é possível editar arquivos pelo portal Azure após o deploy.**
- Qualquer alteração ou atualização deve ser feita via novo deploy/pipeline.
- Para edições urgentes/hotfix locais, remova temporariamente esse parâmetro nas Configurações do aplicativo, entendendo que ele será restaurado no próximo publish.

> Para produção: mantenha esse parâmetro ativado!

***

## ✅ Todo

- Validar acesso via function key e via portal Azure.
- Atualizar sempre o README.md conforme ajustes.
- Automatizar testes após deploy na CI/CD.

***

***

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

***

> Para dúvidas, contribuições ou sugestões, abra uma [Issue](https://github.com/Jcnok/cpf-serverless-python/issues).

