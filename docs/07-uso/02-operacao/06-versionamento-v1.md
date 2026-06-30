# Versionamento

> Como evoluir registros ao longo do tempo sem perder história.

---

## Dois Mecanismos Complementares

| Mecanismo | Controla | Automático? |
|-----------|---------|-------------|
| **Git** | Todo o histórico de mudanças | Sim — a cada commit |
| **Sufixo `-vN`** | Versão formal do schema/formato | Manual — criado explicitamente |

Na maioria dos casos, o Git é suficiente. O sufixo `-v2` é usado apenas quando o formato do documento mudou formalmente.

---

## Edição Comum (sem nova versão)

Para corrigir dados, adicionar campos, refinar conteúdo — a forma padrão:

```bash
# 1. Editar
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# 2. Atualizar atualizado-em: 2026-06-27

# 3. Re-importar + commitar
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
git commit -am "fix(rec): adiciona notas sobre ponto firme em REC-000001"
```

O histórico git registra automaticamente o estado anterior.

---

## Quando Criar uma Nova Versão Formal (v2)

Justificativas válidas para uma nova versão formal:

- O schema do arquivo mudou e campos antigos ficaram obsoletos
- A receita foi completamente reformulada (não apenas ajustada)
- É necessário manter as duas versões **simultaneamente** como referências separadas

```bash
# Criar v2 a partir de v1
cp dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md \
   dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md

# Editar v2 com as mudanças
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md
# Alterar: versao: 2
# Alterar: atualizado-em: 2026-06-27

# Arquivar v1 (recomendado)
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
# Alterar: status: arquivada

# Importar
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Commitar
git add dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md
git add dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
git commit -m "feat(rec): versão v2 de REC-000001 com proporção 300g açúcar"
```

O `id` (`REC-000001`) permanece idêntico em v1 e v2. O identificador é do conhecimento, não do arquivo.

---

## Consultando o Histórico

```bash
# Ver todos os commits que afetaram um arquivo
git log --oneline dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Ver o arquivo como estava em um commit específico
git show abc1234:dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Comparar dois commits
git diff abc1234 def5678 dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

---

## Recuperando uma Versão Anterior

```bash
# Restaurar para o estado de um commit específico
git checkout abc1234 -- dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Confirmar e commitar, ou cancelar
git checkout HEAD -- dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

---

## Convenção de Mensagens de Commit

```
[tipo]([escopo]): [descrição]

tipos:   feat | fix | refactor | docs | chore | audit
escopos: rec | ing | tec | eqp | exe | obs | exp | schema | docs | faa
```

Exemplos bons:
```
feat(rec): cria REC-000002 pao-de-queijo-mineiro
feat(exe): registra EXE-000002 segundo preparo doce-de-leite
fix(ing): corrige tipo-ingrediente de ING-000003 para mineral
chore(ing): arquiva ING-000005 duplicata de ING-000001
docs(07-uso): adiciona guia de versionamento
audit(faa): corrige falha DEP-002 ciclo informacional
```

---

## Por que dois mecanismos de versionamento

O git captura toda a história incremental — cada correção de typo, cada ajuste de quantidade, cada nota adicionada. O sufixo `-v2` no nome do arquivo é um sinal explícito de que a estrutura mudou de forma que as versões precisam coexistir como referências separadas. Usar apenas git tornaria impossível distinguir "corrigi um campo" de "reformulei completamente a receita".

---

## Próxima leitura

- Boas práticas consolidadas → [`07-boas-praticas-v1.md`](07-boas-praticas-v1.md)
