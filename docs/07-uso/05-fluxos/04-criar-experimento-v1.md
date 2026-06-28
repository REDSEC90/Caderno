# Fluxo: Criar um Experimento

> Tutorial para registrar e conduzir uma investigação deliberada.

**Objetivo:** Testar se aumentar a proporção de açúcar melhora o sabor do doce de leite.

---

## Quando criar um Experimento

Quando você tem uma **hipótese** — algo que quer testar deliberadamente. Não é apenas um preparo alternativo (isso seria uma Execução com desvio). É uma investigação com objetivo definido, variáveis e critério de conclusão.

---

## Passo 1 — Criar o arquivo

```bash
# Próximo EXP: consultar identificadores-v1.md
cp docs/01-dominio/templates/experimento-v1.md \
   dados/experimentos/EXP-000001-proporcao-acucar-doce-leite-v1.md
```

Frontmatter:
```yaml
---
id: EXP-000001
tipo: experimento
schema-version: 1
versao: 1
status: aberto
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
receita-base-id: REC-000001
tags: [doce-de-leite, acucar, sabor]
---
```

Conteúdo:
```markdown
# Experimento: Proporção de Açúcar no Doce de Leite

## Hipótese
Aumentar a proporção de açúcar de 250g para 300g por litro de leite
produz sabor mais intenso sem comprometer textura.

## Variáveis
- **Variável testada:** quantidade de açúcar (250g → 300g)
- **Variáveis mantidas:** leite, bicarbonato, sal, temperatura, tempo

## Receita Base
REC-000001 — Doce de Leite Artesanal

## Critério de Sucesso
Avaliação de sabor ≥ 8/10 com textura ≥ 7/10
```

```bash
scripts/importacao/importar.sh dados/experimentos/EXP-000001-proporcao-acucar-doce-leite-v1.md
git commit -am "feat(exp): abre EXP-000001 hipotese proporcao acucar doce-leite"
```

---

## Durante o Experimento

Cada preparo de teste é uma **Execução** que referencia a Receita base (não o Experimento diretamente). Documente os desvios na EXE.

---

## Concluindo o Experimento

Após realizar os preparos de teste:

```bash
nano dados/experimentos/EXP-000001-proporcao-acucar-doce-leite-v1.md
```

Adicionar ao conteúdo:
```markdown
## Resultado
EXE-000002 com 300g de açúcar: sabor 9/10, textura 8/10.
Hipótese confirmada.

## Conclusão
300g de açúcar por litro de leite produz sabor mais intenso e mantém textura adequada.

## Incorporado em
REC-000001-v2 (atualizar proporção na nova versão)
```

Alterar no frontmatter:
```yaml
status: concluido
atualizado-em: 2026-06-27
```

```bash
scripts/importacao/importar.sh dados/experimentos/EXP-000001-proporcao-acucar-doce-leite-v1.md
git commit -am "feat(exp): conclui EXP-000001 hipotese confirmada"
```

Se o resultado vai gerar uma nova versão da receita:
```yaml
status: incorporado
```
