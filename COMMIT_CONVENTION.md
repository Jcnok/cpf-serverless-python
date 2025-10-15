# Convenção de Commits

Para manter um histórico de commits limpo, consistente e fácil de navegar, adotamos o padrão **Conventional Commits**. Este guia descreve como formatar suas mensagens de commit.

## Formato da Mensagem

Cada mensagem de commit deve seguir o seguinte formato:

```
<tipo>(<escopo>): <assunto>

[corpo opcional]

[rodapé opcional]
```

---

### **1. Tipo**

O tipo deve ser um dos seguintes:

*   **feat**: Uma nova funcionalidade (`feature`).
*   **fix**: Uma correção de bug (`bug fix`).
*   **docs**: Alterações na documentação.
*   **style**: Alterações que não afetam o significado do código (espaços em branco, formatação, etc).
*   **refactor**: Uma alteração de código que não corrige um bug nem adiciona uma funcionalidade.
*   **perf**: Uma alteração de código que melhora o desempenho.
*   **test**: Adicionando testes ou corrigindo testes existentes.
*   **chore**: Alterações no processo de build ou em ferramentas auxiliares e bibliotecas, como a geração de documentação.

### **2. Escopo (Opcional)**

O escopo fornece informações contextuais adicionais e deve estar entre parênteses.

*   **Exemplos**: `feat(api):`, `fix(ci):`, `docs(readme):`

### **3. Assunto**

O assunto é uma descrição curta e concisa da alteração:

*   Use o imperativo, tempo presente: "adiciona" em vez de "adicionado" ou "adicionando".
*   Não capitalize a primeira letra.
*   Não coloque ponto final (`.`) no final.

### **4. Corpo (Opcional)**

O corpo é usado para fornecer informações contextuais adicionais sobre a alteração, como a motivação e o contraste com o comportamento anterior.

### **5. Rodapé (Opcional)**

O rodapé é usado para referenciar issues ou Pull Requests do GitHub.

*   **Exemplo**: `Closes #12`

---

## Exemplos Práticos

### Commit Simples
```
feat: Adiciona validação de CNPJ
```

### Commit com Escopo
```
fix(api): Corrige tratamento de erro para CPFs inválidos
```

### Commit com Corpo e Rodapé
```
docs(readme): Melhora a seção de instalação com mais detalhes

Adiciona informações sobre a necessidade de ter o `pyenv` e `poetry`
instalados globalmente, para evitar problemas comuns durante o setup
inicial do projeto.

Closes #15
```
