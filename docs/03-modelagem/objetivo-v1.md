# Objetivo

## Propósito

A pasta `03-basededados` existe para documentar como o Caderno representa, transforma, relaciona, armazena e recupera conhecimento.

Esta documentação não descreve apenas tabelas ou estruturas técnicas.

Seu objetivo é definir a linguagem de dados do sistema, servindo como referência para toda decisão relacionada ao armazenamento, processamento e consulta de conhecimento.

O banco de dados é uma implementação.

O modelo de conhecimento é a verdade.

---

# Visão

O Caderno não deve ser construído como um sistema de receitas.

O Caderno deve ser construído como um sistema de conhecimento gastronômico capaz de preservar experiências, aprendizados, descobertas e evolução ao longo do tempo.

Receitas representam apenas um dos tipos de conhecimento suportados pelo sistema.

O objetivo de longo prazo é permitir que qualquer conhecimento gastronômico relevante possa ser registrado, relacionado, consultado e preservado.

---

# Problema Que o Projeto Resolve

Ao longo dos anos uma pessoa acumula:

* Receitas.
* Técnicas.
* Ingredientes.
* Equipamentos.
* Experiências.
* Preferências.
* Observações.
* Descobertas.
* Ajustes pessoais.
* Aprendizados.

Grande parte desse conhecimento é perdida, esquecida ou fica espalhada entre cadernos, aplicativos, arquivos e memória pessoal.

O Caderno busca consolidar esse conhecimento em um único local, preservando não apenas informações isoladas, mas também as relações existentes entre elas.

---

# Objetivo Principal

Transformar informações gastronômicas em conhecimento estruturado.

O sistema deve ser capaz de:

* Receber informações.
* Interpretar informações.
* Identificar entidades.
* Identificar relacionamentos.
* Preservar histórico.
* Facilitar consultas.
* Permitir evolução contínua do conhecimento.

---

# Filosofia de Dados

O Caderno não armazena documentos.

O Caderno não armazena páginas.

O Caderno não armazena apenas textos.

O Caderno armazena conhecimento estruturado.

Todo conhecimento deve ser representado de forma compreensível pelo sistema e reutilizável no futuro.

---

# Princípios Fundamentais

## Tudo é Conhecimento

Toda informação relevante inserida no sistema representa conhecimento.

Exemplos:

* Receita.
* Ingrediente.
* Técnica.
* Equipamento.
* Experiência.
* Avaliação.
* Observação.
* Categoria.

---

## Conhecimento Possui Estrutura

Nenhuma informação deve existir isoladamente.

Todo conhecimento deve poder:

* Ser identificado.
* Ser relacionado.
* Ser pesquisado.
* Ser evoluído.

---

## Conhecimento Possui Contexto

Uma receita isolada possui valor limitado.

Uma receita associada a:

* Experiências.
* Avaliações.
* Ajustes.
* Observações.
* Histórico.

possui valor significativamente maior.

---

## Conhecimento Evolui

O sistema deve permitir acompanhar mudanças ao longo do tempo.

Exemplos:

* Melhorias em receitas.
* Mudanças de gosto.
* Novas técnicas aprendidas.
* Descoberta de novos ingredientes.
* Evolução culinária pessoal.

Nenhuma informação importante deve ser perdida.

---

# Papel do Motor de Conhecimento

Toda informação inserida no sistema deverá passar pelo Motor de Conhecimento.

Fluxo esperado:

Informação Bruta

↓

Validação

↓

Interpretação

↓

Identificação de Entidades

↓

Identificação de Relacionamentos

↓

Persistência

↓

Consulta

O Motor de Conhecimento é o núcleo responsável por transformar informação em conhecimento estruturado.

---

# O Que Deve Ser Documentado Nesta Seção

Esta seção deverá definir:

* Conceitos fundamentais.
* Entidades.
* Relacionamentos.
* Experiências.
* Metadados.
* Fluxos de dados.
* Modelo lógico.
* Modelo físico.
* Versionamento.
* Glossário.

Toda implementação futura deverá ser compatível com estas definições.

---

# Estado Desejado

Ao longo dos próximos anos o Caderno deverá evoluir para uma memória gastronômica pessoal baseada em conhecimento.

O sistema deverá permitir responder perguntas como:

* Qual foi a melhor receita que preparei?
* Como determinada receita evoluiu ao longo do tempo?
* Quais técnicas utilizo com mais frequência?
* Quais ingredientes aparecem com maior frequência?
* Quais experiências tiveram melhores resultados?
* Como minha jornada gastronômica evoluiu ao longo dos anos?

O objetivo final não é armazenar receitas.

O objetivo final é preservar, organizar e entregar experiências gastronômicas através de uma rede estruturada de conhecimento construída continuamente ao longo do tempo.

