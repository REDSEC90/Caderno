# Release Gate — Critérios Obrigatórios para Release

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Lei do Projeto  
**Aplicável a partir de:** v0.9.0

---

## 🎯 Propósito

Este documento define os **critérios obrigatórios** que devem ser satisfeitos antes de qualquer release oficial do SOE-CCG.

**Nenhuma release ocorre sem passar por todos os gates.**

---

## 🚪 Gates Obrigatórios

### Gate 1: Testes

```
□ Todos os testes passaram (100%)
□ Nenhum teste desabilitado ou marcado como @skip
□ Tempo de execução total < 10 minutos
□ Zero falhas intermitentes (flaky tests)
```

**Comando de validação:**
```bash
make test
# Deve retornar exit code 0
# Todos os testes devem passar
```

---

### Gate 2: Cobertura de Código

```
□ Cobertura global ≥ 95%
□ Nenhum módulo crítico < 90%
□ Branches cobertas ≥ 90%
□ Relatório de cobertura gerado
```

**Módulos críticos:**
- `kernel/`
- `codigo/`

**Comando de validação:**
```bash
make coverage
# coverage.json deve mostrar ≥95%
```

---

### Gate 3: Qualidade de Código (Lint)

```
□ Ruff: 0 erros
□ Ruff: 0 avisos críticos
□ Formatação consistente (ruff format --check)
□ Sem código comentado (TODO/FIXME resolvidos ou documentados)
```

**Comando de validação:**
```bash
make lint
# Deve retornar exit code 0
```

---

### Gate 4: Type Checking

```
□ mypy --strict: 0 erros
□ Todos os módulos públicos tipados
□ Nenhum uso de 'Any' não justificado
□ Type stubs para dependências externas (se necessário)
```

**Comando de validação:**
```bash
make type-check
# mypy --strict codigo/ kernel/
# Deve retornar exit code 0
```

---

### Gate 5: Auditoria de Qualidade (FAA)

```
□ FAA score ≥ 95 (v1.0)
□ FAA score ≥ 92 (v0.9.5)
□ FAA score ≥ 90 (v0.9.0)
□ Snapshot criado e arquivado
□ Nenhuma violação crítica não documentada
```

**Comando de validação:**
```bash
make audit
# FAA deve gerar snapshot em docs/99-referencias/snapshots/
# Score deve estar acima do mínimo
```

---

### Gate 6: Documentação

```
□ README.md atualizado com versão correta
□ CHANGELOG.md contém entry da versão
□ Todos os módulos públicos documentados
□ Exemplos de uso funcionam
□ Links internos válidos (sem 404)
□ INDICE-MESTRE.md sincronizado
```

**Comando de validação:**
```bash
make doc-check
# Valida links, sincronização, exemplos
```

---

### Gate 7: Versionamento

```
□ Tag criada no formato vX.Y.Z (semver)
□ CHANGELOG.md contém entry da tag
□ Versão atualizada em:
  - README.md
  - pyproject.toml (se aplicável)
  - __version__ no código
□ Commit de release assinado (GPG, se aplicável)
```

**Comando de validação:**
```bash
git tag -l "v*" | grep <versão>
# Tag deve existir
```

---

### Gate 8: Build Reproduzível

```
□ Build funciona em ambiente limpo
□ Dependências fixadas (requirements.txt ou similar)
□ Instalação testada em Python 3.11+
□ Sem dependências de sistema não documentadas
```

**Comando de validação:**
```bash
# Em virtualenv limpo:
python -m venv test_env
source test_env/bin/activate
pip install -e .
make test
# Deve funcionar sem erros
```

---

### Gate 9: Pipeline Completo

```
□ Pipeline executou sem erros
□ Todos os stages passaram:
  1. Lint
  2. Format check
  3. Type check
  4. Unit tests
  5. Integration tests
  6. E2E tests
  7. FAA audit
  8. Doc validation
  9. Changelog check
□ Tempo total < 10 minutos
```

**Comando de validação:**
```bash
make pipeline
# Deve passar em todos os stages
```

---

### Gate 10: Auditoria Manual (v1.0 apenas)

```
□ Revisão de código por pessoa diferente do autor
□ Teste de instalação em ambiente externo
□ Validação de usabilidade básica
□ Verificação de conformidade com RELEASE-GATE
```

**Checklist:**
- [ ] Código revisado
- [ ] Instalação validada
- [ ] Usabilidade testada
- [ ] Conformidade verificada

---

## 📊 Dashboard de Release Gate

### Comando Único de Validação

```bash
make release-gate
```

**Saída esperada:**

```
╔═══════════════════════════════════════════════════════╗
║             RELEASE GATE — v0.9.0                     ║
╚═══════════════════════════════════════════════════════╝

Gate 1: Testes                 ✅ PASS (516/516)
Gate 2: Cobertura              ✅ PASS (95.2%)
Gate 3: Lint                   ✅ PASS (0 issues)
Gate 4: Type Check             ✅ PASS (0 errors)
Gate 5: FAA                    ✅ PASS (95.3)
Gate 6: Documentação           ✅ PASS
Gate 7: Versionamento          ✅ PASS (v0.9.0)
Gate 8: Build                  ✅ PASS
Gate 9: Pipeline               ✅ PASS (7m32s)
Gate 10: Auditoria Manual      ✅ PASS (v1.0 only)

════════════════════════════════════════════════════════
RELEASE GATE: PASS ✅
Versão v0.9.0 autorizada para release.
════════════════════════════════════════════════════════
```

---

## 🚫 Política de Bloqueio

### Se Qualquer Gate Falhar

1. **Release é BLOQUEADA**
2. **Tag não é criada**
3. **Issue é aberto automaticamente**
4. **Notificação enviada**

### Exceções

**Não há exceções.**

Se um gate falha, a release não ocorre.

Se o gate é inválido, o gate é corrigido (não bypassed).

---

## 📋 Responsabilidades

### Desenvolvedores

- Executar `make release-gate` antes de solicitar release
- Corrigir falhas antes de marcar como "pronto para release"

### Release Manager (se aplicável)

- Validar que todos os gates passaram
- Executar auditoria manual (v1.0)
- Criar tag somente após aprovação completa

### Automatização

- Pipeline deve enforçar gates automaticamente
- Falha em qualquer gate = build failure
- Snapshot FAA deve ser criado automaticamente

---

## 🔄 Evolução deste Documento

### v1.0 (atual)

Gates 1-10 como definidos

### Futuras Versões

Novos gates podem ser adicionados, mas:
- Nunca removidos
- Sempre mais rigorosos (nunca mais permissivos)
- Documentados em ADR correspondente

---

## 📚 Referências

- `docs/00-projeto/DEFINITION-OF-DONE.md` — Critérios para tarefas
- `docs/00-projeto/VERSIONING.md` — Política de versionamento
- `docs/00-projeto/API-STABILITY.md` — Compromisso de estabilidade
- `ROADMAP-v1.0.md` — Roadmap até v1.0

---

## ✨ Filosofia

> "Release Gate não é burocracia. É garantia de qualidade."

> "Se um gate falha, o problema não é o gate. É o código."

> "v1.0 significa: você pode confiar. Gates garantem isso."

---

**Documento:** `RELEASE-GATE-v1.md`  
**Tipo:** Lei do Projeto  
**Autoridade:** Máxima  
**Modificável:** Apenas para adicionar rigor, nunca para relaxar
