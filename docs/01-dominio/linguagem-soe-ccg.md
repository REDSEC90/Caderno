# Linguagem do SOE-CCG

> Vocabulário oficial, estrutura léxica e semântica do sistema. Nenhum termo tem dois significados.

---

## Objetivo

Esta fase elimina toda ambiguidade terminológica do SOE-CCG.

Cada termo aqui definido tem exatamente um significado. O mesmo conceito nunca é chamado por dois nomes diferentes. Duas coisas diferentes nunca compartilham o mesmo nome.

Este documento é a referência definitiva para redação de qualquer documentação, código ou interface do SOE-CCG.

---

## 1. Vocabulário Oficial

### Termos do Domínio Gastronômico

| Termo | Definição formal |
|-------|-----------------|
| **Ingrediente** | Insumo culinário: substância usada no preparo de alimentos. |
| **Técnica** | Procedimento culinário: método aplicado na transformação de ingredientes. |
| **Equipamento** | Ferramenta culinária: utensílio ou aparelho usado no preparo. |
| **Receita** | Definição prescritiva de um preparo: ingredientes, técnicas, equipamentos e processo. |
| **Execução** | Realização concreta de uma Receita: o que aconteceu em um preparo real. |
| **Observação** | Percepção ou aprendizado registrado sobre qualquer aspecto culinário. |
| **Experimento** | Tentativa deliberada de testar hipótese culinária com resultado documentado. |
| **Preparo** | Ato físico de cozinhar. Sinônimo de Execução no domínio gastronômico. |

### Termos do Domínio do Sistema

| Termo | Definição formal |
|-------|-----------------|
| **Registro** | Unidade mínima de conhecimento no SOE-CCG. Toda entidade é um tipo de Registro. |
| **Entidade** | Categoria de Registro com definição, atributos, estados e ciclo de vida próprios. |
| **Identificador (ID)** | Código permanente atribuído a um Registro no momento da criação. Nunca muda. Nunca é reutilizado. |
| **Esquema** | Definição formal dos campos de uma Entidade: quais existem, quais são obrigatórios, seus tipos e restrições. |
| **Template** | Modelo estrutural que define como um Registro deve ser escrito em Markdown. |
| **Versão** | Estado imutável de um Registro em um momento específico. |
| **Histórico** | Conjunto ordenado de todas as versões de um Registro desde sua criação. |
| **Estado** | Fase do ciclo de vida de um Registro (ex: rascunho, ativo, arquivado). |
| **Metadado** | Campo que descreve o Registro em si, não o conhecimento que ele contém (ex: data de criação, autor, versão do esquema). |
| **Catálogo** | Conjunto fechado e padronizado de valores reutilizáveis em uma dimensão do sistema. |
| **Tag** | Marcador livre associado a um Registro para organização informal. |
| **Relacionamento** | Vínculo entre dois Registros, sempre expresso por identificadores, nunca por nomes. |
| **Fonte da Verdade** | O arquivo Markdown em `dados/` — localização oficial e permanente de qualquer Registro. |
| **Índice de Consulta** | O banco de dados SQLite — representação derivada da Fonte da Verdade para eficiência de busca. |
| **Arquivamento** | Transição de um Registro para estado inativo, sem exclusão. |
| **Motor de Conhecimento** | Componente do SOE-CCG responsável por interpretar, estruturar e persistir conhecimento. |

---

## 2. Termos Proibidos

Estes termos criam ambiguidade e **não devem ser usados** na documentação ou código do SOE-CCG:

| Termo proibido | Motivo | Use em vez disso |
|----------------|--------|-----------------|
| "banco de dados" (como sinônimo de fonte da verdade) | Confunde SQLite (índice) com Markdown (fonte) | "Fonte da Verdade" ou "Índice de Consulta" |
| "deletar" / "excluir" | Operação que não existe no SOE-CCG | "Arquivar" |
| "gerenciador de receitas" | Reduz o sistema a apenas um domínio | "Motor de Conhecimento" |
| "salvar" (sem contexto) | Ambíguo — salvar no Markdown ou no SQLite? | "Registrar" (Markdown) ou "Sincronizar" (SQLite) |
| "usuário" (como ator) | Ambíguo em sistemas multi-papel | "Autor", "Revisor", "Mantenedor" ou "Administrador" |
| "campo" (sem especificar esquema ou template) | Confunde campo de esquema com seção de template | "Campo do esquema" ou "Seção do template" |
| "arquivo" (sem contexto) | Ambíguo — arquivo Markdown, SQLite ou de recursos | "Registro Markdown", "Banco SQLite" ou "Recurso" |

---

## 3. Estrutura Léxica dos Documentos

### Regras de redação

Todo documento do SOE-CCG deve seguir estas regras de escrita:

**R1 — Precisão sobre brevidade:**
A frase mais curta que causa ambiguidade é pior que a frase mais longa que a elimina.

**R2 — Uma afirmação por frase:**
Frases compostas que afirmam duas coisas ao mesmo tempo devem ser separadas.

**R3 — Voz ativa:**
"O sistema valida o esquema" — não "O esquema é validado pelo sistema".

**R4 — Definição antes do uso:**
Qualquer termo não-óbvio deve ser definido antes de ser usado. Termos definidos neste documento podem ser usados sem redefinição.

**R5 — Sem sinônimos:**
Se duas palavras significam a mesma coisa no SOE-CCG, escolhe-se uma e abandona-se a outra.

**R6 — Exemplos sempre concretos:**
Exemplos abstratos criam mais dúvida do que certeza. Exemplos concretos usam IDs reais (`ING-000042`), nomes reais ("Tomate Cereja"), estados reais.

---

## 4. Estrutura de Relacionamento

### Como relacionamentos são expressos em Markdown

Todo relacionamento entre Registros usa identificadores no formato `[PREFIXO]-NNNNNN`:

```markdown
## Ingredientes

- 200g [ING-000042]  (Tomate Cereja — comentário opcional, não normativo)
- 5ml [ING-000089]   (Azeite Extra Virgem)
```

**O nome entre parênteses é comentário humano.** O ID é o vínculo real. Se o nome do ingrediente mudar, o ID continua correto. Se o parêntese for removido, o vínculo permanece.

### Hierarquia de relacionamentos

```
Receita
  ├── utiliza → Ingrediente(s)
  ├── aplica  → Técnica(s)
  ├── requer  → Equipamento(s)
  └── possui  → Execução(ões)
         └── gera → Observação(ões)

Experimento
  ├── parte-de  → Receita (base)
  ├── origina   → Receita (nova)
  └── gera      → Observação(ões)

Observação
  └── sobre → qualquer Entidade
```

---

## 5. Semântica dos Estados

### O que "ativo" significa

Um Registro em estado `ativo` é:
- Acessível em buscas padrão.
- Utilizável como referência por outros Registros.
- Considerado conhecimento válido e atual.

### O que "arquivado" significa

Um Registro em estado `arquivado` é:
- Invisível em buscas padrão.
- Ainda consultável por busca explícita.
- Ainda válido como referência histórica.
- Não sujeito a edição.
- Não reutilizável — seu ID permanece reservado.

### O que "obsoleto" significa

Um Registro em estado `obsoleto` é:
- Substituído por versão mais recente (indicada em `substituido-por`).
- Estado final — não pode transitar para outro estado.
- Preservado exclusivamente para rastreabilidade histórica.

### O que "rascunho" significa

Um Registro em estado `rascunho` é:
- Em construção — pode estar incompleto.
- Visível apenas para o autor.
- Não referenciável por outros Registros.
- Não sincronizado com SQLite.

---

## 6. Semântica de Versionamento

### Versão de conteúdo vs versão de esquema

Estes são dois conceitos distintos e não devem ser confundidos:

**Versão de conteúdo (`versao`):**
- Incrementada quando o conhecimento representado muda.
- Ex: Receita de Pão Francês `versao: 1` → adição de nova etapa → `versao: 2`.
- Controlada no campo `versao` do Registro.

**Versão de esquema (`schema-version`):**
- Define qual versão da estrutura de campos o Registro usa.
- Ex: Registro criado com `schema-version: 1` → esquema evolui → novo Registro usa `schema-version: 2`.
- Registro antigo continua válido com `schema-version: 1`.
- Controlada no campo `schema-version` do Registro.

---

## 7. Glossário Oficial

Este glossário consolida todas as definições do SOE-CCG em ordem alfabética para consulta rápida.

| Termo | Definição |
|-------|-----------|
| **Administrador** | Papel com todas as permissões do sistema. |
| **Arquivamento** | Operação que transita um Registro para o estado inativo sem excluí-lo. |
| **Arquivo Markdown** | Arquivo `.md` em `dados/` que constitui a Fonte da Verdade de um Registro. |
| **Ativo** | Estado de um Registro finalizado e em uso. Acessível em buscas padrão. |
| **Autor** | Papel responsável por criar e editar Registros. |
| **Catálogo** | Conjunto fechado de valores padronizados para uma dimensão do sistema. |
| **Ciclo de Vida** | Sequência de estados que um Registro percorre desde a criação até o arquivamento. |
| **Consolidada** | Estado de uma Execução encerrada sem possibilidade de alteração de conteúdo. |
| **Domínio Gastronômico** | Conjunto de conceitos culinários que o SOE-CCG representa. |
| **Domínio do Sistema** | Conjunto de conceitos computacionais do SOE-CCG. |
| **Entidade** | Categoria de Registro com especificação própria. |
| **Equipamento** | Utensílio ou aparelho culinário. Entidade de referência normalizada. |
| **Esquema** | Definição formal dos campos de uma Entidade. |
| **Estado** | Fase do ciclo de vida de um Registro. |
| **Execução** | Registro de um preparo real de uma Receita. |
| **Experimento** | Registro de tentativa deliberada de testar hipótese culinária. |
| **Filosofia** | Conjunto de axiomas que governa todas as decisões do SOE-CCG. |
| **Fonte da Verdade** | Arquivo Markdown em `dados/` — localização oficial de qualquer Registro. |
| **Histórico** | Conjunto de versões de um Registro preservadas no git. |
| **ID** | Código permanente único no formato `[PREFIXO]-NNNNNN`. |
| **Índice de Consulta** | Banco de dados SQLite — derivado da Fonte da Verdade. |
| **Ingrediente** | Insumo culinário. Entidade de referência normalizada. |
| **Mantenedor** | Papel responsável pela curadoria do domínio. |
| **Metadado** | Campo que descreve o Registro em si (id, tipo, versão, data, autor). |
| **Motor de Conhecimento** | Núcleo arquitetural que transforma informação em conhecimento estruturado. |
| **Observação** | Registro de percepção ou aprendizado sobre qualquer entidade. |
| **Obsoleto** | Estado final de um Registro substituído por versão mais recente. |
| **Rascunho** | Estado de um Registro em construção, visível apenas para o autor. |
| **Receita** | Definição prescritiva de um preparo culinário. |
| **Registro** | Unidade mínima de conhecimento no SOE-CCG. |
| **Relacionamento** | Vínculo entre dois Registros, expresso por IDs. |
| **Revisão** | Processo de validação de um Registro antes de ser ativado. |
| **Revisor** | Papel responsável por validar Registros submetidos para revisão. |
| **Tag** | Marcador livre associado a um Registro. |
| **Técnica** | Procedimento culinário. Entidade de referência normalizada. |
| **Template** | Modelo estrutural para escrita de um Registro em Markdown. |
| **Versão** | Estado imutável de um Registro em um momento. Campo `versao` do Registro. |
| **Versão de Esquema** | Versão da estrutura de campos usada pelo Registro. Campo `schema-version`. |
