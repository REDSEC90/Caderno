# Contrato Formal: Execução

**Entidade:** Execução  
**Versão do contrato:** v1  
**Esquema associado:** `docs/01-dominio/esquemas/esquema-execucao-v1.md`  
**Especificação associada:** `docs/01-dominio/especificacao-execucao.md`

---

## 1. Campos Obrigatórios

| Campo | Tipo | Restrição | Mensagem de erro se ausente |
|-------|------|-----------|----------------------------|
| `id` | string | `EXE-NNNNNN` | "ID ausente ou em formato inválido" |
| `tipo` | string | valor fixo: `execucao` | "Tipo de entidade inválido" |
| `schema-version` | integer | ≥ 1 | "Versão de esquema ausente" |
| `versao` | integer | ≥ 1 | "Versão do registro ausente" |
| `status` | string | enum: `registrada`, `revisada`, `consolidada` | "Status inválido ou ausente" |
| `criado-em` | date | `YYYY-MM-DD` | "Data de criação ausente ou inválida" |
| `atualizado-em` | date | `YYYY-MM-DD` | "Data de atualização ausente ou inválida" |
| `autor` | string | não vazio | "Autor ausente" |
| `receita-id` | string | `REC-NNNNNN`, deve existir no sistema | "Receita referenciada ausente ou inválida" |
| `data-execucao` | date | `YYYY-MM-DD`, ≤ `criado-em` | "Data de execução ausente ou inválida" |

---

## 2. Campos Opcionais

| Campo | Tipo | Restrição | Comportamento se ausente |
|-------|------|-----------|--------------------------|
| `hora-inicio` | string | formato `HH:MM` | Tratado como null |
| `hora-fim` | string | formato `HH:MM` | Tratado como null |
| `tempo-total` | string | — | Tratado como null |
| `ingredientes-usados` | list | IDs no formato `ING-NNNNNN` | Tratado como lista vazia |
| `tecnicas-aplicadas` | list | IDs no formato `TEC-NNNNNN` | Tratado como lista vazia |
| `equipamentos-usados` | list | IDs no formato `EQP-NNNNNN` | Tratado como lista vazia |
| `desvios` | text | — | Tratado como null |
| `resultado` | text | — | Tratado como null |
| `avaliacao-sabor` | string | — | Tratado como null |
| `avaliacao-textura` | string | — | Tratado como null |
| `avaliacao-aparencia` | string | — | Tratado como null |
| `avaliacao-geral` | string | — | Tratado como null |
| `peso-final` | string | — | Tratado como null |
| `contexto` | text | — | Tratado como null |
| `tags` | list | minúsculas, hífens | Tratado como lista vazia |
| `notas` | text | — | Tratado como null |

---

## 3. Valores Aceitos por Campo

**`status`:**
```
registrada
revisada
consolidada
```

---

## 4. Pré-condições por Operação

**Criar:**
- [ ] `id` não existe no sistema (unicidade global)
- [ ] Todos os campos obrigatórios estão presentes
- [ ] `receita-id` referencia uma Receita existente
- [ ] `data-execucao` ≤ `criado-em`
- [ ] Todos os `ING-NNNNNN` referenciados existem (se presentes)
- [ ] Todos os `TEC-NNNNNN` referenciados existem (se presentes)
- [ ] Todos os `EQP-NNNNNN` referenciados existem (se presentes)
- [ ] `schema-version` é uma versão de esquema conhecida
- [ ] `atualizado-em` = `criado-em` (primeira criação)

**Atualizar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `consolidada` (execuções consolidadas são imutáveis)
- [ ] `id` não foi alterado
- [ ] `receita-id` não foi alterado (imutável)
- [ ] `criado-em` não foi alterado
- [ ] `data-execucao` não foi alterada
- [ ] `atualizado-em` ≥ valor anterior
- [ ] Todos os IDs referenciados existem

**Consolidar:**
- [ ] Registro existe no sistema
- [ ] `status` = `revisada`

**Arquivar:**
- [ ] Registro existe no sistema
- [ ] Motivo de arquivamento registrado (duplicação ou erro)

---

## 5. Pós-condições por Operação

**Criar:**
- [ ] Registro existe em `dados/execucoes/[id].md`
- [ ] Registro existe no SQLite com os mesmos dados
- [ ] `historico_estados` contém entrada de criação com timestamp
- [ ] `id` é único globalmente
- [ ] Se Receita referenciada estava em `rascunho`, transita automaticamente para `testada`

**Atualizar:**
- [ ] `atualizado-em` foi atualizado para data atual
- [ ] Versão anterior é recuperável via git
- [ ] SQLite reflete os novos valores
- [ ] `historico_estados` contém entrada de atualização se `status` mudou

**Consolidar:**
- [ ] `status` = `consolidada`
- [ ] `atualizado-em` = data da consolidação
- [ ] `historico_estados` contém entrada de consolidação
- [ ] Registro não aceita mais alterações de conteúdo

**Arquivar:**
- [ ] `status` contém flag de arquivamento (ou estado específico)
- [ ] `historico_estados` contém entrada de arquivamento
- [ ] Registro não aparece em consultas padrão

---

## 6. Invariantes

1. `id` nunca muda após criação
2. `id` nunca é reutilizado
3. `receita-id` nunca muda após criação
4. `criado-em` nunca muda após criação
5. `data-execucao` nunca muda após criação
6. Histórico de estados é append-only
7. SQLite é sempre derivado do Markdown, nunca o contrário
8. Relacionamentos usam exclusivamente IDs, nunca nomes
9. `data-execucao` ≤ `criado-em` sempre
10. `atualizado-em` ≥ `criado-em` sempre
11. Execução com `status` = `consolidada` é imutável
12. Arquivo Markdown em `dados/execucoes/` é a única fonte da verdade

---

## 7. Rejeições Explícitas

| Operação | Motivo | Erro |
|----------|--------|------|
| Excluir registro | Violação da política de arquivamento | "Exclusão não permitida. Use arquivamento apenas para erros de registro." |
| Alterar `id` | Violação da imutabilidade de ID | "ID é imutável após criação" |
| Alterar `receita-id` | Violação da integridade histórica | "receita-id é imutável — Execução sempre pertence à mesma Receita" |
| Alterar `criado-em` | Violação da rastreabilidade | "Data de criação é imutável" |
| Alterar `data-execucao` | Violação da rastreabilidade | "Data de execução é imutável" |
| Criar com `id` duplicado | Violação da unicidade | "ID EXE-NNNNNN já existe no sistema" |
| Referenciar `REC-NNNNNN` inexistente | Violação de integridade referencial | "Receita REC-NNNNNN não encontrada" |
| Referenciar `ING-NNNNNN` inexistente | Violação de integridade referencial | "Ingrediente ING-NNNNNN não encontrado" |
| Referenciar `TEC-NNNNNN` inexistente | Violação de integridade referencial | "Técnica TEC-NNNNNN não encontrada" |
| Referenciar `EQP-NNNNNN` inexistente | Violação de integridade referencial | "Equipamento EQP-NNNNNN não encontrado" |
| Atualizar Execução consolidada | Violação da imutabilidade | "Execuções consolidadas não podem ser alteradas" |
| `data-execucao` > `criado-em` | Violação da lógica temporal | "Data de execução não pode ser posterior à data de criação do registro" |

---

## 8. Compatibilidade de Esquema

- Registros com `schema-version: 1` permanecem válidos indefinidamente
- Registros novos devem usar o esquema atual
- O sistema aceita registros de múltiplas versões simultaneamente
- Migração entre versões é opcional, nunca obrigatória

---

## 9. Critério de Aceitação de Implementação

Uma implementação está em conformidade com este contrato quando:

1. Cria, atualiza e consolida Execuções respeitando todas as pré e pós-condições
2. Mantém todas as invariantes após qualquer operação
3. Rejeita todas as operações listadas em "Rejeições Explícitas"
4. Aceita execuções válidas de todas as versões de esquema documentadas
5. Não perde informação entre Markdown e SQLite
6. Valida integridade referencial de `receita-id` e todos os IDs opcionais
7. Preserva histórico de estados como append-only
8. Garante que Markdown em `dados/execucoes/` é sempre a fonte da verdade
9. Transita Receita de `rascunho` para `testada` quando primeira Execução é criada
10. Impede alterações em Execuções com `status` = `consolidada`
