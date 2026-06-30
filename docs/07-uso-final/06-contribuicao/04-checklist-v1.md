# Checklist de Contribuição Segura

> Use este checklist antes de qualquer commit que modifique entidades, schema ou pipeline.

---

## Checklist: Nova Entidade

```
Pré-criação:
[ ] Busquei no banco e nos arquivos — confirmo que não há duplicata
[ ] Consultei identificadores-v1.md e anotei o próximo ID disponível
[ ] Todas as entidades referenciadas (ING, TEC, EQP) já existem no sistema

Criação:
[ ] Template copiado para o diretório correto
[ ] Nome do arquivo segue o padrão [PREFIXO]-[NNNNNN]-[slug]-v1.md
[ ] Campo id no frontmatter = prefixo-número do nome do arquivo
[ ] status é um valor válido para o tipo de entidade
[ ] criado-em e atualizado-em preenchidos em YYYY-MM-DD (não placeholders)
[ ] Campos de relacionamento usam IDs (não nomes)
[ ] Conteúdo Markdown completo abaixo do frontmatter

Pós-criação:
[ ] Parser executado sem erros
[ ] Importador rodou com sucesso
[ ] Verificado no SQLite que a entidade foi persistida
[ ] identificadores-v1.md atualizado com o novo ID
[ ] FAA executado — sem novas falhas críticas
[ ] Commit realizado com mensagem no padrão correto
```

---

## Checklist: Edição de Entidade

```
[ ] Identificado quais outros registros dependem desta entidade
[ ] Campo atualizado-em atualizado para hoje
[ ] Se relações foram alteradas: verificado que novos alvos existem
[ ] Se status foi alterado: transição é válida no catálogo de estados
[ ] Reimportado após edição
[ ] FAA executado — sem novas falhas
[ ] Commit com mensagem descritiva da mudança
```

---

## Checklist: Mudança em Schema/Pipeline

```
[ ] ADR escrita e revisada (se decisão arquitetural)
[ ] Alteração testada em branch separada antes do merge
[ ] Banco reconstruído do zero após mudança no schema
[ ] Todos os arquivos existentes ainda importam sem erro
[ ] FAA executado — sem regressões
[ ] Documentação atualizada (03-validacao/ ou 07-referencia/)
[ ] Commit com escopo correto (schema | parser | faa)
```

---

## Checklist: Sessão de Trabalho (geral)

```
Ao início:
[ ] git pull (se trabalhando com remoto)
[ ] FAA executado para verificar estado inicial

Durante:
[ ] Verificar existência antes de cada novo ING/TEC/EQP
[ ] Criar dependências antes de referenciar

Ao final:
[ ] Todos os novos arquivos estão em dados/
[ ] identificadores-v1.md atualizado
[ ] Parser: sem erros em nenhum arquivo novo
[ ] Importador: todos os arquivos importados
[ ] FAA: sem novas falhas críticas
[ ] git status limpo
[ ] Commit feito com mensagem descritiva
[ ] git push (se trabalhando com remoto)
```
