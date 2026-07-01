# FASE 6 — SERVICE REGISTRY

**Status:** ✅ CONCLUÍDA  
**Data de início:** 2026-07-01  
**Data de conclusão:** 2026-07-01  
**Versão:** 2.0

---

## Objetivo

Separar conceito de Módulo vs Serviço, criando `ServiceRegistry` para gerenciar
instâncias executáveis de módulos de forma independente do `ModuleRegistry`.

---

## Conceito Central

```
Módulo  = Unidade de código com contrato (estático, imutável)
Serviço = Instância executável de um módulo (dinâmico, em memória)
```

---

## Entregáveis

### ✅ 1. Módulo `kernel/services/`

**Arquivos criados:**

```
kernel/services/
├── __init__.py             (exports públicos)
└── service_registry.py     (ServiceError + ServiceRegistry)
```

---

### ✅ 2. ServiceError — Exceção Pública

```python
class ServiceError(RuntimeError):
    """Erro de operação no ServiceRegistry."""
```

---

### ✅ 3. ServiceRegistry — API completa

#### Escrita

```python
def register_service(name: str, instance: Any) -> None
    """Registra instância. Levanta ServiceError se nome vazio, instância None
    ou nome duplicado."""

def unregister_service(name: str) -> None
    """Remove serviço. Levanta ServiceError se não registrado."""
```

#### Consultas

```python
def get_service(name: str) -> Any
    """Retorna instância. Levanta ServiceError se não registrado."""

def list_services() -> list[str]
    """Nomes registrados em ordem alfabética."""

def has_service(name: str) -> bool
    """True se serviço registrado."""

def service_health(name: str) -> dict
    """Diagnóstico de saúde do serviço (chama instance.health() se disponível)."""

def all_health() -> dict[str, dict]
    """Diagnóstico de todos os serviços, ordenado por nome."""

def stats() -> dict[str, int]
    """Contadores: total_services, with_health_method, without_health_method."""

def reset() -> None
    """Remove todos os serviços (útil para testes)."""
```

---

### ✅ 4. KernelEvent — 2 novos eventos

| Evento | Valor | Quando emitido |
|--------|-------|----------------|
| `SERVICE_REGISTERED` | `"service_registered"` | Após `register_service()` |
| `SERVICE_UNREGISTERED` | `"service_unregistered"` | Após `unregister_service()` |

Total de eventos no barramento: **10** (era 8 na Fase 5)

---

### ✅ 5. Integração com MicroKernel

O `MicroKernel` agora expõe `kernel.services: ServiceRegistry` e
oferece métodos de conveniência que publicam eventos automaticamente:

| Método | Evento publicado |
|--------|-----------------|
| `kernel.register_service(name, instance)` | `SERVICE_REGISTERED` |
| `kernel.unregister_service(name)` | `SERVICE_UNREGISTERED` |
| `kernel.get_service(name)` | — (sem evento) |

Serviços podem ser registrados independentemente do estado do lifecycle
(não requer kernel em RUNNING).

---

### ✅ 6. Diagnóstico de Saúde (service_health)

O `service_health()` retorna:

```python
{
    "name": str,                  # nome do serviço
    "registered": True,           # sempre True (levanta se não registrado)
    "type": str,                  # __class__.__name__ da instância
    "uptime_seconds": float,      # segundos desde o registro
    "has_health_method": bool,    # True se instance.health() existe
    "health_result": Any | None,  # resultado de instance.health()
    "error": str | None,          # mensagem se health() falhar
}
```

---

### ✅ 7. Testes Completos

**Arquivo:** `testes/contract/test_services_v1.py`

**47 testes novos:**

| Classe de teste | Cobertura |
|-----------------|-----------|
| `TestServiceRegistryBasico` | register, get, list, has_service |
| `TestServiceRegistryErros` | guardas de valor, duplicatas, não registrado |
| `TestServiceHealth` | sem health, com health, falha, all_health |
| `TestServiceRegistryStats` | stats vazios, misto, todos int |
| `TestServiceRegistryReset` | reset limpa tudo, permite reregistro |
| `TestUnregister` | remove, atualiza list/stats, permite reregistro |
| `TestKernelEventServicos` | 2 novos eventos, são str, comparação |
| `TestMicroKernelIntegracaoServicos` | kernel.services, eventos, histórico |

**Resultado:** 47/47 testes passando ✅  
**Suite completa:** 226/226 testes passando ✅

---

## Arquivos Criados/Modificados

### Criados

```
kernel/services/
├── __init__.py
└── service_registry.py

testes/contract/
└── test_services_v1.py         (47 testes)

kernel-docs/
└── FASE-6-RESUMO.md            (este arquivo)
```

### Modificados

```
kernel/core/kernel.py            (integração do ServiceRegistry + 3 métodos)
kernel/__init__.py               (export de ServiceError, ServiceRegistry)
kernel/events/bus.py             (2 novos eventos: SERVICE_REGISTERED, SERVICE_UNREGISTERED)
testes/contract/test_events_v1.py (atualizado: 8 → 10 eventos)
```

---

## Decisões de Design

**Separação de responsabilidades** — `ModuleRegistry` gerencia contratos
(metadados estáticos). `ServiceRegistry` gerencia instâncias (objetos em
memória). São componentes independentes sem referência mútua.

**Diagnóstico resiliente** — `service_health()` nunca lança exceção por
falha no método `health()` da instância. Erros são capturados e retornados
no campo `"error"`, preservando a capacidade de inspecionar todos os
serviços mesmo quando alguns estão degradados.

**Registro de tempo** — cada serviço tem timestamp de registro, permitindo
calcular uptime aproximado sem dependências externas.

**Eventos publicados** — `MicroKernel.register_service()` e
`unregister_service()` publicam eventos no barramento, mantendo o padrão
observável estabelecido na Fase 5.

**Independência do lifecycle** — serviços podem ser registrados em
qualquer estado do kernel, sem exigir RUNNING.

---

## Comparação v1.0 (especificado) vs v2.0 (implementado)

| Métrica | v1.0 (spec) | v2.0 (impl) | Variação |
|---------|-------------|-------------|----------|
| Classes criadas | 1 | 2 | +ServiceError |
| Métodos ServiceRegistry | 4 | 9 | +5 |
| Eventos KernelEvent | 8 | 10 | +SERVICE_REGISTERED, +SERVICE_UNREGISTERED |
| Integração no MicroKernel | ❌ | ✅ | +3 métodos |
| Testes | 0 | 47 | +47 |
| Arquivos novos | 2 | 2 | igual |

---

## Checklist de Verificação

- ✅ `ServiceRegistry` implementado em `kernel/services/`
- ✅ `ServiceError` definido como exceção pública
- ✅ `register_service()` com guardas de valor
- ✅ `unregister_service()` com validação
- ✅ `get_service()` com validação
- ✅ `list_services()` em ordem alfabética
- ✅ `has_service()` implementado
- ✅ `service_health()` com diagnóstico resiliente
- ✅ `all_health()` para inspeção em massa
- ✅ `stats()` com contadores int
- ✅ `reset()` para testes e reinicializações
- ✅ 2 novos eventos (`SERVICE_REGISTERED`, `SERVICE_UNREGISTERED`)
- ✅ Integrado ao `MicroKernel` com publicação de eventos
- ✅ Exportado no `kernel/__init__.py`
- ✅ 47 testes novos criados
- ✅ 226/226 testes passando
- ✅ Zero regressões

---

## Próximos Passos

**Fase 13 — Certificação** (checklist formal de estabilidade do Kernel)

---

**Documento:** `FASE-6-RESUMO.md`  
**Versão:** 2.0  
**Data:** 2026-07-01  
**Autor:** Sistema de Consolidação SOE-CCG
