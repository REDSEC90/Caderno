# Validação

Define as regras de validação aplicadas a todo registro do SOE-CCG.

---

## Níveis de Validação

### Nível 1 — Metadados

Verificações aplicadas ao frontmatter de qualquer arquivo.

| Regra                                              | Obrigatório |
|----------------------------------------------------|-------------|
| Campo `id` presente e no formato correto           | sim         |
| Campo `tipo` presente e valor reconhecido          | sim         |
| Campo `schema-version` presente                    | sim         |
| Campo `versao` presente e inteiro >= 1             | sim         |
| Campo `status` presente e valor válido             | sim         |
| Campo `criado-em` no formato `YYYY-MM-DD`          | sim         |
| Campo `atualizado-em` no formato `YYYY-MM-DD`      | sim         |
| Campo `autor` presente                             | sim         |

### Nível 2 — Conteúdo

Verificações específicas por tipo de entidade, conforme o esquema correspondente.

| Regra                                              | Obrigatório |
|----------------------------------------------------|-------------|
| Campos obrigatórios do esquema presentes           | sim         |
| Referências a IDs existentes e no formato correto  | sim         |
| Valores de catálogos controlados válidos           | sim         |
| Unidades de medida reconhecidas                    | sim         |

### Nível 3 — Consistência

Verificações de integridade entre registros.

| Regra                                                      | Obrigatório |
|------------------------------------------------------------|-------------|
| `receita-id` em execuções referencia receita existente     | sim         |
| IDs em relacionamentos existem nas respectivas entidades   | sim         |
| `schema-version` compatível com esquema disponível         | sim         |

---

## Comportamento do Importador

- Arquivo inválido no Nível 1: ignorado, erro registrado em log.
- Arquivo inválido no Nível 2: ignorado, erro registrado em log.
- Arquivo inválido no Nível 3: importado com aviso; referência marcada como pendente.

---

## Regra Geral

Validação nunca modifica o arquivo original.

Erros são reportados; a correção é responsabilidade do autor.
