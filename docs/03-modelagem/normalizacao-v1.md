# Normalização

Define as decisões de normalização do modelo relacional do SOE-CCG.

---

## Forma Normal Alvo

O modelo segue a **Terceira Forma Normal (3FN)**.

---

## Decisões

### Ingredientes, Técnicas e Equipamentos são entidades independentes

Não são duplicados dentro de receitas.

Receitas referenciam essas entidades por ID em tabelas de relacionamento.

### Categorias são entidades independentes

Não são campos de texto livre.

São referenciadas por ID, garantindo consistência e consultabilidade.

### Observações são entidades independentes

Não são campos de texto embutidos em outras entidades.

Referenciam a entidade vinculada por `entidade-id` e `entidade-tipo`.

### Execuções são entidades independentes

Não modificam a Receita original.

Armazenam referência ao ID e à versão da Receita utilizada.

### Metadados não são normalizados separadamente

Campos de metadados (`id`, `versao`, `status`, `criado-em` etc.) residem na própria tabela da entidade.

---

## O que não é normalizado intencionalmente

| Campo             | Motivo                                                      |
|-------------------|-------------------------------------------------------------|
| `modo-de-preparo` | Texto narrativo; não possui estrutura relacional            |
| `notas`           | Texto livre; normalização não agrega valor                  |
| `tags`            | Lista livre; armazenada como texto serializado ou tabela auxiliar |
