# Especificação de Entidade: Equipamento

> Aplicação do template canônico à entidade Equipamento do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Equipamento é o registro de um utensílio, aparelho ou ferramenta culinária reutilizável que pode ser referenciado por Receitas e Execuções.

**Categoria gastronômica:**
Na culinária, equipamento é qualquer objeto físico usado no preparo: panela, forno, batedeira, termômetro, balança. Existe independentemente de qualquer receita.

**Categoria no sistema:**
Equipamento é uma entidade de referência normalizada com identificador `EQP-NNNNNN`, permitindo consultas como "todas as receitas que usam forno elétrico".

---

## 2. Responsabilidade

**Propósito principal:**
Centralizar o catálogo de ferramentas culinárias para eliminar descrições duplicadas e inconsistentes entre Receitas.

**Responsabilidades explícitas:**
- Definir canonicamente um equipamento culinário.
- Servir como referência para Receitas e Execuções.
- Permitir agrupamento e consulta por equipamento.

---

## 3. Limites

**Esta entidade NÃO:**
- Registra o estado ou condição de um equipamento em uma execução específica (isso pertence a Execução ou Observação).
- Inclui técnicas como atributos próprios.

**Fronteira com Técnica:**
Equipamento é o objeto físico. Técnica é o procedimento. Uma técnica pode exigir um equipamento, mas são entidades distintas.

---

## 4. Atributos

Referência ao esquema: `docs/01-dominio/esquemas/esquema-equipamento-v1.md`

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `EQP-NNNNNN` |
| `tipo` | string | Valor fixo: `equipamento` |
| `schema-version` | string | Versão do esquema |
| `versao` | string | Versão do registro |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `nome` | string | Nome do equipamento |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `tipo-equipamento` | string | Categoria do catálogo de tipos de equipamentos |
| `descricao` | text | Características e uso típico |
| `capacidade` | string | Capacidade relevante (ex: "5 litros") |
| `material` | string | Material principal |
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
| `referenciado-por` | Receita | N:N | Receitas listam IDs de Equipamentos |
| `referenciado-por` | Execução | N:N | Execuções registram IDs de Equipamentos usados |
| `observado-em` | Observação | 1:N | Observações podem referenciar Equipamento |

---

## 7. Restrições

1. O `id` é imutável após criação.
2. Equipamentos arquivados permanecem referência válida em Receitas e Execuções históricas.

---

## 8. Ciclo de Vida

**Nascimento:** Nasce quando referenciado pela primeira vez. Campos mínimos: `id`, `nome`.

**Evolução:** Adição de informações descritivas. Especificações técnicas novas incrementam versão.

**Arquivamento:** Equipamento arquivado quando descontinuado ou substituído por modelo mais preciso.
