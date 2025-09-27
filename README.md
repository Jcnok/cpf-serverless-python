# Microsserviço Serverless para Validação de CPF - Azure Functions (Python)
Repositório inicial configurado usando Python 3.8+ (pyenv), Poetry e GitHub. Projeto a ser evoluído com Azure Functions Core Tools!

## Estrutura do projeto:
```
├── src/
│ ├── functions/
│ │ └── cpf_validation/
│ │ ├── init.py
│ │ └── function_app.py
│ ├── core/
│ │ ├── validators/
│ │ ├── models/
│ │ └── utils/
│ └── config/
├── tests/
│ ├── unit/
│ └── integration/
├── docs/
├── .github/
│ └── workflows/
├── scripts/
└── requirements.txt
```
- O projeto segue boas práticas de separação de responsabilidades e organização para Azure Functions e Python.
