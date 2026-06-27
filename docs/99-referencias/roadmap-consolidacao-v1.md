---
id: ROADMAP-001
tipo: roadmap
versao: 1
status: ativo
criado-em: 2026-06-26
atualizado-em: 2026-06-26
autor: FAA v2
---

# Roadmap de Consolidação SOE-CCG v1

> Baseado em análise FAA v2 — Score atual: 81.1/100 | Decisão: DEGRADED

---

## 🎯 Objetivo da Fase 1: CONSOLIDAÇÃO v1

Transformar sistema de **v0.5 (draft)** para **v1 (frozen)** com governança ativa.

**Meta:** Score FAA ≥ 95/100 | Decisão: APPROVED

---

## 📊 Estado atual (FAA)

```json
{
  "score": 81.11,
  "decision": "DEGRADED",
  "issues": {
    "critical": 0,
    "warnings": 34
  },
  "missing_critical": ["docs/01-dominio/glossario-v1.md"]
}
```

---

## 🚨 Bloqueador crítico

❌ **Arquivo ausente:** `docs/01-dominio/glossario-v1.md`

**Ação:** Criar glossário consolidado v1 com todos os termos do domínio.

---

## 📋 Tarefas de consolidação v0.5 → v1

### Prioridade 1: Domínio (12 arquivos)

| Arquivo v0.5 | Ação | Status |
|--------------|------|--------|
| `template-especificacao-entidade-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogacao-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `template-contrato-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `separacao-dominios-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `linguagem-soe-ccg-v0_5.md` | Revisar + renomear → v1 | ⏳ |

### Prioridade 2: Catálogos (10 arquivos)

| Arquivo v0.5 | Ação | Status |
|--------------|------|--------|
| `catalogos/categorias-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/tipos-equipamentos-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/tipos-tecnicas-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/tipos-ingredientes-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/estados-receita-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/unidades-medida-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/estados-todas-entidades-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `catalogos/catalogos-expandidos-v0_5.md` | Revisar + renomear → v1 | ⏳ |

### Prioridade 3: Arquitetura (1 arquivo)

| Arquivo v0.5 | Ação | Status |
|--------------|------|--------|
| `diagrama-mestre-v0_5.md` | Revisar + renomear → v1 | ⏳ |

### Prioridade 4: Desenvolvimento (2 arquivos)

| Arquivo v0.5 | Ação | Status |
|--------------|------|--------|
| `padroes-desenvolvimento-v0_5.md` | Revisar + renomear → v1 | ⏳ |
| `casos-de-uso-v0_5.md` | Revisar + renomear → v1 | ⏳ |

### Prioridade 5: Operação (1 arquivo)

| Arquivo v0.5 | Ação | Status |
|--------------|------|--------|
| `guia-operacao-v0_5.md` | Revisar + renomear → v1 | ⏳ |

### Prioridade 6: Referências (arquivar)

| Arquivo v0.5 | Ação | Status |
|--------------|------|--------|
| Todos em `99-referencias/*-v0_5.md` | Mover para `99-referencias/archive/` | ⏳ |

**Total:** 28 arquivos para consolidar

---

## 🔄 Processo de consolidação (por arquivo)

1. **Revisar conteúdo** — garantir completude
2. **Validar contra contrato** — se aplicável
3. **Atualizar metadados** — frontmatter com versão correta
4. **Renomear** — substituir `-v0_5` por `-v1`
5. **Validar FAA** — executar `./scripts/faa.sh validate`
6. **Commit** — com mensagem: "feat: consolidate [arquivo] to v1"

---

## 🎯 Critérios de aceitação v1

- [ ] Todos os 28 arquivos v0.5 consolidados para v1
- [ ] Glossário v1 criado
- [ ] Score FAA ≥ 95/100
- [ ] 0 problemas críticos
- [ ] < 5 warnings
- [ ] Decisão FAA: APPROVED
- [ ] Snapshot v1 criado

---

## 📊 Métricas de progresso

```bash
# Verificar progresso
./scripts/faa.sh status

# Ver próximas ações
./scripts/faa.sh plan

# Criar snapshot após cada lote
./scripts/faa.sh snapshot
```

---

## 🚀 Execução por lotes

### Lote 1: Bloqueador + Domínio core (6 arquivos)
**Prazo:** 1 sessão  
**Impacto:** Desbloqueia sistema + define linguagem

1. Criar `glossario-v1.md`
2. Consolidar templates (especificação, contrato)
3. Consolidar separacao-dominios, linguagem, catalogacao

### Lote 2: Catálogos (10 arquivos)
**Prazo:** 1 sessão  
**Impacto:** Define taxonomia completa

### Lote 3: Arquitetura + Dev + Ops (4 arquivos)
**Prazo:** 1 sessão  
**Impacto:** Consolida estrutura técnica

### Lote 4: Limpeza (8 arquivos)
**Prazo:** 1 sessão  
**Impacto:** Arquiva referências temporárias

---

## 🧠 FAA como ferramenta de validação

Após cada lote:

```bash
# 1. Executar auditoria
./scripts/faa.sh validate --snapshot

# 2. Verificar decisão
./scripts/faa.sh status | grep "Decisão"

# 3. Se BLOCKED → corrigir críticos
./scripts/faa.sh issues --critical

# 4. Se DEGRADED → ver próximas ações
./scripts/faa.sh plan | head -20

# 5. Commit quando APPROVED
```

---

## 📈 Evolução esperada do score

| Lote | Score esperado | Decisão |
|------|----------------|---------|
| Atual | 81.1 | DEGRADED |
| Lote 1 | ~85.0 | DEGRADED |
| Lote 2 | ~90.0 | DEGRADED |
| Lote 3 | ~95.0 | APPROVED |
| Lote 4 | ~98.0 | APPROVED |

---

## 🎓 Regras de versionamento (lembrete)

1. **-v1** = versão frozen, não pode ser modificada
2. Modificações criam **-v2** como novo arquivo
3. v1 permanece como referência histórica
4. FAA valida que arquivos vN não são alterados (implementar em v2.1)

---

## 📅 Próximos passos após v1

1. **Fase 2:** Expansão controlada de dados
   - Adicionar receitas
   - Adicionar técnicas
   - Adicionar ingredientes
   
2. **Fase 3:** Enriquecimento de relacionamentos
   - Criar grafo de dependências
   - Validar integridade referencial
   
3. **Fase 4:** FAA v2.1
   - Diff entre snapshots
   - Validação de imutabilidade vN
   - Grafo de dependências

---

## ✅ Checklist de finalização v1

- [ ] 28 arquivos consolidados
- [ ] Glossário v1 criado
- [ ] FAA score ≥ 95
- [ ] Snapshot v1 oficial criado
- [ ] Tag git: `v1.0-consolidated`
- [ ] README atualizado com status v1
- [ ] Documento de freeze publicado

---

**Status:** ⏳ AGUARDANDO EXECUÇÃO  
**Responsável:** Desenvolvimento SOE-CCG  
**Ferramenta de controle:** FAA v2  
**Próxima ação:** Executar Lote 1
