---
id: KDOC-002
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Invariantes

1. Todo acesso estrutural a path vem do kernel.
2. Todo modulo estrutural tem contrato declarativo.
3. Todo contrato e validado antes da execucao.
4. Toda dependencia declarada tem provedor registrado.
5. Nenhum provedor fornece a mesma capacidade que outro provedor.
6. O kernel nao importa implementacoes de aplicacao.
7. O runtime atual pode permanecer em `codigo/` ate migracao formal.
8. O FAA pode permanecer em `scripts/` ate fusao formal em `runtime/analysis/`.
9. Documentos normativos ficam versionados.
10. Artefatos `v1` sao referencias congeladas.
