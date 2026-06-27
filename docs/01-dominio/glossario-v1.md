---
id: DOC-GLOSSARIO-V1
tipo: documento
versao: 1
status: ativo
criado-em: 2026-06-26
atualizado-em: 2026-06-26
autor: Sistema SOE-CCG
schema-version: 1
---

# Glossário Oficial do SOE-CCG v1

> Definições canônicas de todos os termos do sistema

---

## Propósito

Este documento é a **fonte única de verdade** para terminologia do SOE-CCG.

Cada termo tem exatamente uma definição. Nenhum conceito tem dois nomes. Nenhum nome tem dois significados.

---

## Domínio Gastronômico

### Ingrediente
Insumo culinário: substância usada no preparo de alimentos.

### Técnica
Procedimento culinário: método aplicado na transformação de ingredientes.

### Equipamento
Ferramenta culinária: utensílio ou aparelho usado no preparo.

### Receita
Definição prescritiva de um preparo: ingredientes, técnicas, equipamentos e processo.

### Execução
Realização concreta de uma Receita: registro do que aconteceu em um preparo real.

### Preparo
Ato físico de cozinhar. Sinônimo de Execução no contexto gastronômico.

### Observação
Percepção ou aprendizado registrado sobre qualquer aspecto culinário.

### Experimento
Tentativa deliberada de testar hipótese culinária com resultado documentado.

---

## Domínio do Sistema

### Registro
Unidade mínima de conhecimento no SOE-CCG. Toda entidade é um tipo de Registro.

### Entidade
Categoria de Registro com definição, atributos, estados e ciclo de vida próprios.

### Identificador (ID)
Código permanente atribuído a um Registro no momento da criação.  
**Propriedades:** Nunca muda. Nunca é reutilizado. Formato: `[PREFIXO]-NNNNNN`

### Esquema
Definição formal dos campos de uma Entidade: quais existem, quais são obrigatórios, seus tipos e restrições.

### Template
Modelo estrutural que define como um Registro deve ser escrito em Markdown.

### Versão
Estado imutável de um Registro em um momento específico. Campo `versao` do frontmatter.

### Versão de Esquema
Versão da estrutura de campos usada pelo Registro. Campo `schema-version` do frontmatter.

### Histórico
Conjunto ordenado de todas as versões de um Registro desde sua criação (via git).

### Estado
Fase do ciclo de vida de um Registro. Valores possíveis definidos em catálogo próprio.

### Metadado
Campo que descreve o Registro em si, não o conhecimento que ele contém.  
**Exemplos:** `id`, `tipo`, `versao`, `criado-em`, `autor`, `schema-version`

### Catálogo
Conjunto fechado e padronizado de valores reutilizáveis em uma dimensão do sistema.  
**Exemplos:** estados, categorias, unidades de medida, tipos de equipamento

### Tag
Marcador livre associado a um Registro para organização informal.

### Relacionamento
Vínculo entre dois Registros, sempre expresso por identificadores, nunca por nomes.

### Fonte da Verdade
Arquivo Markdown em `dados/` — localização oficial e permanente de qualquer Registro.

### Índice de Consulta
Banco de dados SQLite — representação derivada da Fonte da Verdade para eficiência de busca.

### Arquivamento
Transição de um Registro para estado inativo, sem exclusão física.

### Motor de Conhecimento
Componente do SOE-CCG responsável por interpretar, estruturar e persistir conhecimento.

---

## Estados de Registros

### Rascunho
Estado de um Registro em construção.  
**Características:** Pode estar incompleto. Visível apenas para o autor. Não referenciável. Não sincronizado com SQLite.

### Ativo
Estado de um Registro finalizado e em uso.  
**Características:** Acessível em buscas padrão. Utilizável como referência. Conhecimento válido e atual.

### Arquivado
Estado de um Registro inativo mas preservado.  
**Características:** Invisível em buscas padrão. Consultável por busca explícita. Não editável. ID permanece reservado.

### Obsoleto
Estado final de um Registro substituído por versão mais recente.  
**Características:** Substituído por outro (indicado em `substituido-por`). Preservado para rastreabilidade histórica.

### Consolidada
Estado específico de Execução encerrada sem possibilidade de alteração de conteúdo.

---

## Papéis do Sistema

### Autor
Papel responsável por criar e editar Registros.

### Revisor
Papel responsável por validar Registros submetidos para revisão.

### Mantenedor
Papel responsável pela curadoria do domínio e evolução estrutural.

### Administrador
Papel com todas as permissões do sistema.

---

## Conceitos Arquiteturais

### Filosofia
Conjunto de axiomas que governa todas as decisões do SOE-CCG.  
**Documento:** `docs/00-projeto/filosofia-v1.md`

### Constituição
Conjunto de regras fundamentais imutáveis do sistema.  
**Documento:** `docs/00-projeto/constituicao-v1.md`

### Baseline
Conjunto mínimo de artefatos obrigatórios para o sistema ser considerado completo e operacional.

### Contrato
Especificação formal das responsabilidades, interface e comportamento de um componente.

### Ciclo de Vida
Sequência de estados que um Registro percorre desde a criação até o arquivamento.

---

## Operações do Sistema

### Registrar
Persistir conhecimento em arquivo Markdown na Fonte da Verdade.

### Sincronizar
Atualizar o Índice de Consulta (SQLite) a partir da Fonte da Verdade.

### Arquivar
Transitar um Registro para o estado `arquivado`.

### Revisar
Processo de validação de um Registro antes de ser ativado.

### Consolidar
Finalizar uma Execução, impedindo modificações futuras.

---

## Termos Técnicos

### Frontmatter
Bloco YAML no início de arquivo Markdown contendo metadados estruturados.  
**Formato:**
```yaml
---
id: XXX-NNNNNN
tipo: entidade
versao: N
---
```

### Prefixo
Parte inicial do ID que identifica o tipo de Registro.  
**Exemplos:** `ING` (ingrediente), `TEC` (técnica), `REC` (receita), `EXE` (execução)

### Slug
Identificador legível derivado do nome, usado em URLs e nomes de arquivo.  
**Exemplo:** "Tomate Cereja" → `tomate-cereja`

---

## Termos Proibidos

Estes termos criam ambiguidade e **não devem ser usados**:

| Termo proibido | Motivo | Use em vez disso |
|----------------|--------|-----------------|
| "banco de dados" (como sinônimo de fonte) | Confunde SQLite com Markdown | "Fonte da Verdade" ou "Índice" |
| "deletar" / "excluir" | Operação inexistente no SOE | "Arquivar" |
| "gerenciador de receitas" | Reduz o sistema a um domínio | "Motor de Conhecimento" |
| "salvar" (sem contexto) | Ambíguo | "Registrar" ou "Sincronizar" |
| "usuário" (como ator) | Ambíguo em multi-papel | "Autor", "Revisor", etc |
| "campo" (sem contexto) | Confunde esquema e template | "Campo do esquema" ou "Seção" |
| "arquivo" (sem contexto) | Ambíguo | "Registro Markdown", "Banco SQLite" |

---

## Índice Alfabético

| Termo | Categoria |
|-------|-----------|
| Administrador | Papel |
| Ativo | Estado |
| Arquivado | Estado |
| Arquivamento | Operação |
| Autor | Papel |
| Baseline | Arquitetura |
| Catálogo | Sistema |
| Ciclo de Vida | Arquitetura |
| Consolidar | Operação |
| Consolidada | Estado |
| Constituição | Arquitetura |
| Contrato | Arquitetura |
| Entidade | Sistema |
| Equipamento | Gastronômico |
| Esquema | Sistema |
| Estado | Sistema |
| Execução | Gastronômico |
| Experimento | Gastronômico |
| Filosofia | Arquitetura |
| Fonte da Verdade | Sistema |
| Frontmatter | Técnico |
| Histórico | Sistema |
| ID / Identificador | Sistema |
| Índice de Consulta | Sistema |
| Ingrediente | Gastronômico |
| Mantenedor | Papel |
| Metadado | Sistema |
| Motor de Conhecimento | Arquitetura |
| Observação | Gastronômico |
| Obsoleto | Estado |
| Prefixo | Técnico |
| Preparo | Gastronômico |
| Rascunho | Estado |
| Receita | Gastronômico |
| Registrar | Operação |
| Registro | Sistema |
| Relacionamento | Sistema |
| Revisar | Operação |
| Revisor | Papel |
| Sincronizar | Operação |
| Slug | Técnico |
| Tag | Sistema |
| Técnica | Gastronômico |
| Template | Sistema |
| Versão | Sistema |
| Versão de Esquema | Sistema |

---

**Status:** ✅ CONGELADO (v1)  
**Imutabilidade:** Este documento não pode ser modificado. Atualizações geram nova versão.  
**Próxima versão:** glossario-v2.md (se necessário)
