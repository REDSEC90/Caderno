# Feature Freeze — Congelamento de Funcionalidades

**Versão:** 1.0  
**Data de Início:** 2026-07-01 (tag v0.8.1)  
**Data de Término:** Release v1.0.0  
**Status:** ATIVO  
**Autoridade:** Máxima

---

## 🎯 Declaração Oficial

> **A partir da tag v0.8.1, NENHUMA nova funcionalidade poderá ser adicionada ao SOE-CCG até a publicação da versão v1.0.0.**

Este congelamento é **obrigatório** e **sem exceções**.

---

## 📋 O Que Está Congelado

### ❌ PROIBIDO até v1.0

```
✗ Novas entidades (FON, PRC, PRD, LOT)
✗ Novos comandos CLI
✗ Novas APIs públicas
✗ Novos módulos em kernel/
✗ Novos módulos em codigo/
✗ Novas features de importação/exportação
✗ Novos formatos de arquivo
✗ Novas integrações externas
✗ Mudanças em schema de entidades existentes
✗ Novos tipos de relacionamento
✗ Expansão de funcionalidades existentes
```

---

## ✅ O Que É Permitido

### ✓ PERMITIDO durante Feature Freeze

```
✓ Bugfix (correções de bugs)
✓ Documentação (adição, correção, melhoria)
✓ Testes (novos testes, melhoria de cobertura)
✓ Type hints (adição, correção)
✓ Pipeline (automação, CI/CD)
✓ Hardening (robustez, tratamento de erros)
✓ Performance (otimizações que não mudam API)
✓ Refactoring (interno, sem mudança de comportamento)
✓ Tooling (scripts de automação, auditoria)
✓ Linting/formatting
✓ Segurança (correções de vulnerabilidades)
```

---

## 🚫 Exemplos Detalhados

### ❌ NÃO Permitido

**Exemplo 1: Nova entidade**
```python
# ❌ PROIBIDO
class Fonte:
    """Nova entidade para rastreabilidade científica."""
    ...
```

**Exemplo 2: Novo comando CLI**
```bash
# ❌ PROIBIDO
python -m codigo export --format=json
```

**Exemplo 3: Nova API pública**
```python
# ❌ PROIBIDO
def exportar_para_json(grafo: KnowledgeGraph) -> str:
    """Nova funcionalidade de exportação."""
    ...
```

---

### ✅ Permitido

**Exemplo 1: Bugfix**
```python
# ✅ PERMITIDO
def importar(grafo, db):
    # Fix: tratamento de erro quando banco não existe
    if not db.exists():
        raise ImportError(f"Banco {db} não encontrado")
    ...
```

**Exemplo 2: Documentação**
```python
# ✅ PERMITIDO
def parse_file(path: Path) -> Entity:
    """Parseia arquivo Markdown e retorna entidade.
    
    Args:
        path: Caminho do arquivo
    
    Returns:
        Entidade parseada
    
    Examples:
        >>> entity = parse_file(Path("receitas/REC-000001.md"))
        >>> entity.id
        'REC-000001'
    """
    ...
```

**Exemplo 3: Type hints**
```python
# ✅ PERMITIDO
# Antes
def resolver(grafo):
    ...

# Depois
def resolver(grafo: KnowledgeGraph) -> list[ResolverError]:
    ...
```

**Exemplo 4: Hardening**
```python
# ✅ PERMITIDO
def parse_file(path: Path) -> Entity:
    # Hardening: validar tamanho do arquivo
    if path.stat().st_size > 10_000_000:  # 10MB
        raise ParseError(f"Arquivo muito grande: {path}")
    
    # Hardening: tratamento de encoding
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise ParseError(f"Encoding inválido: {path}")
    ...
```

---

## 🔍 Processo de Aprovação

### Para Qualquer Mudança

1. **Classificar mudança:**
   - É bugfix? → Permitido
   - É documentação? → Permitido
   - É nova feature? → BLOQUEADO

2. **Se dúvida, documentar:**
   - Criar issue explicando
   - Justificar por que é necessário
   - Classificar segundo critérios deste documento

3. **Se nova feature:**
   - **REJEITAR imediatamente**
   - Adicionar ao backlog pós-v1.0
   - Documentar em `docs/99-referencias/BACKLOG-v1.x.md`

---

## 📊 Monitoramento

### Validação Automatizada

```bash
# scripts/automacao/validate-freeze.sh

#!/bin/bash

echo "=== Feature Freeze Validation ==="

# Verifica se novos arquivos foram adicionados em áreas sensíveis
NEW_KERNEL=$(git diff --name-status v0.8.1..HEAD | grep "^A.*kernel/" | wc -l)
NEW_CODIGO=$(git diff --name-status v0.8.1..HEAD | grep "^A.*codigo/" | wc -l)

if [ $NEW_KERNEL -gt 0 ]; then
    echo "⚠️  Warning: $NEW_KERNEL novos arquivos em kernel/"
    echo "   Revisar se são features ou apenas testes/docs"
fi

if [ $NEW_CODIGO -gt 0 ]; then
    echo "⚠️  Warning: $NEW_CODIGO novos arquivos em codigo/"
    echo "   Revisar se são features ou apenas testes/docs"
fi

# Verifica se houve mudanças em schemas
SCHEMA_CHANGES=$(git diff v0.8.1..HEAD -- "docs/01-dominio/esquemas/" | wc -l)

if [ $SCHEMA_CHANGES -gt 0 ]; then
    echo "❌ BLOCKED: Mudanças em schemas durante Feature Freeze"
    exit 1
fi

echo "✅ Feature Freeze: OK"
```

---

## 🚨 Violações

### O Que Acontece se Feature Freeze for Violada

1. **Pull request é rejeitado**
2. **Commit é revertido**
3. **Issue é aberto para documentar violação**
4. **Feature vai para backlog v1.x**

### Não Há Exceções

- Nem para "feature pequena"
- Nem para "feature já quase pronta"
- Nem para "feature solicitada por usuário"

**Todas as features vão para v1.x.**

---

## 📅 Duração

### Início

**Tag:** v0.8.1  
**Data:** 2026-07-01

### Término

**Tag:** v1.0.0  
**Data prevista:** 2026-08-15 (4-6 semanas)

### Após v1.0

Feature Freeze é **levantado**.

Novas features podem ser adicionadas em v1.1, v1.2, etc.

Mas sempre:
- Sem breaking changes (até v2.0)
- Seguindo API Stability Policy
- Passando por Release Gate

---

## 🎯 Justificativa

### Por Que Feature Freeze?

**1. Focar em qualidade**
- Automação (pipeline)
- Testes (cobertura ≥95%)
- Docs (completas e atualizadas)
- Robustez (hardening)

**2. Evitar scope creep**
- v1.0 nunca seria alcançada
- Cada feature adia release
- Features aumentam risco

**3. Estabilizar arquitetura**
- Código maduro → mais confiável
- APIs estáveis → commitment possível
- Processo reproduzível → sustentável

**4. Preparar para longo prazo**
- v1.0 = base sólida
- v1.x = evolução incremental
- v2.0 = breaking changes (futuro distante)

---

## 📚 Backlog pós-v1.0

### Features Planejadas para v1.x

```
□ Entidades expandidas (FON, PRC, PRD, LOT)
□ Comando de exportação (JSON, YAML)
□ Modo interativo do CLI
□ Validação strict mode (--strict)
□ Benchmark automatizado
□ Relatórios de auditoria
```

**Local:** `docs/99-referencias/BACKLOG-v1.x.md`

---

## ✨ Filosofia

> "Feature Freeze não é limitação. É disciplina."

> "v1.0 não precisa de mais features. Precisa de mais confiabilidade."

> "Adicionar features é fácil. Manter qualidade é difícil."

> "Features sempre podem esperar. Qualidade não pode."

---

## 📖 Referências

- `docs/00-projeto/RELEASE-GATE-v1.md` — Critérios de release
- `docs/00-projeto/API-STABILITY.md` — Política de estabilidade
- `docs/00-projeto/VERSIONING.md` — Política de versionamento
- `ROADMAP-v1.0.md` — Roadmap até v1.0

---

**Documento:** `FEATURE-FREEZE-v1.md`  
**Tipo:** Política Obrigatória  
**Autoridade:** Máxima  
**Vigência:** v0.8.1 → v1.0.0  
**Violações:** Não permitidas, sem exceções
