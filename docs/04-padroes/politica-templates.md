# Política de Templates

> Como templates nascem, evoluem e garantem compatibilidade.

---

## Definição

Um **template** é um modelo estrutural que define **como** um registro deve ser escrito em Markdown.

Templates são distintos de esquemas:
- **Template** define a forma (estrutura do documento Markdown)
- **Esquema** define o conteúdo (campos obrigatórios e opcionais)

Exemplo: o template diz "use cabeçalhos H2 para seções". O esquema diz "campo 'nome' é obrigatório".

---

## Criação

### Quando um template nasce

Um template nasce quando:
1. Uma nova entidade é definida
2. Uma entidade existente muda de estrutura suficientemente para justificar nova versão

### Processo de criação

1. Identificar necessidade
2. Propor estrutura Markdown
3. Validar contra princípios (legibilidade humana, processabilidade por máquina)
4. Documentar em `docs/01-dominio/templates/`
5. Versionar desde v1

---

## Estrutura

### Anatomia de um template

Todo template deve conter:

```markdown
# [Nome da Entidade] — Template v[N]

## Metadados

[estrutura padronizada de metadados]

## [Seção Principal 1]

[campos e formato esperado]

## [Seção Principal 2]

...

## Exemplo Completo

[exemplo real aplicando este template]
```

### Convenções obrigatórias

1. Metadados sempre no topo
2. Seções principais em H2
3. Subseções em H3 ou inferior
4. Listas para itens relacionados
5. Blocos de código para dados estruturados (quando necessário)

---

## Versionamento

### Quando um template muda de versão

Um template recebe nova versão quando:

**Mudança maior (v1 → v2):**
- Estrutura de seções muda
- Campos obrigatórios mudam de lugar
- Formato quebra compatibilidade com parsers existentes

**Mudança menor (v1.0 → v1.1):**
- Adição de seção opcional
- Esclarecimento de convenção
- Exemplo adicional

### Nomenclatura

Formato: `[entidade]-v[versão].md`

Exemplos:
- `receita-v1.md`
- `ingrediente-v2.md`

Versionamento segue semântica: `vX.Y`
- `X` = versão maior (incompatível)
- `Y` = versão menor (compatível)

Para simplificação, versões menores podem ser omitidas: `v1` = `v1.0`.

---

## Compatibilidade

### Mudanças compatíveis

Não exigem nova versão maior:
- Adicionar seção opcional ao final
- Esclarecer descrição de campo existente
- Adicionar exemplo
- Corrigir erro tipográfico

### Mudanças incompatíveis

Exigem nova versão maior:
- Remover seção
- Renomear seção obrigatória
- Alterar ordem de seções obrigatórias
- Mudar formato de campo obrigatório

### Convivência de versões

Múltiplas versões de template podem coexistir:
- Registros antigos mantêm template original
- Registros novos usam template atual
- Conversão é opcional, nunca obrigatória

---

## Depreciação

### Processo de descontinuação

Um template nunca é excluído, mas pode ser marcado como **deprecado**:

1. Template novo é criado
2. Template antigo recebe marcação `[DEPRECADO]` no título
3. Documentação recomenda migração, mas não força
4. Registros existentes continuam válidos indefinidamente

### Template deprecado permanece suportado

Mesmo deprecado, o template antigo:
- Continua documentado
- Continua sendo aceito pelo sistema
- Pode continuar sendo usado para novos registros (não recomendado, mas permitido)

**Razão filosófica:** conhecimento antigo não deixa de ser válido porque o formato evoluiu.

---

## Relação com Esquemas

Template e esquema são complementares:

| Template | Esquema |
|----------|---------|
| Define forma | Define conteúdo |
| Estrutura Markdown | Campos e tipos |
| Como escrever | O que escrever |
| Visual/legibilidade | Semântica/validação |

Exemplo:

**Template diz:**
```
## Ingredientes

- [quantidade] [unidade] [nome]
```

**Esquema diz:**
```
Campo "ingredientes":
- Tipo: lista
- Obrigatório: sim
- Cada item contém: quantidade (número), unidade (string), nome (string)
```

Ambos devem evoluir juntos, mas possuem versionamento independente.

---

## Exemplos

### Exemplo 1: Adição compatível

**receita-v1.md** original:
```markdown
## Metadados
## Ingredientes
## Modo de Preparo
```

**receita-v1.1.md** atualizado:
```markdown
## Metadados
## Ingredientes
## Modo de Preparo
## Notas (opcional)
```

Mudança menor. v1 continua válido.

---

### Exemplo 2: Mudança incompatível

**ingrediente-v1.md** original:
```markdown
## Metadados
## Informações Básicas
```

**ingrediente-v2.md** novo:
```markdown
## Metadados
## Identidade
## Características
```

Seções mudaram de nome. Versão maior obrigatória. v1 permanece suportado.

---

## Validação

Templates são validados por:

1. **Conformidade filosófica** — legível por humano, processável por máquina?
2. **Consistência estrutural** — segue convenções do SOE-CCG?
3. **Completude** — possui exemplo completo?
4. **Versionamento correto** — mudanças refletem versão adequada?

---

## Governança

### Quem pode criar templates?

Qualquer contribuidor, mas deve seguir esta política.

### Quem aprova novos templates?

Revisão por mantenedores do domínio.

### Quando templates são obrigatórios?

Toda entidade oficial do SOE-CCG deve ter template versionado e documentado.

---

## Resumo

- Template define **forma** (estrutura Markdown)
- Template versiona com semântica `vX.Y`
- Mudanças compatíveis: versão menor
- Mudanças incompatíveis: versão maior
- Templates nunca são excluídos, apenas deprecados
- Templates convivem: registros mantêm versão original
