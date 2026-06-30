# Glossário — SOE-CCG

> Todos os termos técnicos utilizados no sistema, em ordem alfabética.

---

## ADR (Architectural Decision Record)
Documento que registra formalmente uma decisão arquitetural: o contexto, as opções consideradas, a decisão tomada e as consequências. Localizados em `docs/04-padroes/`.

## Aresta (Edge)
Conexão direcional entre duas entidades no grafo de conhecimento. Toda aresta tem um tipo (EdgeKind), uma origem (EdgeOrigin) e fonte e destino identificados por ID. Implementada em `codigo/ir-v1.py`.

## Baseline
Conjunto mínimo de artefatos que o sistema considera obrigatórios para estar em conformidade. Verificado pelo motor `baseline` do FAA. Um sistema que não atinge 100% do baseline bloqueante é reprovado.

## Ciclo (Cycle)
Situação onde as arestas de um grafo formam um caminho fechado: A → B → C → A. Ciclos em arestas estruturais são sempre problemáticos. Ciclos em arestas informacionais podem ser semanticamente válidos (referências cruzadas).

## Contrato
Documento formal que especifica as obrigações que uma entidade deve cumprir — campos obrigatórios, relacionamentos permitidos e restrições. Localizado em `docs/01-dominio/contratos/`.

## EdgeKind (Tipo de Aresta)
Classificação semântica de uma aresta no grafo. Os tipos são:
- `STRUCTURAL` — relação estrutural (frontmatter, campo de referência simples)
- `COMPOSITIONAL` — composição (listas como `ingredientes`, `tecnicas`, `equipamentos`)
- `HIERARCHICAL` — hierarquia (pai/filho)
- `DERIVATION` — derivação (experimento baseado em receita)
- `INFORMATIONAL` — menção contextual (referência no corpo do documento)
- `OPTIONAL` — referência opcional

## EdgeOrigin (Origem da Aresta)
De onde a aresta foi extraída pelo Parser:
- `FRONTMATTER` — campo no cabeçalho YAML do arquivo
- `BODY` — menção de ID no corpo do documento
- `GENERATED` — gerada automaticamente pelo sistema

## Entidade
Um objeto de conhecimento com identidade permanente, tipo definido, metadados padronizados e relacionamentos formais. Os sete tipos de entidade são: Receita, Ingrediente, Técnica, Equipamento, Execução, Observação, Experimento.

## Esquema (Schema)
Definição formal dos campos, tipos e restrições de um tipo de entidade. O `schema-version` no frontmatter indica qual versão do esquema o arquivo segue.

## Experimento (EXP)
Entidade que registra uma hipótese sendo testada deliberadamente. Tem ciclo de vida próprio: `aberto → concluido → incorporado | descartado`.

## Execução (EXE)
Registro de um preparo real de uma receita em um momento específico. Captura o que realmente aconteceu — ingredientes usados, métricas, avaliações, desvios.

## FAA (Framework de Auditoria Arquitetural)
Sistema de verificação automatizada da saúde arquitetural do repositório. Composto por 12 motores de auditoria. Produz uma decisão (`APROVADO` ou `REPROVADO`) e um score numérico (0–100%). Executado via `python3 scripts/auditoria/auditor-v1.py`.

## Frontmatter
Cabeçalho YAML delimitado por `---` no início de cada arquivo Markdown. Contém os metadados estruturados da entidade (id, tipo, status, datas, relacionamentos).

## Grafo de Conhecimento (KnowledgeGraph)
Estrutura em memória construída pelo Parser que representa todas as entidades e suas arestas. É o objeto central do pipeline de validação.

## Identificador (ID)
Código permanente no formato `[PREFIXO]-[NNNNNN]` atribuído a uma entidade no momento de sua criação. Nunca muda. Nunca é reutilizado. Exemplos: `REC-000001`, `ING-000004`.

## Importador
Script (`codigo/importador-v1.py`) que recebe um KnowledgeGraph resolvido e persiste os dados no banco SQLite. Nunca lê Markdown diretamente — sempre opera sobre o grafo.

## IR (Intermediate Representation)
A camada de representação interna do sistema, definida em `codigo/ir-v1.py`. Contém as classes `Edge`, `EdgeKind`, `EdgeOrigin`, `Entity` e `KnowledgeGraph`.

## Motor de Auditoria
Módulo Python (`scripts/auditoria/motores/`) responsável por verificar um aspecto específico do sistema. Cada motor produz uma lista de issues com severidade e uma pontuação.

## Observação (OBS)
Entidade que registra uma percepção, descoberta ou nota vinculada a qualquer outra entidade. Tem campo `relevancia` (baixa, media, alta) e `entidade-referenciada`.

## Parser
Script (`codigo/parser-v1.py`) que lê arquivos Markdown e constrói o KnowledgeGraph. Extrai entidades do frontmatter e arestas tanto do frontmatter quanto do corpo do documento.

## Plugin
Módulo de extensão do FAA que adiciona regras customizadas de validação. Localizado em `scripts/faa/plugins/`.

## Proveniência
Rastreabilidade da origem de um dado — de onde veio, quem criou, quando. O campo `origem` em receitas e o histórico git são os principais mecanismos de proveniência do SOE.

## Query
Consulta ao banco SQLite. O banco é o mecanismo de consulta derivado da fonte canônica em Markdown.

## Receita (REC)
Entidade que representa o conhecimento de como fazer um prato. Não é um preparo específico — é a especificação. Preparos específicos são Execuções (EXE).

## Resolver (Resolvedor)
Script (`codigo/resolvedor-v1.py`) que percorre o grafo e resolve referências — verifica se cada aresta aponta para uma entidade que realmente existe. Referências quebradas são reportadas como erros.

## Runtime
O estado do sistema durante a execução do pipeline de validação e importação. Distinto do estado persistido em disco.

## Schema Version
Campo `schema-version` no frontmatter. Indica qual versão do esquema formal o arquivo segue. Permite evolução do formato sem quebrar compatibilidade.

## Seed Data
Dados iniciais carregados no banco para garantir consistência mínima — principalmente as categorias e catálogos de referência. Localizado em `banco_de_dados/seeds/`.

## Slug
Versão normalizada de um nome para uso em nomes de arquivos. Minúsculas, sem acentos, com hífens. Exemplo: "Doce de Leite Artesanal" → `doce-de-leite-artesanal`.

## Snapshot
Estado completo do sistema em um momento específico. O git produz snapshots a cada commit. O FAA produz snapshots do estado arquitetural em `docs/99-referencias/faa-state.json`.

## Status
Campo que indica o estado atual de uma entidade em seu ciclo de vida. Cada tipo de entidade tem um conjunto válido de status. Ver `docs/01-dominio/catalogos/estados-todas-entidades-v1.md`.

## Template
Arquivo Markdown pré-preenchido com a estrutura mínima de uma entidade. Usado como ponto de partida ao criar novos registros. Localizado em `docs/01-dominio/templates/`.

## Validador
Script (`codigo/validador-v1.py`) que verifica consistência semântica do grafo — detecta ciclos em arestas estruturais, status inválidos, e outras violações das regras do domínio.

---

## Próxima leitura

- Colocar os conceitos em prática → [`02-primeiros-passos-v1.md`](02-primeiros-passos-v1.md)
- Referência visual rápida → [`../07-referencia/cheat-sheet-v1.md`](../07-referencia/cheat-sheet-v1.md)
