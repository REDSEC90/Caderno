# Contrato Formal: Técnica

**Entidade:** Técnica  
**Versão do contrato:** v1  
**Esquema associado:** `docs/01-dominio/esquemas/esquema-tecnica-v1.md`  
**Especificação associada:** `docs/01-dominio/especificacao-tecnica.md`

---

## 1. Campos Obrigatórios

| Campo | Tipo | Restrição | Mensagem de erro se ausente |
|-------|------|-----------|----------------------------|
| `id` | string | `TEC-NNNNNN` | "ID ausente ou em formato inválido" |
| `tipo` | string | valor fixo: `tecnica` | "Tipo de entidade inválido" |
| `schema-version` | integer | ≥ 1 | "Versão de esquema ausente" |
| `versao` | integer | ≥ 1 | "Versão do registro ausente" |
| `status` | string | enum: `ativo`, `descontinuado`, `arquivado` | "Status inválido ou ausente" |
| `criado-em` | date | `YYYY-MM-DD` | "Data de criação ausente ou inválida" |
| `atualizado-em` | date | `YYYY-MM-DD` | "Data de atualização ausente ou inválida" |
| `autor` | string | não vazio | "Autor ausente" |
| `nome` | string | não vazio | "Nome da técnica ausente" |

---

## 2. Campos Opcionais

| Campo | Tipo | Restrição | Comportamento se ausente |
|-------|------|-----------|--------------------------|
| `tipo-tecnica` | string | valores do catálogo oficial | Tratado como null |
| `descricao` | text | — | Tratado como null |
| `aplicacoes` | text | — | Tratado como null |
| `dificuldade` | string | enum: `baixa`, `media`, `alta` | Tratado como null |
| `tags` | list | minúsculas, hífens | Tratado como lista vazia |
| `notas` | text | — | Tratado como null |

---

## 3. Valores Aceitos por Campo

**`status`:**
```
ativo
descontinuado
arquivado
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
- [ ] `schema-version` é uma versão de esquema conhecida
- [ ] `criado-em` ≤ data atual
- [ ] `atualizado-em` = `criado-em` (primeira criação)
- [ ] `tipo-tecnica` existe no catálogo (se presente)

**Atualizar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `arquivado`
- [ ] `id` não foi alterado
- [ ] `criado-em` não foi alterado
- [ ] `atualizado-em` ≥ valor anterior

**Arquivar:**
- [ ] Registro existe no sistema
- [ ] `status` ≠ `arquivado`

**Restaurar (arquivado → ativo):**
- [ ] Registro existe no sistema
- [ ] `status` = `arquivado`
- [ ] Nenhuma Técnica ativa com mesmo `id`

---

## 5. Pós-condições por Operação

**Criar:**
- [ ] Registro existe em `dados/tecnicas/[id].md`
- [ ] Registro existe no SQLite com os mesmos dados
- [ ] `historico_estados` contém entrada de criação com timestamp
- [ ] `id` é único globalmente

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
- [ ] Receitas e Execuções históricas que referenciam a Técnica permanecem válidas

---

## 6. Invariantes

1. `id` nunca muda após criação
2. `id` nunca é reutilizado
3. `criado-em` nunca muda após criação
4. Registro nunca é excluído — apenas arquivado
5. Histórico de estados é append-only
6. SQLite é sempre derivado do Markdown, nunca o contrário
7. Técnica pode existir sem ser referenciada por nenhuma Receita
8. `atualizado-em` ≥ `criado-em` sempre
9. Arquivo Markdown em `dados/tecnicas/` é a única fonte da verdade

---

## 7. Rejeições Explícitas

| Operação | Motivo | Erro |
|----------|--------|------|
| Excluir registro | Violação da política de arquivamento | "Exclusão não permitida. Use arquivamento." |
| Alterar `id` | Violação da imutabilidade de ID | "ID é imutável após criação" |
| Alterar `criado-em` | Violação da rastreabilidade | "Data de criação é imutável" |
| Criar com `id` duplicado | Violação da unicidade | "ID TEC-NNNNNN já existe no sistema" |
| Atribuir `tipo-tecnica` inválido | Violação do catálogo | "Tipo de técnica não encontrado no catálogo" |

---

## 8. Compatibilidade de Esquema

- Registros com `schema-version: 1` permanecem válidos indefinidamente
- Registros novos devem usar o esquema atual
- O sistema aceita registros de múltiplas versões simultaneamente
- Migração entre versões é opcional, nunca obrigatória

---

## 9. Critério de Aceitação de Implementação

Uma implementação está em conformidade com este contrato quando:

1. Cria, atualiza e arquiva Técnicas respeitando todas as pré e pós-condições
2. Mantém todas as invariantes após qualquer operação
3. Rejeita todas as operações listadas em "Rejeições Explícitas"
4. Aceita técnicas válidas de todas as versões de esquema documentadas
5. Não perde informação entre Markdown e SQLite
6. Preserva histórico de estados como append-only
7. Garante que Markdown em `dados/tecnicas/` é sempre a fonte da verdade
8. Permite que Técnica exista sem nenhuma Receita que a referencie
