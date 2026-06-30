# Fluxo: Criar uma Técnica

> Uma Técnica documenta um método culinário de forma reutilizável.

---

## Quando criar uma Técnica

Quando o método que você usa em uma receita:
- Pode ser aplicado em múltiplas outras receitas
- Tem pontos críticos, variações ou riscos que merecem documentação centralizada
- Ainda não existe no sistema

Não crie TEC para cada variação mínima — "mexer" e "agitar continuamente" são variações da mesma técnica base.

---

## Passo a Passo

```bash
# 1. Verificar se já existe
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM tecnicas WHERE nome LIKE '%emulsif%';"

# 2. Obter próximo ID de TEC (identificadores-v1.md)
# Suponha: TEC-000003 → próximo TEC-000004

# 3. Criar a partir do template
cp docs/01-dominio/templates/tecnica-v1.md \
   dados/tecnicas/TEC-000004-emulsificacao-v1.md

# 4. Editar
nano dados/tecnicas/TEC-000004-emulsificacao-v1.md
```

Frontmatter:
```yaml
---
id: TEC-000004
tipo: tecnica
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
tags: [mecanica, textura, mistura]
---
```

Conteúdo:
```markdown
# Emulsificação

## Informações
- **Tipo:** Mecânica — criação de emulsão estável
- **Dificuldade:** média

## Descrição
Processo de dispersão de duas substâncias imiscíveis (ex: gordura e água)
em uma mistura estável, geralmente com auxílio de um emulsificante.

## Aplicações
Maionese, hollandaise, vinagrete emulsificado, molhos de sobremesa.

## Pontos Críticos
- Temperatura: as substâncias devem estar em temperatura adequada
- Emulsificante: gema de ovo (lecitina) é o emulsificante mais comum
- Velocidade: adição lenta do óleo garante emulsão estável
```

```bash
# 5. Importar
scripts/importacao/importar.sh dados/tecnicas/TEC-000004-emulsificacao-v1.md

# 6. Atualizar identificadores-v1.md e commitar
git commit -am "feat(tec): cria TEC-000004 emulsificacao"
```

---

## Verificação final

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome, status FROM tecnicas WHERE id = 'TEC-000004';"
```

```
# Resultado esperado:
TEC-000004|Emulsificação|ativo
```

---

## Problemas comuns neste fluxo

| Problema | Causa | Solução |
|----------|-------|---------|
| `status inválido` ao importar | Status com valor incorreto para TEC | Status válidos: `ativo`, `arquivado` |
| TEC duplicada detectada pelo FAA | Conceito similar já existe com outro ID | Arquivar a nova TEC e usar o ID já existente |

---

## Próxima leitura

- Criar uma receita que usa esta técnica → [`01-criar-receita-v1.md`](01-criar-receita-v1.md)
- Versão rápida (TEC e EQP juntos) → [`../10-cookbook/03-criar-tecnica-equipamento-v1.md`](../10-cookbook/03-criar-tecnica-equipamento-v1.md)
