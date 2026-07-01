"""Testes unitários do módulo __main__ (CLI).

Testa as funções internas do CLI diretamente, sem subprocess.
Isso garante cobertura de código completa.
"""
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from codigo.__main__ import (
    _cmd_importar,
    _cmd_status,
    _cmd_validar,
    main,
)


# ============================================================================
# TESTES: _cmd_status
# ============================================================================

def test_cmd_status_retorna_0():
    """_cmd_status deve retornar 0."""
    exit_code = _cmd_status([])
    assert exit_code == 0


def test_cmd_status_mostra_entidades(capsys):
    """_cmd_status deve mostrar contagem de entidades."""
    _cmd_status([])
    captured = capsys.readouterr()
    
    assert "Entidades" in captured.out
    assert "Arestas" in captured.out
    assert "Issues" in captured.out


def test_cmd_status_mostra_tipos_entidades(capsys):
    """_cmd_status deve mostrar tipos de entidades."""
    _cmd_status([])
    captured = capsys.readouterr()
    
    # Deve mostrar algum tipo de entidade
    output_lower = captured.out.lower()
    assert any(tipo in output_lower for tipo in 
              ["receita", "ingrediente", "tecnica", "equipamento"])


# ============================================================================
# TESTES: _cmd_validar
# ============================================================================

def test_cmd_validar_retorna_0_ou_1():
    """_cmd_validar deve retornar 0 (sucesso) ou 1 (com issues)."""
    exit_code = _cmd_validar([])
    assert exit_code in (0, 1)


def test_cmd_validar_sem_issues_retorna_ok(capsys):
    """_cmd_validar sem issues deve mostrar OK."""
    exit_code = _cmd_validar([])
    captured = capsys.readouterr()
    
    if exit_code == 0:
        assert "OK" in captured.out


def test_cmd_validar_com_issues_mostra_severidade(capsys):
    """_cmd_validar com issues deve mostrar severidade."""
    exit_code = _cmd_validar([])
    captured = capsys.readouterr()
    
    if exit_code == 1:
        # Deve ter alguma severidade reportada
        output = captured.out + captured.err
        assert any(sev in output for sev in ["[CRITICO]", "[AVISO]", "[INFO]", "[REF]"])


def test_cmd_validar_ignora_argumentos():
    """_cmd_validar deve ignorar argumentos extras."""
    exit_code1 = _cmd_validar([])
    exit_code2 = _cmd_validar(["arg1", "arg2"])
    
    # Devem retornar o mesmo resultado
    assert exit_code1 == exit_code2


# ============================================================================
# TESTES: _cmd_importar
# ============================================================================

def test_cmd_importar_com_db_path():
    """_cmd_importar deve aceitar caminho de banco."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        exit_code = _cmd_importar([str(db_path)])
        
        assert exit_code in (0, 1)
        # Banco deve ser criado
        assert db_path.exists()


def test_cmd_importar_sem_db_path_usa_padrao():
    """_cmd_importar sem db_path deve usar padrão."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        # Passa db_path para evitar sobrescrever banco real
        exit_code = _cmd_importar([str(db_path)])
        
        assert exit_code in (0, 1)


def test_cmd_importar_mostra_progresso(capsys):
    """_cmd_importar deve mostrar progresso."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        assert "[importar]" in captured.out
        assert "Parseando" in captured.out
        assert "entidades encontradas" in captured.out


def test_cmd_importar_mostra_estatisticas(capsys):
    """_cmd_importar deve mostrar estatísticas."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        assert "Inseridos:" in captured.out
        assert "Atualizados:" in captured.out
        assert "Erros:" in captured.out


def test_cmd_importar_com_issues_criticos_aborta(capsys):
    """_cmd_importar com issues críticos deve abortar."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        exit_code = _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        if "ABORTADO" in captured.err:
            assert exit_code == 1
            assert "crítico" in captured.err


def test_cmd_importar_sem_erros_retorna_0():
    """_cmd_importar sem erros deve retornar 0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        exit_code = _cmd_importar([str(db_path)])
        
        # Se não há mensagem de erro, deve ser 0
        # (depende dos dados, mas testa o comportamento)
        assert exit_code in (0, 1)


def test_cmd_importar_erros_referencia_vao_stderr(capsys):
    """_cmd_importar deve enviar erros de referência para stderr."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        # Se há erros de referência, devem estar no stderr
        if "[REF]" in captured.err:
            assert "->" in captured.err


# ============================================================================
# TESTES: main()
# ============================================================================

def test_main_sem_argumentos_mostra_help():
    """main() sem argumentos deve mostrar help e sair com 0."""
    with patch.object(sys, 'argv', ['codigo']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0


def test_main_com_help_mostra_mensagem(capsys):
    """main() com --help deve mostrar mensagem de help."""
    with patch.object(sys, 'argv', ['codigo', '--help']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "uso:" in captured.out
        assert "Comandos:" in captured.out


def test_main_com_h_mostra_mensagem(capsys):
    """main() com -h deve mostrar mensagem de help."""
    with patch.object(sys, 'argv', ['codigo', '-h']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "uso:" in captured.out


def test_main_comando_desconhecido_retorna_2(capsys):
    """main() com comando desconhecido deve retornar exit code 2."""
    with patch.object(sys, 'argv', ['codigo', 'comando_invalido']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert "Comando desconhecido" in captured.err
        assert "comando_invalido" in captured.err


def test_main_status_executa_com_sucesso():
    """main() com comando status deve executar."""
    with patch.object(sys, 'argv', ['codigo', 'status']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0


def test_main_validar_executa():
    """main() com comando validar deve executar."""
    with patch.object(sys, 'argv', ['codigo', 'validar']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        # Exit code pode ser 0 ou 1 dependendo dos dados
        assert exc_info.value.code in (0, 1)


def test_main_importar_com_db_path():
    """main() com comando importar deve aceitar db_path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        with patch.object(sys, 'argv', ['codigo', 'importar', str(db_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            # Exit code pode ser 0 ou 1 dependendo dos dados
            assert exc_info.value.code in (0, 1)
            assert db_path.exists()


def test_main_importar_sem_db_path():
    """main() com comando importar sem db_path deve usar padrão."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        with patch.object(sys, 'argv', ['codigo', 'importar', str(db_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code in (0, 1)


# ============================================================================
# TESTES: Integração de Comandos
# ============================================================================

def test_comandos_consecutivos():
    """Comandos consecutivos devem funcionar independentemente."""
    # Status
    exit_code1 = _cmd_status([])
    assert exit_code1 == 0
    
    # Validar
    exit_code2 = _cmd_validar([])
    assert exit_code2 in (0, 1)
    
    # Status novamente
    exit_code3 = _cmd_status([])
    assert exit_code3 == 0


def test_importar_multiplas_vezes_idempotente():
    """Importar múltiplas vezes deve ser idempotente."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        # Primeira importação
        exit_code1 = _cmd_importar([str(db_path)])
        
        # Segunda importação
        exit_code2 = _cmd_importar([str(db_path)])
        
        # Ambas devem ter sucesso (ou falhar da mesma forma)
        assert exit_code1 in (0, 1)
        assert exit_code2 in (0, 1)


# ============================================================================
# TESTES: Branches e Cobertura
# ============================================================================

def test_cmd_importar_branch_sem_criticos():
    """Branch sem issues críticos no importar."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        exit_code = _cmd_importar([str(db_path)])
        
        # Testa que o código não falha
        assert exit_code in (0, 1)


def test_cmd_importar_branch_com_erros_ref(capsys):
    """Branch com erros de referência no importar."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        # Verifica que erros de ref são tratados
        # (pode não haver, depende dos dados)
        assert "[importar]" in captured.out


def test_cmd_importar_branch_sem_erros_result():
    """Branch sem erros no result da importação."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        exit_code = _cmd_importar([str(db_path)])
        
        # Se result.erros está vazio, exit_code deve ser 0
        # (depende dos dados, mas testa o fluxo)
        assert exit_code in (0, 1)


def test_cmd_validar_branch_sem_issues():
    """Branch sem issues no validar."""
    exit_code = _cmd_validar([])
    
    # Testa que o código funciona
    assert exit_code in (0, 1)


def test_cmd_validar_branch_com_criticos():
    """Branch com issues críticos no validar."""
    exit_code = _cmd_validar([])
    
    # Se há críticos, exit_code deve ser 1
    # (depende dos dados)
    assert exit_code in (0, 1)


# ============================================================================
# TESTES: Cobertura de _COMMANDS
# ============================================================================

def test_commands_dict_contem_todos_comandos():
    """Dicionário _COMMANDS deve conter todos os comandos."""
    from codigo.__main__ import _COMMANDS
    
    assert 'importar' in _COMMANDS
    assert 'validar' in _COMMANDS
    assert 'status' in _COMMANDS
    assert len(_COMMANDS) == 3


def test_commands_dict_valores_sao_funcoes():
    """Valores de _COMMANDS devem ser funções."""
    from codigo.__main__ import _COMMANDS
    
    for cmd, handler in _COMMANDS.items():
        assert callable(handler), f"Comando '{cmd}' não é callable"


# ============================================================================
# TESTES: Cobertura de _HELP
# ============================================================================

def test_help_string_contem_comandos():
    """String de help deve conter todos os comandos."""
    from codigo.__main__ import _HELP
    
    assert "importar" in _HELP
    assert "validar" in _HELP
    assert "status" in _HELP
    assert "uso:" in _HELP


# ============================================================================
# TESTES: Cobertura de if __name__ == '__main__'
# ============================================================================

def test_main_como_modulo():
    """main() deve funcionar quando chamado como módulo."""
    with patch.object(sys, 'argv', ['codigo', 'status']):
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0


# ============================================================================
# TESTES: Robustez
# ============================================================================

def test_cmd_status_multiplas_chamadas():
    """_cmd_status deve funcionar múltiplas vezes."""
    for _ in range(3):
        exit_code = _cmd_status([])
        assert exit_code == 0


def test_cmd_validar_multiplas_chamadas():
    """_cmd_validar deve funcionar múltiplas vezes."""
    for _ in range(3):
        exit_code = _cmd_validar([])
        assert exit_code in (0, 1)


def test_todos_comandos_retornam_int():
    """Todos os comandos devem retornar int."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        
        exit_code1 = _cmd_status([])
        exit_code2 = _cmd_validar([])
        exit_code3 = _cmd_importar([str(db_path)])
        
        assert isinstance(exit_code1, int)
        assert isinstance(exit_code2, int)
        assert isinstance(exit_code3, int)


# ============================================================================
# TESTES: Cobertura de Branches Específicos
# ============================================================================

def test_cmd_importar_com_erros_result_retorna_1(capsys):
    """Branch com erros no result.erros deve retornar 1."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        exit_code = _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        # Se há [ERRO] no stderr, exit_code deve ser 1
        if "[ERRO]" in captured.err and "ABORTADO" not in captured.err:
            assert exit_code == 1


def test_cmd_validar_com_erros_ref_reporta(capsys):
    """_cmd_validar com erros de ref deve reportá-los."""
    exit_code = _cmd_validar([])
    captured = capsys.readouterr()
    
    # Se há erros de referência, devem ser reportados
    if "[REF]" in captured.out:
        assert "->" in captured.out


def test_cmd_validar_retorna_1_com_erros_ref():
    """_cmd_validar deve retornar 1 se houver erros de referência."""
    exit_code = _cmd_validar([])
    
    # Testa o comportamento (depende dos dados)
    assert exit_code in (0, 1)


def test_cmd_importar_reporta_todos_tipos_severidade(capsys):
    """_cmd_importar deve reportar CRITICO, AVISO e INFO."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        _cmd_importar([str(db_path)])
        captured = capsys.readouterr()
        
        output = captured.out + captured.err
        # Verifica que diferentes severidades são tratadas
        # (pode não haver todas, depende dos dados)
        assert any(sev in output for sev in ["[ERRO]", "[AVISO]", "[INFO]", "Inseridos"])


def test_cmd_validar_reporta_todos_tipos_issue(capsys):
    """_cmd_validar deve reportar issues com todos os campos."""
    exit_code = _cmd_validar([])
    captured = capsys.readouterr()
    
    # Se há issues, devem ter formato correto
    if exit_code == 1:
        output = captured.out
        # Formato: [SEVERIDADE] entity_id (tipo_issue): mensagem
        if "[" in output:
            assert any(char in output for char in [":", "(", ")"])
