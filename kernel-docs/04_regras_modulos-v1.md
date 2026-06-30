---
id: KDOC-004
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Regras de Modulos

## Modulo Valido

Um modulo e valido quando:

- possui contrato registravel;
- declara capacidades fornecidas;
- declara capacidades exigidas;
- nao redefine paths estruturais;
- nao depende de cwd para localizar a raiz do projeto.

## Modulo Legado

Um modulo legado pode existir quando:

- esta coberto por adapter em entrypoint;
- nao redefine `ROOT`;
- e validado por testes;
- tem caminho de migracao documentado.

## Proibicoes

Modulos nao podem:

- importar o kernel e depois alterar estado interno do kernel;
- acessar paths estruturais por calculo proprio;
- introduzir dependencia circular;
- definir regra arquitetural fora de `kernel-docs/` ou `kernel/`.
