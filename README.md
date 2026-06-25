# SOE-CCG

> Sistema de Registro, Organização, Evolução e Consulta de Conhecimento Gastronômico.

## Visão

O SOE-CCG nasceu da necessidade de registrar, preservar, organizar, relacionar e evoluir conhecimento gastronômico durante muitos anos, independentemente da tecnologia utilizada para acessá-lo.

Não é um gerenciador de receitas.

É um motor de conhecimento gastronômico.

## Filosofia

O software não nasce pelo código. Nasce pelo conhecimento.

Toda implementação é consequência do domínio previamente definido.

```
Filosofia → Constituição → Governança → Especificações → Modelagem → Implementação → Interface
```

## Princípios

* O conhecimento é permanente. A implementação é temporária.
* Markdown é o formato canônico.
* SQLite é apenas um mecanismo de consulta.
* Nenhuma informação deve existir exclusivamente no banco de dados.
* Todo registro possui identificador permanente.
* Relacionamentos utilizam identificadores, nunca nomes.

## Status

🚧 Fase de fundação — domínio e arquitetura em definição.

Nenhuma API ou estrutura de implementação deve ser considerada estável neste momento.

## Documentação

```
docs/00-projeto/    Visão, constituição, objetivos, escopo, roadmap, glossário
docs/01-dominio/    Entidades, esquemas, templates, catálogos
docs/02-arquitetura/  Fluxo de dados, versionamento, importação, exportação
docs/03-modelagem/  Modelo ER, normalização, IDs, SQLite
docs/04-padroes/    Nomenclatura, identificadores, metadados, tags, validação
```

## Licença

A definir.
