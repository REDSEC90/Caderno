# Importação

Define como arquivos Markdown de `dados/` são processados e inseridos no SQLite.

---

## Responsabilidade do Importador

- Ler arquivos Markdown de `dados/`.
- Validar metadados obrigatórios conforme o esquema correspondente.
- Validar valores contra catálogos controlados.
- Inserir ou atualizar registros no SQLite.
- Registrar erros sem interromper o processamento dos demais arquivos.

---

## Fluxo de Importação

```
1. Varrer dados/ recursivamente
2. Para cada arquivo .md encontrado:
   a. Ler frontmatter (metadados)
   b. Identificar tipo e schema-version
   c. Carregar esquema correspondente
   d. Validar campos obrigatórios
   e. Validar valores de catálogos
   f. Inserir ou atualizar no SQLite
   g. Registrar resultado (sucesso ou erro)
```

---

## Regras

- O importador nunca modifica os arquivos Markdown.
- Erros de validação são registrados em log; o arquivo é ignorado naquele ciclo.
- Um arquivo com `id` já existente no banco tem seu registro atualizado, não duplicado.
- A reconstrução completa do banco a partir de `dados/` deve produzir resultado idêntico.

---

## Dados de Entrada

Arquivos `.md` com frontmatter YAML localizado em:

```
dados/receitas/
dados/execucoes/
dados/ingredientes/
dados/tecnicas/
dados/equipamentos/
dados/observacoes/
dados/experimentos/
```

## Dados de Saída

Tabelas no banco SQLite em `banco_de_dados/sqlite/`.
