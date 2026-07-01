# FASE 1 — RESPONSABILIDADES DOS MÓDULOS

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Consolidado

---

## 1. Bootstrap (`bootstrap.py`)

### Objetivo

Inicializar o Kernel e descobrir módulos.

### Responsabilidades

1. ✅ Garantir que `PROJECT_ROOT` esteja em `sys.path`
2. ✅ Registrar módulos padrão (`DEFAULT_MODULES`)
3. ✅ Registrar módulos adicionais opcionais
4. ✅ Inicializar o Kernel
5. ✅ Retornar instância configurada de `MicroKernel`

### Quem Pode Utilizá-lo

- **Aplicações** que precisam inicializar o SOE-CCG
- **Testes** que precisam de um Kernel configurado

### Quem Depende Dele

Nenhum módulo interno depende de `bootstrap`. Ele é o **ponto de entrada**.

### Quem Ele Pode Importar

- ✅ `kernel.core.MicroKernel`
- ✅ `kernel.contracts.ModuleContract`
- ✅ `kernel.shared.paths`
- ✅ `sys` (stdlib)

### Quem Ele NUNCA Poderá Importar

- ❌ Módulos de `codigo/`
- ❌ Módulos de `scripts/`
- ❌ Qualquer módulo de domínio

**Razão:** Bootstrap não deve conhecer lógica de negócio.

### Estado Atual

✅ Implementado e estável

### Observações

- `DEFAULT_MODULES` contém a lista de módulos padrão do sistema
- Essa lista **não deveria estar aqui** (violação de separação)
- **Ação futura (Fase 7):** Mover para descoberta automática via `module.toml`

---

## 2. Core (`core/kernel.py`)

### Objetivo

Coordenar Registry, Lifecycle e Contracts sem lógica de negócio.

### Responsabilidades

1. ✅ Manter instância de `ModuleRegistry`
2. ✅ Manter instância de `KernelLifecycle`
3. ✅ Delegar registro de módulos ao Registry
4. ✅ Delegar validação de dependências ao Registry
5. ✅ Delegar transições de estado ao Lifecycle
6. ✅ Expor ordem de inicialização via `startup_order()`

### Quem Pode Utilizá-lo

- **Bootstrap** — inicializa o Kernel
- **Testes** — verificam comportamento do Kernel

### Quem Depende Dele

- `bootstrap.py` — único consumidor direto

### Quem Ele Pode Importar

- ✅ `kernel.contracts.ModuleContract`
- ✅ `kernel.lifecycle.KernelLifecycle`
- ✅ `kernel.lifecycle.LifecycleState`
- ✅ `kernel.registry.ModuleRegistry`

### Quem Ele NUNCA Poderá Importar

- ❌ `bootstrap.py`
- ❌ Módulos de `codigo/`
- ❌ Módulos de `scripts/`
- ❌ Módulos de domínio

**Razão:** O Core é a base. Não pode depender de camadas superiores.

### Estado Atual

✅ Implementado e estável

### Observações

- É a única classe que coordena Registry e Lifecycle
- Não contém lógica de negócio
- Puro coordenador estrutural

---

## 3. Contracts (`contracts/`)

### 3.1. `module.py`

#### Objetivo

Definir o contrato declarativo de módulos.

#### Responsabilidades

1. ✅ Representar metadados de um módulo (`name`, `version`, `provides`, `requires`)
2. ✅ Validar estrutura do contrato
3. ✅ Detectar conflitos (provides/requires simultâneos)
4. ✅ Levantar `ContractError` em caso de invalidade

#### Quem Pode Utilizá-lo

- **Todos os módulos do Kernel**
- **Módulos de aplicação** que se registram no Kernel

#### Quem Depende Dele

- `bootstrap.py`
- `core/kernel.py`
- `registry/module_registry.py`
- `contracts/validator.py`

#### Quem Ele Pode Importar

- ✅ `dataclasses` (stdlib)

#### Quem Ele NUNCA Poderá Importar

- ❌ Qualquer outro módulo do Kernel
- ❌ Qualquer módulo externo

**Razão:** É a base de tudo. Não deve depender de nada.

#### Estado Atual

✅ Implementado e estável

---

### 3.2. `validator.py`

#### Objetivo

Validar a arquitetura do projeto.

#### Responsabilidades

1. ✅ Verificar existência de `kernel-docs/`
2. ✅ Verificar existência de `kernel/registry/module_registry.py`
3. ✅ Verificar que há apenas uma raiz de código
4. ✅ Verificar isolamento do Kernel (não importa de fora)
5. ✅ Verificar que não há manipulações de `sys.path` fora de adaptadores
6. ✅ Retornar `ValidationResult` estruturado

#### Quem Pode Utilizá-lo

- **Testes de contrato** — validam arquitetura
- **Pipelines de CI/CD** — verificam conformidade

#### Quem Depende Dele

- Nenhum módulo interno depende dele (é auxiliar)

#### Quem Ele Pode Importar

- ✅ `ast` (stdlib)
- ✅ `pathlib` (stdlib)
- ✅ `dataclasses` (stdlib)
- ✅ `kernel.shared.paths`

#### Quem Ele NUNCA Poderá Importar

- ❌ Módulos de `codigo/`
- ❌ Módulos de `scripts/`

**Razão:** Validação arquitetural não deve depender do sistema validado.

#### Estado Atual

✅ Implementado e estável

---

## 4. Lifecycle (`lifecycle/manager.py`)

### Objetivo

Gerenciar estados do Kernel de forma determinística.

### Responsabilidades

1. ✅ Manter estado atual (`LifecycleState`)
2. ✅ Validar transições de estado
3. ✅ Executar transições válidas
4. ✅ Levantar `LifecycleError` em transições inválidas

### Quem Pode Utilizá-lo

- **Core** — único consumidor

### Quem Depende Dele

- `core/kernel.py`

### Quem Ele Pode Importar

- ✅ `enum` (stdlib)

### Quem Ele NUNCA Poderá Importar

- ❌ Qualquer outro módulo do Kernel
- ❌ Qualquer módulo externo

**Razão:** Máquina de estados pura. Não deve ter dependências.

### Estado Atual

✅ Implementado e estável

### Observações

- Estados atuais: `CREATED`, `INITIALIZED`, `RUNNING`, `STOPPED`
- **Expansão futura (Fase 3):** Adicionar estados intermediários

---

## 5. Registry (`registry/module_registry.py`)

### Objetivo

Manter registro de módulos e resolver dependências.

### Responsabilidades

1. ✅ Registrar contratos de módulos
2. ✅ Validar contratos ao registrar
3. ✅ Detectar conflitos de capabilities
4. ✅ Detectar módulos duplicados
5. ✅ Validar dependências globais
6. ✅ Resolver ordem de inicialização (topological sort)
7. ✅ Detectar dependências circulares
8. ✅ Fornecer acesso a módulos por nome ou capability

### Quem Pode Utilizá-lo

- **Core** — único consumidor

### Quem Depende Dele

- `core/kernel.py`

### Quem Ele Pode Importar

- ✅ `collections` (stdlib)
- ✅ `kernel.contracts.ModuleContract`
- ✅ `kernel.contracts.ContractError`

### Quem Ele NUNCA Poderá Importar

- ❌ `core/kernel.py` (dependência circular!)
- ❌ `bootstrap.py`
- ❌ Módulos de `codigo/`
- ❌ Módulos de `scripts/`

**Razão:** Registry é uma estrutura de dados. Não deve conhecer quem o usa.

### Estado Atual

✅ Implementado e estável

### Observações

- Implementa algoritmo de ordenação topológica
- Detecta ciclos de forma determinística
- **Expansão futura (Fase 4):** Adicionar consultas avançadas

---

## 6. Shared (`shared/paths.py`)

### Objetivo

Fornecer caminhos canônicos do projeto.

### Responsabilidades

1. ✅ Definir `PROJECT_ROOT` (raiz do projeto)
2. ✅ Definir caminhos principais (`KERNEL`, `CODIGO`, `DADOS`, etc.)
3. ✅ Fornecer `project_path()` para caminhos relativos

### Quem Pode Utilizá-lo

- **Todos os módulos do Kernel**
- **Todos os módulos de aplicação**

### Quem Depende Dele

- `bootstrap.py`
- `contracts/validator.py`
- Módulos externos (`codigo/`, `scripts/`)

### Quem Ele Pode Importar

- ✅ `pathlib` (stdlib)

### Quem Ele NUNCA Poderá Importar

- ❌ Qualquer outro módulo do Kernel
- ❌ Qualquer módulo externo

**Razão:** É a base de tudo. Não deve depender de nada.

### Estado Atual

✅ Implementado e estável

---

## Resumo de Dependências

```
shared/paths.py          ← base (sem dependências)
    ↓
contracts/module.py      ← base (sem dependências)
    ↓
lifecycle/manager.py     ← base (sem dependências)
    ↓
registry/module_registry.py  ← depende de contracts/module.py
    ↓
core/kernel.py           ← depende de registry, lifecycle, contracts
    ↓
bootstrap.py             ← depende de core, contracts, shared
```

**Validação:** Nenhuma dependência circular detectada ✅

---

**Documento:** `FASE-1-RESPONSABILIDADES.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
