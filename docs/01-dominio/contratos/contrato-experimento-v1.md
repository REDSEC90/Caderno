# Contrato Formal: Experimento

**Entidade:** Experimento  
**Versão do contrato:** v1  
**Esquema associado:** `docs/01-dominio/esquemas/esquema-experimento-v1.md`  
**Especificação associada:** `docs/01-dominio/especificacao-experimento.md`

---

## 1. Campos Obrigatórios

| Campo | Tipo | Restrição | Mensagem de erro se ausente |
|-------|------|-----------|----------------------------|
| `id` | string | `EXP-NNNNNN` | "ID ausente ou em formato inválido" |
| `tipo` | string | valor fixo: `experimento` | "Tipo de entidade inválido" |
| `schema-version` | integer | ≥ 1 | "Versão de esquema ausente" |
| `versao` | integer | ≥ 1 | "Versão do registro ausente" |
| `status` | string | enum: `aberto`, `concluido`, `incorporado`, `descartado` | "Status inválido ou ausente" |
| `criado-em` | date | `YYYY-MM-DD` | "Data de criação ausente ou inválida" |
| `atualizado-em` | date | `YYYY-MM-DD` | "Data de atualização ausente ou inválida" |
| `autor` | string | não vazio | "Autor ausente" |
| `titulo` | string | não vazio | "Título do experimento ausente" |
| `hipotese` | text | não vazio | "Hipótese do experimento ausente" |

---

## 2. Campos Opcionais

| Campo | Tipo | Restrição | Comportamento se ausente |
|-------|------|-----------|--------------------------|
| `receita-base-id` | string | formato `REC-NNNNNN`, deve existir no sistema | Tratado como null (experimento sem base) |
| `variaveis` | text | — | Tratado como null |
| `processo` | text | — | Tratado como null |
| `resultado` | text | — | Tratado como null |
| `conclusao` | text | — | Tratado como null |
| `incorporado-em` | string | formato `REC-NNNNNN`, deve existir no sistema | Tratado como null |
| `tags` | list | minúsculas, hífens | Tratado como lista vazia |
| `notas` | text | — | Tratado como null |

---

## 3. Valores Aceitos por Campo

**`status`:**
```
aberto
concluido
incorporado
descartado
```

---

## 4. Pré-condições por Operação

**Criar:**
- [ ] `id` não existe no sistema (unicidade global)
- [ ] Todos os campos obrigatórios estão presentes
- [ ] `schema-version` é uma versão de esquema conhecida
- [ ] `criado-em` ≤ data atual
- [ ] `atualizado-em` = `criado-em` (primeira criação)
- [ ] `receita-base-id` existe no sistema (se presente)
- [ ] `status` = `aberto` na criação

**Atualizar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `descartado` (descartados não são editáveis)
- [ ] `id` não foi alterado
- [ ] `criado-em` não foi alterado
- [ ] `atualizado-em` ≥ valor anterior
- [ ] `receita-base-id` não foi alterado (imutável)
- [ ] Se `incorporado-em` está presente, deve existir no sistema

**Concluir:**
- [ ] Registro existe no sistema
- [ ] `status` = `aberto`
- [ ] `resultado` está presente
- [ ] `conclusao` está presente

**Incorporar:**
- [ ] Registro existe no sistema
- [ ] `status` = `concluido`
- [ ] `incorporado-em` está presente e referencia Receita existente

**Descartar:**
- [ ] Registro existe no sistema
- [ ] `status` = `concluido`
- [ ] `conclusao` justifica o descarte

---

## 5. Pós-condições por Operação

**Criar:**
- [ ] Registro existe em `dados/experimentos/[id].md`
- [ ] Registro existe no SQLite com os mesmos dados
- [ ] `historico_estados` contém entrada de criação com timestamp
- [ ] `id` é único globalmente
- [ ] `status` = `aberto`

**Atualizar:**
- [ ] `atualizado-em` foi atualizado para data atual
- [ ] Versão anterior é recuperável via git
- [ ] SQLite reflete os novos valores
- [ ] `historico_estados` contém entrada de atualização se `status` mudou

**Concluir:**
- [ ] `status` = `concluido`
- [ ] `atualizado-em` = data da conclusão
- [ ] `historico_estados` contém entrada de conclusão
- [ ] `resultado` e `conclusao` estão preenchidos

**Incorporar:**
- [ ] `status` = `incorporado`
- [ ] `atualizado-em` = data da incorporação
- [ ] `incorporado-em` referencia Receita existente
- [ ] `historico_estados` contém entrada de incorporação
- [ ] Receita referenciada contém campo `origem-experimento: [EXP-NNNNNN]` (recomendado)

**Descartar:**
- [ ] `status` = `descartado`
- [ ] `atualizado-em` = data do descarte
- [ ] `historico_estados` contém entrada de descarte
- [ ] Registro preservado no histórico

---

## 6. Invariantes

1. `id` nunca muda após criação
2. `id` nunca é reutilizado
3. `criado-em` nunca muda após criação
4. `receita-base-id` nunca muda após criação (se presente)
5. Registro nunca é excluído — estados finais são `incorporado` ou `descartado`
6. Histórico de estados é append-only
7. SQLite é sempre derivado do Markdown, nunca o contrário
8. Experimento com `status` = `incorporado` deve ter `incorporado-em` preenchido
9. Experimento com `status` = `descartado` deve ter `conclusao` preenchido
10. Experimentos em estado `descartado` não são editáveis
11. `atualizado-em` ≥ `criado-em` sempre
12. Arquivo Markdown em `dados/experimentos/` é a única fonte da verdade

---

## 7. Rejeições Explícitas

| Operação | Motivo | Erro |
|----------|--------|------|
| Excluir registro | Violação da política de arquivamento | "Exclusão não permitida. Use status 'descartado'." |
| Alterar `id` | Violação da imutabilidade de ID | "ID é imutável após criação" |
| Alterar `receita-base-id` | Violação da imutabilidade | "receita-base-id é imutável após criação" |
| Alterar `criado-em` | Violação da rastreabilidade | "Data de criação é imutável" |
| Criar com `id` duplicado | Violação da unicidade | "ID EXP-NNNNNN já existe no sistema" |
| Referenciar `REC-NNNNNN` inexistente | Violação de integridade referencial | "Receita REC-NNNNNN não encontrada" |
| Concluir sem `resultado` e `conclusao` | Violação de completude | "Resultado e conclusão devem estar preenchidos ao concluir" |
| Incorporar sem `incorporado-em` | Violação de consistência | "Campo incorporado-em deve estar preenchido ao incorporar" |
| Incorporar sem ter concluído antes | Violação de fluxo | "Experimento deve estar concluído antes de ser incorporado" |
| Descartar sem `conclusao` | Violação de rastreabilidade | "Conclusão deve justificar o descarte" |
| Editar experimento descartado | Violação de imutabilidade | "Experimentos descartados não podem ser editados" |
| Criar com `status` ≠ `aberto` | Violação de fluxo | "Experimentos devem nascer com status 'aberto'" |

---

## 8. Compatibilidade de Esquema

- Registros com `schema-version: 1` permanecem válidos indefinidamente
- Registros novos devem usar o esquema atual
- O sistema aceita registros de múltiplas versões simultaneamente
- Migração entre versões é opcional, nunca obrigatória

---

## 9. Critério de Aceitação de Implementação

Uma implementação está em conformidade com este contrato quando:

1. Cria, atualiza, conclui, incorpora e descarta Experimentos respeitando todas as pré e pós-condições
2. Mantém todas as invariantes após qualquer operação
3. Rejeita todas as operações listadas em "Rejeições Explícitas"
4. Aceita experimentos válidos de todas as versões de esquema documentadas
5. Não perde informação entre Markdown e SQLite
6. Valida integridade referencial de `receita-base-id` e `incorporado-em` (se presentes)
7. Preserva histórico de estados como append-only
8. Garante que Markdown em `dados/experimentos/` é sempre a fonte da verdade
9. Impede alterações em experimentos com `status` = `descartado`
10. Garante consistência entre `status` = `incorporado` e presença de `incorporado-em`
11. Garante que transições de estado seguem o fluxo: `aberto` → `concluido` → (`incorporado` | `descartado`)
