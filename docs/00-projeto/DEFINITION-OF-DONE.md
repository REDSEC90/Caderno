# Definition of Done — Critérios de Completude

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Padrão Obrigatório  
**Aplicável a partir de:** v0.9.0

---

## 🎯 Propósito

Este documento define quando uma tarefa, feature ou bugfix é considerada **PRONTA (Done)**.

**Nada está "pronto" sem satisfazer todos os critérios.**

---

## ✅ Critérios Universais

### Toda tarefa deve atender:

```
□ IMPLEMENTADA — código escrito e funcional
□ TESTADA — testes automatizados criados e passando
□ TIPADA — type hints completos (mypy strict)
□ DOCUMENTADA — docstrings, comentários, docs atualizadas
□ AUDITADA — FAA sem regressões
□ INTEGRADA — mergeada na branch principal
□ VALIDADA — revisão de código aprovada (se aplicável)
```

---

## 📋 Checklist Detalhada

### 1. Implementação

```
□ Código escrito segue style guide do projeto
□ Funcionalidade implementada conforme especificação
□ Código formatado (ruff format)
□ Sem warnings de lint (ruff check)
□ Sem código comentado ou debug statements
□ Sem TODOs ou FIXMEs não documentados
```

**Validação:**
```bash
ruff check <arquivo>
ruff format <arquivo> --check
```

---

### 2. Testes

```
□ Testes unitários criados para nova funcionalidade
□ Testes de integração atualizados (se aplicável)
□ Testes E2E atualizados (se aplicável)
□ Cobertura do módulo ≥ 90%
□ Todos os testes passando localmente
□ Nenhum teste marcado como @skip sem justificativa
```

**Tipos de teste por contexto:**

| Contexto | Testes Necessários |
|----------|-------------------|
| Nova função pública | Unit + Integration |
| Bugfix | Unit (reproduz bug) + Regression |
| API pública | Unit + Integration + E2E |
| Refactoring | Todos os existentes devem passar |
| Performance | Benchmark (se aplicável) |

**Validação:**
```bash
pytest <arquivo_teste> -v
pytest --cov=<módulo> --cov-report=term
```

---

### 3. Type Hints

```
□ Type hints em todas as funções públicas
□ Type hints em todas as funções privadas (se complexas)
□ Parâmetros tipados (incluindo *args, **kwargs)
□ Retorno tipado (incluindo None)
□ mypy --strict sem erros no módulo
□ Uso de Union, Optional, Generic quando apropriado
```

**Exemplo correto:**
```python
def processar_entidade(
    entidade_id: str,
    opcoes: dict[str, Any] | None = None
) -> tuple[bool, str]:
    """Processa entidade e retorna sucesso e mensagem."""
    ...
```

**Validação:**
```bash
mypy --strict <arquivo>
```

---

### 4. Documentação

```
□ Docstring na função/classe (formato Google ou NumPy)
□ Parâmetros documentados
□ Retorno documentado
□ Exceções documentadas
□ Exemplos de uso (se API pública)
□ Comentários em código complexo
□ CHANGELOG.md atualizado (se necessário)
□ README.md atualizado (se API pública)
□ INDICE-MESTRE.md atualizado (se novo módulo)
```

**Template de docstring:**
```python
def funcao_exemplo(param1: str, param2: int = 0) -> bool:
    """Descrição breve de uma linha.
    
    Descrição detalhada opcional explicando comportamento,
    casos de uso e considerações importantes.
    
    Args:
        param1: Descrição do parâmetro 1
        param2: Descrição do parâmetro 2 (padrão: 0)
    
    Returns:
        True se sucesso, False caso contrário.
    
    Raises:
        ValueError: Se param1 está vazio
        RuntimeError: Se operação falha
    
    Examples:
        >>> funcao_exemplo("teste", 42)
        True
    """
    ...
```

**Validação:**
```bash
# Verificar se docstring existe
python -c "import <módulo>; help(<módulo>.<função>)"
```

---

### 5. Auditoria (FAA)

```
□ FAA executado localmente
□ Score FAA não regrediu (comparar com snapshot anterior)
□ Novas violações justificadas em comentário
□ Snapshot atualizado (se necessário)
```

**Validação:**
```bash
./scripts/faa.sh
# Comparar score com último snapshot
```

---

### 6. Integração

```
□ Branch atualizada com main/master
□ Conflitos resolvidos
□ Commit message segue convenção do projeto
□ Pipeline CI passou (se existir)
□ Aprovação de code review (se aplicável)
□ Merge sem --force
```

**Formato de commit:**
```
tipo(escopo): descrição breve

Descrição detalhada opcional.

Refs: #issue-number
```

**Tipos válidos:**
- `feat` — nova funcionalidade
- `fix` — correção de bug
- `docs` — apenas documentação
- `test` — apenas testes
- `refactor` — refatoração sem mudança de comportamento
- `perf` — melhoria de performance
- `chore` — tarefas de manutenção

---

### 7. Validação (Code Review)

```
□ Pull request criado (se workflow com PR)
□ Descrição clara do que foi feito e por quê
□ Checklist de DoD preenchida
□ Aprovação de pelo menos 1 revisor (v1.0+)
□ Feedback incorporado
□ CI verde antes de merge
```

---

## 🚫 Casos Especiais

### Hotfix Crítico

**Pode relaxar:**
- Code review (se urgente)
- Documentação extensiva

**NÃO pode relaxar:**
- Testes (obrigatório reproduzir bug + fix)
- Type hints
- FAA (não pode regredir)
- Pipeline (deve passar)

### Refactoring

**Deve garantir:**
- Todos os testes anteriores passam
- Cobertura não regride
- Comportamento externo inalterado

**Pode não ter:**
- Novos testes (se comportamento inalterado)

### Documentação Only

**Deve garantir:**
- Links válidos
- Exemplos funcionam
- Sincronização com código

**Não requer:**
- Novos testes
- Type hints

---

## 📊 Definition of Done por Tipo

### Nova Feature

```
✓ IMPLEMENTADA
✓ TESTADA (unit + integration + E2E)
✓ TIPADA (mypy strict)
✓ DOCUMENTADA (docstrings + README + CHANGELOG)
✓ AUDITADA (FAA sem regressão)
✓ INTEGRADA (mergeada)
✓ VALIDADA (code review aprovado)
```

### Bugfix

```
✓ IMPLEMENTADA (correção aplicada)
✓ TESTADA (teste reproduz bug + fix)
✓ TIPADA (mantém type hints)
✓ DOCUMENTADA (CHANGELOG atualizado)
✓ AUDITADA (FAA sem regressão)
✓ INTEGRADA (mergeada)
✓ VALIDADA (opcional para hotfix)
```

### Refactoring

```
✓ IMPLEMENTADA (código reestruturado)
✓ TESTADA (todos os testes anteriores passam)
✓ TIPADA (type hints mantidos/melhorados)
✓ DOCUMENTADA (docstrings atualizadas se necessário)
✓ AUDITADA (FAA sem regressão, pode melhorar)
✓ INTEGRADA (mergeada)
✓ VALIDADA (code review aprovado)
```

### Documentação

```
✓ IMPLEMENTADA (docs escritas)
✓ TESTADA (exemplos validados, links funcionam)
✓ TIPADA (N/A)
✓ DOCUMENTADA (sincronizada com código)
✓ AUDITADA (FAA doc score melhorado)
✓ INTEGRADA (mergeada)
✓ VALIDADA (revisão de clareza)
```

---

## 🔍 Validação Automatizada

### Script de Validação

```bash
#!/bin/bash
# scripts/automacao/validate-dod.sh

echo "=== Definition of Done Validation ==="

# 1. Lint
echo "[1/7] Lint..."
ruff check codigo/ kernel/ || exit 1

# 2. Format
echo "[2/7] Format check..."
ruff format --check codigo/ kernel/ || exit 1

# 3. Type check
echo "[3/7] Type check..."
mypy --strict codigo/ kernel/ || exit 1

# 4. Tests
echo "[4/7] Tests..."
pytest -v || exit 1

# 5. Coverage
echo "[5/7] Coverage..."
pytest --cov=codigo --cov=kernel --cov-report=term | grep "TOTAL" | grep -E "[0-9]{2,3}%" || exit 1

# 6. FAA
echo "[6/7] FAA audit..."
./scripts/faa.sh || exit 1

# 7. Docs
echo "[7/7] Doc check..."
# Verificar se CHANGELOG tem entry recente
grep "$(date +%Y-%m-%d)" CHANGELOG.md || echo "Warning: CHANGELOG não atualizado hoje"

echo "✅ Definition of Done: PASS"
```

**Uso:**
```bash
./scripts/automacao/validate-dod.sh
```

---

## 📐 Responsabilidades

### Desenvolvedor

- Garantir que tarefa atende DoD antes de marcar como pronta
- Executar validação automatizada
- Preencher checklist em PR/issue

### Revisor

- Verificar que DoD foi satisfeita
- Rejeitar se critérios não atendidos
- Usar checklist como guia de revisão

### CI/CD

- Enforçar critérios automatizáveis
- Bloquear merge se DoD não satisfeita
- Gerar relatório de conformidade

---

## 🔄 Evolução deste Documento

### Adicionar Critérios

Critérios podem ser adicionados se:
- Melhoram qualidade
- São objetivamente verificáveis
- Não criam burocracia excessiva

### Remover Critérios

Critérios **não devem ser removidos**.

Se um critério é inviável:
- Ajustar critério (tornar mais realista)
- Adicionar exceções documentadas
- Nunca simplesmente remover

---

## ✨ Filosofia

> "Done significa: pode ir para produção sem medo."

> "Se você pulou um critério, não está done."

> "DoD não é checklist burocrática. É garantia de qualidade."

---

## 📚 Referências

- `docs/00-projeto/RELEASE-GATE-v1.md` — Critérios de release
- `docs/04-padroes/` — Style guides e convenções
- `CONTRIBUTING.md` — Guia de contribuição

---

**Documento:** `DEFINITION-OF-DONE.md`  
**Tipo:** Padrão Obrigatório  
**Autoridade:** Alta  
**Aplicável a:** Todas as tarefas de desenvolvimento
