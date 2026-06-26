# Especificação de Entidade: Ingrediente

> Aplicação do template canônico à entidade Ingrediente do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Ingrediente é o registro de um insumo culinário reutilizável que pode ser referenciado por múltiplas Receitas e Execuções.

**Categoria gastronômica:**
Na culinária, ingrediente é qualquer substância usada no preparo de alimentos: tomate, sal, farinha, azeite, ovo. Um ingrediente existe independentemente de qualquer receita.

**Categoria no sistema:**
No SOE-CCG, Ingrediente é uma entidade de referência normalizada. Cada ingrediente é um registro único com identificador `ING-NNNNNN` que serve como ponto de referência compartilhado por todas as Receitas e Execuções que o utilizam.

---

## 2. Responsabilidade

**Propósito principal:**
Evitar que o mesmo insumo seja descrito de forma diferente em cada receita, garantindo consistência e permitindo consultas como "todas as receitas com tomate".

**Responsabilidades explícitas:**
- Ser a definição canônica de um insumo culinário.
- Servir como referência estável para Receitas e Execuções.
- Centralizar características do insumo (tipo, unidade padrão, sazonalidade).
- Ser reutilizável indefinidamente sem duplicação.

---

## 3. Limites

**Esta entidade NÃO:**
- Especifica a quantidade usada em uma Receita (isso está no campo `ingredientes` da Receita, com a quantidade).
- Registra a qualidade de um lote específico (isso pertence a Execução ou Observação).
- Armazena preferências do usuário sobre o insumo (isso pertence a Observação).

**Fronteira com Receita:**
Ingrediente define o insumo em si. A Receita define quanto e como o insumo é usado. O campo `ingredientes` de uma Receita é uma lista de referências `ING-NNNNNN` com quantidade associada, não uma descrição do ingrediente.

---

## 4. Atributos

Referência ao esquema: `docs/01-dominio/esquemas/esquema-ingrediente-v1.md`

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `ING-NNNNNN` |
| `tipo` | string | Valor fixo: `ingrediente` |
| `schema-version` | string | Versão do esquema aplicado |
| `versao` | string | Versão do registro |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `nome` | string | Nome do ingrediente |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `tipo-ingrediente` | string | Categoria do catálogo de tipos de ingredientes |
| `unidade-padrao` | string | Unidade de medida padrão para este ingrediente |
| `descricao` | string | Características relevantes do ingrediente |
| `sazonalidade` | string | Informações sobre disponibilidade sazonal |
| `origem` | string | Procedência geográfica ou produção |
| `tags` | list | Marcadores livres |
| `notas` | text | Observações sobre o ingrediente |

---

## 5. Estados

| Estado | Significado |
|--------|-------------|
| `ativo` | Disponível para referência em Receitas e Execuções |
| `descontinuado` | Não mais recomendado, mas mantido para registros históricos |
| `arquivado` | Fora de uso, preservado no histórico |

**Diagrama de transição:**
```
[ativo] → [descontinuado] → [arquivado]
[ativo] → [arquivado]
```

---

## 6. Eventos

| Evento | Descrição | Gatilho |
|--------|-----------|---------|
| `criacao` | Novo ingrediente registrado | Usuário cria primeiro uso |
| `atualizacao` | Informações do ingrediente editadas | Usuário edita campos |
| `descontinuacao` | Ingrediente marcado como não recomendado | Mantenedor declara descontinuação |
| `arquivamento` | Ingrediente arquivado | Transição explícita de estado |

---

## 7. Relacionamentos

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| `referenciado-por` | Receita | N:N | Receitas listam IDs de Ingredientes |
| `referenciado-por` | Execução | N:N | Execuções registram IDs de Ingredientes usados |
| `observado-em` | Observação | 1:N | Observações podem referenciar Ingrediente |

---

## 8. Dependências

**Dependências obrigatórias:**
Nenhuma. Ingrediente é uma entidade de referência — pode existir sem nenhuma Receita que o utilize.

**Dependências opcionais:**
- `Catálogo de tipos de ingredientes`: quando `tipo-ingrediente` é preenchido.
- `Catálogo de unidades de medida`: quando `unidade-padrao` é preenchido.

---

## 9. Restrições

1. O `id` é imutável após criação.
2. O `id` nunca é reutilizado.
3. O `nome` deve ser suficientemente específico para distinguir do ingrediente similar (ex: "Tomate Cereja" em vez de "Tomate" quando aplicável).
4. Ingredientes arquivados continuam sendo referência válida em Receitas e Execuções históricas.

---

## 10. Ciclo de Vida

**Nascimento:** Um Ingrediente nasce quando aparece pela primeira vez como necessário em uma Receita, ou quando o usuário deseja catalogar um insumo. Campos mínimos: `id`, `nome`.

**Evolução:** Ingredientes evoluem por adição de informações opcionais (descrição, sazonalidade). Mudança de nome exige versionamento (v2), mas o ID permanece o mesmo.

**Arquivamento:** Um ingrediente é arquivado quando descontinuado permanentemente (ex: produto fora de produção). Receitas e Execuções históricas que o referenciam permanecem válidas.
