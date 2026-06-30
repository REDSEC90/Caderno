# Como Pensar no SOE-CCG

> Este documento muda a mentalidade. Leia antes de qualquer tutorial.

---

## A Mudança Fundamental

Você **não está escrevendo Markdown**.

Você está **registrando conhecimento**.

O Markdown é apenas o formato que o sistema usa para armazenar esse conhecimento de forma legível e durável. Ele é um meio, não um fim.

Essa distinção muda completamente a forma de trabalhar com o SOE.

---

## O que "registrar conhecimento" significa na prática

Quando você aprende que o bicarbonato de sódio evita a coagulação das proteínas do leite durante o preparo do doce de leite, isso é um **conhecimento** que tem valor independente de qualquer receita específica.

No SOE, esse conhecimento não vai em uma nota solta no arquivo da receita. Ele vira uma **Observação** (`OBS`), vinculada ao ingrediente (`ING-000004`) ou à execução onde foi observado, com relevância registrada, para que qualquer outra receita que use bicarbonato possa se beneficiar dessa informação.

A diferença:

| Mentalidade "escrevendo Markdown" | Mentalidade "registrando conhecimento" |
|-----------------------------------|----------------------------------------|
| Adiciona uma nota na receita | Cria uma OBS vinculada ao ING |
| Anota "usei 300g de açúcar" no corpo do texto | Registra uma EXE com desvio documentado |
| Copia a técnica de redução em cada receita | Cria TEC-000001 uma vez e referencia em todas |
| Renomeia um ingrediente na receita | Cria novo ING se for conceito diferente |

---

## Entidade vs. Ocorrência

Uma das distinções mais importantes do sistema:

**Entidade** — o conceito abstrato. Existe uma vez. É reutilizável.
**Ocorrência** — uma instância concreta. Pertence a um momento específico.

| Entidade | Ocorrência |
|----------|-----------|
| `ING-000001` Leite Integral | A quantidade usada em uma execução específica |
| `TEC-000001` Redução | A aplicação da redução em uma receita específica |
| `REC-000001` Doce de Leite | `EXE-000001` — o preparo feito em 25/06/2026 |

Quando você prepara doce de leite pela segunda vez, não cria uma segunda Receita. Cria uma segunda **Execução** (`EXE-000002`) referenciando a mesma Receita (`REC-000001`).

---

## Reutilização é a norma, não a exceção

Sempre que for criar algo, pergunte primeiro: **isso já existe?**

```bash
# Antes de criar um ingrediente, verificar
ls dados/ingredientes/ | grep -i "manteiga"
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%manteiga%';"
```

Criar duplicatas contamina o grafo de conhecimento. Se `ING-000005 Manteiga` e `ING-000012 Manteiga Integral` existem como entidades separadas sem relação, receitas que usam "manteiga" ficam espalhadas e a busca perde coerência.

---

## Identificadores são o que conecta tudo

O ID (`REC-000001`, `ING-000004`, `TEC-000001`) é a identidade permanente de uma entidade. **Nunca muda. Nunca é reutilizado.**

Se você renomear "Leite Integral" para "Leite Integral UHT" amanhã, o ID `ING-000001` continua sendo o mesmo. Todas as receitas que referenciam `ING-000001` continuam corretas sem precisar de nenhuma atualização.

Isso é o que torna o grafo de conhecimento robusto ao longo do tempo.

---

## O pipeline existe para proteger o conhecimento

O processo `parsear → resolver → validar → importar` não é burocracia. Ele garante que:

- Nenhum ID referenciado existe apenas "por declaração" — o Resolver confirma que o alvo realmente existe.
- Nenhum dado inválido entra no banco — o Validador rejeita estados inconsistentes.
- O banco é sempre fiel à fonte — o Importador reflete exatamente o que está no Markdown.

Quando o pipeline rejeita um arquivo, ele está protegendo a integridade do grafo, não criando obstáculos.

---

## Git é a memória do sistema

Cada commit é um snapshot do estado do conhecimento. O histórico git responde perguntas como:

- "Como era essa receita antes da última alteração?"
- "Quando esse ingrediente foi adicionado ao sistema?"
- "Quais mudanças foram feitas na sessão de ontem?"

Por isso: **um commit por sessão, no mínimo**. Commits descritivos. Nunca commitar o banco SQLite.

---

## Resumindo

| O que parece | O que é |
|-------------|---------|
| Escrever um arquivo .md | Registrar uma entidade no grafo de conhecimento |
| Preencher um campo `id:` | Atribuir identidade permanente a um objeto |
| Colocar `ING-000001` em uma lista | Criar uma aresta no grafo |
| Rodar o importador | Derivar o índice SQLite a partir da fonte canônica |
| Fazer um commit | Criar um snapshot imutável do estado do conhecimento |

---

## Próxima leitura

- Criar a primeira entidade → [`../02-operacao/02-criando-entidades-v1.md`](../02-operacao/02-criando-entidades-v1.md)
- Tutorial de sessão completa → [`../05-fluxos/07-fluxo-completo-v1.md`](../05-fluxos/07-fluxo-completo-v1.md)
