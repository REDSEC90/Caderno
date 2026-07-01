# API PÚBLICA DO KERNEL

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Congelada

---

## Definição

A **API Pública** consiste em todas as funções, classes e interfaces que devem ser acessadas por código externo ao Kernel.

Toda mudança nesta API requer aprovação via RFC após o Release 1.0.

---

## 1. Bootstrap

### `kernel.bootstrap.bootstrap_system()`

**Assinatura:**
```python
def bootstrap_system(extra_modules: tuple[ModuleContract, ...] = ()) -> MicroKernel
```

**Responsabilidade:** Inicializar e retornar uma instância configurada do Kernel.

**Parâmetros:**
- `extra_modules` — Tupla opcional de contratos de módulos adicionais

**Retorno:** Instância de `MicroKernel` pronta para uso

**Status:** Estável

---

## 2. Core

### `kernel.core.MicroKernel`

**Classe principal do Kernel.**

#### Métodos Públicos

##### `__init__()`
```python
def __init__(self) -> None
```
Inicializa o Kernel.

##### `register(contract: ModuleContract)`
```python
def register(self, contract: ModuleContract) -> None
```
Registra um módulo no Kernel.

##### `initialize()`
```python
def initialize(self) -> None
```
Inicializa todos os módulos registrados.

##### `start()`
```python
def start(self) -> None
```
Inicia o Kernel e todos os módulos.

##### `stop()`
```python
def stop(self) -> None
```
Para o Kernel e todos os módulos.

##### `state -> LifecycleState`
```python
@property
def state(self) -> LifecycleState
```
Retorna o estado atual do ciclo de vida do Kernel.

##### `startup_order() -> tuple[ModuleContract, ...]`
```python
def startup_order(self) -> tuple[ModuleContract, ...]
```
Retorna a ordem de inicialização dos módulos.

**Status:** Estável

---

## 3. Contracts

### `kernel.contracts.ModuleContract`

**Contrato oficial de módulos.**

#### Atributos Públicos

```python
name: str                          # Nome único do módulo
version: str                       # Versão semântica (ex: "1.0.0")
provides: tuple[str, ...]          # Capabilities fornecidas
requires: tuple[str, ...]          # Capabilities requeridas
priority: int                      # Prioridade de inicialização (padrão: 100)
entrypoint: Callable[[], None]     # Função de entrada do módulo
```

#### Métodos Públicos

##### `validate()`
```python
def validate(self) -> None
```
Valida o contrato. Levanta `ContractError` se inválido.

**Status:** Estável

---

### `kernel.contracts.ContractError`

**Exceção levantada quando um contrato é inválido.**

```python
class ContractError(ValueError)
```

**Status:** Estável

---

### `kernel.contracts.validate_architecture()`

**Valida a arquitetura do projeto.**

```python
def validate_architecture(root: Path = PROJECT_ROOT) -> ValidationResult
```

**Parâmetros:**
- `root` — Raiz do projeto (padrão: PROJECT_ROOT)

**Retorno:** `ValidationResult` com resultados da validação

**Status:** Estável

---

### `kernel.contracts.assert_architecture_valid()`

**Valida a arquitetura e levanta exceção se houver erros.**

```python
def assert_architecture_valid(root: Path = PROJECT_ROOT) -> None
```

**Levanta:** `ArchitectureValidationError` se houver erros

**Status:** Estável

---

## 4. Lifecycle

### `kernel.lifecycle.LifecycleState`

**Estados do ciclo de vida.**

```python
class LifecycleState(str, Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
```

**Status:** Estável

---

### `kernel.lifecycle.LifecycleError`

**Exceção levantada em transições de estado inválidas.**

```python
class LifecycleError(RuntimeError)
```

**Status:** Estável

---

## 5. Registry

### `kernel.registry.ModuleRegistry`

**Registro central de módulos.**

#### Métodos Públicos

##### `register(contract: ModuleContract)`
```python
def register(self, contract: ModuleContract) -> None
```
Registra um contrato no registro.

##### `get(name: str) -> ModuleContract`
```python
def get(self, name: str) -> ModuleContract
```
Obtém um contrato por nome.

**Levanta:** `RegistryError` se não encontrado.

##### `provider_for(capability: str) -> ModuleContract`
```python
def provider_for(self, capability: str) -> ModuleContract
```
Obtém o provedor de uma capability.

**Levanta:** `RegistryError` se não encontrado.

##### `validate()`
```python
def validate(self) -> None
```
Valida todas as dependências.

**Levanta:** `RegistryError` se houver dependências não resolvidas.

##### `resolve_order() -> list[ModuleContract]`
```python
def resolve_order(self) -> list[ModuleContract]
```
Retorna a ordem de inicialização baseada em dependências.

**Levanta:** `RegistryError` se houver dependências circulares.

##### `contracts -> tuple[ModuleContract, ...]`
```python
@property
def contracts(self) -> tuple[ModuleContract, ...]
```
Retorna todos os contratos registrados.

**Status:** Estável

---

### `kernel.registry.RegistryError`

**Exceção levantada em erros de registro.**

```python
class RegistryError(RuntimeError)
```

**Status:** Estável

---

## 6. Shared

### `kernel.shared.project_path()`

**Retorna um caminho relativo à raiz do projeto.**

```python
def project_path(*parts: str) -> Path
```

**Parâmetros:**
- `*parts` — Partes do caminho relativo

**Retorno:** `Path` absoluto

**Exemplo:**
```python
project_path("kernel", "core")  # → /home/user/SOE-CCG/kernel/core
```

**Status:** Estável

---

## Resumo

| Componente | Classes Públicas | Funções Públicas | Exceções |
|------------|------------------|------------------|----------|
| bootstrap  | 0                | 1                | 0        |
| core       | 1                | 0                | 0        |
| contracts  | 2                | 2                | 2        |
| lifecycle  | 2                | 0                | 1        |
| registry   | 1                | 0                | 1        |
| shared     | 0                | 1                | 0        |
| **Total**  | **6**            | **4**            | **4**    |

---

## Política de Mudanças

Após o Release 1.0:

1. Toda mudança na API pública requer RFC
2. Breaking changes seguem SemVer (major bump)
3. Novas funcionalidades seguem SemVer (minor bump)
4. Correções de bugs seguem SemVer (patch bump)

---

**Documento:** `FASE-0-API-PUBLICA.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
