# MIGRATION_INVENTORY

> Inventário da Fase 1 do Roadmap de Migração Arquitetural.
>
> Nenhuma modificação foi realizada. Este documento é somente leitura nesta fase.
>
> Gerado em: 2026-06-26
> Fonte da cópia: `copia/SOE-CCG-completo/saida-projeto/`
> Destino: `SOE-CCG/` (projeto principal)

---

## Contagens

```
Documentos (docs/)         ......... 51
  00-projeto               .........  8
  01-dominio               ......... 27
    catalogos              .........  8
    esquemas               .........  6
    templates              .........  7
    outros                 .........  6
  02-arquitetura           .........  7
  03-modelagem             .........  7
  04-padroes               ......... 12
  05-desenvolvimento       .........  2
  06-operacao              .........  1
  99-referencias           .........  5

Dados (dados/)             .........  9
  receitas                 .........  1
  ingredientes             .........  4
  equipamentos             .........  2
  tecnicas                 .........  3
  execucoes                .........  1
  observacoes              .........  1

Banco de dados             .........  3
  esquemas                 .........  1  (schema-sqlite-v1.sql)
  seeds                    .........  2  (.gitkeep, seed-categorias.sql)

Scripts                    .........  1  (importar.sh)

Raiz                       .........  3  (README.md, LICENSE, .gitignore)

─────────────────────────────────────
TOTAL                      ......... 67
```

---

## Arquivos Exclusivos da Cópia

Documentos presentes na cópia que NÃO existem no projeto principal.
São os candidatos primários à migração.

### docs/01-dominio/

| Arquivo | Tamanho |
|---------|---------|
| `linguagem-soe-ccg.md` | 11.228 bytes |
| `mapa-relacionamentos.md` | 9.664 bytes |
| `especificacao-receita.md` | 9.219 bytes |
| `especificacao-registro.md` | 5.944 bytes |
| `especificacao-ingrediente.md` | 5.537 bytes |
| `especificacao-execucao.md` | 6.545 bytes |
| `especificacao-experimento.md` | 4.562 bytes |
| `especificacao-tecnica.md` | 3.978 bytes |
| `especificacao-equipamento.md` | 3.610 bytes |
| `especificacao-observacao.md` | 4.709 bytes |
| `template-especificacao-entidade.md` | 4.703 bytes |
| `template-contrato.md` | 5.771 bytes |
| `catalogos/catalogos-expandidos.md` | 7.428 bytes |
| `catalogos/estados-todas-entidades.md` | 4.850 bytes |

### docs/05-desenvolvimento/ (diretório vazio no principal)

| Arquivo | Tamanho |
|---------|---------|
| `casos-de-uso.md` | 7.989 bytes |
| `padroes-desenvolvimento.md` | 6.988 bytes |

### docs/06-operacao/ (diretório vazio no principal)

| Arquivo | Tamanho |
|---------|---------|
| `guia-operacao.md` | 5.963 bytes |

### docs/99-referencias/

| Arquivo | Tamanho | Observação |
|---------|---------|------------|
| `rastreamento-atualizado.md` | 9.984 bytes | Versão mais recente do rastreamento |
| `validacao-arquitetural-fase12.md` | 7.643 bytes | Documento novo |

### banco_de_dados/

| Arquivo | Tamanho |
|---------|---------|
| `esquemas/schema-sqlite-v1.sql` | desconhecido |
| `seeds/seed-categorias.sql` | desconhecido |

### scripts/

| Arquivo | Tamanho |
|---------|---------|
| `importacao/importar.sh` | desconhecido |

### dados/

| Arquivo | Observação |
|---------|------------|
| `dados/observacoes/OBS-000001-bicarbonato-efeito.md` | Novo registro de observação |
| `dados/tecnicas/TEC-000001-reducao.md` | Novo dado |
| `dados/tecnicas/TEC-000002-caramelizacao.md` | Novo dado |
| `dados/tecnicas/TEC-000003-agitacao-continua.md` | Novo dado |

---

## Arquivos Presentes em Ambos

Documentos que existem tanto na cópia quanto no projeto principal.
Requerem análise de comparação (Fase 4).

### docs/00-projeto/

| Arquivo | Principal | Cópia | Observação |
|---------|-----------|-------|------------|
| `constituicao.md` | ✅ | ✅ | Comparar |
| `escopo.md` | ✅ | ✅ | Comparar |
| `filosofia.md` | ✅ | ✅ | Comparar |
| `glossario.md` | ✅ | ✅ | Comparar |
| `objetivos.md` | ✅ | ✅ | Comparar |
| `principios.md` | ✅ | ✅ | Comparar |
| `roadmap-master.md` | ✅ | ✅ | Comparar |
| `visão.md` | ✅ | ✅ | Cópia com encoding diferente no nome (`vis#U00e3o.md`) |

### docs/01-dominio/

| Arquivo | Principal | Cópia | Observação |
|---------|-----------|-------|------------|
| `catalogacao.md` | ✅ | ✅ | Comparar |
| `ciclo-de-vida.md` | ✅ | ✅ | Comparar |
| `entidades.md` | ✅ | ✅ | Comparar |
| `overview.md` | ✅ | ✅ | Comparar |
| `relacionamentos.md` | ✅ | ✅ | Comparar |
| `separacao-dominios.md` | ✅ | ✅ | Principal tem versão recente (25/06 22:15) |
| `catalogos/categorias.md` | ✅ | ✅ | Comparar |
| `catalogos/estados-receita.md` | ✅ | ✅ | Comparar |
| `catalogos/tipos-equipamentos.md` | ✅ | ✅ | Comparar |
| `catalogos/tipos-ingredientes.md` | ✅ | ✅ | Comparar |
| `catalogos/tipos-tecnicas.md` | ✅ | ✅ | Comparar |
| `catalogos/unidades-medida.md` | ✅ | ✅ | Comparar |
| `esquemas/esquema-equipamento-v1.md` | ✅ | ✅ | Comparar |
| `esquemas/esquema-execucao-v1.md` | ✅ | ✅ | Comparar |
| `esquemas/esquema-ingrediente-v1.md` | ✅ | ✅ | Comparar |
| `esquemas/esquema-observacao-v1.md` | ✅ | ✅ | Comparar |
| `esquemas/esquema-receita-v1.md` | ✅ | ✅ | Comparar |
| `esquemas/esquema-tecnica-v1.md` | ✅ | ✅ | Comparar |
| `templates/equipamento-v1.md` | ✅ | ✅ | Comparar |
| `templates/execucao-v1.md` | ✅ | ✅ | Comparar |
| `templates/experimento-v1.md` | ✅ | ✅ | Comparar |
| `templates/ingrediente-v1.md` | ✅ | ✅ | Comparar |
| `templates/observacao-v1.md` | ✅ | ✅ | Comparar |
| `templates/receita-v1.md` | ✅ | ✅ | Comparar |
| `templates/tecnica-v1.md` | ✅ | ✅ | Comparar |

### docs/02-arquitetura/

| Arquivo | Principal | Cópia |
|---------|-----------|-------|
| `diagrama-mestre.md` | ✅ | ✅ |
| `diagrama-mestre.txt` | ✅ | ✅ |
| `estrutura-diretorios.md` | ✅ | ✅ |
| `exportacao.md` | ✅ | ✅ |
| `fluxo-dados.md` | ✅ | ✅ |
| `importacao.md` | ✅ | ✅ |
| `versionamento.md` | ✅ | ✅ |

### docs/03-modelagem/

| Arquivo | Principal | Cópia |
|---------|-----------|-------|
| `conceitos-fundamentais.md` | ✅ | ✅ |
| `entidades-er.md` | ✅ | ✅ |
| `ids.md` | ✅ | ✅ |
| `normalizacao.md` | ✅ | ✅ |
| `objetivo.md` | ✅ | ✅ |
| `relacionamentos.md` | ✅ | ✅ |
| `sqlite.md` | ✅ | ✅ |

### docs/04-padroes/

| Arquivo | Principal | Cópia |
|---------|-----------|-------|
| `ADR-0001-MOTOR-DE-CONHECIMENTO.md` | ✅ | ✅ |
| `identificadores.md` | ✅ | ✅ |
| `metadados.md` | ✅ | ✅ |
| `nomenclatura.md` | ✅ | ✅ |
| `politica-arquivamento.md` | ✅ | ✅ |
| `politica-conflito.md` | ✅ | ✅ |
| `politica-esquemas.md` | ✅ | ✅ |
| `politica-revisao.md` | ✅ | ✅ |
| `politica-templates.md` | ✅ | ✅ |
| `tags.md` | ✅ | ✅ |
| `validacao.md` | ✅ | ✅ |
| `versionamento.md` | ✅ | ✅ |

### docs/99-referencias/

| Arquivo | Principal | Cópia | Observação |
|---------|-----------|-------|------------|
| `rastreamento-roadmap.md` | ✅ | ✅ | Cópia tem versão mais antiga (23% progresso) |
| `roadmap-maturidade-arquitetural.md` | ✅ | ✅ | Comparar |
| `tarefas-desbloqueio.md` | ✅ | ✅ | Comparar |

### dados/

| Arquivo | Principal | Cópia | Observação |
|---------|-----------|-------|------------|
| `dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md` | ⚠️ nome diferente | ✅ | Principal: `doce-de-leite-artesanal-v1.md` (sem prefixo REC) |
| `dados/ingredientes/ING-000001-leite-integral.md` | ✅ | ✅ | Comparar |
| `dados/ingredientes/ING-000002-acucar-refinado.md` | ✅ | ✅ | Comparar |
| `dados/ingredientes/ING-000003-sal-refinado.md` | ✅ | ✅ | Comparar |
| `dados/ingredientes/ING-000004-bicarbonato-sodio.md` | ✅ | ✅ | Comparar |
| `dados/equipamentos/EQP-000001-panela-fundo-grosso.md` | ✅ | ✅ | Comparar |
| `dados/equipamentos/EQP-000002-colher-silicone.md` | ✅ | ✅ | Comparar |
| `dados/execucoes/EXE-000001-doce-leite-v1-execucao1.md` | ✅ | ✅ | Comparar |

---

## Arquivos Exclusivos do Principal

Presentes no projeto principal e ausentes na cópia.
Não estão em risco. Registrados para completude do inventário.

| Arquivo | Observação |
|---------|------------|
| `docs/99-referencias/tarefas-desbloqueio.md` | Presente em ambos — ver seção acima |
| `docs/04-padroes/ADR-0001-MOTOR-DE-CONHECIMENTO.md` | Presente em ambos |

> Nota: após análise detalhada, não foram encontrados arquivos exclusivos do principal que estejam ausentes da cópia, exceto os documentos de rastreamento mais recentes (`rastreamento-roadmap.md` na versão 78% vs 23% da cópia).

---

## Anomalias Identificadas

| # | Tipo | Descrição | Ação Recomendada |
|---|------|-----------|-----------------|
| A-001 | Nome incorreto | `dados/receitas/doce-de-leite-artesanal-v1.md` no principal não segue a convenção de IDs (`REC-NNNNNN-`) | Avaliar na Fase 4 |
| A-002 | Encoding no nome | `docs/00-projeto/vis#U00e3o.md` na cópia — nome com escape de URL em vez de caractere UTF-8 | Ignorar na migração; usar arquivo do principal |
| A-003 | Rastreamento divergente | `rastreamento-roadmap.md` na cópia reflete estado de 23% (anterior); principal tem 78% | Cópia está desatualizada neste ponto |

---

## Unidades de Migração Propostas

Agrupamento lógico para a Fase 2 (Classificação).

| Unidade | Conteúdo | Arquivos Exclusivos da Cópia | Dependências |
|---------|----------|------------------------------|--------------|
| MU-001 | Filosofia, Objetivos, Princípios, Visão | Nenhum | — |
| MU-002 | Constituição e Governança (políticas) | Nenhum | MU-001 |
| MU-003 | Linguagem e Glossário | `linguagem-soe-ccg.md` | MU-001 |
| MU-004 | Catálogos e Taxonomias | `catalogos-expandidos.md`, `estados-todas-entidades.md` | MU-003 |
| MU-005 | Especificações de Entidades | 9 arquivos `especificacao-*.md`, `template-especificacao-entidade.md` | MU-004 |
| MU-006 | Contratos | `template-contrato.md` | MU-005 |
| MU-007 | Relacionamentos | `mapa-relacionamentos.md` | MU-005 |
| MU-008 | Arquitetura e Fluxos | Nenhum | MU-005 |
| MU-009 | Modelagem SQLite | `schema-sqlite-v1.sql` | MU-008 |
| MU-010 | Scripts e Importação | `importar.sh` | MU-009 |
| MU-011 | Padrões de Desenvolvimento | `padroes-desenvolvimento.md`, `casos-de-uso.md` | MU-009 |
| MU-012 | Operação | `guia-operacao.md` | MU-011 |
| MU-013 | Dados Canônicos | 3 técnicas, 1 observação, renomeação da receita | MU-005 |
| MU-014 | Rastreamento e Referências | `rastreamento-atualizado.md`, `validacao-arquitetural-fase12.md` | MU-013 |

---

## Próxima Fase

**Fase 2 — Classificação:** atribuir categoria e prioridade a cada arquivo do inventário.

Arquivo de saída: `MIGRATION_CLASSIFICATION.md`
