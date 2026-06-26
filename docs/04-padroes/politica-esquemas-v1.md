# Política de Esquemas

> Como esquemas de entidades nascem, evoluem e garantem compatibilidade.

---

## Definição

Um **esquema** define **o que** deve estar presente em um registro: campos obrigatórios, opcionais, tipos, restrições e validações.

Diferença essencial:
- **Esquema** define conteúdo semântico (quais dados, que tipo, quais restrições)
- **Template** define apresentação (como esses dados são escritos em Markdown)

---

## Criação

### Quando um esquema nasce

Um esquema nasce quando:
1. Uma nova entidade é definida no domínio
2. Uma entidade existente evolui suficientemente para justificar nova versão

### Processo de criação

1. Definir campos obrigatórios
2. Definir campos opcionais
3. Definir tipos de cada campo
4. Definir restrições e validações
5. Documentar em `docs/01-dominio/esquemas/`
6. Versionar desde v1

---

## Estrutura

### Anatomia de um esquema

Todo esquema deve conter:

```markdown
# Esquema [Entidade] v[N]

## Campos Obrigatórios

| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| ... | ... | ... | ... |

## Campos Opcionais

| Campo | Tipo | Descrição | Restrições |
|-------|------|-----------|------------|
| ... | ... | ... | ... |

## Validações

[regras de validação]

## Exemplos

[exemplos de registros válidos]

## Contra-exemplos

[exemplos de registros inválidos e por quê]
```

---

## Campos

### Como campos são adicionados

**Campo opcional:**
- Pode ser adicionado sem mudar versão maior
- Não quebra registros existentes
- Versão menor incrementa (v1.0 → v1.1)

**Campo obrigatório:**
- Exige nova versão maior (v1 → v2)
- Registros antigos continuam válidos sob esquema antigo
- Novos registros devem usar novo esquema

### Como campos são modificados

**Mudança compatível:**
- Tornar campo obrigatório em opcional
- Relaxar restrição (ex: string de 50 chars → 100 chars)
- Adicionar valor aceito em enum

**Mudança incompatível:**
- Tornar campo opcional em obrigatório
- Mudar tipo (string → número)
- Restringir valores (enum com menos opções)
- Renomear campo

### Como campos são removidos

Campos **nunca são removidos**. São **deprecados**:

1. Campo marcado como `[DEPRECADO]` na documentação
2. Campo torna-se opcional (se era obrigatório)
3. Novo esquema recomenda não usar
4. Registros antigos continuam válidos

**Razão filosófica:** conhecimento registrado com campo antigo não se torna inválido porque o domínio evoluiu.

---

## Versionamento

### Semântica de versão

Formato: `vX.Y`

**Versão maior (X):**
- Campo obrigatório adicionado
- Campo modificado incompativelmente
- Validação nova que invalida registros antigos

**Versão menor (Y):**
- Campo opcional adicionado
- Restrição relaxada
- Validação esclarecida sem mudança de comportamento

### Nomenclatura

Formato: `esquema-[entidade]-v[versão].md`

Exemplos:
- `esquema-receita-v1.md`
- `esquema-ingrediente-v2.md`

---

## Compatibilidade

### Princípio de compatibilidade retroativa

Um registro válido sob esquema vN deve permanecer válido indefinidamente, mesmo quando esquema vN+1 existir.

**Implicação:**
O sistema aceita registros de múltiplas versões simultaneamente.

### Mudanças compatíveis

Não exigem nova versão maior:
- Adicionar campo opcional
- Tornar campo obrigatório em opcional
- Relaxar validação
- Esclarecer descrição

### Mudanças incompatíveis

Exigem nova versão maior:
- Adicionar campo obrigatório
- Mudar tipo de campo
- Restringir validação
- Renomear campo

---

## Migração

### Quando migração é necessária

Migração de registros existentes ocorre quando:
1. Usuário deseja adotar novo esquema explicitamente
2. Sistema identifica que campo novo melhora qualidade dos dados

Migração é **sempre opcional**, nunca obrigatória.

### Processo de migração

1. Identificar registros sob esquema antigo
2. Validar que novo esquema é aplicável
3. Adicionar campos novos (opcionais vazios, obrigatórios com valor padrão ou fornecido)
4. Atualizar metadado `versao_esquema`
5. Preservar histórico (versão antiga no git)

### Migração automática vs manual

**Automática:**
- Possível quando campos novos são opcionais
- Sistema adiciona campo vazio
- Usuário preenche depois

**Manual:**
- Necessária quando campos obrigatórios adicionados
- Sistema solicita valores
- Usuário valida antes de confirmar

---

## Relação com Templates

Esquema e template evoluem independentemente:

| Cenário | Esquema | Template |
|---------|---------|----------|
| Novo campo opcional | v1.1 | pode manter v1 |
| Novo campo obrigatório | v2 | v2 recomendado |
| Mudança estrutural visual | v1 | v2 |
| Mudança de tipo | v2 | pode manter v1 |

Registros sempre declaram:
- `versao_esquema: v1`
- `versao_template: v1`

Ambos podem ser diferentes: esquema v2 com template v1 é válido se compatível.

---

## Validação

### Níveis de validação

1. **Estrutural** — campos obrigatórios presentes?
2. **Tipagem** — valores nos tipos corretos?
3. **Restrições** — valores dentro dos limites?
4. **Semântica** — valores fazem sentido no domínio?

### Processo de validação

```
Registro → Parser → Extração de Campos → Validação Estrutural → Validação de Tipos → Validação de Restrições → Validação Semântica → ✓ Válido / ✗ Inválido
```

### Tratamento de erros

- **Erro estrutural** — campo obrigatório faltando → registro rejeitado
- **Erro de tipo** — string onde esperava número → registro rejeitado
- **Erro de restrição** — valor fora do intervalo → registro rejeitado
- **Aviso semântico** — valor atípico mas válido → registro aceito com alerta

---

## Exemplos

### Exemplo 1: Campo opcional adicionado

**esquema-receita-v1.md:**
```
Campos obrigatórios:
- nome (string)
- ingredientes (lista)

Campos opcionais:
- tags (lista de strings)
```

**esquema-receita-v1.1.md:**
```
Campos obrigatórios:
- nome (string)
- ingredientes (lista)

Campos opcionais:
- tags (lista de strings)
- tempo_preparo (número, minutos)  ← NOVO
```

Registros v1 continuam válidos. `tempo_preparo` ausente é aceitável.

---

### Exemplo 2: Campo obrigatório adicionado

**esquema-ingrediente-v1.md:**
```
Campos obrigatórios:
- nome (string)
```

**esquema-ingrediente-v2.md:**
```
Campos obrigatórios:
- nome (string)
- tipo (string, enum: vegetal|animal|mineral)  ← NOVO OBRIGATÓRIO
```

Registros v1 continuam válidos sob v1. Novos registros devem usar v2.

---

### Exemplo 3: Mudança de tipo (incompatível)

**esquema-receita-v1.md:**
```
tempo_preparo (string, ex: "30 minutos")
```

**esquema-receita-v2.md:**
```
tempo_preparo (número, minutos)
```

Incompatível. v2 é novo esquema. Registros v1 permanecem válidos.

---

## Governança

### Quem pode criar esquemas?

Mantenedores do domínio, após análise de requisitos.

### Quem aprova mudanças?

Mudanças menores: revisão técnica.
Mudanças maiores: revisão de domínio + validação de impacto.

### Depreciação de esquemas

Esquemas nunca são excluídos. Podem ser marcados como **deprecados**:

```markdown
# [DEPRECADO] Esquema Receita v1

> Este esquema foi substituído por v2. Registros v1 continuam válidos indefinidamente.
```

---

## Resumo

- Esquema define **conteúdo** (campos, tipos, restrições)
- Esquema versiona com semântica `vX.Y`
- Campos opcionais adicionados: versão menor
- Campos obrigatórios ou mudanças incompatíveis: versão maior
- Campos nunca são removidos, apenas deprecados
- Registros de múltiplas versões coexistem
- Migração é opcional, não obrigatória
- Validação ocorre em 4 níveis: estrutural, tipagem, restrições, semântica
