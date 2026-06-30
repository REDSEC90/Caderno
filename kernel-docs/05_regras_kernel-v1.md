---
id: KDOC-005
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Regras do Kernel

## Responsabilidades

O kernel pode:

- registrar modulos;
- validar contratos;
- resolver dependencias;
- controlar ciclo de vida;
- expor paths canonicos;
- executar validacoes arquiteturais.

## Limites

O kernel nao pode:

- conter regra gastronomica;
- importar `codigo`;
- importar `scripts`;
- ler registros de dominio para decidir comportamento de negocio;
- substituir o FAA.

## Bootstrap

`kernel/bootstrap.py` e o unico ponto logico de inicializacao estrutural.

Entry points podem chama-lo, mas nao podem duplicar sua responsabilidade.
