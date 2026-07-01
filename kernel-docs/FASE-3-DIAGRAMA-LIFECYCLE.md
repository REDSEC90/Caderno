# FASE 3 — DIAGRAMA DE LIFECYCLE EXPANDIDO

**Versão:** 2.0  
**Data:** 2026-07-01  
**Status:** Especificação

---

## Objetivo

Expandir a máquina de estados do Kernel para suportar estados intermediários, tratamento de erros e recuperação.

---

## Estados Atuais (v1.0)

```
CREATED → INITIALIZED → RUNNING → STOPPED
```

**Limitações:**
- Sem estados intermediários (não reflete transições em andamento)
- Sem tratamento de erro (crash vai direto para STOPPED)
- Sem recuperação (não há como voltar de STOPPED)
- Sem pausa (não é possível pausar temporariamente)

---

## Estados Expandidos (v2.0)

```
CREATED
    ↓
INITIALIZING        ← estado intermediário
    ↓
INITIALIZED
    ↓
STARTING            ← estado intermediário
    ↓
RUNNING
    ↓ (pause)
PAUSING             ← estado intermediário
    ↓
PAUSED              ← novo estado
    ↓ (resume)
RESUMING            ← estado intermediário
    ↓
RUNNING
    ↓ (stop)
STOPPING            ← estado intermediário
    ↓
STOPPED
    
    ↓ (restart)
RESTARTING          ← estado intermediário
    ↓
INITIALIZED

(qualquer estado) → FAILED       ← tratamento de erro
    ↓ (recover)
RECOVERING          ← recuperação
    ↓
INITIALIZED

(qualquer estado) → DISABLED     ← desabilitado manualmente
```

---

## Estados Detalhados

### 1. CREATED

**Descrição:** Estado inicial ao criar uma instância do Kernel.

**Transições permitidas:**
- → `INITIALIZING` (via `initialize()`)

**Ações:**
- Nenhuma (estado inerte)

---

### 2. INITIALIZING

**Descrição:** Inicialização em andamento (validando dependências, carregando módulos).

**Transições permitidas:**
- → `INITIALIZED` (sucesso)
- → `FAILED` (erro)

**Ações:**
- Validar dependências
- Registrar módulos
- Preparar recursos

---

### 3. INITIALIZED

**Descrição:** Kernel inicializado e pronto para iniciar.

**Transições permitidas:**
- → `STARTING` (via `start()`)
- → `STOPPED` (via `stop()`)

**Ações:**
- Aguardando comando de start

---

### 4. STARTING

**Descrição:** Iniciando execução (chamando entrypoints dos módulos).

**Transições permitidas:**
- → `RUNNING` (sucesso)
- → `FAILED` (erro)

**Ações:**
- Executar entrypoints na ordem de dependências
- Ativar serviços

---

### 5. RUNNING

**Descrição:** Kernel em execução normal.

**Transições permitidas:**
- → `PAUSING` (via `pause()`)
- → `STOPPING` (via `stop()`)
- → `FAILED` (erro não recuperável)

**Ações:**
- Processar eventos
- Executar serviços
- Monitorar estado

---

### 6. PAUSING

**Descrição:** Pausando execução (salvando estado, suspendendo serviços).

**Transições permitidas:**
- → `PAUSED` (sucesso)
- → `FAILED` (erro)

**Ações:**
- Salvar estado
- Suspender serviços
- Manter contexto

---

### 7. PAUSED

**Descrição:** Execução pausada (estado preservado).

**Transições permitidas:**
- → `RESUMING` (via `resume()`)
- → `STOPPING` (via `stop()`)

**Ações:**
- Aguardando comando de resume ou stop

---

### 8. RESUMING

**Descrição:** Retomando execução a partir de pause.

**Transições permitidas:**
- → `RUNNING` (sucesso)
- → `FAILED` (erro)

**Ações:**
- Restaurar estado
- Reativar serviços
- Retomar processamento

---

### 9. STOPPING

**Descrição:** Parando execução (limpando recursos, finalizando serviços).

**Transições permitidas:**
- → `STOPPED` (sucesso)
- → `FAILED` (erro crítico durante shutdown)

**Ações:**
- Finalizar serviços
- Liberar recursos
- Fazer cleanup

---

### 10. STOPPED

**Descrição:** Kernel parado (pode ser reiniciado).

**Transições permitidas:**
- → `RESTARTING` (via `restart()`)
- → `DISABLED` (via `disable()`)

**Ações:**
- Nenhuma (estado terminal temporário)

---

### 11. RESTARTING

**Descrição:** Reiniciando Kernel a partir de STOPPED.

**Transições permitidas:**
- → `INITIALIZED` (sucesso)
- → `FAILED` (erro)

**Ações:**
- Limpar estado anterior
- Re-inicializar componentes
- Revalidar dependências

---

### 12. FAILED

**Descrição:** Erro não recuperável ou crítico.

**Transições permitidas:**
- → `RECOVERING` (via `recover()`)
- → `DISABLED` (via `disable()`)

**Ações:**
- Registrar erro
- Notificar observers
- Salvar diagnóstico

---

### 13. RECOVERING

**Descrição:** Tentando recuperar de falha.

**Transições permitidas:**
- → `INITIALIZED` (sucesso)
- → `FAILED` (falha na recuperação)

**Ações:**
- Diagnosticar problema
- Tentar correção automática
- Restaurar para estado consistente

---

### 14. DISABLED

**Descrição:** Kernel desabilitado manualmente (estado terminal permanente).

**Transições permitidas:**
- Nenhuma (estado final)

**Ações:**
- Nenhuma (terminal)

---

## Diagrama Visual Completo

```
                    ┌─────────┐
                    │ CREATED │
                    └────┬────┘
                         │ initialize()
                         ↓
                 ┌──────────────┐
                 │ INITIALIZING │ ──────┐
                 └──────┬───────┘       │
                        │               │ erro
                        │ sucesso       ↓
                        ↓          ┌────────┐
                 ┌─────────────┐   │ FAILED │ ←──────┐
         ┌───────│ INITIALIZED │   └───┬────┘        │
         │       └──────┬──────┘       │             │
         │              │               │ recover()  │
         │              │ start()       ↓            │
         │              ↓        ┌──────────────┐    │
         │        ┌──────────┐   │  RECOVERING  │    │
         │        │ STARTING │   └───────┬──────┘    │
         │        └────┬─────┘           │           │
         │             │                 │ sucesso   │
         │             │ sucesso         │           │
         │             ↓                 ↓           │
         │        ┌─────────┐         (volta ao     │
         │   ┌───→│ RUNNING │          INITIALIZED) │
         │   │    └────┬────┘                       │
         │   │         │                            │
         │   │    ┌────┴─────┬─────────┐           │
         │   │    │          │         │           │
         │   │    │ pause()  │ stop()  │ erro      │
         │   │    ↓          ↓         │           │
         │   │ ┌─────────┐ ┌─────────┐│           │
         │   │ │ PAUSING │ │STOPPING ││───────────┘
         │   │ └────┬────┘ └────┬────┘
         │   │      │            │
         │   │      ↓            ↓
         │   │  ┌────────┐  ┌─────────┐
         │   │  │ PAUSED │  │ STOPPED │
         │   │  └────┬───┘  └────┬────┘
         │   │       │            │
         │   │       │ resume()   │ restart()
         │   │       ↓            ↓
         │   │  ┌──────────┐ ┌──────────────┐
         │   └──│ RESUMING │ │  RESTARTING  │
         │      └──────────┘ └──────┬───────┘
         │                          │
         └──────────────────────────┘
         
         (qualquer estado) → DISABLED (estado final)
```

---

## Matriz de Transições

| Estado Atual | Transições Permitidas |
|--------------|----------------------|
| `CREATED` | → `INITIALIZING` |
| `INITIALIZING` | → `INITIALIZED`, → `FAILED` |
| `INITIALIZED` | → `STARTING`, → `STOPPING` |
| `STARTING` | → `RUNNING`, → `FAILED` |
| `RUNNING` | → `PAUSING`, → `STOPPING`, → `FAILED` |
| `PAUSING` | → `PAUSED`, → `FAILED` |
| `PAUSED` | → `RESUMING`, → `STOPPING` |
| `RESUMING` | → `RUNNING`, → `FAILED` |
| `STOPPING` | → `STOPPED`, → `FAILED` |
| `STOPPED` | → `RESTARTING`, → `DISABLED` |
| `RESTARTING` | → `INITIALIZED`, → `FAILED` |
| `FAILED` | → `RECOVERING`, → `DISABLED` |
| `RECOVERING` | → `INITIALIZED`, → `FAILED` |
| `DISABLED` | Nenhuma (terminal) |

---

## Categorização de Estados

### Estados Estáveis
(permanecem até ação explícita)

- `CREATED`
- `INITIALIZED`
- `RUNNING`
- `PAUSED`
- `STOPPED`
- `FAILED`
- `DISABLED`

### Estados Transitórios
(transição automática ao completar)

- `INITIALIZING`
- `STARTING`
- `PAUSING`
- `RESUMING`
- `STOPPING`
- `RESTARTING`
- `RECOVERING`

---

## Métodos da API

### Métodos Públicos

```python
def initialize() -> None
    """CREATED → INITIALIZING → INITIALIZED"""

def start() -> None
    """INITIALIZED → STARTING → RUNNING"""

def pause() -> None
    """RUNNING → PAUSING → PAUSED"""

def resume() -> None
    """PAUSED → RESUMING → RUNNING"""

def stop() -> None
    """RUNNING/PAUSED/INITIALIZED → STOPPING → STOPPED"""

def restart() -> None
    """STOPPED → RESTARTING → INITIALIZED"""

def recover() -> None
    """FAILED → RECOVERING → INITIALIZED"""

def disable() -> None
    """FAILED/STOPPED → DISABLED"""
```

### Métodos de Consulta

```python
def is_stable() -> bool
    """Retorna True se está em estado estável."""

def is_transitioning() -> bool
    """Retorna True se está em estado transitório."""

def is_operational() -> bool
    """Retorna True se está em RUNNING ou PAUSED."""

def is_terminal() -> bool
    """Retorna True se está em DISABLED."""

def can_start() -> bool
    """Retorna True se pode chamar start()."""

def can_stop() -> bool
    """Retorna True se pode chamar stop()."""
```

---

## Integração com ModuleContract

O campo `lifecycle_policy` do `ModuleContract` determina o comportamento:

### `"standard"` (padrão)

- Segue o ciclo completo normal
- Todos os estados disponíveis

### `"singleton"`

- Apenas uma instância do módulo
- `RESTARTING` reinicia a mesma instância

### `"transient"`

- Instância temporária
- Vai direto de `RUNNING` para `DISABLED` ao parar
- Não pode ser reiniciado

---

## Tratamento de Erros

### Erro Durante Inicialização

```
INITIALIZING → FAILED
    ↓ (recover)
RECOVERING → INITIALIZED
```

### Erro Durante Execução

```
RUNNING → FAILED
    ↓ (recover)
RECOVERING → INITIALIZED → STARTING → RUNNING
```

### Erro Não Recuperável

```
FAILED → DISABLED (via disable())
```

---

## Próximos Passos

1. Implementar novos estados em `LifecycleState`
2. Implementar novos métodos em `KernelLifecycle`
3. Adicionar validações de transição
4. Criar testes para cada transição
5. Adicionar logging de transições

---

**Documento:** `FASE-3-DIAGRAMA-LIFECYCLE.md`  
**Versão:** 2.0  
**Data:** 2026-07-01
