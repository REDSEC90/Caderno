# FASE 1 — CAMADAS ARQUITETURAIS

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Normativo

---

## Definição

O Kernel do SOE-CCG é organizado em **camadas** hierárquicas.

Cada camada pode depender apenas de camadas **inferiores**.

Nenhuma camada pode depender de camadas **superiores** ou **paralelas** (exceto quando explicitamente permitido).

---

## Hierarquia de Camadas

```
┌─────────────────────────────────────────┐
│         APPLICATION LAYER               │  ← Aplicações externas
├─────────────────────────────────────────┤
│            KERNEL API                   │  ← Ponto de entrada do Kernel
├─────────────────────────────────────────┤
│         KERNEL SERVICES                 │  ← Coordenação (Core)
├─────────────────────────────────────────┤
│         KERNEL RUNTIME                  │  ← Registry + Lifecycle
├─────────────────────────────────────────┤
│          KERNEL CORE                    │  ← Contracts + Shared
└─────────────────────────────────────────┘
```

---

## Camada 0 — Kernel Core

**Objetivo:** Base de tudo. Sem dependências.

### Módulos

- `shared/paths.py` — Caminhos canônicos
- `contracts/module.py` — Contrato de módulos

### Características

- ✅ Sem dependências internas
- ✅ Sem lógica de negócio
- ✅ Puras estruturas de dados
- ✅ Podem ser usados por qualquer camada

### Regras

- ❌ Não podem importar de outras camadas
- ❌ Não podem importar uns dos outros (exceto stdlib)
- ✅ Podem ser modificados apenas com RFC

---

## Camada 1 — Kernel Runtime

**Objetivo:** Gerenciamento de estado e registro.

### Módulos

- `lifecycle/manager.py` — Máquina de estados
- `registry/module_registry.py` — Registro de módulos
- `contracts/validator.py` — Validação arquitetural

### Características

- ✅ Dependem apenas da Camada 0
- ✅ Sem lógica de negócio
- ✅ Estruturas de controle puras

### Regras

- ✅ Podem importar de Camada 0
- ❌ Não podem importar de Camada 2 ou superior
- ❌ Não podem importar entre si (exceto validações)

---

## Camada 2 — Kernel Services

**Objetivo:** Coordenação entre Runtime e Core.

### Módulos

- `core/kernel.py` — Coordenador principal

### Características

- ✅ Depende de Camada 0 e Camada 1
- ✅ Coordena Registry e Lifecycle
- ✅ Sem lógica de negócio

### Regras

- ✅ Pode importar de Camada 0 e 1
- ❌ Não pode importar de Camada 3
- ❌ Não pode conter lógica de domínio

---

## Camada 3 — Kernel API

**Objetivo:** Ponto de entrada para aplicações.

### Módulos

- `bootstrap.py` — Inicialização do Kernel

### Características

- ✅ Depende de Camada 0, 1 e 2
- ✅ Única interface pública para aplicações
- ✅ Sem lógica de negócio

### Regras

- ✅ Pode importar de Camada 0, 1 e 2
- ❌ Não pode ser importado por outras camadas do Kernel
- ✅ Pode ser importado por Application Layer

---

## Camada 4 — Application Layer

**Objetivo:** Aplicações que usam o Kernel.

### Módulos

- `codigo/` — Runtime de domínio
- `scripts/` — Ferramentas e utilitários
- Aplicações externas

### Características

- ✅ Dependem de Camada 3 (Kernel API)
- ✅ Contêm lógica de negócio
- ✅ Registram-se no Kernel via `ModuleContract`

### Regras

- ✅ Podem importar de `bootstrap.py`
- ✅ Podem usar API pública do Kernel
- ❌ Não podem importar camadas internas do Kernel (0, 1, 2)
- ❌ Não podem modificar o Kernel

---

## Matriz de Dependências Permitidas

|                  | Core (0) | Runtime (1) | Services (2) | API (3) | Application (4) |
|------------------|----------|-------------|--------------|---------|-----------------|
| **Core (0)**     | ❌       | ❌          | ❌           | ❌      | ❌              |
| **Runtime (1)**  | ✅       | ❌          | ❌           | ❌      | ❌              |
| **Services (2)** | ✅       | ✅          | ❌           | ❌      | ❌              |
| **API (3)**      | ✅       | ✅          | ✅           | ❌      | ❌              |
| **Application (4)** | ❌    | ❌          | ❌           | ✅      | ✅              |

**Legenda:**
- ✅ = Dependência permitida
- ❌ = Dependência proibida

---

## Regras de Evolução

### Adicionar novo módulo em Camada 0 (Core)

1. RFC obrigatório
2. Aprovação de arquitetura
3. Validação de ausência de dependências
4. Testes de contrato

### Adicionar novo módulo em Camada 1 (Runtime)

1. RFC obrigatório
2. Aprovação de arquitetura
3. Validação de dependências apenas em Camada 0
4. Testes de integração

### Adicionar novo módulo em Camada 2 (Services)

1. RFC obrigatório
2. Validação de dependências em Camadas 0 e 1
3. Testes de integração e contrato

### Modificar Camada 3 (API)

1. RFC obrigatório (afeta interface pública)
2. Versionamento SemVer
3. Testes de regressão

### Adicionar módulo em Camada 4 (Application)

1. Sem RFC necessário
2. Deve usar apenas API pública
3. Registrar via `ModuleContract`

---

## Diagrama de Fluxo

```
┌───────────────────────────────────────────────────────────┐
│                     APLICAÇÃO                             │
│  (codigo/, scripts/, aplicações externas)                 │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ usa API pública
                     ↓
┌───────────────────────────────────────────────────────────┐
│                   bootstrap.py                            │
│  (Kernel API — Camada 3)                                  │
└────────────────────┬──────────────────────────────────────┘
                     │
                     │ inicializa
                     ↓
┌───────────────────────────────────────────────────────────┐
│                  core/kernel.py                           │
│  (Kernel Services — Camada 2)                             │
└────────────┬────────────────┬─────────────────────────────┘
             │                │
             │                │ coordena
             ↓                ↓
    ┌────────────────┐  ┌────────────────┐
    │ Registry       │  │ Lifecycle      │
    │ (Camada 1)     │  │ (Camada 1)     │
    └────────┬───────┘  └────────┬───────┘
             │                   │
             │ usa               │ usa
             ↓                   ↓
    ┌────────────────────────────────────┐
    │   Contracts + Shared (Camada 0)    │
    └────────────────────────────────────┘
```

---

## Expansão Futura

As seguintes camadas serão adicionadas após a Fase 14:

### Kernel Events (Camada 1)
- `events/` — Sistema de eventos

### Kernel Security (Camada 1)
- `security/` — Políticas de segurança

### Kernel Observability (Camada 1)
- `observability/` — Métricas e diagnósticos

Todas serão **Camada 1** (Runtime) e dependerão apenas da **Camada 0** (Core).

---

## Resumo

| Camada | Nome | Módulos | Dependências Permitidas |
|--------|------|---------|-------------------------|
| 0 | Core | 2 | Nenhuma |
| 1 | Runtime | 3 | Camada 0 |
| 2 | Services | 1 | Camadas 0, 1 |
| 3 | API | 1 | Camadas 0, 1, 2 |
| 4 | Application | ∞ | Camada 3 |

---

**Documento:** `FASE-1-CAMADAS.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
