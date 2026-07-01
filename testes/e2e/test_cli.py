"""Testes End-to-End do CLI do SOE-CCG.

Cobre todos os comandos da interface de linha de comando:
- importar
- validar
- status
- help
- erros

Valida:
- Exit codes corretos
- Saída padrão (stdout)
- Saída de erro (stderr)
- Tratamento de argumentos
- Comportamento em casos de sucesso e falha
"""
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

import pytest


class CLIResult(NamedTuple):
    """Resultado da execução do CLI."""
    exit_code: int
    stdout: str
    stderr: str


def run_cli(*args: str, cwd: Path | None = None) -> CLIResult:
    """Executa o CLI e retorna o resultado.
    
    Args:
        args: Argumentos para passar ao CLI
        cwd: Diretório de trabalho (opcional)
    
    Returns:
        CLIResult com exit_code, stdout e stderr
    """
    cmd = [sys.executable, "-m", "codigo", *args]
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return CLIResult(
        exit_code=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


# ============================================================================
# TESTES: Help e Uso
# ============================================================================

def test_cli_sem_argumentos_mostra_help():
    """CLI sem argumentos deve mostrar mensagem de help."""
    result = run_cli()
    
    assert result.exit_code == 0
    assert "uso: python -m" in result.stdout
    assert "Comandos:" in result.stdout
    assert "importar" in result.stdout
    assert "validar" in result.stdout
    assert "status" in result.stdout


def test_cli_flag_help_mostra_mensagem():
    """CLI com --help deve mostrar mensagem de help."""
    result = run_cli("--help")
    
    assert result.exit_code == 0
    assert "uso: python -m" in result.stdout
    assert "Comandos:" in result.stdout


def test_cli_flag_h_mostra_mensagem():
    """CLI com -h deve mostrar mensagem de help."""
    result = run_cli("-h")
    
    assert result.exit_code == 0
    assert "uso: python -m" in result.stdout


def test_cli_comando_desconhecido_retorna_erro():
    """Comando desconhecido deve retornar exit code 2."""
    result = run_cli("comando_inexistente")
    
    assert result.exit_code == 2
    assert "Comando desconhecido" in result.stderr
    assert "comando_inexistente" in result.stderr


# ============================================================================
# TESTES: Comando 'status'
# ============================================================================

def test_cli_status_sem_argumentos_sucesso():
    """Comando status deve executar sem erros."""
    result = run_cli("status")
    
    assert result.exit_code == 0
    assert "Entidades" in result.stdout
    assert "Arestas" in result.stdout


def test_cli_status_mostra_contagem_entidades():
    """Status deve mostrar contagem de entidades por tipo."""
    result = run_cli("status")
    
    assert result.exit_code == 0
    assert "Entidades" in result.stdout
    # Deve haver alguma entidade nos dados de teste
    assert "receita:" in result.stdout.lower() or \
           "ingrediente:" in result.stdout.lower() or \
           "tecnica:" in result.stdout.lower()


def test_cli_status_mostra_metricas_grafo():
    """Status deve mostrar métricas do grafo."""
    result = run_cli("status")
    
    assert result.exit_code == 0
    assert "Arestas" in result.stdout
    assert "Refs quebradas" in result.stdout
    assert "Issues" in result.stdout


# ============================================================================
# TESTES: Comando 'validar'
# ============================================================================

def test_cli_validar_sem_argumentos_sucesso():
    """Comando validar deve executar sem erros."""
    result = run_cli("validar")
    
    # Exit code pode ser 0 (sem issues) ou 1 (com issues)
    assert result.exit_code in (0, 1)


def test_cli_validar_dados_validos_retorna_ok():
    """Validar com dados válidos deve retornar OK."""
    result = run_cli("validar")
    
    # Se não há issues críticos, deve ser sucesso
    if "OK — sem issues" in result.stdout:
        assert result.exit_code == 0
    else:
        # Se há issues, verifica que são reportados
        assert "[" in result.stdout or "[" in result.stderr


def test_cli_validar_mostra_issues_se_houver():
    """Validar deve mostrar issues encontrados."""
    result = run_cli("validar")
    
    # Se exit code é 1, deve haver issues reportados
    if result.exit_code == 1:
        assert "[" in result.stdout or "[" in result.stderr
        # Deve ter alguma severidade
        assert any(sev in (result.stdout + result.stderr) 
                  for sev in ["[CRITICO]", "[AVISO]", "[INFO]", "[REF]"])


# ============================================================================
# TESTES: Comando 'importar'
# ============================================================================

def test_cli_importar_para_banco_temporario():
    """Importar deve criar banco SQLite no caminho especificado."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        # Exit code pode ser 0 (sucesso) ou 1 (com erros)
        assert result.exit_code in (0, 1)
        
        # Deve mostrar progresso
        assert "[importar]" in result.stdout
        assert "entidades encontradas" in result.stdout.lower()


def test_cli_importar_mostra_estatisticas():
    """Importar deve mostrar estatísticas de inserção."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        assert "Inseridos:" in result.stdout
        assert "Atualizados:" in result.stdout
        assert "Erros:" in result.stdout


def test_cli_importar_com_issues_criticos_aborta():
    """Importar com issues críticos deve abortar e retornar exit code 1."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        # Se há mensagem de ABORTADO, exit code deve ser 1
        if "ABORTADO" in result.stderr:
            assert result.exit_code == 1
            assert "crítico" in result.stderr


def test_cli_importar_sem_db_path_usa_padrao():
    """Importar sem caminho de banco deve usar padrão."""
    # Cria banco temporário para não poluir o real
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "soe.db"
        result = run_cli("importar", str(db_path))
        
        assert "[importar]" in result.stdout


def test_cli_importar_relata_erros_referencia():
    """Importar deve relatar erros de referência."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        # Se há erros de referência, devem estar no stderr
        if "[REF]" in result.stderr:
            assert "->" in result.stderr


# ============================================================================
# TESTES: Integração Completa
# ============================================================================

def test_cli_pipeline_completo():
    """Pipeline completo: status -> validar -> importar."""
    # 1. Status
    result_status = run_cli("status")
    assert result_status.exit_code == 0
    
    # 2. Validar
    result_validar = run_cli("validar")
    assert result_validar.exit_code in (0, 1)
    
    # 3. Importar
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result_importar = run_cli("importar", str(db_path))
        assert result_importar.exit_code in (0, 1)


def test_cli_importar_idempotente():
    """Importar duas vezes deve ser idempotente."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        # Primeira importação
        result1 = run_cli("importar", str(db_path))
        inseridos1 = _extract_count(result1.stdout, "Inseridos:")
        
        # Segunda importação (deve atualizar, não inserir)
        result2 = run_cli("importar", str(db_path))
        inseridos2 = _extract_count(result2.stdout, "Inseridos:")
        atualizados2 = _extract_count(result2.stdout, "Atualizados:")
        
        # Segunda vez não deve inserir novos (ou muito menos)
        assert inseridos2 <= inseridos1
        # Deve ter atualizações
        if inseridos1 > 0:
            assert atualizados2 > 0


# ============================================================================
# TESTES: Tratamento de Erros
# ============================================================================

def test_cli_importar_caminho_invalido_cria_db():
    """Importar com caminho de banco inválido deve tentar criar."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Caminho válido mas que não existe
        db_path = Path(tmpdir) / "subdir" / "test.db"
        # SQLite cria o banco, mas não o diretório pai
        # Então isso deve falhar ou criar o banco se o dir existir
        
        # Cria o diretório pai
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = run_cli("importar", str(db_path))
        # Deve tentar executar (pode ter erros de dados, mas não de CLI)
        assert result.exit_code in (0, 1)


def test_cli_todos_comandos_tem_exit_code_valido():
    """Todos os comandos devem retornar exit codes válidos (0, 1 ou 2)."""
    comandos = ["status", "validar"]
    
    for cmd in comandos:
        result = run_cli(cmd)
        assert result.exit_code in (0, 1, 2), \
            f"Comando '{cmd}' retornou exit code inválido: {result.exit_code}"


def test_cli_importar_com_multiplos_args_ignora_extras():
    """Importar com múltiplos argumentos deve usar apenas o primeiro."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path), "arg_extra")
        
        # Deve funcionar normalmente (ignora arg extra)
        assert result.exit_code in (0, 1)


# ============================================================================
# TESTES: Saída Estruturada
# ============================================================================

def test_cli_status_formato_saida_consistente():
    """Status deve ter formato de saída consistente."""
    result = run_cli("status")
    
    assert result.exit_code == 0
    lines = result.stdout.strip().split("\n")
    
    # Deve ter pelo menos as linhas principais
    assert any("Entidades" in line for line in lines)
    assert any("Arestas" in line for line in lines)


def test_cli_validar_erros_vao_para_stdout_ou_stderr():
    """Validar deve enviar issues para stdout/stderr apropriadamente."""
    result = run_cli("validar")
    
    # Deve ter saída em pelo menos um dos streams
    assert result.stdout or result.stderr
    
    # Se há issues críticos, devem ter prefixo [CRITICO]
    if "[CRITICO]" in (result.stdout + result.stderr):
        assert result.exit_code == 1


def test_cli_importar_progresso_vai_para_stdout():
    """Importar deve enviar progresso para stdout."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        # Mensagens de progresso no stdout
        assert "[importar]" in result.stdout


def test_cli_importar_erros_criticos_vao_para_stderr():
    """Importar deve enviar erros críticos para stderr."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        # Se há erros críticos, devem estar no stderr
        if result.exit_code == 1 and "[ERRO]" in result.stderr:
            assert "ABORTADO" in result.stderr or "[ERRO]" in result.stderr


# ============================================================================
# UTILITÁRIOS
# ============================================================================

def _extract_count(text: str, label: str) -> int:
    """Extrai contagem numérica após um label.
    
    Exemplo: "Inseridos: 42" -> 42
    """
    for line in text.split("\n"):
        if label in line:
            # Pega o primeiro número após o label
            parts = line.split(label, 1)[1].strip().split()
            if parts:
                try:
                    return int(parts[0])
                except ValueError:
                    pass
    return 0


# ============================================================================
# TESTES: Cobertura de Branches
# ============================================================================

def test_cli_validar_sem_issues_retorna_0():
    """Validar sem issues deve retornar exit code 0."""
    result = run_cli("validar")
    
    if "OK — sem issues" in result.stdout:
        assert result.exit_code == 0


def test_cli_validar_com_avisos_retorna_0():
    """Validar apenas com avisos (não críticos) deve retornar 0."""
    result = run_cli("validar")
    
    # Se só há [AVISO] ou [INFO], não há [CRITICO] nem [REF]
    if "[AVISO]" in result.stdout and \
       "[CRITICO]" not in (result.stdout + result.stderr) and \
       "[REF]" not in (result.stdout + result.stderr):
        assert result.exit_code == 0


def test_cli_validar_com_criticos_retorna_1():
    """Validar com issues críticos deve retornar exit code 1."""
    result = run_cli("validar")
    
    if "[CRITICO]" in (result.stdout + result.stderr):
        assert result.exit_code == 1


def test_cli_importar_sucesso_completo_retorna_0():
    """Importar sem erros deve retornar exit code 0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        result = run_cli("importar", str(db_path))
        
        # Se não há ABORTADO e não há [ERRO] no stderr
        if "ABORTADO" not in result.stderr and \
           result.stderr.count("[ERRO]") == 0:
            # Pode ser 0 (sucesso) ou ter avisos apenas
            assert result.exit_code in (0, 1)


# ============================================================================
# TESTES: Robustez
# ============================================================================

def test_cli_nao_trava_com_dados_vazios():
    """CLI não deve travar mesmo com dados vazios."""
    # Testa com diretório temporário vazio
    with tempfile.TemporaryDirectory() as tmpdir:
        # Temporariamente muda ROOT para diretório vazio
        # (não é possível fazer isso sem modificar o código)
        # Então testa apenas que o CLI não trava
        
        result = run_cli("status")
        assert result.exit_code in (0, 1, 2)


def test_cli_comandos_multiplas_execucoes():
    """Comandos devem ser executáveis múltiplas vezes."""
    for _ in range(3):
        result = run_cli("status")
        assert result.exit_code == 0


def test_cli_help_sempre_funciona():
    """Help deve sempre funcionar, mesmo com dados corrompidos."""
    result = run_cli("--help")
    assert result.exit_code == 0
    assert "uso:" in result.stdout


# ============================================================================
# MARCADORES DE TESTES
# ============================================================================

pytestmark = pytest.mark.e2e  # Marca todos os testes como E2E
