# Contrato Formal: Observação

**Entidade:** Observação  
**Versão do contrato:** v1  
**Esquema associado:** `docs/01-dominio/esquemas/esquema-observacao-v1.md`  
**Especificação associada:** `docs/01-dominio/especificacao-observacao.md`

---

## 1. Campos Obrigatórios

| Campo | Tipo | Restrição | Mensagem de erro se ausente |
|-------|------|-----------|----------------------------|
| `id` | string | `OBS-NNNNNN` | "ID ausente ou em formato inválido" |
| `tipo` | string | valor fixo: `observacao` | "Tipo de entidade inválido" |
| `schema-version` | integer | ≥ 1 | "Versão de esquema ausente" |
| `versao` | integer | ≥ 1 | "Versão do registro ausente" |
| `status` | string | enum: `ativo`, `arquivado`, `obsoleto` | "Status inválido ou ausente" |
| `criado-em` | date | `YYYY-MM-DD` | "Data de criação ausente ou inválida" |
| `atualizado-em` | date | `YYYY-MM-DD` | "Data de atualização ausente ou inválida" |
| `autor` | string | não vazio | "Autor ausente" |
| `conteudo` | text | não vazio | "Conteúdo da observação ausente" |

---

## 2. Campos Opcionais

| Campo | Tipo | Restrição | Comportamento se ausente |
|-------|------|-----------|--------------------------|
| `entidade-referenciada` | string | formato `[PREFIXO]-NNNNNN`, deve existir no sistema | Tratado como null (observação geral) |
| `tipo-entidade` | string | enum: `receita`, `execucao`, `ingrediente`, `tecnica`, `equipamento`, `experimento` | Tratado como null |
| `contexto` | text | — | Tratado como null |
| `tags` | list | minúsculas, hífens | Tratado como lista vazia |
| `relevancia` | string | enum: `baixa`, `media`, `alta` | Tratado como null |

---

## 3. Valores Aceitos por Campo

**`status`:**
```
ativo
arquivado
obsoleto
```

**`tipo-entidade`:**
```
receita
execucao
ingrediente
tecnica
equipamento
experimento
```

**`relevancia`:**
```
baixa
media
alta
```

---

## 4. Pré-condições por Operação

**Criar:**
- [ ] `id` não existe no sistema (unicidade global)
- [ ] Todos os campos obrigatórios estão presentes
- [ ] `schema-version` é uma versão de esquema conhecida
- [ ] `criado-em` ≤ data atual
- [ ] `atualizado-em` = `criado-em` (primeira criação)
- [ ] `entidade-referenciada` existe no sistema (se presente)
- [ ] `tipo-entidade` está presente se e somente se `entidade-referenciada` está presente

**Atualizar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `arquivado`
- [ ] `id` não foi alterado
- [ ] `criado-em` não foi alterado
- [ ] `atualizado-em` ≥ valor anterior

**Arquivar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `arquivado`

**Marcar como obsoleto:**
- [ ] Registro existe no sistema
- [ ] `status` = `ativo`
- [ ] Nova observação substituta existe (recomendado)

---

## 5. Pós-condições por Operação

**Criar:**
- [ ] Registro existe em `dados/observacoes/[id].md`
- [ ] Registro existe no SQLite com os mesmos dados
- [ ] `historico_estados` contém entrada de criação com timestamp
- [ ] `id` é único globalmente
- [ ] `status` = `ativo` automaticamente (não requer revisão)

**Atualizar:**
- [ ] `atualizado-em` foi atualizado para data atual
- [ ] Versão anterior é recuperável via git
- [ ] SQLite reflete os novos valores
- [ ] `historico_estados` contém entrada de atualização se `status` mudou

**Arquivar:**
- [ ] `status` = `arquivado`
- [ ] `atualizado-em` = data do arquivamento
- [ ] `historico_estados` contém entrada de arquivamento
- [ ] Registro não aparece em consultas padrão

**Marcar como obsoleto:**
- [ ] `status` = `obsoleto`
- [ ] `atualizado-em` = data da marcação
- [ ] `historico_estados` contém entrada de transição

---

## 6. Invariantes

1. `id` nunca muda após criação
2. `id` nunca é reutilizado
3. `criado-em` nunca muda após criação
4. Registro nunca é excluído — apenas arquivado ou marcado como obsoleto
5. Histórico de estados é append-only
6. SQLite é sempre derivado do Markdown, nunca o contrário
7. Observação pode existir sem referenciar nenhuma entidade
8. Se `entidade-referenciada` está presente, `tipo-entidade` deve estar presente
9. `atualizado-em` ≥ `criado-em` sempre
10. Arquivo Markdown em `dados/observacoes/` é a única fonte da verdade
11. Observações tornam-se ativas automaticamente sem revisão

---

## 7. Rejeições Explícitas

| Operação | Motivo | Erro |
|----------|--------|------|
| Excluir registro | Violação da política de arquivamento | "Exclusão não permitida. Use arquivamento." |
| Alterar `id` | Violação da imutabilidade de ID | "ID é imutável após criação" |
| Alterar `criado-em` | Violação da rastreabilidade | "Data de criação é imutável" |
| Criar com `id` duplicado | Violação da unicidade | "ID OBS-NNNNNN já existe no sistema" |
| Referenciar entidade inexistente | Violação de integridade referencial | "Entidade [ID] referenciada não encontrada" |
| Preencher `entidade-referenciada` sem `tipo-entidade` | Violação de consistência | "tipo-entidade deve estar presente quando entidade-referenciada está presente" |
| Preencher `tipo-entidade` sem `entidade-referenciada` | Violação de consistência | "entidade-referenciada deve estar presente quando tipo-entidade está presente" |
| Criar `conteudo` vazio | Violação do domínio | "Conteúdo da observação não pode ser vazio" |

---

## 8. Compatibilidade de Esquema

- Registros com `schema-version: 1` permanecem válidos indefinidamente
- Registros novos devem usar o esquema atual
- O sistema aceita registros de múltiplas versões simultaneamente
- Migração entre versões é opcional, nunca obrigatória

---

## 9. Critério de Aceitação de Implementação

Uma implementação está em conformidade com este contrato quando:

1. Cria, atualiza e arquiva Observações respeitando todas as pré e pós-condições
2. Mantém todas as invariantes após qualquer operação
3. Rejeita todas as operações listadas em "Rejeições Explícitas"
4. Aceita observações válidas de todas as versões de esquema documentadas
5. Não perde informação entre Markdown e SQLite
6. Valida integridade referencial de `entidade-referenciada` (se presente)
7. Preserva histórico de estados como append-only
8. Garante que Markdown em `dados/observacoes/` é sempre a fonte da verdade
9. Permite que Observação exista sem referenciar nenhuma entidade
10. Torna Observação ativa automaticamente sem exigir revisão
