"""Sistema de eventos do microkernel — comunicação desacoplada entre módulos."""
from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Any, Callable


class KernelEvent(str, Enum):
    """Eventos internos publicados pelo microkernel."""

    MODULE_DISCOVERED = "module_discovered"
    """Emitido quando um módulo é descoberto antes do registro."""

    MODULE_REGISTERED = "module_registered"
    """Emitido após registro bem-sucedido de um contrato no registry."""

    MODULE_STARTED = "module_started"
    """Emitido após o kernel entrar em estado RUNNING."""

    MODULE_STOPPED = "module_stopped"
    """Emitido após o kernel entrar em estado STOPPED."""

    MODULE_FAILED = "module_failed"
    """Emitido quando o kernel entra em estado FAILED."""

    CONTRACT_VALIDATED = "contract_validated"
    """Emitido após validate() bem-sucedido no registry."""

    DEPENDENCY_RESOLVED = "dependency_resolved"
    """Emitido após resolve_order() bem-sucedido."""

    STATE_CHANGED = "state_changed"
    """Emitido em toda transição de estado do lifecycle."""

    SERVICE_REGISTERED = "service_registered"
    """Emitido após registro bem-sucedido de uma instância no ServiceRegistry."""

    SERVICE_UNREGISTERED = "service_unregistered"
    """Emitido após remoção de uma instância do ServiceRegistry."""


# Tipo de handler: recebe o evento e dados arbitrários
EventHandler = Callable[[KernelEvent, dict[str, Any]], None]


class KernelEventBus:
    """Barramento de eventos do kernel — pub/sub síncrono e desacoplado.

    Permite que módulos e o próprio kernel publiquem e consumam eventos
    sem referência direta entre si.

    Exemplo de uso::

        bus = KernelEventBus()

        def on_registered(event, data):
            print(f"módulo registrado: {data['name']}")

        bus.subscribe(KernelEvent.MODULE_REGISTERED, on_registered)
        bus.publish(KernelEvent.MODULE_REGISTERED, {"name": "runtime.parser"})
        # imprime: módulo registrado: runtime.parser

        bus.unsubscribe(KernelEvent.MODULE_REGISTERED, on_registered)
    """

    def __init__(self) -> None:
        # {evento: [handler, ...]} — ordem de inserção preservada
        self._handlers: dict[KernelEvent, list[EventHandler]] = defaultdict(list)
        # histórico de eventos publicados (evento, dados)
        self._history: list[tuple[KernelEvent, dict[str, Any]]] = []

    # ------------------------------------------------------------------
    # Subscrição
    # ------------------------------------------------------------------

    def subscribe(self, event: KernelEvent, handler: EventHandler) -> None:
        """Registra um handler para o evento indicado.

        O mesmo handler pode ser registrado para múltiplos eventos
        distintos, mas não pode ser registrado duas vezes no mesmo evento.

        Args:
            event: Evento a monitorar.
            handler: Callable ``(event, data) -> None`` chamado na
                     publicação.

        Raises:
            ValueError: Se o handler já estiver registrado para o evento.
        """
        if handler in self._handlers[event]:
            raise ValueError(
                f"handler já registrado para {event.value!r}: {handler!r}"
            )
        self._handlers[event].append(handler)

    def unsubscribe(self, event: KernelEvent, handler: EventHandler) -> None:
        """Remove um handler previamente registrado.

        Args:
            event: Evento do qual remover o handler.
            handler: Handler a remover.

        Raises:
            ValueError: Se o handler não estiver registrado para o evento.
        """
        handlers = self._handlers[event]
        if handler not in handlers:
            raise ValueError(
                f"handler não registrado para {event.value!r}: {handler!r}"
            )
        handlers.remove(handler)

    # ------------------------------------------------------------------
    # Publicação
    # ------------------------------------------------------------------

    def publish(
        self,
        event: KernelEvent,
        data: dict[str, Any] | None = None,
    ) -> int:
        """Publica um evento, chamando todos os handlers registrados.

        Handlers são chamados na ordem de subscrição. Exceções levantadas
        por handlers individuais são capturadas — a entrega continua para
        os demais handlers. Ao final, se houver exceções, a primeira é
        re-levantada.

        Args:
            event: Evento a publicar.
            data: Dicionário de dados associados ao evento (opcional;
                  usa ``{}`` se omitido).

        Returns:
            Número de handlers notificados.

        Raises:
            Exception: Primeira exceção levantada por algum handler, após
                       todos os handlers terem sido chamados.
        """
        payload = dict(data) if data else {}
        self._history.append((event, payload))

        handlers = list(self._handlers[event])
        errors: list[Exception] = []

        for handler in handlers:
            try:
                handler(event, payload)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        if errors:
            raise errors[0]

        return len(handlers)

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def handlers_for(self, event: KernelEvent) -> tuple[EventHandler, ...]:
        """Retorna os handlers registrados para o evento, em ordem de subscrição.

        Args:
            event: Evento a consultar.

        Returns:
            Tupla imutável de handlers.
        """
        return tuple(self._handlers[event])

    def history(
        self,
        event: KernelEvent | None = None,
    ) -> list[tuple[KernelEvent, dict[str, Any]]]:
        """Retorna o histórico de eventos publicados.

        Args:
            event: Se informado, filtra apenas eventos desse tipo.

        Returns:
            Lista de tuplas ``(evento, dados)`` em ordem cronológica.
        """
        if event is None:
            return list(self._history)
        return [(e, d) for e, d in self._history if e == event]

    def clear_history(self) -> None:
        """Limpa o histórico de eventos publicados."""
        self._history.clear()

    def reset(self) -> None:
        """Remove todos os handlers e limpa o histórico."""
        self._handlers.clear()
        self._history.clear()

    def stats(self) -> dict[str, int]:
        """Retorna estatísticas do barramento.

        Returns:
            Dicionário com:

            - ``total_handlers`` — soma de todos os handlers registrados.
            - ``total_events_published`` — total de eventos no histórico.
            - por evento: ``event_<nome>_handlers`` e
              ``event_<nome>_published``.
        """
        result: dict[str, int] = {
            "total_handlers": sum(len(v) for v in self._handlers.values()),
            "total_events_published": len(self._history),
        }
        for ev in KernelEvent:
            key = ev.value.replace(".", "_")
            result[f"event_{key}_handlers"] = len(self._handlers[ev])
            result[f"event_{key}_published"] = sum(
                1 for e, _ in self._history if e == ev
            )
        return result
