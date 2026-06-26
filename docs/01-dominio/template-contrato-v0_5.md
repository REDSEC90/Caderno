# Template Canônico de Contrato de Entidade

> Modelo formal que define o contrato de comportamento de cada entidade do SOE-CCG.
> O contrato é a especificação vinculante que toda implementação deve respeitar.

---

## O que é um Contrato

O contrato de uma entidade define formalmente o que o sistema **garante** sobre ela:
quais dados são aceitos, quais são rejeitados, o que acontece em cada operação e quais condições devem ser verdadeiras sempre.

Um contrato não descreve como implementar — descreve o que qualquer implementação deve garantir.

---

## Estrutura do Contrato

---

### 1. Identificação

**Entidade:** [Nome]
**Versão do contrato:** v1
**Esquema associado:** `docs/01-dominio/esquemas/esquema-[entidade]-v1.md`
**Especificação associada:** `docs/01-dominio/especificacao-[entidade].md`

---

### 2. Campos Obrigatórios

> O sistema deve rejeitar qualquer Registro que não contenha estes campos com valores válidos.

| Campo | Tipo | Restrição | Mensagem de erro se ausente |
|-------|------|-----------|----------------------------|
| `id` | string | `[PREFIXO]-NNNNNN` | "ID ausente ou em formato inválido" |
| `tipo` | string | valor fixo: `[tipo]` | "Tipo de entidade inválido" |
| `schema-version` | integer | ≥ 1 | "Versão de esquema ausente" |
| `versao` | integer | ≥ 1 | "Versão do registro ausente" |
| `status` | string | enum definido | "Status inválido ou ausente" |
| `criado-em` | date | `YYYY-MM-DD` | "Data de criação ausente ou inválida" |
| `atualizado-em` | date | `YYYY-MM-DD` | "Data de atualização ausente ou inválida" |
| `autor` | string | não vazio | "Autor ausente" |
| [campos específicos] | | | |

---

### 3. Campos Opcionais

> O sistema deve aceitar estes campos quando presentes, mas não exigi-los.

| Campo | Tipo | Restrição | Comportamento se ausente |
|-------|------|-----------|--------------------------|
| `tags` | list | minúsculas, hífens | Tratado como lista vazia |
| `origem` | string | — | Tratado como null |
| [campos específicos] | | | |

---

### 4. Valores Aceitos por Campo

> Enumeração completa dos valores válidos para campos com domínio restrito.

**`status`:**
```
[lista de valores válidos]
```

**`[outro campo com enum]`:**
```
[lista de valores válidos]
```

---

### 5. Pré-condições por Operação

> O que deve ser verdadeiro **antes** de cada operação ser executada.

**Criar:**
- [ ] `id` não deve existir no sistema (unicidade)
- [ ] Todos os campos obrigatórios devem estar presentes
- [ ] Todos os IDs referenciados devem existir
- [ ] `schema-version` deve ser uma versão de esquema conhecida

**Atualizar:**
- [ ] O Registro deve existir
- [ ] O Registro não deve estar em estado `arquivado` ou `obsoleto`
- [ ] `id` não pode ser alterado
- [ ] `criado-em` não pode ser alterado
- [ ] `atualizado-em` deve ser igual ou posterior à data anterior

**Arquivar:**
- [ ] O Registro deve existir
- [ ] O Registro deve estar em estado compatível com arquivamento

**Restaurar (arquivado → ativo):**
- [ ] O Registro deve estar em estado `arquivado`
- [ ] Nenhum conflito com Registros ativos

---

### 6. Pós-condições por Operação

> O que deve ser verdadeiro **depois** de cada operação executada com sucesso.

**Criar:**
- [ ] Registro existe em `dados/[entidade]/[id].md`
- [ ] Registro existe no SQLite com os mesmos dados
- [ ] `historico_estados` contém entrada de criação
- [ ] `id` é único no sistema

**Atualizar:**
- [ ] `atualizado-em` foi incrementado
- [ ] Versão anterior é recuperável via git
- [ ] SQLite reflete os novos valores

**Arquivar:**
- [ ] `status` é `arquivado`
- [ ] `historico_estados` contém entrada de arquivamento
- [ ] Registro não aparece em consultas padrão

---

### 7. Invariantes

> Condições que devem ser verdadeiras **sempre**, independentemente do estado ou operação.

1. `id` nunca muda após criação
2. `id` nunca é reutilizado
3. `criado-em` nunca muda após criação
4. Registro nunca é excluído — apenas arquivado
5. Histórico de estados é append-only
6. SQLite é sempre derivado do Markdown, nunca o contrário
7. [invariantes específicos da entidade]

---

### 8. Rejeições Explícitas

> Operações que o sistema deve sempre recusar, independentemente do contexto.

| Operação | Motivo | Erro |
|----------|--------|------|
| Excluir registro | Violação da política de arquivamento | "Exclusão não permitida. Use arquivamento." |
| Alterar `id` | Violação da imutabilidade de ID | "ID é imutável após criação" |
| Alterar `criado-em` | Violação da rastreabilidade | "Data de criação é imutável" |
| Criar com `id` duplicado | Violação da unicidade | "ID já existe no sistema" |
| Referenciar ID inexistente | Violação de integridade referencial | "ID referenciado não encontrado: [ID]" |
| Atribuir status inválido | Violação do domínio | "Status inválido: [valor]" |

---

### 9. Compatibilidade de Esquema

> Como diferentes versões de esquema coexistem.

- Registros com `schema-version: 1` permanecem válidos indefinidamente
- Registros novos devem usar o esquema atual (versão mais recente)
- O sistema aceita registros de múltiplas versões simultaneamente
- Migração entre versões é opcional, nunca obrigatória

---

### 10. Critério de Aceitação de Implementação

Uma implementação está em conformidade com este contrato quando:

1. Cria, atualiza e arquiva Registros respeitando todas as pré e pós-condições
2. Mantém todas as invariantes após qualquer operação
3. Rejeita todas as operações listadas em "Rejeições Explícitas"
4. Aceita registros válidos de todas as versões de esquema documentadas
5. Não perde informação entre Markdown e SQLite
