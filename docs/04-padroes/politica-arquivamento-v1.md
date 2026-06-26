# Política de Arquivamento

> Nada é excluído. Tudo é arquivado.

---

## Princípio

**Lei Fundamental:** Conhecimento registrado no SOE-CCG nunca é destruído.

Registros não são excluídos. São arquivados, preservando:
- Todo o conteúdo
- Todo o histórico
- Todos os metadados
- Todos os relacionamentos

**Razão filosófica:** conhecimento tem valor permanente, mesmo quando deixa de ser usado ativamente.

---

## Estados

Todo registro possui um estado do ciclo de vida.

### Estados possíveis

| Estado | Significado | Visibilidade |
|--------|-------------|--------------|
| `rascunho` | Em construção, não finalizado | Apenas autor |
| `ativo` | Finalizado e em uso ativo | Todos |
| `revisao` | Sob revisão antes de ativação | Revisores |
| `arquivado` | Não mais em uso, mas preservado | Consultas explícitas |
| `obsoleto` | Substituído por versão mais recente | Histórico apenas |
| `deprecado` | Não recomendado, mas ainda válido | Todos (com aviso) |

### Estado padrão

Novos registros nascem em:
- `rascunho` — se em construção
- `ativo` — se criados completos

---

## Transições

### Diagrama de estados

```
[rascunho] → [revisao] → [ativo]
                ↓           ↓
           [arquivado] ← [deprecado]
                ↓
           [obsoleto]
```

### Transições permitidas

| De | Para | Condição |
|----|------|----------|
| rascunho | revisao | Registro considerado completo |
| rascunho | ativo | Registro completo sem necessidade de revisão |
| rascunho | arquivado | Rascunho descartado (mas preservado) |
| revisao | ativo | Revisão aprovada |
| revisao | rascunho | Revisão solicita alterações |
| revisao | arquivado | Revisão rejeita registro |
| ativo | deprecado | Não mais recomendado, mas válido |
| ativo | arquivado | Não mais usado |
| deprecado | arquivado | Oficialmente descontinuado |
| arquivado | ativo | Restauração explícita |
| ativo | obsoleto | Nova versão do registro criada |

### Transições proibidas

- De `arquivado` para `obsoleto` diretamente
- De `obsoleto` para qualquer outro estado (final)
- Exclusão (não existe como operação)

---

## Histórico

### Preservação de estado

Cada mudança de estado é registrada:

```yaml
historico_estados:
  - estado: rascunho
    data: 2026-01-15T10:00:00Z
    autor: usuario@example.com
  - estado: revisao
    data: 2026-01-20T14:30:00Z
    autor: usuario@example.com
  - estado: ativo
    data: 2026-01-22T09:00:00Z
    autor: revisor@example.com
    nota: "Aprovado após ajustes"
  - estado: arquivado
    data: 2026-06-10T16:00:00Z
    autor: admin@example.com
    nota: "Substituído por ING-0042-v2"
```

### Histórico de conteúdo

Git preserva todas as versões anteriores do arquivo Markdown. Histórico de estados complementa com metadado de ciclo de vida.

---

## Consultas

### Comportamento padrão

Consultas retornam apenas registros em estado `ativo` por padrão.

```sql
SELECT * FROM receitas;  -- apenas ativas
```

### Consulta explícita de arquivados

```sql
SELECT * FROM receitas WHERE estado = 'arquivado';
```

### Consulta de todos os estados

```sql
SELECT * FROM receitas WHERE estado IN ('ativo', 'arquivado', 'deprecado');
```

### Filtros na interface

Interfaces devem oferecer filtro explícito:
- [ ] Mostrar apenas ativos (padrão)
- [ ] Mostrar ativos e deprecados
- [ ] Mostrar todos, incluindo arquivados

---

## Restauração

### Quando restaurar

Um registro arquivado pode retornar a `ativo` quando:
1. O motivo do arquivamento não é mais válido
2. Conhecimento volta a ter relevância
3. Usuário solicita explicitamente

### Processo de restauração

1. Identificar registro arquivado
2. Validar que registro está íntegro
3. Validar que não há conflito com registros ativos
4. Atualizar estado para `ativo`
5. Registrar no histórico de estados

### Restauração vs recriação

**Restauração** recupera registro existente (mantém ID, histórico).

**Recriação** cria novo registro (novo ID, histórico zerado).

Restauração é preferida sempre que o registro original é semanticamente o mesmo conhecimento.

---

## Arquivamento vs Obsolescência

### Arquivado

Registro não mais em uso **ativo**, mas ainda válido e íntegro.

Exemplo: receita que não é mais preparada, mas continua correta.

### Obsoleto

Registro **substituído** por uma versão mais recente.

Exemplo: receita v1 substituída por receita v2.

### Diferença essencial

- **Arquivado** pode ser restaurado
- **Obsoleto** é final — a versão nova é a referência

---

## Metadados de Arquivamento

### Campos relacionados

```yaml
estado: arquivado
data_arquivamento: 2026-06-10T16:00:00Z
arquivado_por: admin@example.com
motivo_arquivamento: "Substituído por versão v2"
substituido_por: REC-0123-v2  # opcional, apenas se obsoleto
```

### Motivos comuns

- Substituído por nova versão
- Não mais relevante
- Duplicado de outro registro
- Erro de criação (preservado para auditoria)
- Mudança no domínio (ex: ingrediente descontinuado)

---

## Impacto em Relacionamentos

### Quando um registro arquivado possui referências

Registros ativos podem referenciar registros arquivados:

```markdown
## Ingredientes

- 200g [ING-0042] (arquivado)
```

Sistema deve alertar, mas não proibir.

**Razão:** execuções antigas de receitas usaram ingredientes que hoje estão arquivados. O histórico é válido.

### Quando criar novo relacionamento

Ao criar **novo** registro, sistema deve alertar se tentar referenciar registro arquivado, sugerindo alternativas ativas.

---

## Exemplos

### Exemplo 1: Receita não mais preparada

```yaml
id: REC-0089
nome: Bolo de Cenoura Antigo
estado: arquivado
data_arquivamento: 2025-12-01T10:00:00Z
motivo_arquivamento: "Substituído por versão aprimorada REC-0089-v2"
```

Registro continua acessível. Histórico preservado. Pode ser consultado explicitamente.

---

### Exemplo 2: Ingrediente descontinuado

```yaml
id: ING-0203
nome: Corante Artificial X
estado: arquivado
motivo_arquivamento: "Produto descontinuado pelo fabricante"
```

Receitas antigas que usaram este ingrediente continuam válidas. Novas receitas recebem aviso ao tentar usar.

---

### Exemplo 3: Observação substituída

```yaml
id: OBS-0450
estado: obsoleto
substituido_por: OBS-0450-v2
```

Estado final. v2 é a versão atual. v1 permanece no histórico.

---

## Governança

### Quem pode arquivar?

- Autor do registro
- Administradores do sistema
- Mantenedores do domínio

### Quem pode restaurar?

- Administradores do sistema
- Mantenedores do domínio (com justificativa)

### Auditoria

Toda operação de arquivamento e restauração é auditada:
- Quem executou
- Quando executou
- Motivo declarado

---

## Exceções

### Casos onde exclusão é permitida

Apenas quando:
1. **Dados sensíveis** — informações que violam privacidade e devem ser removidas por lei (LGPD, GDPR)
2. **Erro crítico de sistema** — corrupção que impede funcionamento

**Processo:**
1. Justificativa formal documentada
2. Aprovação de múltiplos mantenedores
3. Backup antes da exclusão
4. Registro na auditoria

**Estes casos são exceções raríssimas.** Regra geral: nada é excluído.

---

## Resumo

- Registros **nunca são excluídos**, apenas arquivados
- Estados: rascunho, revisao, ativo, deprecado, arquivado, obsoleto
- Transições de estado são auditadas
- Consultas retornam apenas ativos por padrão
- Arquivados podem ser restaurados
- Obsoletos são finais (substituídos por nova versão)
- Relacionamentos com arquivados são válidos mas alertados
- Histórico completo é sempre preservado
