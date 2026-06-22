# Conceitos Fundamentais

## Objetivo

Este documento define os conceitos fundamentais do Caderno.

Os conceitos aqui descritos representam o núcleo lógico permanente do sistema e devem permanecer válidos independentemente de mudanças na implementação, banco de dados, linguagem de programação ou domínio específico.

Toda funcionalidade futura deve respeitar estes conceitos.

---

# Filosofia Fundamental

O Caderno não armazena arquivos.

O Caderno não armazena documentos.

O Caderno não armazena apenas textos.

O Caderno transforma informações em conhecimento persistente.

O conhecimento persistente representa a verdade armazenada pelo sistema.

---

# O Fluxo da Verdade

Toda informação percorre o seguinte fluxo:

Fonte

↓

Informação

↓

Interpretação

↓

Conhecimento

↓

Persistência

↓

Consulta

---

A informação original pode desaparecer.

O conhecimento extraído deve permanecer.

---

# Conhecimento

Conhecimento é qualquer informação que possua significado para o sistema e possa ser armazenada, relacionada e recuperada.

O conhecimento representa o principal ativo do Caderno.

Todo elemento armazenado pelo sistema deve existir para preservar conhecimento.

---

# Entidade

Uma entidade representa uma unidade individual de conhecimento.

Toda entidade possui identidade própria.

Exemplos de entidades:

* Receita
* Ingrediente
* Técnica
* Equipamento
* Experiência
* Avaliação
* Categoria
* Observação

O conceito de entidade é permanente.

Os tipos de entidade podem evoluir ao longo do tempo.

---

# Relacionamento

Um relacionamento representa uma conexão semântica entre entidades.

Nenhuma entidade deve ser considerada isoladamente.

O conhecimento surge da combinação entre entidades e relacionamentos.

Exemplo conceitual:

Receita

↓

usa

↓

Ingrediente

---

Sem relacionamentos existe apenas armazenamento.

Com relacionamentos existe conhecimento conectado.

---

# Experiência

Uma experiência representa um evento ocorrido ao longo do tempo.

Experiências registram vivências, resultados, observações e aprendizados.

Exemplos:

* Preparação de uma receita.
* Teste de uma técnica.
* Utilização de um equipamento.
* Avaliação de um resultado.

A experiência representa conhecimento temporal.

---

# Metadado

Metadado representa informação complementar utilizada para descrever conhecimento.

Metadados adicionam contexto sem alterar a identidade principal de uma entidade.

Exemplos:

* Tempo de preparo.
* Quantidade.
* Dificuldade.
* Temperatura.
* Nota.

---

# Histórico

Histórico representa a evolução do conhecimento ao longo do tempo.

O sistema deve preservar alterações relevantes.

O objetivo do histórico não é apenas registrar mudanças.

O objetivo é permitir compreender a evolução do conhecimento.

---

# Fonte

Fonte representa a origem de uma informação.

Exemplos:

* Arquivo.
* Importação.
* Entrada manual.
* Integração externa.

Uma fonte gera informação.

A informação gera conhecimento.

O conhecimento permanece mesmo após a remoção da fonte original.

---

# Persistência

Persistência representa a capacidade do sistema de manter conhecimento disponível ao longo do tempo.

Uma vez assimilado pelo Motor de Conhecimento, o conhecimento passa a existir independentemente da forma pela qual foi recebido.

A persistência garante continuidade, rastreabilidade e preservação.

---

# Consulta

Consulta representa a capacidade de localizar, recuperar e navegar pelo conhecimento armazenado.

Conhecimento não encontrado é equivalente a conhecimento perdido.

Toda informação persistida deve ser recuperável.

---

# Motor de Conhecimento

O Motor de Conhecimento é o componente responsável por transformar informação em conhecimento persistente.

Fluxo conceitual:

Fonte

↓

Informação

↓

Análise

↓

Entidades

↓

Relacionamentos

↓

Persistência

↓

Consulta

---

O Motor de Conhecimento não armazena documentos.

O Motor de Conhecimento assimila conhecimento.

---

# Princípios Fundamentais

## Todo conhecimento possui significado

Nenhum dado deve existir sem propósito definido.

---

## Todo conhecimento possui contexto

Nenhuma informação relevante deve existir isoladamente.

---

## Todo conhecimento pode ser relacionado

O sistema deve permitir conexões entre conhecimentos distintos.

---

## Todo conhecimento possui origem

A rastreabilidade deve ser preservada.

---

## Todo conhecimento pode evoluir

O histórico faz parte do conhecimento.

---

## Todo conhecimento deve ser recuperável

A consulta é parte fundamental do sistema.

---

## A verdade do sistema é o conhecimento persistido

Arquivos, documentos, importações e registros externos são fontes.

A verdade do sistema é o conhecimento extraído, organizado, relacionado e armazenado pelo Motor de Conhecimento.

---

# Núcleo Conceitual do Caderno

Conhecimento

├── Entidades

├── Relacionamentos

├── Experiências

├── Metadados

├── Histórico

├── Fontes

├── Persistência

└── Consulta

---

Todo o restante do sistema deve ser construído sobre este núcleo.

Receitas, ingredientes, técnicas, equipamentos e demais domínios representam especializações do conhecimento e não alteram os conceitos fundamentais aqui definidos.

