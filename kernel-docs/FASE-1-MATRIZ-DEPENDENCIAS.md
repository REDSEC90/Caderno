# FASE 1 — MATRIZ DE DEPENDÊNCIAS

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Validado

---

## Visão Geral

A matriz documenta **quem depende de quem** no Kernel.

Toda dependência circular é proibida e detectada automaticamente.

---

## Matriz Completa

```
┌─────────────────────────────────────────────────────────────┐
│                     KERNEL DEPENDENCY GRAPH                  │
└─────────────────────────────────────────────────────────────┘

Nível 0 (Base — sem dependências)
═════════════════════════════════════
shared/paths.py
contracts/module.py
lifecycle/manager.py


Nível 1 (Depende apenas de Nível 0)
═════════════════════════════════════
contracts/validator.py
    ↓ shared/paths.py

registry/module_registry.py
    ↓ contracts/module.py


Nível 2 (Depende de Nível 0 e 1)
═════════════════════════════════════
core/kernel.py
    ↓ contracts/module.py
    ↓ lifecycle/manager.py
    ↓ registry/module_registry.py


Nível 3 (Ponto de entrada)
═════════════════════════════════════
bootstrap.py
    ↓ core/kernel.py
    ↓ contracts/module.py
    ↓ shared/paths.py
```

---

## Tabela de Dependências

| Módulo | Depende De | Dependentes |
|--------|------------|-------------|
| `shared/paths.py` | — | `bootstrap.py`, `contracts/validator.py`, externos |
| `contracts/module.py` | — | `bootstrap.py`, `core/kernel.py`, `registry/module_registry.py` |
| `lifecycle/manager.py` | — | `core/kernel.py` |
| `contracts/validator.py` | `shared/paths.py` | testes, CI/CD |
| `registry/module_registry.py` | `contracts/module.py` | `core/kernel.py` |
| `core/kernel.py` | `contracts/module.py`, `lifecycle/manager.py`, `registry/module_registry.py` | `bootstrap.py` |
| `bootstrap.py` | `core/kernel.py`, `contracts/module.py`, `shared/paths.py` | aplicações, testes |

---

## Grafo Visual

```
                    bootstrap.py
                         │
                         │ usa
                         ↓
                   core/kernel.py
                    ┌────┴────┐
                    │         │
                    ↓         ↓
          registry/       lifecycle/
       module_registry.py  manager.py
                │
                ↓
          contracts/
           module.py


          contracts/          shared/
          validator.py        paths.py
                │
                ↓
            shared/
            paths.py
```

---

## Regras de Dependência

### Proibições Absolutas

1. ❌ **Dependências circulares**
   ```
   A → B → A  (PROIBIDO)
   ```

2. ❌ **Dependência de camadas superiores**
   ```
   core/kernel.py → bootstrap.py  (PROIBIDO)
   ```

3. ❌ **Dependência de módulos externos**
   ```
   kernel/* → codigo/*  (PROIBIDO)
   kernel/* → scripts/*  (PROIBIDO)
   ```

4. ❌ **Dependência de lógica de negócio**
   ```
   kernel/* → qualquer domínio  (PROIBIDO)
   ```

### Permissões

1. ✅ **Dependência de módulos base**
   ```
   qualquer → shared/paths.py  (OK)
   qualquer → contracts/module.py  (OK)
   ```

2. ✅ **Dependência da stdlib**
   ```
   qualquer → sys, pathlib, dataclasses, etc.  (OK)
   ```

3. ✅ **Dependência de níveis inferiores**
   ```
   Nível 2 → Nível 1  (OK)
   Nível 2 → Nível 0  (OK)
   ```

---

## Validação Automática

O validador (`contracts/validator.py`) verifica automaticamente:

- ✅ Isolamento do Kernel (não importa de fora)
- ✅ Ausência de manipulações de `sys.path` (exceto em adaptadores)
- ✅ Existência de componentes obrigatórios

Rodar validação:

```python
from kernel.contracts.validator import assert_architecture_valid

assert_architecture_valid()  # Levanta exceção se houver problemas
```

---

## Análise de Impacto

### Se `shared/paths.py` mudar:

**Impacto direto:**
- `bootstrap.py`
- `contracts/validator.py`

**Impacto indireto:**
- Todos os módulos externos

**Risco:** 🟡 Médio (usado amplamente)

---

### Se `contracts/module.py` mudar:

**Impacto direto:**
- `bootstrap.py`
- `core/kernel.py`
- `registry/module_registry.py`

**Impacto indireto:**
- Toda aplicação (todos os módulos usam contratos)

**Risco:** 🔴 Alto (base do sistema)

---

### Se `lifecycle/manager.py` mudar:

**Impacto direto:**
- `core/kernel.py`

**Impacto indireto:**
- `bootstrap.py`

**Risco:** 🟢 Baixo (encapsulado)

---

### Se `registry/module_registry.py` mudar:

**Impacto direto:**
- `core/kernel.py`

**Impacto indireto:**
- `bootstrap.py`

**Risco:** 🟢 Baixo (encapsulado)

---

### Se `core/kernel.py` mudar:

**Impacto direto:**
- `bootstrap.py`

**Impacto indireto:**
- Todas as aplicações

**Risco:** 🟡 Médio (API pública principal)

---

### Se `bootstrap.py` mudar:

**Impacto direto:**
- Aplicações que usam `bootstrap_system()`

**Impacto indireto:**
- Nenhum (é o topo da cadeia)

**Risco:** 🟢 Baixo (ponto de entrada)

---

## Estatísticas

| Métrica | Valor |
|---------|-------|
| Módulos no Kernel | 6 |
| Dependências totais | 9 |
| Dependências circulares | 0 ✅ |
| Nível máximo de profundidade | 3 |
| Módulos base (Nível 0) | 3 |
| Módulos intermediários (Nível 1) | 2 |
| Módulos de coordenação (Nível 2) | 1 |
| Pontos de entrada (Nível 3) | 1 |

---

## Próximos Passos

**Fase 2 — Consolidação do ModuleContract**

- Expandir campos do contrato
- Adicionar metadados (autor, checksum, signature)
- Criar schema oficial

---

**Documento:** `FASE-1-MATRIZ-DEPENDENCIAS.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
