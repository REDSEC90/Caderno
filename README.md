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

🟡 Fase de fundação — 78% completa. Pronto para iniciar implementação básica.

**Fases concluídas:** 0 (Identidade) · 1 (Constituição) · 2 (Governança) · 3 (Linguagem) · 4 (Domínio) · 6 (Catálogos) · 7 (Relacionamentos) · 8 (Padrões) · 9 (Modelagem) · 11 (Casos de Uso) · 12 (Validação)

**Fases parciais:** 5 (Contratos — template definido, contratos individuais pendentes)

**Fases pendentes:** 10 (Dados Canônicos — inicial criado) · 13 (Implementação)

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
