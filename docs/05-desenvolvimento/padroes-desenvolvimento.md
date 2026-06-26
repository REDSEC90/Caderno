# Padrões de Desenvolvimento — SOE-CCG

> Convenções de implementação para a Fase 8 do roadmap de maturidade.

---

## 1. Nomenclatura de Arquivos

### Registros em `dados/`

Formato: `[ID]-[slug-do-nome]-v[versao].md`

```
REC-000001-doce-de-leite-artesanal-v1.md
ING-000042-tomate-cereja-v1.md
TEC-000007-fermentacao-v1.md
EQP-000003-forno-eletrico-v1.md
EXE-000001-doce-de-leite-execucao-1.md
OBS-000015-ponto-caramelo.md
EXP-000002-dobrar-fermento.md
```

**Regras:**
- Minúsculas, hífens, sem acentos, sem espaços
- ID sempre no início
- Slug gerado a partir do nome (remover acentos, substituir espaços por hífens)
- Versão apenas em Receitas e Ingredientes — entidades que evoluem formalmente

### Documentação em `docs/`

Formato: `[slug-descritivo].md`

```
politica-templates.md
especificacao-receita.md
esquema-receita-v1.md
```

---

## 2. Estrutura do Frontmatter

Todo arquivo Markdown de dados começa com frontmatter YAML delimitado por `---`:

```yaml
---
id: REC-000001
tipo: receita
schema-version: 1
versao: 1
status: rascunho
criado-em: 2026-06-25
atualizado-em: 2026-06-25
autor: nome-do-autor
origem:
tags: []
---
```

**Regras obrigatórias:**
- Frontmatter deve ser o **primeiro bloco** do arquivo, sem linhas antes dos `---`
- Campos opcionais ausentes são declarados vazios (não omitidos)
- `tags` sempre como lista YAML: `[]` ou `[tag-a, tag-b]`
- Datas no formato ISO 8601: `YYYY-MM-DD`

---

## 3. Estrutura Markdown dos Registros

### Cabeçalho

Título H1 imediatamente após o frontmatter:

```markdown
---
[frontmatter]
---

# Título do Registro
```

### Seções principais

H2 para seções principais, H3 para subseções:

```markdown
## Informações

- **Campo:** valor

## Ingredientes

| ID | Nome | Quantidade | Unidade |
|----|------|------------|---------|

## Modo de Preparo

1. Passo um
2. Passo dois
```

### Referências a outras entidades

IDs sempre com comentário opcional do nome atual (não normativo):

```markdown
| ING-000001 | Leite Integral | 1000 | ml |
```

ou em texto:

```markdown
Esta receita utiliza a técnica de redução (TEC-000001) como etapa central.
```

---

## 4. Convenções do SQLite

### Nomes de tabelas
Minúsculas, plural, underline: `receitas`, `ingredientes`, `receita_ingrediente`

### Nomes de colunas
Minúsculas, underline: `schema_version`, `criado_em`, `receita_id`

### Tipos de dados

| Dado | Tipo SQLite |
|------|-------------|
| ID (`REC-000001`) | `TEXT` |
| Texto curto | `TEXT` |
| Texto longo | `TEXT` |
| Data (`YYYY-MM-DD`) | `TEXT` |
| Inteiro | `INTEGER` |
| Decimal | `REAL` |
| Booleano | `INTEGER` (0 ou 1) |
| Lista (tags) | `TEXT` (JSON serializado) |

### PRAGMA obrigatório no início de cada sessão
```sql
PRAGMA foreign_keys = ON;
```

---

## 5. Organização de Diretórios

```
SOE-CCG/
├── README.md
├── LICENSE
│
├── docs/
│   ├── 00-projeto/         ← visão, filosofia, constituição, roadmap
│   ├── 01-dominio/         ← entidades, esquemas, templates, catálogos
│   ├── 02-arquitetura/     ← fluxo de dados, diagrama mestre
│   ├── 03-modelagem/       ← ER, normalização, SQLite
│   ├── 04-padroes/         ← nomenclatura, políticas, ADRs
│   ├── 05-desenvolvimento/ ← guias de contribuição (este arquivo)
│   ├── 06-operacao/        ← backup, manutenção, monitoramento
│   ├── 98-rascunhos/       ← documentos em elaboração
│   └── 99-referencias/     ← rastreamento, índices
│
├── dados/                  ← FONTE DA VERDADE
│   ├── receitas/
│   ├── execucoes/
│   ├── ingredientes/
│   ├── tecnicas/
│   ├── equipamentos/
│   ├── observacoes/
│   ├── experimentos/
│   ├── anexos/
│   └── importacao/         ← arquivos a serem processados
│
├── banco_de_dados/
│   ├── esquemas/           ← schema.sql e versões
│   ├── migracoes/          ← migration scripts
│   ├── seeds/              ← dados iniciais para novo banco
│   └── sqlite/             ← arquivo .db (não commitar)
│
├── scripts/
│   ├── importacao/         ← parse e sync Markdown → SQLite
│   ├── instalacao/         ← setup do ambiente
│   ├── copia_seguranca/    ← backup automatizado
│   └── manutencao/         ← limpeza, validação
│
├── codigo/                 ← implementação futura
├── testes/                 ← testes automatizados
└── recursos/
    ├── imagens/
    ├── videos/
    ├── audios/
    └── documentos/
```

---

## 6. Fluxo de Criação de um Registro

```
1. Identificar o próximo ID disponível no prefixo correto
   → consultar docs/04-padroes/identificadores.md

2. Copiar o template correspondente
   → docs/01-dominio/templates/[entidade]-v1.md

3. Preencher os campos obrigatórios do frontmatter

4. Preencher o conteúdo seguindo o esquema
   → docs/01-dominio/esquemas/esquema-[entidade]-v1.md

5. Salvar em dados/[entidade]/[ID]-[slug]-v1.md

6. Executar o importador para sincronizar com SQLite
   → scripts/importacao/importar.sh dados/[entidade]/[arquivo].md
```

---

## 7. Fluxo de Atualização de um Registro

**Atualização menor** (correção, esclarecimento, adição de campo opcional):
```
1. Editar o arquivo Markdown em dados/
2. Atualizar atualizado-em para hoje
3. Não incrementar versao
4. Executar importador
```

**Atualização maior** (mudança de conteúdo significativa):
```
1. Criar nova versão do arquivo: [ID]-[slug]-v2.md
2. Incrementar versao para 2
3. Marcar arquivo anterior como obsoleto (status: obsoleto)
4. Atualizar atualizado-em em ambos
5. Executar importador
```

---

## 8. Validação Local

Antes de commitar, validar manualmente:

- [ ] Frontmatter está completo com todos os campos obrigatórios
- [ ] ID está no formato correto (`[PREFIXO]-NNNNNN`)
- [ ] ID não existe em outro arquivo
- [ ] Todos os IDs referenciados existem em `dados/`
- [ ] Status é um valor válido para a entidade
- [ ] Data está no formato `YYYY-MM-DD`
- [ ] Tags estão em minúsculas com hífens

---

## 9. Convenções de Commit

Formato: `[tipo]: [descrição curta]`

**Tipos:**
- `add` — novo registro
- `update` — atualização de registro existente
- `archive` — arquivamento de registro
- `schema` — mudança de esquema
- `doc` — documentação
- `fix` — correção de erro

**Exemplos:**
```
add: REC-000001 doce de leite artesanal v1
update: ING-000001 leite integral - adicionar sazonalidade
archive: EQP-000005 fogão antigo - substituído por EQP-000012
doc: especificacao-receita - adicionar seção de invariantes
```

---

## 10. O que NÃO commitar

```gitignore
banco_de_dados/sqlite/*.db
banco_de_dados/sqlite/*.db-shm
banco_de_dados/sqlite/*.db-wal
dados/importacao/*.tmp
scripts/instalacao/.env
.DS_Store
```
