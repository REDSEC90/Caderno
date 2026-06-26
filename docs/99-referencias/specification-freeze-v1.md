# Specification Freeze v1.0

**Data:** 2026-06-26  
**Status:** ✅ Congelada — especificação estável, pronta para implementação  

---

## Declaração

A especificação formal do SOE-CCG atingiu o estado de completude arquitetural.

Todas as camadas de conhecimento necessárias para implementação consistente foram formalizadas:

- Filosofia e constituição
- Governança documental e técnica
- Linguagem do domínio
- Especificações de entidades
- Contratos formais de comportamento
- Relacionamentos e dependências
- Modelagem de dados
- Catálogos e padrões
- Casos de uso e validações

A partir deste ponto, a especificação entra em estado de **manutenção controlada**. Alterações são permitidas apenas através de ADRs (Architecture Decision Records) que justifiquem a necessidade, avaliem o impacto e documentem o raciocínio.

---

## Completude por Fase

| Fase | Nome | Status | Observação |
|------|------|--------|------------|
| 0 | Identidade | ✅ Completa | Visão, filosofia, princípios |
| 1 | Constituição | ✅ Completa | 10 leis fundamentais |
| 2 | Governança | ✅ Completa | 8 políticas formalizadas |
| 3 | Linguagem | ✅ Completa | Vocabulário oficial, termos proibidos, glossário |
| 4 | Domínio | ✅ Completa | 8 entidades especificadas |
| 5 | Contratos | ✅ Completa | 7 contratos formais vinculantes |
| 6 | Catálogos | ✅ Completa | 11 catálogos definidos |
| 7 | Relacionamentos | ✅ Completa | 13 relacionamentos documentados |
| 8 | Padrões | ✅ Completa | Nomenclatura, IDs, metadados, tags, validação |
| 9 | Modelagem | ✅ Completa | Modelo ER, normalização, esquema SQLite |
| 10 | Dados Canônicos | 🔄 Contínua | Seeds iniciais criados, expansão iterativa |
| 11 | Casos de Uso | ✅ Completa | 10 casos de uso documentados |
| 12 | Validação | ✅ Completa | Auditoria arquitetural concluída |
| 13 | Implementação | ⏳ Próxima | Parser → Validador → Importador → CLI → API |

---

## Artefatos Críticos Consolidados

### Constituição
- `docs/00-projeto/filosofia.md`
- `docs/00-projeto/constituicao.md`
- `docs/00-projeto/principios.md`

### Governança
- `docs/04-padroes/politica-identificadores.md`
- `docs/04-padroes/politica-versionamento.md`
- `docs/04-padroes/politica-metadados.md`
- `docs/04-padroes/politica-templates.md`
- `docs/04-padroes/politica-esquemas.md`
- `docs/04-padroes/politica-arquivamento.md`
- `docs/04-padroes/politica-revisao.md`
- `docs/04-padroes/politica-conflito.md`

### Linguagem
- `docs/01-dominio/linguagem-soe-ccg.md`

### Especificações de Entidades
- `docs/01-dominio/especificacao-receita.md`
- `docs/01-dominio/especificacao-ingrediente.md`
- `docs/01-dominio/especificacao-tecnica.md`
- `docs/01-dominio/especificacao-equipamento.md`
- `docs/01-dominio/especificacao-execucao.md`
- `docs/01-dominio/especificacao-observacao.md`
- `docs/01-dominio/especificacao-experimento.md`

### Contratos Formais
- `docs/01-dominio/contratos/contrato-receita-v1.md`
- `docs/01-dominio/contratos/contrato-ingrediente-v1.md`
- `docs/01-dominio/contratos/contrato-tecnica-v1.md`
- `docs/01-dominio/contratos/contrato-equipamento-v1.md`
- `docs/01-dominio/contratos/contrato-execucao-v1.md`
- `docs/01-dominio/contratos/contrato-observacao-v1.md`
- `docs/01-dominio/contratos/contrato-experimento-v1.md`

### Relacionamentos
- `docs/01-dominio/mapa-relacionamentos.md`

### Modelagem
- `docs/03-modelagem/conceitos-fundamentais.md`
- `docs/03-modelagem/entidades-er.md`
- `banco_de_dados/esquemas/schema-sqlite-v1.sql`

### Padrões
- `docs/04-padroes/identificadores.md`
- `docs/04-padroes/nomenclatura.md`
- `docs/04-padroes/metadados.md`
- `docs/04-padroes/versionamento.md`
- `docs/04-padroes/tags.md`
- `docs/04-padroes/validacao.md`

### Casos de Uso
- `docs/05-desenvolvimento/casos-de-uso.md`

### Validação
- `docs/99-referencias/validacao-arquitetural-fase12.md`

---

## Contratos Formais — Resumo Executivo

Cada entidade possui contrato formal que define:

1. **Campos obrigatórios** — o que deve existir sempre
2. **Campos opcionais** — o que pode existir
3. **Valores aceitos** — domínios restritos de campos
4. **Pré-condições** — o que deve ser verdadeiro antes de cada operação
5. **Pós-condições** — o que deve ser verdadeiro depois de cada operação
6. **Invariantes** — o que deve ser verdadeiro sempre
7. **Rejeições explícitas** — operações que devem ser sempre recusadas
8. **Compatibilidade de esquema** — como versões coexistem
9. **Critério de aceitação** — quando implementação está conforme

Estas são especificações vinculantes. Qualquer implementação que viole um contrato está incorreta por definição.

---

## Garantias Arquiteturais

A especificação congelada garante:

### Domínio
- Todas as entidades possuem responsabilidade única
- Todos os relacionamentos estão documentados com cardinalidade e restrições
- Não há ambiguidade terminológica (linguagem formal)
- Não há conflito entre documentos (hierarquia definida)

### Identificadores
- Formato estável: `[PREFIXO]-NNNNNN`
- Imutabilidade garantida por contrato
- Unicidade global
- Não-reutilização
- Escalabilidade para 999.999 registros por entidade

### Persistência
- Markdown é a única fonte da verdade
- SQLite é índice derivado, nunca fonte
- Relacionamentos por ID, nunca por nome
- Histórico via git, nunca exclusão
- Arquivamento, nunca deleção

### Governança
- Toda mudança de esquema é versionada
- Toda mudança de estado é rastreada
- Todo conflito possui política de resolução
- Toda revisão possui processo documentado

---

## Bloqueadores Resolvidos

| Bloqueador | Status | Resolução |
|------------|--------|-----------|
| Ambiguidade terminológica | ✅ Resolvido | `linguagem-soe-ccg.md` — vocabulário oficial e termos proibidos |
| Responsabilidades de entidades difusas | ✅ Resolvido | 7 especificações com limites explícitos |
| Pré/pós-condições implícitas | ✅ Resolvido | 7 contratos formais vinculantes |
| Relacionamentos não-documentados | ✅ Resolvido | 13 relacionamentos com cardinalidade e restrições |
| Política de IDs instável | ✅ Resolvido | Formato congelado, imutabilidade contratual |
| Fonte da verdade ambígua | ✅ Resolvido | Markdown declarado como fonte única |
| Ausência de governança documental | ✅ Resolvido | 8 políticas formalizadas |

---

## Próximos Passos — Fase 13

Ordem recomendada de implementação:

### 1. Parser Markdown (crítico)
**Objetivo:** Ler arquivos `.md` de `dados/`, extrair frontmatter YAML e corpo Markdown.

**Entradas:** Caminho para arquivo `.md`  
**Saídas:** Estrutura de dados com metadados e conteúdo  
**Restrições:** Deve preservar exatamente o que está no arquivo, sem interpretação  

**Tecnologia sugerida:** Python com `PyYAML` e `python-frontmatter`

---

### 2. Validador de Contratos (crítico)
**Objetivo:** Verificar se um registro respeita o contrato formal de sua entidade.

**Entradas:** Registro parseado + Contrato formal  
**Saídas:** Lista de violações (vazia se válido)  
**Restrições:** Deve validar todos os pontos do contrato (campos, pré-condições, invariantes)

**Tecnologia sugerida:** Python com `jsonschema` ou validador customizado

---

### 3. Importador SQLite (crítico)
**Objetivo:** Sincronizar `dados/` → `banco_de_dados/sqlite/soe.db`

**Entradas:** Registros validados  
**Saídas:** Banco SQLite populado  
**Restrições:** 
- Markdown sempre sobrescreve SQLite (nunca o contrário)
- Integridade referencial deve ser validada
- Histórico de estados deve ser preservado

**Tecnologia sugerida:** Python com `sqlite3`

---

### 4. CLI Básica (prioridade média)
**Objetivo:** Interface de linha de comando para consultas e registro.

**Comandos mínimos:**
```bash
soe list receitas
soe show REC-000001
soe search "tomate"
soe validate dados/receitas/REC-000001.md
soe import dados/
```

**Tecnologia sugerida:** Python com `click` ou `typer`

---

### 5. API REST (prioridade baixa)
**Objetivo:** Acesso programático aos registros.

**Endpoints mínimos:**
```
GET /receitas
GET /receitas/{id}
GET /ingredientes
POST /observacoes
```

**Tecnologia sugerida:** Python com `FastAPI`

---

### 6. Interface Web (prioridade baixa)
**Objetivo:** Navegação e consulta visual.

**Funcionalidades mínimas:**
- Listar receitas
- Visualizar receita com ingredientes/técnicas/equipamentos linkados
- Histórico de execuções

**Tecnologia sugerida:** Framework moderno (React, Vue, Svelte)

---

## Política de Alteração Pós-Freeze

A partir deste ponto, alterações na especificação seguem o processo:

1. **Proposta via ADR** — criar `docs/04-padroes/ADR-NNNN-titulo.md`
2. **Justificativa** — por que a mudança é necessária
3. **Impacto** — o que será afetado
4. **Alternativas consideradas** — por que outras opções foram rejeitadas
5. **Decisão** — o que será alterado
6. **Aprovação** — revisão por mantenedor
7. **Implementação** — atualização dos documentos afetados
8. **Rastreamento** — commit referenciando o ADR

Mudanças permitidas:
- Correções de erros ou inconsistências
- Adição de campos opcionais
- Expansão de catálogos
- Refinamento de descrições

Mudanças que exigem ADR com justificativa forte:
- Alteração de campos obrigatórios
- Mudança de formato de ID
- Alteração de relacionamentos
- Remoção de entidades ou campos

Mudanças proibidas:
- Remoção de invariantes
- Quebra de compatibilidade retroativa de esquemas
- Alteração de IDs existentes

---

## Assinaturas

**Especificação congelada em:** 2026-06-26  
**Responsável:** Sistema SOE-CCG  
**Próxima revisão:** Após conclusão da Fase 13 (implementação inicial)
