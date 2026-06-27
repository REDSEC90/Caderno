Após analisar a estrutura do projeto, fica claro que o SOE-CCG já atingiu um nível em que a documentação não deve mais ser vista como "documentação de apoio". Ela passa a ser parte da própria arquitetura do sistema.

A V2 deveria considerar `docs/07-uso/` como um **produto oficial**, equivalente a uma API pública: altamente estável, previsível, versionado e com mudanças extremamente controladas.

Minha recomendação é que a V2 trate essa pasta como uma **Especificação Operacional Imutável (Operational Specification)**.

O objetivo deixa de ser "explicar como usar" e passa a ser:

> **Definir, de forma única, oficial e normativa, como qualquer ser humano, ferramenta ou agente de IA deve operar o SOE-CCG.**

Isso conversa diretamente com toda a arquitetura existente do projeto (domínio, FAA, parser, resolver, importador, Knowledge Graph, runtime e governança).

---

# Objetivos da documentação V2

A documentação deve ser capaz de:

* ensinar um usuário novo;
* servir de referência rápida;
* padronizar procedimentos;
* eliminar interpretações diferentes;
* permitir execução por IA;
* servir como documentação normativa;
* permanecer estável durante toda a V2.

Ela não deve conter decisões arquiteturais.

Ela não deve explicar implementação interna.

Ela deve explicar somente **operação**.

---

# Estrutura Geral

```text
docs/
└── 07-uso/
    │
    ├── README.md
    │
    ├── 00-politicas/
    │
    ├── 01-fundamentos/
    │
    ├── 02-modelo-mental/
    │
    ├── 03-operacao/
    │
    ├── 04-fluxos/
    │
    ├── 05-validacao/
    │
    ├── 06-consultas/
    │
    ├── 07-manutencao/
    │
    ├── 08-contribuicao/
    │
    ├── 09-referencia/
    │
    ├── 10-exemplos/
    │
    ├── 11-checklists/
    │
    └── 12-apendices/
```

Essa estrutura acompanha o ciclo completo de vida do conhecimento.

---

# 00 — Políticas

Esta seção define regras imutáveis.

Não ensina.

Define.

Exemplo:

```
00-politicas/

01-escopo.md
02-garantias.md
03-convencoes.md
04-versionamento.md
05-estabilidade.md
06-documentacao-normativa.md
```

Ela responde perguntas como:

* o que pertence ao manual;
* o que não pertence;
* quais documentos são normativos;
* quais documentos são apenas informativos;
* como futuras alterações devem ocorrer.

---

# 01 — Fundamentos

Explica apenas conceitos.

Nunca procedimentos.

Arquivos:

```
01-o-que-e-o-soe.md

02-conceitos.md

03-entidades.md

04-relacionamentos.md

05-grafo.md

06-documentos.md

07-conhecimento.md
```

---

# 02 — Modelo Mental

Na minha opinião esta será uma das partes mais importantes.

Ela muda completamente a forma como o usuário enxerga o projeto.

Exemplo:

```
01-como-pensar-no-soe.md

02-conhecimento-vs-arquivos.md

03-modelagem.md

04-reutilizacao.md

05-granularidade.md

06-evolucao.md
```

Aqui o usuário entende que:

> Ele nunca cria Markdown.

Ele cria conhecimento.

Markdown é apenas uma representação.

---

# 03 — Operação

Aqui começa o uso real.

```
01-primeiros-passos.md

02-ciclo-de-vida.md

03-criar-entidade.md

04-criar-relacionamento.md

05-editar.md

06-remover.md

07-versionar.md

08-validar.md

09-importar.md

10-consultar.md
```

Cada documento ensina uma única operação.

---

# 04 — Fluxos

Talvez a pasta mais usada.

Cada documento representa um caso real.

```
01-criar-receita.md

02-criar-tecnica.md

03-criar-observacao.md

04-criar-experimento.md

05-atualizar.md

06-corrigir-erro.md

07-resolver-ciclo.md

08-fluxo-completo.md
```

Todos seguem exatamente o mesmo template.

```
Objetivo

Pré-requisitos

Passo 1

Passo 2

...

Validação

Resultado esperado

Checklist

Erros comuns
```

---

# 05 — Validação

Explica o pipeline operacional.

Não implementação.

```
01-parser.md

02-resolver.md

03-validator.md

04-faa.md

05-importador.md

06-pipeline.md

07-resolucao-de-erros.md
```

---

# 06 — Consultas

Pensada para o Knowledge Graph.

```
01-como-consultar.md

02-pesquisa.md

03-navegacao.md

04-relacionamentos.md

05-exemplos.md
```

---

# 07 — Manutenção

Uma seção normalmente esquecida.

```
01-atualizando-documentos.md

02-refatoracao.md

03-migracoes.md

04-obsolescencia.md

05-compatibilidade.md

06-integridade.md
```

---

# 08 — Contribuição

Voltada aos colaboradores.

```
01-padroes.md

02-estilo.md

03-adr.md

04-code-review.md

05-checklist.md

06-erros-comuns.md
```

---

# 09 — Referência

Consulta rápida.

Sem explicações longas.

```
01-entidades.md

02-relacionamentos.md

03-estados.md

04-campos.md

05-comandos.md

06-cheat-sheet.md
```

Tudo em tabelas.

---

# 10 — Exemplos

Casos completos.

```
01-receita.md

02-ingrediente.md

03-observacao.md

04-tecnica.md

05-experimento.md

06-correcao.md

07-ciclo.md

08-grande-exemplo.md
```

---

# 11 — Checklists

Extremamente útil.

```
01-criacao.md

02-validacao.md

03-importacao.md

04-release.md

05-auditoria.md
```

Um operador consegue confirmar rapidamente que nenhuma etapa foi esquecida.

---

# 12 — Apêndices

Material complementar.

```
01-glossario.md

02-acronimos.md

03-diagramas.md

04-faq.md

05-historico.md
```

---

# Padronização obrigatória dos documentos

Todos os arquivos devem seguir exatamente o mesmo template, por exemplo:

```text
Título

Objetivo

Escopo

Quando utilizar

Pré-requisitos

Procedimento

Exemplos

Boas práticas

Erros comuns

Validação

Resultado esperado

Referências relacionadas

Histórico
```

Essa uniformidade reduz a carga cognitiva e facilita a navegação tanto por pessoas quanto por agentes de IA.

---

# Princípios de Imutabilidade da V2

Para que essa documentação permaneça estável durante todo o ciclo da V2, proponho estabelecer regras de governança:

* **Estrutura congelada**: não criar, remover ou renomear diretórios sem uma ADR aprovada.
* **Documentos normativos**: cada procedimento oficial possui uma única fonte de verdade.
* **Separação de responsabilidades**: arquitetura, implementação e operação nunca se misturam.
* **Links permanentes**: caminhos e âncoras devem ser preservados para evitar quebra de referências.
* **Template obrigatório**: todos os documentos seguem a mesma organização.
* **Versionamento controlado**: alterações em fluxos operacionais exigem revisão formal.
* **Orientação ao ciclo de vida**: toda documentação acompanha o fluxo completo do conhecimento, da modelagem à consulta.
* **Compatibilidade com IA**: documentos escritos para serem facilmente interpretados e executados por agentes automatizados.

## Visão de longo prazo

Na V2, `docs/07-uso` deve deixar de ser apenas uma coleção de guias e tornar-se uma **Especificação Operacional Canônica do SOE-CCG**. Ela será a fonte única de verdade para a operação do sistema, consumida por usuários, desenvolvedores, mantenedores, ferramentas e agentes de IA, garantindo que todos executem os mesmos processos, na mesma ordem, com os mesmos critérios de validação e qualidade. Esse caráter normativo reduz ambiguidades, facilita auditorias, preserva a consistência da base de conhecimento e permite que a evolução do projeto ocorra sem comprometer a estabilidade operacional.

