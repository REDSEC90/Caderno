# Especificação de Entidade: Registro

> Especificação da entidade fundamental que serve de base para todas as entidades do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Registro é a unidade mínima de conhecimento no SOE-CCG — a abstração base da qual todas as entidades específicas (Receita, Ingrediente, Técnica, Equipamento, Execução, Observação, Experimento) derivam.

**Categoria gastronômica:**
Não há equivalente gastronômico direto. Registro é um conceito exclusivamente do sistema — a "célula" fundamental que encapsula qualquer pedaço de conhecimento.

**Categoria no sistema:**
Registro é a especificação abstrata que define o que todo objeto de conhecimento no SOE-CCG deve ter: identidade permanente, metadados padronizados, formato canônico e ciclo de vida. Toda entidade específica é um tipo especializado de Registro.

---

## 2. Responsabilidade

**Propósito principal:**
Garantir que todo conhecimento no sistema seja identificável, rastreável, versionável e consultável de forma uniforme, independentemente do tipo de conhecimento que representa.

**Responsabilidades explícitas:**
- Definir o conjunto mínimo de metadados obrigatórios para qualquer objeto de conhecimento.
- Garantir identidade permanente por ID imutável.
- Garantir rastreabilidade por histórico de versões.
- Garantir consistência por metadados padronizados.
- Estabelecer o ciclo de vida comum a todas as entidades.

---

## 3. Limites

**Esta entidade NÃO:**
- É instanciada diretamente — nunca existe um "Registro genérico", apenas Receitas, Ingredientes, etc.
- Define o conteúdo específico de cada entidade — isso pertence às especificações e esquemas de cada entidade.
- Representa um conceito gastronômico — é exclusivamente um conceito do sistema.

**Relação com entidades específicas:**
Toda entidade específica herda a estrutura de Registro e adiciona seus próprios atributos. O esquema de Receita, por exemplo, começa com todos os campos de Registro e adiciona `titulo`, `ingredientes`, `modo-de-preparo`, etc.

---

## 4. Atributos

**Metadados obrigatórios em todo Registro:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente no formato `[PREFIXO]-NNNNNN` |
| `tipo` | string | Tipo da entidade: `receita`, `ingrediente`, `tecnica`, `equipamento`, `execucao`, `observacao`, `experimento` |
| `schema-version` | string | Versão do esquema aplicado ao registro |
| `versao` | string | Versão do conteúdo do registro |
| `status` | string | Estado no ciclo de vida |
| `criado-em` | date | Data de criação. Formato: `YYYY-MM-DD` |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador de quem criou ou é responsável |

**Metadados opcionais comuns:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `tags` | list | Marcadores livres para organização |
| `origem` | string | Fonte ou inspiração do conhecimento |
| `notas` | text | Observações livres gerais |

---

## 5. Estados

O estado base de um Registro é definido por três condições ortogonais:

**Estado de elaboração:**
- `rascunho`: em construção, não finalizado
- `ativo`: finalizado e em uso

**Estado de ciclo de vida:**
(específico por entidade — ver especificação de cada entidade)

**Estado de arquivamento:**
- `arquivado`: fora do uso ativo, preservado no histórico
- `obsoleto`: substituído por versão mais recente, estado final

---

## 6. Invariantes

Regras que se aplicam a todo Registro sem exceção:

1. **Identidade permanente:** o `id` nunca muda após a criação.
2. **Não-reutilização:** nenhum `id` é reutilizado, mesmo após arquivamento.
3. **Não-destruição:** nenhum Registro é deletado — apenas arquivado.
4. **Rastreabilidade:** toda alteração significativa é registrada (via git).
5. **Formato canônico:** todo Registro existe como arquivo Markdown em `dados/`.
6. **Metadados obrigatórios:** os 8 campos obrigatórios devem estar presentes em qualquer Registro válido.
7. **Referência por ID:** todo relacionamento entre Registros usa IDs, nunca nomes.

---

## 7. Estrutura de ID

O formato de ID de todo Registro é: `[PREFIXO]-NNNNNN`

| Prefixo | Entidade |
|---------|----------|
| `REC` | Receita |
| `EXE` | Execução |
| `ING` | Ingrediente |
| `TEC` | Técnica |
| `EQP` | Equipamento |
| `OBS` | Observação |
| `EXP` | Experimento |
| `CAT` | Categoria |

---

## 8. Relação com Markdown e SQLite

**Em Markdown:**
Todo Registro existe como arquivo `.md` em `dados/[tipo-da-entidade]/`. Este é o formato canônico e permanente. O arquivo é a verdade.

**Em SQLite:**
Todo Registro tem representação no banco de dados, derivada do Markdown. O banco é índice de consulta, não fonte de verdade. Se há conflito, o Markdown prevalece.

---

## 9. Ciclo de Vida Base

**Nascimento:**
Um Registro nasce quando um arquivo Markdown é criado em `dados/` com os 8 campos obrigatórios preenchidos. O ID é atribuído no momento da criação e nunca muda.

**Evolução:**
Registros evoluem por edições ao arquivo Markdown. Alterações são rastreadas pelo git. Alterações significativas de conteúdo geram incremento do campo `versao`.

**Arquivamento:**
Registros arquivados têm `status: arquivado`. Continuam existindo em `dados/` e no git. Não são excluídos. Podem ser consultados explicitamente.

---

## 10. Critério de Implementabilidade

Um desenvolvedor que compreende esta especificação e as especificações das entidades específicas deve ser capaz de:

1. Implementar a estrutura de arquivos em `dados/`.
2. Implementar o parser que extrai metadados obrigatórios de qualquer Markdown.
3. Implementar o validador que verifica presença dos 8 campos obrigatórios.
4. Implementar o sincronizador que replica Registros para SQLite.
5. Implementar a lógica de arquivamento sem exclusão.
