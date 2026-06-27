# SOE-CCG V2

## Plano Diretor da Plataforma Semântica

**Status:** Proposta Arquitetural
**Versão:** V2 Draft
**Objetivo:** Evoluir o SOE-CCG de um sistema documental para uma plataforma semântica viva.

---

# 1. Introdução

A primeira versão do SOE-CCG resolveu um problema extremamente importante:

> representar conhecimento de forma estruturada, auditável e persistente.

Durante a V1 foram consolidados:

* modelo documental;
* convenções de domínio;
* banco SQLite;
* parser Markdown;
* IR (Intermediate Representation);
* KnowledgeGraph em memória;
* resolvedor de referências;
* importador;
* FAA.

Com a criação do pipeline

```
Markdown
    ↓
Parser
    ↓
IR
    ↓
KnowledgeGraph
    ↓
SQLite
```

o projeto deixou de ser apenas um conjunto de documentos e passou a possuir um núcleo computacional de conhecimento.

A V2 não pretende substituir esse núcleo.

Seu objetivo é transformá-lo em uma plataforma permanente.

---

# 2. Princípio Arquitetural

A V2 adota como princípio central:

> Todo conhecimento é representado como um grafo tipado vivo, governado por regras declarativas, operado por uma plataforma independente dos consumidores.

Existem quatro consequências dessa decisão.

O conhecimento deixa de ser:

* arquivos;
* tabelas;
* consultas SQL;
* texto Markdown.

E passa a existir como:

* entidades;
* relacionamentos;
* regras;
* eventos;
* inferências.

---

# 3. Objetivos da V2

A V2 possui cinco grandes objetivos.

## Objetivo 1

Transformar o núcleo existente em uma plataforma reutilizável.

## Objetivo 2

Eliminar duplicação entre FAA, parser e futuras ferramentas.

## Objetivo 3

Permitir evolução incremental do conhecimento.

## Objetivo 4

Preparar o sistema para múltiplos domínios.

## Objetivo 5

Preparar a arquitetura para V3 sem necessidade de reestruturação.

---

# 4. Arquitetura Geral

```
                    Consumidores

       FAA
       CLI
       API
       GUI
       IA
       Ferramentas

                 │

                 ▼

             SOE Platform

        RuntimeContext
        Query Engine
        Rule Engine
        Event Bus
        Schema Registry
        Plugin Manager
        Lifecycle
        Config
        Logging

                 │

                 ▼

           KnowledgeGraph

        Entidades
        Relacionamentos
        Índices
        Proveniência

                 │

                 ▼

        Parser / Importador

                 │

                 ▼

        Markdown (Fonte da Verdade)

                 │

                 ▼

            SQLite (Cache)
```

O Markdown permanece como fonte oficial.

SQLite passa a ser apenas armazenamento otimizado.

O KnowledgeGraph passa a representar o estado vivo do conhecimento.

---

# 5. E00 — Plataforma

Antes de qualquer nova funcionalidade será construída a plataforma.

Estrutura proposta:

```
soe/

    core/

        graph.py

        parser.py

        resolver.py

        importer.py

        ir.py

    platform/

        context.py

        lifecycle.py

        config.py

        logging.py

        schema_registry.py

        metrics.py

    engines/

        query/

        validation/

        inference/

        indexing/

    consumers/

        faa/

        cli/

        api/

        gui/

    plugins/

        base/

        domains/
```

Todo o conteúdo atual de `codigo/` migra para `soe/core`.

---

# 6. RuntimeContext

O RuntimeContext representa o ponto de entrada da plataforma.

Ele não deve se tornar um objeto gigante.

Cada componente será exposto através de interfaces pequenas.

Exemplo:

```
ctx.query()

ctx.rules()

ctx.events()

ctx.schemas()

ctx.plugins()
```

Consumidores nunca acessam estruturas internas diretamente.

Exemplo incorreto:

```
ctx.graph.edges(...)
```

Exemplo correto:

```
ctx.query(
    outgoing_kind=STRUCTURAL,
    source="REC-000001"
)
```

A plataforma controla como responder.

---

# 7. KnowledgeGraph

O KnowledgeGraph deixa de ser um snapshot temporário.

Passa a ser um componente residente.

Responsabilidades:

* armazenar entidades;
* armazenar relacionamentos;
* manter índices;
* oferecer navegação;
* armazenar proveniência;
* suportar snapshots imutáveis.

Não possui regras de negócio.

Não realiza inferência.

Não valida documentos.

---

# 8. Query Engine

Toda consulta ao conhecimento passa obrigatoriamente pelo Query Engine.

Nenhum consumidor navega diretamente pelo grafo.

O Query Engine deve suportar:

* consulta por entidade;
* consulta por relacionamento;
* travessias;
* filtros;
* predicados;
* consultas futuras por subgrafos.

A interface não deve limitar futuras consultas estruturais.

---

# 9. Rule Engine

Toda validação deixa de ser código hardcoded.

As regras passam a ser declarativas.

Exemplos:

* obrigatoriedade de campos;
* cardinalidade;
* restrições entre entidades;
* ciclos;
* dependências.

FAA torna-se apenas executor de regras.

---

# 10. Schema Registry

O Schema Registry torna-se a representação oficial dos esquemas.

Cada entidade possui definição própria.

Exemplo conceitual:

```
Receita

campos obrigatórios

campos opcionais

relacionamentos permitidos

restrições

versão
```

Ele conecta:

* parser;
* validator;
* ontologia futura.

---

# 11. Sistema de Relacionamentos

A arquitetura diferencia origem e natureza das relações.

## Origem

Existem apenas duas categorias.

### SourcedEdge

Originada do Markdown.

Persistente.

Auditável.

### DerivedEdge

Produzida por inferência.

Nunca editada manualmente.

Sempre reconstruível.

---

# 12. Proveniência

Toda DerivedEdge deve registrar:

* regra aplicada;
* caminho utilizado;
* entidades intermediárias;
* timestamp;
* versão do runtime.

Toda inferência deve ser explicável.

---

# 13. Regra Fundamental da Inferência

DerivedEdges nunca podem ser utilizadas como entrada para novas inferências.

Inferência opera exclusivamente sobre SourcedEdges.

Isso elimina:

* loops infinitos;
* crescimento exponencial;
* proveniência impossível.

---

# 14. Event Bus

Mudanças deixam de exigir reimportação completa.

Eventos típicos:

```
EntityCreated

EntityUpdated

EntityRemoved

RelationshipAdded

RelationshipRemoved

ImportFinished
```

Consumidores se inscrevem nesses eventos.

---

# 15. Modelo de Concorrência

A V2 adota:

Single Writer

Multiple Readers

Cada atualização produz um novo snapshot do grafo.

Consultas continuam utilizando o snapshot anterior até sua conclusão.

Benefícios:

* ausência de locks complexos;
* consistência;
* simplicidade;
* previsibilidade.

---

# 16. Plugin System

Plugins deixam de modificar código interno.

Eles registram:

* regras;
* esquemas;
* consultas;
* tipos;
* importadores especializados.

Cada domínio torna-se um pacote independente.

---

# 17. Ontologia

Tipos não pertencem ao runtime.

Tipos pertencem ao próprio conhecimento.

Exemplo:

```
Ingrediente

↓

Subtipo

↓

Fermentável

↓

Subtipo

↓

Açúcar
```

A ontologia passa a existir como subgrafo.

Isso torna o sistema verdadeiramente agnóstico ao domínio.

---

# 18. FAA

FAA deixa de conhecer:

* Markdown;
* parser;
* SQLite;
* importação.

FAA apenas solicita:

```
executar regras
```

ou

```
executar auditoria
```

Toda lógica reside na plataforma.

---

# 19. Roadmap

## Fase 1

Plataforma

* migração para pacote Python;
* RuntimeContext;
* configuração;
* lifecycle;
* logging;
* Schema Registry;
* testes.

---

## Fase 2

Formalização do núcleo

* KnowledgeGraph residente;
* Query Engine;
* interfaces públicas;
* eliminação de duplicação.

---

## Fase 3

Validação

* Rule Engine;
* DSL declarativa;
* migração das regras atuais do FAA.

---

## Fase 4

Inferência

* DerivedEdges;
* proveniência;
* explicabilidade;
* consultas derivadas.

---

## Fase 5

Reatividade

* Event Bus;
* snapshots;
* atualização incremental;
* índice semântico.

---

## Fase 6

Extensibilidade

* plugins;
* ontologia;
* múltiplos domínios;
* versionamento de entidades.

---

# 20. Objetivos Não Pertencentes à V2

Os seguintes itens são explicitamente adiados para V3:

* comparação estrutural entre subgrafos;
* detecção automática de duplicação conceitual;
* clustering semântico;
* recomendação de documentação;
* análise de impacto baseada em similaridade;
* raciocínio sobre padrões estruturais;
* aprendizado sobre evolução do conhecimento.

Essas funcionalidades dependem de uma plataforma consolidada e de um Query Engine capaz de operar sobre predicados estruturais.

---

# 21. Visão Final

Ao término da V2, o SOE-CCG deixa de ser um conjunto de ferramentas independentes e passa a constituir uma plataforma semântica reutilizável.

O Markdown permanece como fonte oficial do conhecimento.

O KnowledgeGraph representa o estado vivo desse conhecimento.

A Plataforma coordena seu ciclo de vida, regras, consultas, eventos e extensões.

Todos os consumidores — FAA, CLI, API, interfaces gráficas e futuros agentes de IA — passam a utilizar exatamente a mesma infraestrutura, eliminando duplicação de lógica e permitindo evolução incremental, auditável e escalável para milhões de entidades e múltiplos domínios de conhecimento.

