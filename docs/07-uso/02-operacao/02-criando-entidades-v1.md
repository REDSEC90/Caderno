# Criando Entidades

> Quando criar, quando reutilizar, como obter IDs e como preencher corretamente.

---

## Antes de Criar: Verificar se Já Existe

**Esta etapa é obrigatória.** Duplicatas corrompem o grafo.

```bash
# Por nome aproximado no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%farinha%';"

# Por arquivo no diretório
ls dados/ingredientes/ | grep -i "farinha"

# Busca em texto livre nos arquivos
grep -r "Farinha de Trigo" dados/ingredientes/
```

Se encontrar o conceito que você quer registrar, **use o ID existente**. Não crie outro.

---

## Obtendo o Próximo ID

Consulte a tabela de controle em `docs/04-padroes/identificadores-v1.md`:

| Prefixo | Último ID utilizado |
|---------|---------------------|
| `REC`   | REC-000001          |
| `ING`   | ING-000004          |
| `TEC`   | TEC-000003          |
| `EQP`   | EQP-000002          |
| `EXE`   | EXE-000001          |
| `OBS`   | OBS-000001          |
| `EXP`   | —                   |

O próximo ID é o último + 1, mantendo os 6 dígitos com zeros à esquerda.
`ING-000004` → próximo é `ING-000005`.

⚠️ Atualize esta tabela imediatamente após criar cada entidade.

---

## Nome do Arquivo

Padrão obrigatório:
```
[PREFIXO]-[NNNNNN]-[slug]-v[schema-version].md
```

Exemplos válidos:
```
ING-000005-farinha-de-trigo-v1.md
REC-000002-pao-de-queijo-mineiro-v1.md
TEC-000004-emulsificacao-v1.md
EXE-000002-doce-de-leite-execucao2-v1.md
OBS-000002-acidez-leite-v1.md
EXP-000001-reducao-acucar-v1.md
```

Slug: minúsculas, sem acentos, sem espaços, hífens como separadores.

---

## Copiando o Template

```bash
cp docs/01-dominio/templates/[entidade]-v1.md \
   dados/[entidade]s/[ID]-[slug]-v1.md
```

Templates disponíveis:
- `docs/01-dominio/templates/receita-v1.md`
- `docs/01-dominio/templates/ingrediente-v1.md`
- `docs/01-dominio/templates/tecnica-v1.md`
- `docs/01-dominio/templates/equipamento-v1.md`
- `docs/01-dominio/templates/execucao-v1.md`
- `docs/01-dominio/templates/observacao-v1.md`
- `docs/01-dominio/templates/experimento-v1.md`

---

## Preenchendo o Frontmatter

### Campos comuns a todas as entidades

```yaml
---
id: ING-000005                # IDÊNTICO ao prefixo-número no nome do arquivo
tipo: ingrediente             # tipo canônico: receita | ingrediente | tecnica | equipamento | execucao | observacao | experimento
schema-version: 1             # versão do schema — usar 1 para novos registros
versao: 1                     # versão do conteúdo do documento
status: ativo                 # ver catálogo de estados para cada entidade
criado-em: 2026-06-27         # data de criação do arquivo (ISO 8601)
atualizado-em: 2026-06-27     # igual a criado-em na criação, atualizar a cada edição
autor: nome-do-autor          # quem criou
tags: []                      # lista de tags descritivas, sem acentos, com hífens
---
```

### O campo `id` deve coincidir com o nome do arquivo

```
Arquivo:     ING-000005-farinha-de-trigo-v1.md
Frontmatter: id: ING-000005                    ← deve ser idêntico
```

O Parser extrai o ID do campo `id`. Se houver divergência, o sistema usará o campo `id` do frontmatter, mas isso cria inconsistência entre o nome do arquivo e o ID — evitar.

---

## Validando Antes de Importar

```bash
# Verificar que o Parser consegue ler o arquivo sem erros
python3 codigo/parser-v1.py dados/ingredientes/ING-000005-farinha-de-trigo-v1.md
```

Erros comuns e soluções:

| Erro | Causa | Solução |
|------|-------|---------|
| `KeyError: 'id'` | Campo `id` ausente no frontmatter | Adicionar `id: ING-NNNNNN` |
| `frontmatter ausente` | Delimitadores `---` faltando | Garantir `---` no início e após o YAML |
| `referencia_quebrada: TEC-000099` | ID referenciado não existe | Criar a TEC antes, ou corrigir o ID |
| `status inválido` | Valor não está no catálogo | Ver `docs/01-dominio/catalogos/estados-todas-entidades-v1.md` |

---

## Checklist de Criação

```
[ ] Verificado que não existe duplicata no sistema
[ ] Próximo ID obtido da tabela de controle
[ ] Nome de arquivo no padrão correto
[ ] Template copiado para o diretório correto
[ ] Campo id no frontmatter = prefixo-número do arquivo
[ ] status válido para o tipo de entidade
[ ] criado-em e atualizado-em preenchidos (ISO 8601: YYYY-MM-DD)
[ ] Relacionamentos usando IDs (nunca nomes)
[ ] Parser executado sem erros
[ ] Importado com sucesso no SQLite
[ ] Controle de IDs (identificadores-v1.md) atualizado
[ ] Commit realizado
```
