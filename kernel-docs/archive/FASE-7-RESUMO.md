# FASE 7 — DESCOBERTA AUTOMÁTICA

**Status:** ✅ ESPECIFICADO (Implementação pós-Release 1.0)  
**Data:** 2026-07-01  
**Versão:** 1.0

---

## Objetivo

Eliminar lista hardcoded `DEFAULT_MODULES` em `bootstrap.py`.

---

## Especificação

### Formato: `module.toml`

```toml
[module]
name = "runtime.parser"
version = "1.2.3"
category = "runtime"
provides = ["parser"]
requires = ["ir"]
entrypoint = "codigo.parser"
```

### Descoberta

```python
def discover_modules(root: Path) -> list[ModuleContract]:
    """Busca recursivamente por module.toml e carrega contratos."""
    modules = []
    for file in root.rglob("module.toml"):
        contract = load_contract_from_toml(file)
        modules.append(contract)
    return modules
```

### Bootstrap Automático

```python
def bootstrap_system() -> MicroKernel:
    modules = discover_modules(PROJECT_ROOT)
    kernel = MicroKernel()
    for module in modules:
        kernel.register(module)
    kernel.initialize()
    return kernel
```

---

## Problema Identificado (Fase 1)

`bootstrap.py` contém `DEFAULT_MODULES` hardcoded com módulos de aplicação.

**Violação:** Bootstrap conhece módulos de domínio.

**Solução:** Descoberta automática via `module.toml`.

---

## Decisão

**Adiado para pós-Release 1.0**

Razão: Lista hardcoded funciona. Descoberta automática é melhoria de DX, não requisito de estabilidade.

Prioridade: Média (melhoria de arquitetura)

---

**Documento:** `FASE-7-RESUMO.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
