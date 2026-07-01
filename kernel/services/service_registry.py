"""Registry de serviços do microkernel SOE-CCG.

Um **serviço** é uma instância executável de um módulo — objeto em memória
pronto para ser consumido.  O ``ServiceRegistry`` separa esse conceito do
``ModuleRegistry``, que lida com *contratos* (metadados estáticos).

Diferença central::

    Módulo  = Unidade de código com contrato (estático, imutável)
    Serviço = Instância executável de um módulo (dinâmico, em memória)

Exemplo de uso::

    registry = ServiceRegistry()
    registry.register_service("parser", ParserImpl())
    registry.register_service("validator", ValidatorImpl())

    parser = registry.get_service("parser")
    health = registry.service_health("parser")
    names  = registry.list_services()
"""
from __future__ import annotations

import time
from typing import Any


class ServiceError(RuntimeError):
    """Erro de operação no ServiceRegistry."""


class ServiceRegistry:
    """Registro de instâncias de serviço do kernel.

    Responsabilidades:
    - Registrar instâncias de serviço por nome.
    - Recuperar serviços por nome.
    - Reportar saúde individual de cada serviço.
    - Listar serviços registrados.
    - Desregistrar serviços sob demanda.

    Não é responsabilidade deste componente:
    - Gerenciar o ciclo de vida dos módulos (isso é do ``KernelLifecycle``).
    - Resolver dependências (isso é do ``ModuleRegistry``).
    - Emitir eventos (isso é do ``KernelEventBus``).
    """

    def __init__(self) -> None:
        # {nome: instância}
        self._services: dict[str, Any] = {}
        # {nome: timestamp de registro (epoch float)}
        self._registered_at: dict[str, float] = {}

    # ------------------------------------------------------------------
    # Operações de escrita
    # ------------------------------------------------------------------

    def register_service(self, name: str, instance: Any) -> None:
        """Registra uma instância de serviço.

        Args:
            name: Identificador único do serviço.  Não pode ser vazio.
            instance: Instância do serviço.  Não pode ser ``None``.

        Raises:
            ServiceError: Se ``name`` for vazio, ``instance`` for ``None``,
                ou se já existir um serviço com o mesmo nome.
        """
        if not name or not name.strip():
            raise ServiceError("nome do serviço não pode ser vazio")
        if instance is None:
            raise ServiceError(
                f"instância do serviço {name!r} não pode ser None"
            )
        if name in self._services:
            raise ServiceError(f"serviço já registrado: {name!r}")

        self._services[name] = instance
        self._registered_at[name] = time.time()

    def unregister_service(self, name: str) -> None:
        """Remove um serviço registrado.

        Args:
            name: Identificador do serviço a remover.

        Raises:
            ServiceError: Se o serviço não estiver registrado.
        """
        if name not in self._services:
            raise ServiceError(f"serviço não registrado: {name!r}")
        del self._services[name]
        del self._registered_at[name]

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def get_service(self, name: str) -> Any:
        """Retorna a instância do serviço registrado.

        Args:
            name: Identificador do serviço.

        Returns:
            Instância do serviço.

        Raises:
            ServiceError: Se o serviço não estiver registrado.
        """
        if name not in self._services:
            raise ServiceError(f"serviço não registrado: {name!r}")
        return self._services[name]

    def list_services(self) -> list[str]:
        """Retorna os nomes dos serviços registrados em ordem alfabética.

        Returns:
            Lista de nomes de serviços (pode ser vazia).
        """
        return sorted(self._services)

    def has_service(self, name: str) -> bool:
        """Verifica se um serviço está registrado.

        Args:
            name: Identificador do serviço.

        Returns:
            ``True`` se o serviço estiver registrado, ``False`` caso contrário.
        """
        return name in self._services

    def service_health(self, name: str) -> dict[str, Any]:
        """Retorna informações de saúde do serviço.

        O diagnóstico verifica:
        - Se o serviço está registrado.
        - Se possui método ``health()`` e o chama.
        - Tempo de registro (uptime aproximado em segundos).

        Args:
            name: Identificador do serviço.

        Returns:
            Dicionário com:

            - ``name`` (str) — nome do serviço.
            - ``registered`` (bool) — True se registrado.
            - ``type`` (str) — tipo da instância (``__class__.__name__``).
            - ``uptime_seconds`` (float) — segundos desde o registro.
            - ``has_health_method`` (bool) — True se a instância tem ``health()``.
            - ``health_result`` (Any | None) — resultado de ``instance.health()``
              se disponível, ``None`` caso contrário.
            - ``error`` (str | None) — mensagem de erro se ``health()`` falhar.

        Raises:
            ServiceError: Se o serviço não estiver registrado.
        """
        if name not in self._services:
            raise ServiceError(f"serviço não registrado: {name!r}")

        instance = self._services[name]
        registered_at = self._registered_at[name]
        uptime = time.time() - registered_at

        has_health = callable(getattr(instance, "health", None))
        health_result: Any = None
        error: str | None = None

        if has_health:
            try:
                health_result = instance.health()
            except Exception as exc:  # noqa: BLE001
                error = str(exc)

        return {
            "name": name,
            "registered": True,
            "type": type(instance).__name__,
            "uptime_seconds": uptime,
            "has_health_method": has_health,
            "health_result": health_result,
            "error": error,
        }

    def all_health(self) -> dict[str, dict[str, Any]]:
        """Retorna o diagnóstico de saúde de todos os serviços registrados.

        Returns:
            Dicionário ``{nome: service_health(nome)}`` para cada serviço,
            ordenado por nome.
        """
        return {name: self.service_health(name) for name in sorted(self._services)}

    def stats(self) -> dict[str, int]:
        """Retorna estatísticas do registry de serviços.

        Returns:
            Dicionário com:

            - ``total_services`` — Total de serviços registrados.
            - ``with_health_method`` — Serviços que possuem método ``health()``.
            - ``without_health_method`` — Serviços sem método ``health()``.
        """
        instances = list(self._services.values())
        with_health = sum(
            1 for inst in instances if callable(getattr(inst, "health", None))
        )
        return {
            "total_services": len(instances),
            "with_health_method": with_health,
            "without_health_method": len(instances) - with_health,
        }

    def reset(self) -> None:
        """Remove todos os serviços registrados.

        Útil para testes e reinicializações controladas.
        """
        self._services.clear()
        self._registered_at.clear()
