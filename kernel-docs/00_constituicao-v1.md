---
id: KDOC-000
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Constituicao do Kernel

O kernel do SOE-CCG e a autoridade estrutural do sistema.

Ele nao define conhecimento gastronomico.
Ele define como o sistema permanece coerente enquanto processa conhecimento gastronomico.

## Leis

1. O Markdown em `dados/` e a fonte canonica do conhecimento.
2. O SQLite e sempre indice derivado.
3. O kernel nao contem regra de negocio.
4. O kernel controla contratos, paths, registro de modulos e ciclo de vida.
5. Todo modulo estrutural deve ser registravel.
6. Toda dependencia estrutural deve ser declarada.
7. Nenhum modulo fora do kernel pode redefinir `ROOT`.
8. Nenhuma evolucao pode depender de estado global implicito.
9. Scripts legados podem usar adapters temporarios, mas a autoridade de path continua sendo `kernel.shared.paths`.
10. Regras arquiteturais devem ser verificaveis por contrato automatizado.

## Fonte Superior

Este documento complementa `docs/00-projeto/constituicao-v1.md`.
Em caso de conflito, a constituicao do projeto define o principio e este documento define o mecanismo tecnico.
