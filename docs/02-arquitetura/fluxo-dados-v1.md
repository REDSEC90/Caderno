# Fluxo de Dados

Descreve como o conhecimento flui entre as camadas do SOE-CCG.

---

## Camadas

```
Autor
  ↓
Arquivo Markdown (dados/)        ← fonte oficial do conhecimento
  ↓
Importador                       ← lê e valida os arquivos
  ↓
SQLite                           ← mecanismo de consulta derivado
  ↓
Código / API                     ← acesso programático
  ↓
Interface                        ← acesso humano
```

---

## Princípios do Fluxo

- O conhecimento nasce em `dados/` como Markdown.
- O SQLite é sempre derivado. Pode ser descartado e reconstruído.
- Nenhuma informação nasce no banco de dados.
- Nenhuma informação nasce na interface.
- O importador é o único ponto de entrada para o banco.

---

## Fluxo de Criação de um Registro

```
1. Autor copia o template correspondente
2. Preenche os campos conforme o esquema
3. Salva o arquivo em dados/{entidade}/
4. Importador detecta o arquivo novo
5. Importador valida contra o esquema
6. Importador insere no SQLite
```

## Fluxo de Atualização de um Registro

```
1. Autor edita o arquivo Markdown em dados/
2. Incrementa o campo versao nos metadados
3. Atualiza atualizado-em
4. Importador detecta a alteração
5. Importador atualiza o SQLite
```

---

## Reconstrução do Banco

O banco SQLite pode ser completamente reconstruído a partir de `dados/` a qualquer momento, sem perda de informação.
