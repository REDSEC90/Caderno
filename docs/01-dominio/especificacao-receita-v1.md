# Especificação de Entidade: Receita

> Aplicação do template canônico à entidade Receita do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Receita é o registro estruturado de conhecimento que define a composição e o processo de preparo de um prato ou preparação culinária, independentemente de qualquer execução real.

**Categoria gastronômica:**
No mundo da culinária, uma receita é o conjunto de instruções — ingredientes, quantidades, técnicas e passos — que descreve como produzir um determinado prato. Ela existe no plano do conhecimento: uma receita de pão pode existir há décadas sem nunca ter sido executada.

**Categoria no sistema:**
No SOE-CCG, Receita é a entidade central do domínio gastronômico. É o nó ao qual Execuções, Ingredientes, Técnicas e Equipamentos se relacionam. Cada Receita é um registro com identificador `REC-NNNNNN`, versionável, auditável e consultável.

---

## 2. Responsabilidade

**Propósito principal:**
Centralizar o conhecimento sobre como preparar algo, separando o "como fazer" (Receita) do "o que aconteceu quando fiz" (Execução).

**Responsabilidades explícitas:**
- Definir ingredientes necessários por referência a IDs de Ingrediente.
- Definir técnicas aplicadas por referência a IDs de Técnica.
- Definir equipamentos utilizados por referência a IDs de Equipamento.
- Descrever o processo de preparo (modo de preparo).
- Servir como referência para múltiplas Execuções ao longo do tempo.
- Evoluir por versionamento quando o conhecimento sobre o preparo muda.

---

## 3. Limites

**Esta entidade NÃO:**
- Registra o que aconteceu em uma execução real (isso pertence a Execução).
- Armazena resultados, avaliações ou métricas de uma preparação específica (isso pertence a Execução e Observação).
- Substitui os registros de Ingrediente, Técnica ou Equipamento — apenas os referencia.
- Registra opiniões ou impressões sobre o prato (isso pertence a Observação).
- Representa experimentos culinários em andamento (isso pertence a Experimento).

**Fronteira com Execução:**
Receita é o conhecimento prescritivo ("o que deveria acontecer"). Execução é o registro descritivo ("o que aconteceu"). Uma Receita pode nunca ter sido executada. Uma Execução sempre pertence a uma Receita.

**Fronteira com Experimento:**
Quando ainda há incerteza sobre a fórmula ou processo, usa-se Experimento. Quando o conhecimento está consolidado o suficiente para ser referência, registra-se como Receita. Experimentos bem-sucedidos podem originar Receitas.

---

## 4. Atributos

Referência ao esquema: `docs/01-dominio/esquemas/esquema-receita-v1.md`

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `REC-NNNNNN` |
| `tipo` | string | Valor fixo: `receita` |
| `schema-version` | string | Versão do esquema aplicado. Ex: `1` |
| `versao` | string | Versão do registro. Ex: `1`, `2` |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação. Formato: `YYYY-MM-DD` |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `titulo` | string | Nome da receita |
| `ingredientes` | list | Lista de IDs de Ingrediente |
| `modo-de-preparo` | text | Descrição do processo de preparo |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `descricao` | string | Resumo descritivo da receita |
| `categorias` | list | Categorias do catálogo oficial |
| `rendimento` | string | Quantidade produzida. Ex: `500g`, `12 unidades` |
| `tempo-preparo` | string | Tempo estimado de preparo |
| `tempo-cozimento` | string | Tempo estimado de cozimento |
| `dificuldade` | string | `baixa`, `media` ou `alta` |
| `tecnicas` | list | IDs de Técnicas utilizadas |
| `equipamentos` | list | IDs de Equipamentos utilizados |
| `notas` | text | Observações livres sobre a receita |
| `origem` | string | Fonte ou inspiração do conhecimento |
| `tags` | list | Marcadores livres |

---

## 5. Estados

**Estados possíveis:**

| Estado | Significado | Quem pode atribuir |
|--------|-------------|-------------------|
| `rascunho` | Em elaboração, não finalizada | Autor |
| `testada` | Executada ao menos uma vez | Sistema (via Execução vinculada) |
| `validada` | Resultado satisfatório e reproduzível | Autor ou mantenedor |
| `publicada` | Conhecimento consolidado e referenciável | Mantenedor |
| `arquivada` | Fora do uso ativo, preservada no histórico | Mantenedor ou administrador |

**Diagrama de transição:**

```
[rascunho] → [testada] → [validada] → [publicada]
                                           ↓
                                       [arquivada]
     ↓
 [arquivada]  (rascunho descartado)
```

**Regras de transição:**
- `rascunho` → `testada`: quando ao menos uma Execução for vinculada à Receita.
- `testada` → `validada`: quando o autor declara resultado satisfatório.
- `validada` → `publicada`: quando o mantenedor consolida como referência.
- `publicada` → `arquivada`: quando a Receita deixa de ser referência ativa.
- `rascunho` → `arquivada`: quando o rascunho é descartado sem execução.

---

## 6. Eventos

| Evento | Descrição | Gatilho |
|--------|-----------|---------|
| `criacao` | Registro criado pela primeira vez | Usuário cria nova receita |
| `atualizacao` | Campo de conteúdo modificado | Usuário edita a receita |
| `versionamento` | Nova versão do registro criada | Alteração significativa de conteúdo |
| `vinculo-execucao` | Execução é vinculada à Receita | Usuário registra nova Execução |
| `transicao-estado` | Estado do ciclo de vida muda | Condição de transição atendida |
| `arquivamento` | Receita sai do uso ativo | Transição para estado `arquivada` |

---

## 7. Relacionamentos

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| `utiliza` | Ingrediente | N:N | Receita referencia IDs de Ingredientes necessários |
| `aplica` | Técnica | N:N | Receita referencia IDs de Técnicas usadas |
| `requer` | Equipamento | N:N | Receita referencia IDs de Equipamentos necessários |
| `possui` | Execução | 1:N | Execuções pertencem a uma Receita |
| `origina-de` | Experimento | N:1 | Receita pode ter surgido de um Experimento |
| `pertence-a` | Categoria | N:N | Receita pode ter múltiplas categorias |

**Como o relacionamento é expresso:**
Todo relacionamento usa identificadores permanentes no formato `[PREFIXO]-NNNNNN`. Nunca usa o nome da entidade relacionada como referência.

---

## 8. Dependências

**Dependências obrigatórias:**
- `Ingrediente`: toda Receita com lista de ingredientes depende de registros de Ingrediente existentes.

**Dependências opcionais:**
- `Técnica`: quando a Receita referencia técnicas específicas.
- `Equipamento`: quando a Receita referencia equipamentos específicos.
- `Categoria`: quando categorizada no catálogo oficial.

**Nota:** uma Receita pode existir sem Execuções, sem Técnicas e sem Equipamentos referenciados. O único campo de relacionamento obrigatório é `ingredientes`.

---

## 9. Restrições

1. O `id` é imutável após a criação do registro.
2. O `id` nunca é reutilizado, mesmo após arquivamento.
3. Todo relacionamento usa `id` da entidade relacionada, nunca seu nome.
4. `modo-de-preparo` deve ser suficientemente descritivo para reprodução sem ambiguidade.
5. O estado `publicada` só pode ser atribuído por mantenedores.
6. A transição para estado `testada` é derivada da existência de Execução vinculada — não pode ser declarada manualmente sem evidência.
7. Versões anteriores do registro são preservadas no histórico git. Nenhuma versão pode ser destruída.
8. Uma Receita arquivada continua válida para Execuções históricas que a referenciam.

**Restrições herdadas da Constituição:**
- ID permanente (Lei 1)
- Metadados padronizados (Lei 2)
- Origem registrada (Lei 3)
- Markdown como formato canônico (Lei 4)
- Relacionamentos por ID (Lei 8)

---

## 10. Ciclo de Vida

**Nascimento:**
Uma Receita nasce quando um usuário registra um novo preparo no sistema. O registro mínimo exige `id`, `titulo`, `ingredientes` e `modo-de-preparo`. O estado inicial é `rascunho`, a menos que o autor declare o registro completo ao criar, caso em que pode nascer como `ativo` diretamente.

**Evolução:**
O conhecimento de uma Receita evolui por duas formas:
- Edição menor (correções, esclarecimentos, adição de campos opcionais): commit no git, `atualizado-em` atualizado.
- Edição maior (mudança de ingredientes, processo reformulado): nova versão do registro (`versao: 2`), registro anterior marcado como `obsoleto`.

Execuções vinculadas ao longo do tempo enriquecem o histórico da Receita mas não alteram seu conteúdo.

**Arquivamento:**
Uma Receita é arquivada quando deixa de ser referência ativa. O arquivamento preserva o registro integralmente. Execuções históricas continuam válidas. A Receita arquivada pode ser consultada explicitamente mas não aparece em buscas padrão.
