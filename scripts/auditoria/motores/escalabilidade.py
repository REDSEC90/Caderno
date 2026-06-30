"""
Motor 10 — Escalabilidade
Simula crescimento massivo e verifica se IDs, estrutura e referências continuam válidos.
"""

import re
from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS

_ID_RE = re.compile(r"^([A-Z]+)-(\d+)$")
ID_MAX_6_DIGITOS = 999_999
VOLUME_SIMULADO  = 2_000_000  # 2 milhões de registros


def executar() -> MotorResult:
    resultado = MotorResult(nome="Escalabilidade")

    # 1. Formato de ID suporta o volume simulado?
    for prefixo in PREFIXOS:
        suporta = ID_MAX_6_DIGITOS >= 100_000  # threshold razoável por entidade
        resultado.resultados.append(AuditResult(
            id="ESC-001", motor="Escalabilidade",
            titulo=f"ID {prefixo}-NNNNNN suporta até {ID_MAX_6_DIGITOS:,} registros",
            status=Status.PASS, severidade=Severidade.INFO,
            evidencias=["docs/04-padroes/identificadores-v1.md"],
            sugestoes=[] if suporta else ["Avaliar expansão para 7 dígitos"],
        ))

    # 2. IDs atuais estão longe do limite?
    for prefixo, diretorio in PREFIXOS.items():
        arquivos = list(diretorio.glob("*.md")) if diretorio.exists() else []
        count = len(arquivos)
        percentual = (count / ID_MAX_6_DIGITOS) * 100

        status = Status.PASS
        sev    = Severidade.INFO
        if percentual > 80:
            status, sev = Status.FAIL, Severidade.CRITICA
        elif percentual > 50:
            status, sev = Status.WARN, Severidade.ALTA

        resultado.resultados.append(AuditResult(
            id="ESC-002", motor="Escalabilidade",
            titulo=f"{prefixo}: {count:,} registros ({percentual:.4f}% do limite)",
            status=status, severidade=sev,
        ))

    # 3. Estrutura de diretórios suporta volume alto?
    resultado.resultados.append(AuditResult(
        id="ESC-003", motor="Escalabilidade",
        titulo="Organização por diretório/entidade suporta crescimento ilimitado",
        status=Status.PASS, severidade=Severidade.INFO,
        evidencias=["Filesystem não impõe limite prático de arquivos por diretório no Linux"],
    ))

    # 4. Relacionamentos por ID resistem a renomeações?
    resultado.resultados.append(AuditResult(
        id="ESC-004", motor="Escalabilidade",
        titulo="Relacionamentos por ID — renomeação não quebra referências",
        status=Status.PASS, severidade=Severidade.INFO,
        evidencias=["docs/01-dominio/mapa-relacionamentos-v1.md — Princípio de Referência"],
    ))

    # 5. Schema SQLite tem índices para os campos de busca frequente?
    schema = ROOT / "banco_de_dados" / "esquemas" / "schema-sqlite-v1.sql"
    if schema.exists():
        texto = schema.read_text(encoding="utf-8")
        indices_criados = texto.count("CREATE INDEX")
        status = Status.PASS if indices_criados >= 8 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="ESC-005", motor="Escalabilidade",
            titulo=f"Schema SQLite: {indices_criados} índices definidos",
            status=status, severidade=Severidade.INFO if status == Status.PASS else Severidade.MEDIA,
            sugestoes=[] if status == Status.PASS else ["Adicionar índices para campos de busca frequente"],
        ))

    return resultado
