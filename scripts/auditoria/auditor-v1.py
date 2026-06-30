#!/usr/bin/env python3
"""
FAA v1 — Framework de Auditoria Arquitetural do SOE-CCG
========================================================
Versão 1: sistema de decisão arquitetural + kernel de estado para agentes.

Uso:
    python3 auditor-v1.py                      # auditoria completa + estado JSON
    python3 auditor-v1.py --motor baseline     # apenas um motor
    python3 auditor-v1.py --relatorio          # gera Markdown
    python3 auditor-v1.py state                # exibe último estado
    python3 auditor-v1.py state --json         # saída JSON pura
    python3 auditor-v1.py entity REC-000001    # inspeciona registro
    python3 auditor-v1.py issues [--critical]  # lista problemas

Motores v1:
  baseline    Motor de decisão — compara contra ground truth oficial (BASELINE_V1)
  estrutura   Diretórios, nomenclatura, arquivos críticos
  filosofia   Documentos fundacionais (axiomas, constituição, princípios)
  dominio     Artefatos por entidade (especificação, contrato, template, esquema)
  cobertura   % de cobertura por tipo de artefato
  maturidade  Pontuação por camada arquitetural
  semantica   Termos obrigatórios e proibidos na linguagem oficial
  dados       Frontmatter, IDs, estados e datas nos registros canônicos
  integridade Referências entre registros em dados/
  padroes     Nomenclatura, encoding, slug dos arquivos em dados/
  escalabilidade Limites de IDs e estrutura para crescimento
  dependencias   Grafo de relacionamentos, ciclos, nós isolados
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict

_PROJECT_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT_FOR_IMPORT))

from kernel.bootstrap import bootstrap_system
from kernel.shared.paths import SCRIPTS_AUDITORIA

bootstrap_system()

if str(SCRIPTS_AUDITORIA) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_AUDITORIA))

import importlib.util, types

def _importar_v1(nome_modulo: str, caminho: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(nome_modulo, caminho)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_MOTORES_V1 = {
    "baseline":      SCRIPTS_AUDITORIA / "motores" / "baseline_v1.py",
    "estrutura":     SCRIPTS_AUDITORIA / "motores" / "estrutura_v1.py",
    "filosofia":     SCRIPTS_AUDITORIA / "motores" / "filosofia_v1.py",
    "dominio":       SCRIPTS_AUDITORIA / "motores" / "dominio_v1.py",
    "cobertura":     SCRIPTS_AUDITORIA / "motores" / "cobertura_v1.py",
    "maturidade":    SCRIPTS_AUDITORIA / "motores" / "maturidade_v1.py",
    "semantica":     SCRIPTS_AUDITORIA / "motores" / "semantica_v1.py",
    "dados":         SCRIPTS_AUDITORIA / "motores" / "dados-v2.py",
    "integridade":   SCRIPTS_AUDITORIA / "motores" / "integridade-v2.py",
    "padroes":       SCRIPTS_AUDITORIA / "motores" / "padroes.py",
    "escalabilidade":SCRIPTS_AUDITORIA / "motores" / "escalabilidade.py",
    "dependencias":  SCRIPTS_AUDITORIA / "motores" / "dependencias-v2.py",
}
_LEGADOS = {"dados", "integridade", "padroes", "escalabilidade", "dependencias"}

from config_v1 import ROOT, PREFIXOS, ID_PATTERN, NOME_DADOS_PATTERN, DOCS
from models_v1 import Status

STATE_PATH = DOCS / "99-referencias" / "faa-state.json"

# ── Collector ──────────────────────────────────────────────────────────────
@dataclass
class FileRecord:
    id: str
    tipo: str
    versao: str
    status: str
    path: str
    nome_valido: bool
    metadados_ok: bool
    links: list[str] = field(default_factory=list)
    tags: list[str]  = field(default_factory=list)

try:
    import frontmatter as _fm
    def _read_fm(path: Path) -> dict:
        return dict(_fm.load(str(path)).metadata)
except ImportError:
    import yaml, re as _re
    def _read_fm(path: Path) -> dict:
        text = path.read_text(encoding="utf-8")
        m = _re.match(r"^---\n(.*?)\n---", text, _re.DOTALL)
        return yaml.safe_load(m.group(1)) if m else {}

_METADADOS_OBR = ["id", "tipo", "schema-version", "versao", "status", "criado-em", "atualizado-em", "autor"]

def _extrair_links(meta: dict) -> list[str]:
    links = []
    for val in meta.values():
        if isinstance(val, str) and ID_PATTERN.match(val):
            links.append(val)
        elif isinstance(val, list):
            links += [v for v in val if isinstance(v, str) and ID_PATTERN.match(v)]
    return list(dict.fromkeys(links))

def _coletar_registros() -> list[FileRecord]:
    records = []
    for prefixo, diretorio in PREFIXOS.items():
        if not diretorio.exists():
            continue
        for arquivo in sorted(diretorio.glob("*.md")):
            meta = _read_fm(arquivo)
            rec_id = str(meta.get("id", ""))
            tipo   = str(meta.get("tipo", prefixo.lower()))
            versao = str(meta.get("versao", ""))
            status = str(meta.get("status", ""))
            tags   = meta.get("tags", []) or []
            links  = _extrair_links(meta)
            nome_ok = bool(NOME_DADOS_PATTERN.match(arquivo.name))
            meta_ok = all(k in meta for k in _METADADOS_OBR)
            records.append(FileRecord(
                id=rec_id or arquivo.stem,
                tipo=tipo, versao=versao, status=status,
                path=str(arquivo.relative_to(ROOT)),
                nome_valido=nome_ok, metadados_ok=meta_ok,
                links=links, tags=list(tags),
            ))
    return records

# ── State Engine ───────────────────────────────────────────────────────────
def _build_state(motores, records) -> dict:
    agora = datetime.now(timezone.utc).isoformat()
    score = round(sum(m.pontuacao for m in motores) / len(motores), 1) if motores else 0.0
    baseline_motor = next((m for m in motores if m.nome == "Baseline"), None)
    decisao = getattr(baseline_motor, "_decisao", None)
    approved = decisao.aprovado if decisao else all(not m.falhas for m in motores)
    domains = {m.nome: round(m.pontuacao, 1) for m in motores}
    completeness = decisao.grupos if decisao else {}
    critical, warnings = [], []
    for m in motores:
        for r in m.resultados:
            item = {"id": r.id, "motor": m.nome, "severity": r.severidade.value,
                    "title": r.titulo, "suggestions": r.sugestoes}
            if r.status == Status.FAIL:
                critical.append(item)
            elif r.status == Status.WARN:
                warnings.append(item)
    trend = "stable"
    if STATE_PATH.exists():
        try:
            prev = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            prev_score = prev.get("score", score)
            if score > prev_score + 0.5:
                trend = "improving"
            elif score < prev_score - 0.5:
                trend = "degrading"
        except:
            pass
    state = {
        "timestamp": agora, "score": score, "decision": "APPROVED" if approved else "REPROVADO",
        "trend": trend,
        "baseline": {
            "present": decisao.artefatos_presentes if decisao else 0,
            "total":   decisao.artefatos_total if decisao else 0,
            "pct":     decisao.pontuacao_geral if decisao else 0.0,
            "groups":  completeness,
            "missing": decisao.artefatos_ausentes if decisao else [],
        },
        "domains": domains,
        "issues": {"critical": critical, "warnings": warnings,
                   "counts": {"critical": len(critical), "warnings": len(warnings)}},
        "index": [asdict(r) for r in records],
    }
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    return state

def _load_state() -> dict | None:
    return json.loads(STATE_PATH.read_text(encoding="utf-8")) if STATE_PATH.exists() else None

# ── Motores ────────────────────────────────────────────────────────────────
def _carregar(nome: str):
    caminho = _MOTORES_V1[nome]
    sufixo = "" if nome in _LEGADOS else "_v1"
    return _importar_v1(f"motores.{nome}{sufixo}", caminho)

def _executar_motores(nomes: list[str]):
    from models_v1 import MotorResult, AuditResult, Severidade
    resultados = []
    for nome in nomes:
        try:
            mod = _carregar(nome)
            resultados.append(mod.executar())
        except Exception as e:
            mr = MotorResult(nome=nome.capitalize())
            mr.resultados.append(AuditResult(
                id="ERR-000", motor=nome, titulo=f"Erro interno: {e}",
                status=Status.FAIL, severidade=Severidade.CRITICA,
            ))
            resultados.append(mr)
    return resultados

def _pontuacao_geral(motores) -> float:
    return round(sum(m.pontuacao for m in motores) / len(motores), 1) if motores else 0.0

# ── Subcomandos ────────────────────────────────────────────────────────────
def cmd_run(args):
    nomes = [args.motor] if args.motor else (["baseline"] + [n for n in _MOTORES_V1 if n != "baseline"])
    records = _coletar_registros()
    resultados = _executar_motores(nomes)
    pct = _pontuacao_geral(resultados)
    console_v1 = _importar_v1(
        "relatorios.console_v1",
        SCRIPTS_AUDITORIA / "relatorios" / "console_v1.py",
    )
    console_v1.imprimir_console(resultados, pct)
    if args.relatorio:
        console_v1.gerar_markdown(resultados, pct)
    state = _build_state(resultados, records)
    nc = state["issues"]["counts"]["critical"]
    print(f"💾 Estado persistido: {STATE_PATH.relative_to(ROOT)}  |  {len(records)} registros indexados")
    return 1 if nc else 0

def cmd_state(args):
    state = _load_state()
    if not state:
        print("⚠️  Nenhum estado disponível. Execute: python3 auditor-v1.py")
        return 1
    if args.json:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0
    ts = state["timestamp"][:16].replace("T", " ")
    nc, nw = state["issues"]["counts"]["critical"], state["issues"]["counts"]["warnings"]
    icon = "✅" if state["decision"] == "APPROVED" else "❌"
    print(f"\n{icon} {state['decision']}  |  Score: {state['score']}%  |  Trend: {state['trend']}")
    print(f"   Timestamp: {ts}")
    print(f"   Baseline: {state['baseline']['present']}/{state['baseline']['total']} ({state['baseline']['pct']:.0f}%)")
    print(f"   Críticos: {nc}  |  Avisos: {nw}  |  Registros: {len(state['index'])}\n  Domínios:")
    for dom, pct in state["domains"].items():
        bar = "✅" if pct == 100 else ("⚠️" if pct >= 70 else "❌")
        print(f"    {bar} {dom:<20} {pct:.1f}%")
    return 0

def cmd_entity(args):
    state = _load_state()
    if not state:
        print("⚠️  Execute auditor-v1.py primeiro.")
        return 1
    eid = args.id.upper()
    matches = [r for r in state["index"] if r["id"].upper() == eid]
    if not matches:
        print(f"❌ Entidade '{eid}' não encontrada.")
        return 1
    rec = matches[0]
    print(f"\n📄 {rec['id']}  ({rec['tipo']}  v{rec['versao']})")
    print(f"   Status:       {rec['status']}\n   Path:         {rec['path']}")
    print(f"   Nome válido:  {'✅' if rec['nome_valido'] else '❌'}  |  Metadados ok: {'✅' if rec['metadados_ok'] else '❌'}")
    print(f"   Tags:         {', '.join(rec['tags']) or '—'}\n   Links:        {', '.join(rec['links']) or '—'}")
    return 0

def cmd_issues(args):
    state = _load_state()
    if not state:
        print("⚠️  Execute auditor-v1.py primeiro.")
        return 1
    items = state["issues"]["critical"] if args.critical else state["issues"]["critical"] + state["issues"]["warnings"]
    if not items:
        print("✅ Nenhum problema.")
        return 0
    for issue in items:
        icon = "❌" if issue["severity"] in ("ALTA", "CRITICA") else "⚠️"
        print(f"  {icon} [{issue['id']}] {issue['title']}")
        if issue["suggestions"]:
            print(f"       → {issue['suggestions'][0]}")
    return 0

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    # Detecta se é subcomando explícito
    subcommands = {"run", "state", "entity", "issues"}
    is_subcommand = len(sys.argv) > 1 and sys.argv[1] in subcommands
    
    if not is_subcommand:
        # Modo legado: sem subcomando ou com flags
        parser = argparse.ArgumentParser(description="FAA v1 — Auditoria Arquitetural")
        parser.add_argument("--motor", help="Executar apenas um motor")
        parser.add_argument("--relatorio", action="store_true", help="Gerar Markdown")
        args = parser.parse_args()
        args.cmd = "run"
        sys.exit(cmd_run(args))
    
    # Subcomandos explícitos
    parser = argparse.ArgumentParser(description="FAA v1 — Framework de Auditoria Arquitetural")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    p_run = sub.add_parser("run", help="Auditoria completa")
    p_run.add_argument("--motor", help="Executar apenas um motor")
    p_run.add_argument("--relatorio", action="store_true", help="Gerar Markdown")
    
    p_state = sub.add_parser("state", help="Exibe estado atual")
    p_state.add_argument("--json", action="store_true", help="Saída JSON")
    
    p_entity = sub.add_parser("entity", help="Inspeciona registro")
    p_entity.add_argument("id", help="Ex: REC-000001")
    
    p_issues = sub.add_parser("issues", help="Lista problemas")
    p_issues.add_argument("--critical", action="store_true", help="Apenas críticos")
    
    args = parser.parse_args()
    dispatch = {"run": cmd_run, "state": cmd_state, "entity": cmd_entity, "issues": cmd_issues}
    sys.exit(dispatch[args.cmd](args))

if __name__ == "__main__":
    main()
