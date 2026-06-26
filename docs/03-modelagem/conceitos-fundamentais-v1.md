# Conceitos Fundamentais

## Objetivo

Este documento define formalmente os 13 conceitos estruturais fundamentais do SOE-CCG.

Os conceitos aqui descritos representam o núcleo lógico permanente do sistema e devem permanecer válidos independentemente de mudanças na implementação, banco de dados, linguagem de programação ou tecnologia de interface.

---

## 1. Registro

**Definição:** unidade mínima de conhecimento persistente no SOE-CCG, identificada de forma permanente e imutável por um ID único.

Todo Registro:
- Possui ID permanente no formato `[PREFIXO]-NNNNNN`
- Nunca é excluído; apenas muda de estado (ex: arquivado)
- Possui metadados obrigatórios (autor, criado-em, atualizado-em, versão, status, schema-version)
- Representa conhecimento, não armazenamento de documento ou arquivo

**Propriedade fundamental:** a existência de um Registro independe da tecnologia usada para consultá-lo.

---

## 2. Entidade

**Definição:** tipo de Registro com responsabilidade e estrutura próprias no domínio gastronômico ou no sistema.

Exemplos de entidades do SOE-CCG:
- **Domínio gastronômico:** Receita, Ingrediente, Técnica, Equipamento
- **Domínio do sistema:** Execução, Observação, Experimento, Categoria

Toda entidade possui:
- Esquema próprio definindo campos obrigatórios e opcionais
- Estados de ciclo de vida específicos
- Relacionamentos com outras entidades
- Template de criação para o autor

**Propriedade fundamental:** nenhuma entidade deve ser considerada isoladamente; o conhecimento surge da combinação entre entidades e relacionamentos.

---

## 3. Relacionamento

**Definição:** conexão semântica tipada entre dois Registros, expressa sempre por ID (nunca por nome).

Todo relacionamento possui:
- Nome (ex: `utiliza`, `origina`, `refere`)
- Origem e destino (entidades envolvidas)
- Direção (unidirecional ou bidirecional)
- Cardinalidade (1:1, 1:N, N:N)
- Significado semântico documentado

Exemplo conceitual:
```
Receita [REC-000001]
   ↓
utiliza (relacionamento)
   ↓
Ingrediente [ING-000003]
```

**Propriedade fundamental:** relacionamentos utilizam identificadores permanentes, nunca nomes ou referências transitórias.

---

## 4. Versão

**Definição:** número inteiro incremental que registra a evolução de conteúdo de um Registro ao longo do tempo.

**Distinção crítica:**
- **`versao`** (versão de conteúdo) — incrementada quando o autor altera informações do registro (ex: ajusta modo de preparo, corrige quantidade)
- **`schema-version`** (versão de esquema) — incrementada quando a estrutura de campos muda (ex: esquema v1 → v2)

**Propriedade fundamental:** versões de conteúdo são incrementais e nunca decrescentes; não existe "versão 3 substituindo versão 5".

---

## 5. Histórico

**Definição:** sequência cronológica ordenada de todas as alterações de estado ou conteúdo de um Registro, preservada permanentemente.

Todo evento relevante gera entrada no histórico:
- Mudança de estado (rascunho → testada)
- Alteração de conteúdo (incremento de versão)
- Arquivamento ou restauração
- Substituição por nova versão

**Propriedade fundamental:** o histórico é append-only; nunca é sobrescrito ou excluído.

---

## 6. Identificador

**Definição:** código alfanumérico único, permanente e imutável que identifica um Registro no SOE-CCG.

**Formato:** `[PREFIXO]-NNNNNN`

Exemplos:
- `REC-000001` — Receita
- `ING-000042` — Ingrediente
- `EXE-000138` — Execução

**Propriedades:**
- Atribuído no momento da criação
- Nunca reutilizado (mesmo após arquivamento)
- Sequencial por tipo de entidade
- Independente de nome, título ou conteúdo

**Propriedade fundamental:** IDs são a única forma aceitável de expressar relacionamentos entre Registros.

---

## 7. Metadados

**Definição:** conjunto de campos descritivos obrigatórios presentes em todo Registro, independentemente do tipo de entidade.

**Metadados obrigatórios:**
- `id` — identificador permanente
- `autor` — quem criou o registro
- `criado-em` — data de criação (YYYY-MM-DD)
- `atualizado-em` — data da última modificação
- `versao` — número da versão de conteúdo
- `schema-version` — número da versão do esquema
- `status` — estado atual do ciclo de vida

**Propriedade fundamental:** metadados são a interface de rastreabilidade e governança do sistema.

---

## 8. Template

**Definição:** arquivo Markdown pré-estruturado que o autor copia para criar um novo Registro, contendo frontmatter YAML com campos obrigatórios e seções do corpo já formatadas.

Exemplo: `docs/01-dominio/templates/receita-v1.md`

Todo template:
- Inclui comentários explicativos em cada campo
- Segue o esquema correspondente (ex: `esquema-receita-v1.md`)
- É versionado (sufixo `-v1`, `-v2`)
- Está em `docs/01-dominio/templates/`

**Propriedade fundamental:** templates são a interface de entrada do conhecimento no sistema; o autor não escreve YAML do zero.

---

## 9. Esquema

**Definição:** especificação formal da estrutura de campos de uma entidade, incluindo tipos, obrigatoriedade, valores aceitos e regras de validação.

Exemplo: `docs/01-dominio/esquemas/esquema-receita-v1.md`

Todo esquema define:
- Campos obrigatórios e opcionais
- Tipo de dado de cada campo (texto, número, data, lista, ID)
- Valores controlados (enumerações)
- Validações (ex: formato de ID, data no padrão ISO)
- Compatibilidade com versões anteriores

**Propriedade fundamental:** o esquema é o contrato entre o autor (que cria o Markdown) e o sistema (que valida e importa).

---

## 10. Estado

**Definição:** valor controlado que representa a posição de um Registro em seu ciclo de vida, determinando visibilidade, permissões e transições possíveis.

Exemplos de estados:
- Receita: `rascunho`, `testada`, `validada`, `publicada`, `arquivada`
- Execução: `registrada`, `revisada`, `consolidada`
- Ingrediente: `ativo`, `descontinuado`, `arquivado`

**Regras universais:**
- Todo Registro inicia em um estado definido (geralmente `rascunho` ou `ativo`)
- Transições de estado são controladas (não é possível pular estados arbitrariamente)
- Estado `arquivado` não significa "excluído"; o registro permanece consultável
- Mudanças de estado geram entrada no histórico

**Propriedade fundamental:** estados controlam comportamento, nunca existência; nenhum estado destrói um Registro.

---

## 11. Catálogo

**Definição:** conjunto controlado e versionado de valores válidos para um campo específico, mantido centralmente em `docs/01-dominio/catalogos/`.

Exemplos de catálogos:
- `tipos-ingredientes.md` — valores aceitos para o campo `tipo-ingrediente`
- `unidades-medida.md` — valores aceitos para `unidade`
- `estados-todas-entidades.md` — valores aceitos para `status` por entidade

**Propriedades:**
- Catálogos são a única fonte da verdade para valores controlados
- Adicionar valor novo ao catálogo requer revisão arquitetural
- Campos que referenciam catálogos não aceitam valores arbitrários

**Propriedade fundamental:** catálogos eliminam ambiguidade e inconsistência terminológica.

---

## 12. Tag

**Definição:** palavra-chave livre atribuída a um Registro para facilitar busca e agrupamento, sem impacto em validação ou estrutura.

Diferença entre Tag e Catálogo:
- **Catálogo:** valor controlado, validado, obrigatório ou restrito (ex: `tipo-ingrediente: lacteo`)
- **Tag:** valor livre, opcional, múltiplo (ex: `tags: [mineiro, tradicional, festa-junina]`)

Exemplos de uso:
- `tags: [vegetariano, sem-gluten, rapido]` — facilitam busca por características não formalizadas
- `tags: [experimental, revisao-pendente]` — marcadores de trabalho

**Propriedade fundamental:** tags são descritores auxiliares; nunca substituem campos estruturados ou relacionamentos.

---

## 13. Referência

**Definição:** menção explícita de um Registro a outro, expressa exclusivamente por ID no formato `[PREFIXO]-NNNNNN`.

Formas de referência no SOE-CCG:
- **Campo dedicado:** `receita-id: REC-000001` (referência forte, validada)
- **Lista de IDs:** `ingredientes: [ING-000001, ING-000003, ING-000042]`
- **Referência genérica:** `entidade-referenciada: EXE-000015` + `tipo-entidade: execucao` (usado em Observação)

**Regras:**
- Referências nunca usam nomes, títulos ou descrições
- Referências quebradas (ID inexistente) geram erro de validação
- Referências a entidades arquivadas são permitidas (histórico permanece consultável)

**Propriedade fundamental:** referências por ID garantem que relacionamentos permanecem válidos independentemente de renomeações, reorganizações ou mudanças de texto.

---

## Resumo dos 13 Conceitos

| # | Conceito | Descrição resumida |
|---|----------|-------------------|
| 1 | Registro | Unidade mínima de conhecimento permanente com ID único |
| 2 | Entidade | Tipo de Registro com estrutura e responsabilidade próprias |
| 3 | Relacionamento | Conexão semântica tipada entre Registros por ID |
| 4 | Versão | Número incremental de evolução de conteúdo ou esquema |
| 5 | Histórico | Sequência append-only de todas as mudanças de um Registro |
| 6 | Identificador | Código alfanumérico permanente formato `[PREFIXO]-NNNNNN` |
| 7 | Metadados | Campos descritivos obrigatórios em todo Registro |
| 8 | Template | Arquivo Markdown pré-estruturado para criação de Registros |
| 9 | Esquema | Especificação formal de campos, tipos e validações |
| 10 | Estado | Valor controlado que representa posição no ciclo de vida |
| 11 | Catálogo | Conjunto controlado de valores válidos para campos |
| 12 | Tag | Palavra-chave livre para busca e agrupamento |
| 13 | Referência | Menção explícita de um Registro a outro por ID |

---

## Nota Final

Estes 13 conceitos formam a base conceitual do SOE-CCG. Toda decisão arquitetural, implementação ou extensão futura deve ser expressa em termos destes conceitos ou derivada logicamente deles.

Qualquer funcionalidade que viole um destes conceitos deve ser recusada como incompatível com a arquitetura do sistema.
