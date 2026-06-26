# MATRIZ DE VALIDAÇÃO ARQUITETURAL — SOE-CCG

**Versão:** 1.0  
**Data:** 2026-06-26  
**Tipo:** Certificação arquitetural — VAF (Validação Arquitetural Final)  
**Status:** ✅ APROVADA

> Esta matriz é a lista de inspeção oficial do SOE-CCG. Cada requisito arquitetural possui evidência verificada. Implementação só é autorizada após aprovação integral desta matriz.

---

## MOTOR FILOSÓFICO

> Verifica consistência, ausência de contradições e cobertura explicativa da base filosófica.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0001 | Filosofia formalizada com rigor axiomático | `docs/00-projeto/filosofia.md` | 5 axiomas com enunciado, consequências e implicação arquitetural | ✅ Aprovado | Axiomas 1–5 documentados com derivações e teste filosófico de 4 perguntas |
| VAF-0002 | Ausência de contradições internas na filosofia | `docs/00-projeto/filosofia.md` + `constituicao.md` | Nenhuma lei fundamental contradiz axioma | ✅ Aprovado | Constituição deriva explicitamente da filosofia; cadeia documentada |
| VAF-0003 | Filosofia explica todas as decisões posteriores | `docs/00-projeto/filosofia.md` | Cada axioma possui implicação arquitetural rastreável | ✅ Aprovado | Axioma 2 → Markdown como fonte; Axioma 4 → SQLite como índice; Axioma 5 → implementação temporária |
| VAF-0004 | Constituição possui leis sem ambiguidade | `docs/00-projeto/constituicao.md` | 10 leis enumeradas, precisas e verificáveis | ✅ Aprovado | Leis 1–10 documentadas; invariantes e restrições explícitas |
| VAF-0005 | Princípios do projeto são coerentes com filosofia | `docs/00-projeto/principios.md` | Nenhum princípio contradiz axioma | ✅ Aprovado | 11 princípios alinhados; Princípio 3 (Dados Primeiro) = Axioma 1; Princípio 7 (Independência) = Axioma 3 |
| VAF-0006 | Objetivos e escopo derivam da visão | `docs/00-projeto/objetivos.md` + `escopo.md` | Objetivos atingíveis dentro do escopo definido | ✅ Aprovado | Objetivo principal e 7 específicos; fronteiras explícitas do sistema |
| VAF-0007 | Hierarquia de camadas documentada | `docs/04-padroes/politica-conflito.md` | Cadeia Filosofia → Constituição → Governança → Domínio → Implementação | ✅ Aprovado | Hierarquia com exemplos e regra de precedência explícita |

**RESULTADO: ✅ FILOSOFIA APROVADA**

---

## MOTOR DE DOMÍNIO

> Verifica cobertura e consistência de entidades, contratos, relacionamentos, estados e catálogos.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0008 | Todas as entidades possuem especificação formal | `docs/01-dominio/especificacao-*.md` | 7 entidades + Registro especificados com template canônico | ✅ Aprovado | Receita, Ingrediente, Técnica, Equipamento, Execução, Observação, Experimento + Registro |
| VAF-0009 | Todas as entidades possuem contrato formal | `docs/01-dominio/contratos/contrato-*-v1.md` | 7 contratos com campos, pré/pós-condições, invariantes, rejeições | ✅ Aprovado | 7/7 contratos presentes e completos |
| VAF-0010 | Nenhum contrato define campo inexistente no esquema | Contratos vs `esquemas/` | Cada campo do contrato existe no esquema correspondente | ✅ Aprovado | Verificação cruzada: campos coincidem em todos os 7 contratos |
| VAF-0011 | Todos os estados de todas as entidades documentados | `docs/01-dominio/catalogos/estados-todas-entidades.md` | Estados, transições e quem os atribui definidos por entidade | ✅ Aprovado | 7 entidades + Categoria + estados universais documentados |
| VAF-0012 | Nenhuma entidade sem ciclo de vida definido | Especificações de entidades | Cada entidade tem nascimento, evolução e arquivamento | ✅ Aprovado | Ciclo de vida presente em todas as especificações |
| VAF-0013 | Todos os relacionamentos documentados com cardinalidade | `docs/01-dominio/mapa-relacionamentos.md` | 13 relacionamentos com nome, direção, cardinalidade, restrições | ✅ Aprovado | REL-001 a REL-013 documentados; diagrama ASCII completo |
| VAF-0014 | Ausência de referência circular entre entidades | `docs/01-dominio/mapa-relacionamentos.md` | Grafo de dependências acíclico | ✅ Aprovado | Fluxo unidirecional: Experimento → Receita → Execução → Observação |
| VAF-0015 | Separação clara entre domínio gastronômico e sistema | `docs/01-dominio/separacao-dominios.md` | Mapeamento explícito de conceito gastronômico para entidade do sistema | ✅ Aprovado | Tabela de mapeamento e 3 exemplos de ambiguidade resolvida |
| VAF-0016 | Catálogos cobrem todos os campos controlados | `docs/01-dominio/catalogos/` | Nenhum campo enum sem catálogo correspondente | ✅ Aprovado | 11 catálogos; tipos, estados, unidades, classificações, escalas, materiais, métodos, vocabulário |
| VAF-0017 | Contratos definem rejeições explícitas | Contratos formais | Operações proibidas listadas com mensagem de erro | ✅ Aprovado | Seção 7 em todos os 7 contratos |

**RESULTADO: ✅ DOMÍNIO APROVADO**

---

## MOTOR DE PADRONIZAÇÃO

> Verifica nomenclatura, templates, IDs, versionamento, metadados, frontmatter e organização.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0018 | Nomenclatura de arquivos padronizada | `docs/04-padroes/nomenclatura.md` + `docs/05-desenvolvimento/padroes-desenvolvimento.md` | Padrão `[ID]-[slug]-v[N].md` definido e documentado | ✅ Aprovado | Dados reais seguem padrão: `REC-000001-doce-de-leite-artesanal-v1.md` |
| VAF-0019 | Todos os templates possuem frontmatter completo | `docs/01-dominio/templates/` | Frontmatter com todos os campos obrigatórios do contrato | ✅ Aprovado | 7 templates corrigidos e alinhados com contratos (correção realizada em 2026-06-26) |
| VAF-0020 | Formato de ID padronizado e sem variações | `docs/04-padroes/identificadores.md` | Formato `[PREFIXO]-NNNNNN` obrigatório, zeros à esquerda | ✅ Aprovado | 8 prefixos definidos: REC, EXE, ING, TEC, EQP, OBS, EXP, CAT |
| VAF-0021 | Política de versionamento sem ambiguidade | `docs/04-padroes/versionamento.md` + `linguagem-soe-ccg.md` | Distinção clara entre versão de conteúdo e versão de esquema | ✅ Aprovado | `versao` vs `schema-version` — dois campos distintos com semânticas documentadas |
| VAF-0022 | Metadados obrigatórios definidos para todos os registros | `docs/04-padroes/metadados.md` + `docs/03-modelagem/conceitos-fundamentais.md` | Lista de campos obrigatórios com tipos e formato | ✅ Aprovado | id, tipo, schema-version, versao, status, criado-em, atualizado-em, autor |
| VAF-0023 | Estrutura de diretórios documentada e em uso | `docs/02-arquitetura/estrutura-diretorios.md` | Diretórios definidos coincidem com estrutura real | ✅ Aprovado | `dados/`, `banco_de_dados/`, `docs/`, `scripts/`, `recursos/` — todos existem |
| VAF-0024 | Política de templates completa | `docs/04-padroes/politica-templates.md` | Criação, versionamento, compatibilidade, depreciação | ✅ Aprovado | 8 seções cobrindo ciclo de vida completo dos templates |
| VAF-0025 | Política de esquemas completa | `docs/04-padroes/politica-esquemas.md` | Criação, campos, versionamento, migração, compatibilidade | ✅ Aprovado | Distinção esquema/template; compatibilidade retroativa obrigatória |

**RESULTADO: ✅ PADRÕES APROVADOS**

---

## MOTOR DE INTEGRIDADE

> Verifica referências internas, consistência de IDs, catálogos e dados reais.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0026 | Dados reais seguem templates aprovados | `dados/` | Frontmatter dos dados reais contém campos obrigatórios | ✅ Aprovado | EXE-000001, OBS-000001, REC-000001, ING-000001–4, TEC-000001–3, EQP-000001–2 verificados |
| VAF-0027 | Referências entre dados reais usam IDs válidos | `dados/execucoes/` + `dados/observacoes/` | IDs referenciados existem no sistema | ✅ Aprovado | EXE-000001 referencia REC-000001 ✓; ING-000001–4 ✓; TEC-000001,3 ✓; EQP-000001–2 ✓ |
| VAF-0028 | OBS-000001 referencia entidade existente | `dados/observacoes/OBS-000001-bicarbonato-efeito.md` | `entidade-referenciada: EXE-000001` deve existir | ✅ Aprovado | EXE-000001 existe em `dados/execucoes/` |
| VAF-0029 | Esquema SQLite cobre todas as entidades | `banco_de_dados/esquemas/schema-sqlite-v1.sql` | Tabela para cada entidade + tabelas N:N + histórico + índices + views | ✅ Aprovado | 7 tabelas principais + 8 tabelas N:N + historico_estados + 11 índices + 2 views |
| VAF-0030 | Todos os estados do schema SQL coincidem com catálogos | Schema SQL vs `estados-todas-entidades.md` | Enums no CHECK() do SQL = valores do catálogo | ✅ Aprovado | Receita: rascunho/testada/validada/publicada/arquivada ✓; Execução: registrada/revisada/consolidada ✓; demais verificados |
| VAF-0031 | Seed de categorias consistente com catálogo | `banco_de_dados/seeds/seed-categorias.sql` vs `catalogos/categorias.md` | Categorias do seed existem no catálogo | ✅ Aprovado | 10 categorias seed alinhadas; IDs seguem padrão CAT-NNNNNN |
| VAF-0032 | Controle de sequência de IDs atualizado | `docs/04-padroes/identificadores.md` | Tabela de último ID reflete dados reais | ⚠️ Pendente | Tabela mostra REC-000001 mas EXE, ING, TEC, EQP, OBS com "—" apesar de dados existirem |
| VAF-0033 | Todos os templates são utilizáveis para criar novos registros | `docs/01-dominio/templates/` | Nenhum campo obrigatório faltante; nenhum campo inválido | ✅ Aprovado | Templates corrigidos em 2026-06-26; alinhados com contratos |

**Pendência identificada:** VAF-0032 — tabela de controle de sequência de IDs desatualizada.

**RESULTADO: ✅ INTEGRIDADE APROVADA** (com pendência menor não-bloqueadora)

---

## MOTOR SEMÂNTICO

> Verifica unicidade e consistência de significado de todos os termos ao longo da documentação.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0034 | Vocabulário oficial sem termos duplicados | `docs/01-dominio/linguagem-soe-ccg.md` | Cada conceito tem exatamente um nome | ✅ Aprovado | 15 termos gastronômicos + 16 termos do sistema; glossário alfabético com 45 entradas |
| VAF-0035 | Termos proibidos documentados | `docs/01-dominio/linguagem-soe-ccg.md` | Lista de ambiguidades com alternativas corretas | ✅ Aprovado | 7 termos proibidos: deletar, excluir, gerenciador, salvar, usuário, campo (sem contexto), arquivo (sem contexto) |
| VAF-0036 | "Execução" tem significado único | Linguagem + Especificações + Contratos | Termo usado consistentemente em todos os documentos | ✅ Aprovado | Definição formal: "Realização concreta de uma Receita"; uso consistente verificado |
| VAF-0037 | "Versão" não é ambígua | `linguagem-soe-ccg.md` seção 6 | `versao` (conteúdo) e `schema-version` (estrutura) distinguidos explicitamente | ✅ Aprovado | Seção 6 do documento de linguagem; distinção formal e com exemplos |
| VAF-0038 | "Arquivo" não é ambíguo | `linguagem-soe-ccg.md` seção 2 | Termos proibidos incluem "arquivo" sem contexto | ✅ Aprovado | Substituído por "Registro Markdown", "Banco SQLite" ou "Recurso" conforme contexto |
| VAF-0039 | Domínio gastronômico separado do domínio do sistema | `docs/01-dominio/separacao-dominios.md` | Tabela de mapeamento explícita | ✅ Aprovado | "Ingrediente" (gastronômico) ≠ "Entidade Ingrediente" (sistema) — distinção documentada |
| VAF-0040 | Glossário oficial unificado | `linguagem-soe-ccg.md` seção 7 | Todos os termos em ordem alfabética com definição única | ✅ Aprovado | 45 termos; sem sinônimos; sem definições conflitantes |

**RESULTADO: ✅ SEMÂNTICA APROVADA**

---

## MOTOR DE CONHECIMENTO

> Verifica se a arquitetura representa adequadamente os diferentes tipos de conhecimento gastronômico.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0041 | Sistema representa conhecimento culinário estruturado | Entidades: Receita, Ingrediente, Técnica, Equipamento | Receita pode descrever qualquer preparo culinário com estrutura | ✅ Aprovado | Template de Receita: modo de preparo livre + ingredientes + técnicas + equipamentos referenciados |
| VAF-0042 | Sistema representa conhecimento científico/químico | Entidade: Observação | Observação pode registrar fenômenos científicos sem estrutura rígida | ✅ Aprovado | OBS-000001 registra química do bicarbonato com precisão científica |
| VAF-0043 | Sistema representa conhecimento experimental | Entidade: Experimento | Hipótese + Método + Resultado + Conclusão cobre método científico | ✅ Aprovado | Template de Experimento cobre ciclo científico completo |
| VAF-0044 | Sistema representa conhecimento histórico/evolutivo | Versionamento + git | Toda evolução de conhecimento é rastreável | ✅ Aprovado | `versao` incrementável; histórico via git; estado `obsoleto` para substituições |
| VAF-0045 | Sistema representa conhecimento relacional | Mapa de relacionamentos | Receita pode apontar para ingredientes agrícolas, técnicas industriais, equipamentos especializados | ✅ Aprovado | 13 relacionamentos cobrem todos os vínculos possíveis entre entidades |
| VAF-0046 | Arquitetura não impede futuros tipos de conhecimento | Políticas de esquemas + contratos | Esquemas versionáveis; contratos compatíveis retroativamente | ✅ Aprovado | `schema-version` permite evolução; campos opcionais futuros sem quebra |
| VAF-0047 | Conhecimento sobrevive sem o sistema | Axioma 1 + Axioma 3 | Markdown legível sem ferramentas proprietárias | ✅ Aprovado | Arquivos `.md` legíveis em qualquer editor de texto; sem formato binário |

**RESULTADO: ✅ MOTOR DE CONHECIMENTO APROVADO**

---

## MOTOR DE EVOLUÇÃO

> Verifica se a arquitetura suporta crescimento massivo sem necessidade de reestruturação.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0048 | IDs suportam crescimento massivo | `docs/04-padroes/identificadores.md` | Formato NNNNNN suporta 999.999 registros por entidade | ✅ Aprovado | 6 dígitos = 999.999 por prefixo; expansível para 7+ sem quebra de contrato |
| VAF-0049 | Esquemas evoluem sem invalidar registros antigos | `docs/04-padroes/politica-esquemas.md` + contratos seção 8 | Compatibilidade retroativa obrigatória; sistema aceita múltiplas versões | ✅ Aprovado | "Registros com schema-version: 1 permanecem válidos indefinidamente" — todos os contratos |
| VAF-0050 | Relacionamentos por ID resistem a renomeações | `docs/03-modelagem/conceitos-fundamentais.md` | Renomear entidade não quebra nenhuma referência | ✅ Aprovado | Relações por ID, nunca nome; exemplificado no mapa de relacionamentos |
| VAF-0051 | Catálogos expansíveis sem quebra | `docs/01-dominio/catalogos/` | Novos valores adicionáveis a catálogos existentes | ✅ Aprovado | Política de conflito cobre extensão compatível de enums |
| VAF-0052 | Estrutura de diretórios escala com volume | `dados/` por entidade | Diretório por tipo permite milhões de arquivos organizados | ✅ Aprovado | `dados/receitas/`, `dados/ingredientes/` etc.; filesystem é escala ilimitada |
| VAF-0053 | SQLite pode ser substituído sem perda de conhecimento | Axioma 4 | Markdown permanece se SQLite for descartado | ✅ Aprovado | "Banco pode ser destruído e reconstruído sem perda" — Axioma 4 |
| VAF-0054 | Histórico de estados nunca comprime nem perde dados | `docs/04-padroes/politica-arquivamento.md` | Append-only; nenhuma transição pode ser apagada | ✅ Aprovado | `historico_estados` no schema SQL é append-only; política formal documentada |

**RESULTADO: ✅ ARQUITETURA EVOLUTIVA APROVADA**

---

## MOTOR DE IMPLEMENTABILIDADE

> Verifica se toda regra está escrita e nenhuma decisão dependerá do programador.

| ID | Requisito | Documento | Critério | Status | Evidência |
|----|-----------|-----------|----------|--------|-----------|
| VAF-0055 | Nenhuma pré-condição implícita | Contratos formais (seção 4 de cada) | Toda pré-condição de toda operação está explícita | ✅ Aprovado | Criar, Atualizar, Arquivar — pré-condições checklist em todos os 7 contratos |
| VAF-0056 | Nenhuma pós-condição implícita | Contratos formais (seção 5 de cada) | Toda pós-condição de toda operação está explícita | ✅ Aprovado | Pós-condições por operação em todos os 7 contratos |
| VAF-0057 | Todos os invariantes documentados | Contratos formais (seção 6 de cada) | Lista de invariantes obrigatórios por entidade | ✅ Aprovado | 7–12 invariantes por entidade nos contratos |
| VAF-0058 | Parser pode ser implementado sem inventar comportamento | Templates + Esquemas + `padroes-desenvolvimento.md` | Estrutura frontmatter YAML + corpo Markdown totalmente especificados | ✅ Aprovado | Frontmatter YAML obrigatório; campos tipados; corpo em seções nomeadas |
| VAF-0059 | Importador pode ser implementado sem decisões não-documentadas | Schema SQL + Contratos + Casos de Uso | Fluxo Markdown → Validação → SQLite completamente especificado | ✅ Aprovado | UC-001 a UC-010 cobrem fluxo completo; schema SQL com FK e constraints |
| VAF-0060 | Critério de aceitação por entidade definido | Contratos formais (seção 9 de cada) | Lista de condições que provam conformidade da implementação | ✅ Aprovado | Seção 9 em todos os 7 contratos; 7–11 critérios verificáveis por entidade |
| VAF-0061 | Mensagens de erro padronizadas | Contratos formais (seções 4 e 7) | Mensagem de erro definida para cada falha de validação | ✅ Aprovado | Coluna "Mensagem de erro" nas tabelas de campos e rejeições explícitas |
| VAF-0062 | Fluxo de dados arquitetural documentado | `docs/02-arquitetura/fluxo-dados.md` + `diagrama-mestre.md` | Markdown → Validador → SQLite; nunca o contrário | ✅ Aprovado | Fluxo unidirecional documentado; diagrama arquitetural completo |

**RESULTADO: ✅ IMPLEMENTAÇÃO AUTORIZADA**

---

## SUMÁRIO EXECUTIVO

| Motor | Resultado | Pendências |
|-------|-----------|------------|
| Filosófico | ✅ APROVADO | Nenhuma |
| Domínio | ✅ APROVADO | Nenhuma |
| Padronização | ✅ APROVADO | Nenhuma |
| Integridade | ✅ APROVADO | VAF-0032 (menor, não-bloqueadora) |
| Semântico | ✅ APROVADO | Nenhuma |
| Conhecimento | ✅ APROVADO | Nenhuma |
| Evolução | ✅ APROVADO | Nenhuma |
| Implementabilidade | ✅ APROVADO | Nenhuma |

**Total de requisitos:** 62  
**Aprovados:** 61  
**Pendentes menores:** 1 (VAF-0032 — tabela de IDs desatualizada)  
**Reprovados:** 0  
**Bloqueadores para implementação:** 0

---

## PENDÊNCIA VAF-0032 — Detalhamento

**Descrição:** Tabela de controle de sequência em `docs/04-padroes/identificadores.md` mostra "—" para EXE, ING, TEC, EQP, OBS mas os dados reais já possuem registros nesses prefixos.

**Impacto:** Não-bloqueador. Apenas risco de criação de ID duplicado ao adicionar novos dados.

**Resolução:** Atualizar a tabela manualmente ou automatizar via parser no início da Fase 13.

**Prioridade:** Alta para dados, baixa para início da implementação.

---

## DECLARAÇÃO FINAL

> A arquitetura do SOE-CCG foi submetida a Validação Arquitetural Final em 2026-06-26 e foi considerada **apta para implementação**.
>
> Toda regra está escrita. Toda operação tem critério de aceitação. Nenhuma decisão crítica dependerá do implementador.
>
> **A Fase 13 está autorizada a iniciar.**
