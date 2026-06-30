# Invariantes do Sistema

> Regras que nunca mudam, nunca têm exceção e nunca podem ser violadas por nenhum agente.

Estas regras são invariantes arquiteturais. Violar qualquer uma delas introduz corrupção no sistema que pode ser difícil ou impossível de reverter.

---

## Invariante 1 — Nunca editar o SQLite diretamente

```
PROIBIDO: UPDATE ingredientes SET nome = 'X' WHERE id = 'ING-000001'
PROIBIDO: INSERT INTO receitas VALUES (...)
PROIBIDO: DELETE FROM ingredientes WHERE id = 'ING-000005'
```

**Por quê:** O banco é um índice derivado dos arquivos Markdown. Qualquer edição direta é sobrescrita na próxima importação. Além disso, edições diretas criam divergência entre a fonte (Markdown) e o índice (SQLite), quebrando a garantia de que o banco reflete fielmente o conhecimento.

**Ação correta:** Editar o arquivo `.md` em `dados/` e re-importar.

---

## Invariante 2 — Nunca reutilizar um ID

```
PROIBIDO: criar ING-000003 se ING-000003 já existiu (mesmo arquivado)
```

**Por quê:** IDs são permanentes no grafo de conhecimento. Um ID arquivado ainda pode ser referenciado no histórico git, em logs, em OBS antigas, em EXE antigas. Reutilizar um ID cria ambiguidade irresolvível: o sistema não consegue distinguir se `ING-000003` em uma OBS de 2024 se refere à entidade original (arquivada) ou à nova.

**Ação correta:** IDs são sempre incrementais. Nunca reciclar.

---

## Invariante 3 — Nunca alterar o campo `id` de uma entidade existente

```
PROIBIDO: abrir ING-000005 e mudar id: ING-000005 para id: ING-000012
```

**Por quê:** Todos os arquivos que referenciam `ING-000005` continuarão apontando para o ID antigo. A entidade renomeada passa a ser invisível para o grafo — e os referenciadoss ficam com referências quebradas.

**Ação correta:** IDs não mudam nunca. Se um ID foi criado com erro, arquivar a entidade errada e criar uma nova com o ID correto.

---

## Invariante 4 — Nunca deletar arquivos de `dados/`

```
PROIBIDO: rm dados/ingredientes/ING-000005-slug-v1.md
PROIBIDO: git rm dados/receitas/REC-000002-slug-v1.md
```

**Por quê:** O arquivo `.md` é o registro histórico. Deletar destrói o conhecimento permanentemente — o git preserva a existência do arquivo mas a intenção do sistema é que arquivos deletados intencionalmente não existam.

**Ação correta:** Mudar o `status` para `arquivado` e re-importar. O arquivo permanece em disco.

---

## Invariante 5 — Nunca referenciar entidades por nome em campos de relacionamento

```yaml
# PROIBIDO
ingredientes: [Leite Integral, Açúcar Refinado]

# CORRETO
ingredientes: [ING-000001, ING-000002]
```

**Por quê:** Nomes mudam. IDs não. Se `Leite Integral` for renomeado para `Leite Integral Pasteurizado`, todas as receitas que referenciam pelo nome ficam com referência inválida. IDs são imutáveis por definição.

---

## Invariante 6 — Nunca commitar o banco SQLite

```
PROIBIDO: git add banco_de_dados/sqlite/soe-ccg.db
```

**Por quê:** O banco é derivado e reconstruível. Commitá-lo polui o histórico git com binários grandes, cria conflitos impossíveis de resolver em merges, e dá a falsa impressão de que o banco é a fonte de verdade.

**Verificação:** O `.gitignore` já exclui `*.db`. Se este arquivo aparecer em `git status`, algo está errado com a configuração.

---

## Invariante 7 — Nunca criar entidade sem verificar existência

```
PROIBIDO: criar ING sem consultar o banco e os arquivos primeiro
```

**Por quê:** Duplicatas dividem o grafo de conhecimento. Se `ING-000005 Leite de Coco` e `ING-000011 Leite Coco` existem como entidades separadas, receitas que usam um não aparecem nas consultas de quem buscou pelo outro.

**Ação correta:** Sempre executar a verificação de existência antes de criar qualquer entidade. Ver [`01-protocolo-operacional-v1.md`](01-protocolo-operacional-v1.md#verificação-de-existência-antes-de-criar).

---

## Invariante 8 — Nunca criar entidade sem importar imediatamente

```
PROIBIDO: criar 10 arquivos .md e só depois importar
```

**Por quê:** Se você criar REC-000002 que referencia ING-000005, e ING-000005 ainda não foi importado, o Resolver vai falhar. A ordem de importação importa. Criar e importar cada entidade imediatamente garante que o banco está sempre sincronizado com os arquivos.

**Ação correta:** Criar → importar → verificar → próxima entidade.

---

## Resumo para implementação de agente

```python
# Pseudocódigo de operação segura

def criar_entidade(tipo, dados):
    # Invariante 7: verificar existência
    if existe_conceito_similar(tipo, dados["nome"]):
        raise DuplicataError("Entidade similar já existe")
    
    # Obter próximo ID
    proximo_id = obter_proximo_id(tipo)
    
    # Criar arquivo
    arquivo = criar_arquivo_markdown(proximo_id, dados)
    
    # Invariante 8: importar imediatamente
    resultado = importar(arquivo)
    if not resultado.sucesso:
        raise ImportacaoError(resultado.erro)
    
    # Verificar resultado
    entidade = consultar_banco(proximo_id)
    assert entidade is not None
    
    # Commitar
    git_commit(arquivo, f"feat({tipo}): adiciona {proximo_id}")
    
    return proximo_id
```
