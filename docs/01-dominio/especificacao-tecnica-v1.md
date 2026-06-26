# Especificação de Entidade: Técnica

> Aplicação do template canônico à entidade Técnica do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Técnica é o registro de um método ou procedimento culinário reutilizável que pode ser referenciado por Receitas e Execuções.

**Categoria gastronômica:**
Na culinária, técnica é qualquer procedimento aplicado no preparo de alimentos: refogar, emulsionar, fermentar, branquear, sovar. Uma técnica existe independentemente de qualquer receita específica.

**Categoria no sistema:**
No SOE-CCG, Técnica é uma entidade de referência que permite associar conhecimento procedimental a múltiplas Receitas, viabilizando consultas como "todas as receitas que usam fermentação".

---

## 2. Responsabilidade

**Propósito principal:**
Centralizar o conhecimento sobre procedimentos culinários, evitando descrições dispersas e inconsistentes em cada Receita.

**Responsabilidades explícitas:**
- Definir canonicamente um procedimento culinário.
- Servir como referência para Receitas e Execuções.
- Permitir agrupamento de receitas por técnica comum.
- Centralizar aprendizados sobre a técnica em um único ponto.

---

## 3. Limites

**Esta entidade NÃO:**
- Descreve como a técnica foi aplicada em uma execução específica (isso pertence a Execução).
- Armazena resultado de uma aplicação concreta (isso pertence a Observação).
- Inclui equipamentos necessários como atributos próprios — Receitas referenciam ambos separadamente.

**Fronteira com Receita:**
A Técnica descreve o procedimento em abstrato. A Receita descreve como a técnica é aplicada naquele preparo específico.

---

## 4. Atributos

Referência ao esquema: `docs/01-dominio/esquemas/esquema-tecnica-v1.md`

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `TEC-NNNNNN` |
| `tipo` | string | Valor fixo: `tecnica` |
| `schema-version` | string | Versão do esquema |
| `versao` | string | Versão do registro |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `nome` | string | Nome da técnica |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `tipo-tecnica` | string | Categoria do catálogo de tipos de técnicas |
| `descricao` | text | Descrição do que é a técnica e como funciona |
| `aplicacoes` | text | Contextos típicos de uso |
| `dificuldade` | string | `baixa`, `media`, `alta` |
| `tags` | list | Marcadores livres |
| `notas` | text | Observações adicionais |

---

## 5. Estados

| Estado | Significado |
|--------|-------------|
| `ativo` | Disponível para referência |
| `descontinuado` | Não mais recomendado, mas mantido para histórico |
| `arquivado` | Fora de uso, preservado |

---

## 6. Relacionamentos

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| `referenciada-por` | Receita | N:N | Receitas listam IDs de Técnicas |
| `referenciada-por` | Execução | N:N | Execuções registram IDs de Técnicas aplicadas |
| `observada-em` | Observação | 1:N | Observações podem referenciar Técnica |

---

## 7. Restrições

1. O `id` é imutável após criação.
2. Técnicas arquivadas permanecem referência válida em Receitas e Execuções históricas.
3. O `nome` deve ser específico o suficiente para distinguir de técnicas similares.

---

## 8. Ciclo de Vida

**Nascimento:** Uma Técnica nasce quando referenciada pela primeira vez ou quando o usuário deseja catalogar um procedimento. Campos mínimos: `id`, `nome`.

**Evolução:** Adição de descrição, aplicações, dificuldade. Renomeação exige versionamento.

**Arquivamento:** Técnica é arquivada quando cai em desuso ou é substituída por conceito mais preciso.
