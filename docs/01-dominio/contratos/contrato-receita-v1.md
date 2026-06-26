# Contrato Formal: Receita

**Entidade:** Receita  
**Versão do contrato:** v1  
**Esquema associado:** `docs/01-dominio/esquemas/esquema-receita-v1.md`  
**Especificação associada:** `docs/01-dominio/especificacao-receita.md`

---

## 1. Campos Obrigatórios

| Campo | Tipo | Restrição | Mensagem de erro se ausente |
|-------|------|-----------|----------------------------|
| `id` | string | `REC-NNNNNN` | "ID ausente ou em formato inválido" |
| `tipo` | string | valor fixo: `receita` | "Tipo de entidade inválido" |
| `schema-version` | integer | ≥ 1 | "Versão de esquema ausente" |
| `versao` | integer | ≥ 1 | "Versão do registro ausente" |
| `status` | string | enum: `rascunho`, `testada`, `validada`, `publicada`, `arquivada` | "Status inválido ou ausente" |
| `criado-em` | date | `YYYY-MM-DD` | "Data de criação ausente ou inválida" |
| `atualizado-em` | date | `YYYY-MM-DD` | "Data de atualização ausente ou inválida" |
| `autor` | string | não vazio | "Autor ausente" |
| `titulo` | string | não vazio | "Título ausente" |
| `ingredientes` | list | pelo menos 1 item, cada item com `id` no formato `ING-NNNNNN` | "Lista de ingredientes ausente ou vazia" |
| `modo-de-preparo` | text | não vazio | "Modo de preparo ausente" |

---

## 2. Campos Opcionais

| Campo | Tipo | Restrição | Comportamento se ausente |
|-------|------|-----------|--------------------------|
| `descricao` | string | — | Tratado como null |
| `categorias` | list | valores do catálogo oficial | Tratado como lista vazia |
| `rendimento` | string | — | Tratado como null |
| `tempo-preparo` | string | — | Tratado como null |
| `tempo-cozimento` | string | — | Tratado como null |
| `dificuldade` | string | enum: `baixa`, `media`, `alta` | Tratado como null |
| `tecnicas` | list | IDs no formato `TEC-NNNNNN` | Tratado como lista vazia |
| `equipamentos` | list | IDs no formato `EQP-NNNNNN` | Tratado como lista vazia |
| `notas` | text | — | Tratado como null |
| `origem` | string | — | Tratado como null |
| `tags` | list | minúsculas, hífens | Tratado como lista vazia |

---

## 3. Valores Aceitos por Campo

**`status`:**
```
rascunho
testada
validada
publicada
arquivada
```

**`dificuldade`:**
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
- [ ] Todos os `ING-NNNNNN` referenciados existem no sistema
- [ ] Todos os `TEC-NNNNNN` referenciados existem no sistema (se presentes)
- [ ] Todos os `EQP-NNNNNN` referenciados existem no sistema (se presentes)
- [ ] `schema-version` é uma versão de esquema conhecida
- [ ] `criado-em` ≤ data atual
- [ ] `atualizado-em` = `criado-em` (primeira criação)

**Atualizar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `arquivada`
- [ ] `id` não foi alterado
- [ ] `criado-em` não foi alterado
- [ ] `atualizado-em` ≥ valor anterior
- [ ] Todos os IDs referenciados existem

**Arquivar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `arquivada`

**Restaurar (arquivada → publicada):**
- [ ] Registro existe no sistema
- [ ] `status` = `arquivada`
- [ ] Nenhuma Receita ativa com mesmo `id`

---

## 5. Pós-condições por Operação

**Criar:**
- [ ] Registro existe em `dados/receitas/[id].md`
- [ ] Registro existe no SQLite com os mesmos dados
- [ ] `historico_estados` contém entrada de criação com timestamp
- [ ] `id` é único globalmente
- [ ] Se `status` = `publicada`, mantenedor foi o autor

**Atualizar:**
- [ ] `atualizado-em` foi atualizado para data atual
- [ ] Versão anterior é recuperável via git
- [ ] SQLite reflete os novos valores
- [ ] `historico_estados` contém entrada de atualização se `status` mudou

**Arquivar:**
- [ ] `status` = `arquivada`
- [ ] `atualizado-em` = data do arquivamento
- [ ] `historico_estados` contém entrada de arquivamento
- [ ] Registro não aparece em consultas padrão (flag `WHERE status != 'arquivada'`)
- [ ] Execuções históricas que referenciam a Receita permanecem válidas

---

## 6. Invariantes

1. `id` nunca muda após criação
2. `id` nunca é reutilizado
3. `criado-em` nunca muda após criação
4. Registro nunca é excluído — apenas arquivado
5. Histórico de estados é append-only
6. SQLite é sempre derivado do Markdown, nunca o contrário
7. Toda Receita com `status` = `testada` possui ao menos uma Execução vinculada
8. Relacionamentos usam exclusivamente IDs, nunca nomes
9. `atualizado-em` ≥ `criado-em` sempre
10. Arquivo Markdown em `dados/receitas/` é a única fonte da verdade

---

## 7. Rejeições Explícitas

| Operação | Motivo | Erro |
|----------|--------|------|
| Excluir registro | Violação da política de arquivamento | "Exclusão não permitida. Use arquivamento." |
| Alterar `id` | Violação da imutabilidade de ID | "ID é imutável após criação" |
| Alterar `criado-em` | Violação da rastreabilidade | "Data de criação é imutável" |
| Criar com `id` duplicado | Violação da unicidade | "ID REC-NNNNNN já existe no sistema" |
| Referenciar `ING-NNNNNN` inexistente | Violação de integridade referencial | "Ingrediente ING-NNNNNN não encontrado" |
| Referenciar `TEC-NNNNNN` inexistente | Violação de integridade referencial | "Técnica TEC-NNNNNN não encontrada" |
| Referenciar `EQP-NNNNNN` inexistente | Violação de integridade referencial | "Equipamento EQP-NNNNNN não encontrado" |
| Atribuir `status` = `testada` sem Execução vinculada | Violação de evidência | "Status 'testada' requer ao menos uma Execução vinculada" |
| Atribuir `status` = `publicada` sem permissão de mantenedor | Violação de governança | "Publicação requer permissão de mantenedor" |
| Criar `ingredientes` vazio | Violação do domínio | "Receita deve ter ao menos um ingrediente" |

---

## 8. Compatibilidade de Esquema

- Registros com `schema-version: 1` permanecem válidos indefinidamente
- Registros novos devem usar o esquema atual (versão mais recente disponível)
- O sistema aceita registros de múltiplas versões simultaneamente
- Migração entre versões é opcional, nunca obrigatória
- Campos novos adicionados em versões superiores são ignorados ao ler `schema-version: 1`

---

## 9. Critério de Aceitação de Implementação

Uma implementação está em conformidade com este contrato quando:

1. Cria, atualiza e arquiva Receitas respeitando todas as pré e pós-condições
2. Mantém todas as invariantes após qualquer operação
3. Rejeita todas as operações listadas em "Rejeições Explícitas"
4. Aceita receitas válidas de todas as versões de esquema documentadas
5. Não perde informação entre Markdown e SQLite
6. Valida integridade referencial de todos os IDs antes de aceitar operação
7. Preserva histórico de estados como append-only
8. Garante que Markdown em `dados/receitas/` é sempre a fonte da verdade
