# CHECKLIST — TRANSIÇÃO FASE 0 → FASE 1

**Data:** 2026-06-28  
**Status Atual:** Fase 0 concluída com ressalvas  
**Próximo Marco:** Fase 1 — Freeze Arquitetural

---

## 🔴 BLOQUEADORES (deve ser resolvido antes de Fase 1)

- [ ] **Definir LICENSE**
  - Arquivo atual: vazio
  - Recomendações:
    - MIT (permissivo, uso comercial)
    - Apache 2.0 (permissivo, proteção de patentes)
    - GPL-3.0 (copyleft forte)
    - CC BY-SA 4.0 (documentação, não-software)
  - Ação: Criar `LICENSE` com texto completo da licença escolhida
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de Fase 1

---

## 🟡 RECOMENDADOS (deve ser resolvido antes de Fase 1)

- [ ] **Resolver localização de docs/07-uso/**
  - Problema: manual operacional está em `docs/docs-07-uso-manual-operacional/docs/07-uso/`
  - Opções:
    1. Mover conteúdo para `docs/07-uso/`
    2. Atualizar `README.md` para refletir localização atual
    3. Criar symlink de `docs/07-uso/` para localização real
  - Recomendação: Opção 1 (mover conteúdo)
  - Comando sugerido:
    ```bash
    mv docs/docs-07-uso-manual-operacional/docs/07-uso/* docs/07-uso/
    rm -rf docs/docs-07-uso-manual-operacional/
    ```
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de Fase 1

- [ ] **Renomear 26 arquivos sem sufixo de versão**
  - Arquivos identificados pelo FAA:
    - `docs/99-referencias/faa-state-summary.json`
    - `docs/99-referencias/auditoria-v1-2026-06-26.md` (já tem `-v1`, mas FAA reportou)
    - `docs/99-referencias/relatorio-consolidacao-v1-2026-06-26.md`
    - `docs/99-referencias/progresso-consolidacao-v1.txt`
    - `docs/99-referencias/FAA-v1-RELATORIO-FINAL.md`
    - ... (21 arquivos adicionais)
  - Ação: Adicionar sufixo `-v1` ou `-v2` conforme apropriado
  - Exemplo: `faa-state-summary.json` → `faa-state-summary-v1.json`
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de Fase 1

- [ ] **Executar FAA novamente após correções**
  - Comando:
    ```bash
    cd /home/redsec/Ambiente/SOE-CCG
    python3 scripts/faa/faa status
    ```
  - Critério de sucesso: score ≥ 90%
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de Fase 1

---

## 🟢 OPCIONAIS (pode ser resolvido durante ou após Fase 1)

- [ ] **Criar CONTRIBUTING.md**
  - Conteúdo sugerido:
    - Como contribuir com código
    - Como contribuir com documentação
    - Como reportar bugs
    - Como sugerir features
    - Processo de code review
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de v1.0.0

- [ ] **Criar SECURITY.md**
  - Conteúdo sugerido:
    - Como reportar vulnerabilidades
    - Política de divulgação responsável
    - Versões suportadas
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de v1.0.0

- [ ] **Criar CODE_OF_CONDUCT.md**
  - Recomendação: Contributor Covenant 2.1
  - Link: https://www.contributor-covenant.org/version/2/1/code_of_conduct/
  - Responsável: Mantenedor do projeto
  - Prazo: Antes de v1.0.0

- [ ] **Limpar diretórios vazios em scripts/**
  - `scripts/manutencao/`
  - `scripts/instalacao/`
  - `scripts/copia_seguranca/`
  - Opções:
    1. Adicionar `.gitkeep` para preservar estrutura
    2. Remover diretórios
    3. Adicionar scripts básicos
  - Recomendação: Opção 1 (adicionar `.gitkeep`)
  - Responsável: Mantenedor do projeto
  - Prazo: Opcional

- [ ] **Adicionar experimento de exemplo**
  - Localização: `dados/experimentos/`
  - Exemplo: `EXP-000001-teste-bicarbonato-v1.md`
  - Objetivo: validar suporte completo a 7 entidades
  - Responsável: Mantenedor do projeto
  - Prazo: Opcional

---

## FASE 1 — FREEZE ARQUITETURAL

Após resolver bloqueadores e recomendados, iniciar Fase 1 com os seguintes passos:

### 1.1 Freeze Conceitual

- [ ] Revisar cada conceito fundamental
  - [ ] Entidade
  - [ ] Documento
  - [ ] Conhecimento
  - [ ] Grafo
  - [ ] Snapshot
  - [ ] Proveniência
  - [ ] Edge
  - [ ] Estado
  - [ ] Runtime
- [ ] Para cada conceito, confirmar:
  - [ ] Definição estável?
  - [ ] Documentação oficial?
  - [ ] Identificador permanente?
  - [ ] Exemplos?
  - [ ] Ambiguidades resolvidas?

### 1.2 Freeze do Modelo

- [ ] Congelar EdgeKinds
  - Documento: `codigo/ir-v1.py`
  - ADR: `docs/04-padroes/ADR-0002-IR-ARESTAS-TIPADAS-v1.md`
  - Ação: Declarar EdgeKinds como imutável
- [ ] Congelar EdgeOrigins
  - Documento: `codigo/ir-v1.py`
  - ADR: `docs/04-padroes/ADR-0002-IR-ARESTAS-TIPADAS-v1.md`
  - Ação: Declarar EdgeOrigins como imutável
- [ ] Congelar tipos de entidades
  - Documento: `docs/01-dominio/entidades-v1.md`
  - Ação: Declarar 7 entidades como conjunto fechado para v1
- [ ] Congelar IDs
  - Documento: `docs/04-padroes/identificadores-v1.md`
  - Ação: Declarar formato `PREFIXO-NNNNNN` como imutável
- [ ] Congelar frontmatter
  - Documento: `docs/04-padroes/metadados-v1.md`
  - Ação: Declarar campos obrigatórios como imutável
- [ ] Congelar convenções Markdown
  - Documento: `docs/04-padroes/nomenclatura-v1.md`
  - Ação: Declarar estrutura de arquivos como imutável
- [ ] Congelar schema SQLite v1
  - Documento: `banco_de_dados/esquemas/schema-sqlite-v1.sql`
  - Ação: Declarar schema como imutável (migrações obrigatórias após v1)

### 1.3 Freeze Documental

- [ ] Definir status para toda documentação
  - Status possíveis:
    - `Draft` — rascunho, não finalizado
    - `Review` — em revisão
    - `Approved` — aprovado para uso
    - `Frozen` — congelado, imutável (exceto via ADR)
    - `Deprecated` — obsoleto, mantido para referência
    - `Archived` — arquivado, sem manutenção
  - Ação: Adicionar campo `status:` no frontmatter de todos documentos
- [ ] Mover documentos obsoletos para `docs/99-referencias/archive/`
- [ ] Atualizar README.md com status de cada diretório

### 1.4 Freeze de Interfaces

- [ ] Formalizar contrato do Parser
  - Entrada: arquivo Markdown
  - Saída: `Entity` com `outgoing` preenchido
  - Erros: arquivo não encontrado, frontmatter inválido, ID inválido
  - Pré-condições: arquivo existe, encoding UTF-8
  - Pós-condições: `Entity.id` válido, `Entity.metadata` não vazio
  - Invariantes: `len(Entity.id) > 0`
- [ ] Formalizar contrato do Resolvedor
  - Entrada: `KnowledgeGraph` com referências não resolvidas
  - Saída: `KnowledgeGraph` com `incoming` preenchido
  - Erros: referência não encontrada
  - Pré-condições: todas entidades possuem ID válido
  - Pós-condições: para cada `Edge` em `outgoing`, existe `Edge` correspondente em `incoming`
  - Invariantes: `len(grafo.entities) > 0`
- [ ] Formalizar contrato do Validador
  - Entrada: `KnowledgeGraph` resolvido
  - Saída: lista de diagnósticos (`list[dict]`)
  - Erros: nenhum (validador não falha, apenas reporta)
  - Pré-condições: grafo resolvido
  - Pós-condições: lista de diagnósticos contém apenas problemas reais
  - Invariantes: diagnósticos possuem `severity`, `message`, `entity_id`
- [ ] Formalizar contrato do Importador
  - Entrada: `KnowledgeGraph` validado
  - Saída: caminho do banco SQLite
  - Erros: banco corrompido, violação de constraints
  - Pré-condições: schema v1 aplicado ao banco
  - Pós-condições: todas entidades persistidas, relacionamentos criados
  - Invariantes: foreign keys válidos
- [ ] Formalizar contrato do FAA
  - Entrada: caminho do projeto
  - Saída: `dict` com status, score, issues, metrics
  - Erros: projeto inválido, permissões insuficientes
  - Pré-condições: projeto é diretório válido
  - Pós-condições: score entre 0 e 100
  - Invariantes: issues possuem `severity`, `message`, `file_path`

### 1.5 Registro

- [ ] Criar `docs/03-governanca/ARCHITECTURE_FREEZE.md`
  - Data do freeze
  - Versão: v1.0.0-rc1
  - Contratos congelados (lista completa)
  - Exceções (se houver)
  - Pendências aceitas (se houver)
  - Processo de alteração (ADR obrigatório)

---

## VALIDAÇÃO FINAL PRÉ-FREEZE

Executar checklist antes de declarar Freeze:

- [ ] LICENSE definido e presente no repositório
- [ ] docs/07-uso/ no lugar correto
- [ ] FAA score ≥ 90%
- [ ] Zero issues críticos no FAA
- [ ] Todos os ADRs aprovados
- [ ] Todos os documentos de domínio versionados
- [ ] Schema SQLite v1 aprovado
- [ ] EdgeKinds e EdgeOrigins documentados
- [ ] 7 entidades com contratos formalizados
- [ ] Pipeline Parser → Resolvedor → Validador → Importador operacional
- [ ] Pelo menos 1 entidade de cada tipo em dados/ (exceto experimentos, opcional)

---

## COMUNICAÇÃO DO FREEZE

- [ ] Criar tag `v1.0.0-rc1` no repositório
- [ ] Publicar `ARCHITECTURE_FREEZE.md` no README.md
- [ ] Anunciar freeze em CHANGELOG.md
- [ ] Anunciar freeze em release notes (se aplicável)

---

## PÓS-FREEZE

Após Freeze Arquitetural:

- [ ] Qualquer alteração em contratos congelados deve ser precedida por ADR
- [ ] ADRs devem ser aprovados antes de implementação
- [ ] Migrações de schema devem ser versionadas
- [ ] Mudanças em EdgeKinds/EdgeOrigins exigem ADR + nova versão do IR

---

**Última atualização:** 2026-06-28  
**Próxima revisão:** Após conclusão de Fase 1
