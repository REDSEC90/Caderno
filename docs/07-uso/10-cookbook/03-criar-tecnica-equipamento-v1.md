# Cookbook — Criar uma Técnica (TEC) ou Equipamento (EQP)

> Exemplos copiáveis para registrar técnicas culinárias e equipamentos.

---

## Criar uma Técnica (TEC)

**O que é uma Técnica:** um método culinário reutilizável — algo que pode ser aplicado em múltiplas receitas. Documente o método, não a aplicação específica.

### Passo 1 — Verificar que não existe

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM tecnicas WHERE nome LIKE '%escald%';"
```

### Passo 2 — Obter o próximo ID

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM tecnicas ORDER BY id DESC LIMIT 1;"
```

### Passo 3 — Criar o arquivo

```bash
cp docs/01-dominio/templates/tecnica-v1.md \
   dados/tecnicas/TEC-000004-escaldamento-v1.md
```

### Passo 4 — Editar

```markdown
---
id: TEC-000004
tipo: tecnica
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: [seu-nome]
tags: [amido, temperatura, basico]
---

# Escaldamento

## Descrição
Técnica de adicionar líquido fervendo sobre farinha ou amido, gelatinizando parcialmente
o amido e alterando a textura e absorção da massa resultante.

## Quando usar
Preparos que exigem massa com elasticidade e leveza, como pão de queijo e coxinha.

## Como executar
1. Ferver o líquido (água, leite ou mistura) com gorduras e sal.
2. Jogar o líquido fervendo sobre o amido ou farinha de uma só vez.
3. Misturar vigorosamente enquanto ainda quente.
4. Aguardar amornar antes de adicionar ovos ou outros ingredientes sensíveis ao calor.

## Pontos críticos
- O líquido deve estar fervendo no momento de jogar — não morno.
- A mistura imediata é essencial para gelatinização uniforme.
- Temperatura ao adicionar ovos: menos de 50°C (não pode cozer os ovos).

## Receitas que usam esta técnica
- Pão de queijo (qualquer variação)
- Coxinha de frango
- Massa choux (variação)
```

### Passo 5 — Importar e verificar

```bash
scripts/importacao/importar.sh dados/tecnicas/TEC-000004-escaldamento-v1.md

sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM tecnicas WHERE id = 'TEC-000004';"
```

```
# Resultado esperado:
TEC-000004|Escaldamento
```

### Passo 6 — Commitar

```bash
git add dados/tecnicas/TEC-000004-escaldamento-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(tec): adiciona TEC-000004 escaldamento"
```

---

## Criar um Equipamento (EQP)

**O que é um Equipamento:** qualquer utensílio, aparelho ou instrumento usado nos preparos. Documente características relevantes para o resultado (material, tamanho, capacidade).

### Passo 1 — Verificar que não existe

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM equipamentos WHERE nome LIKE '%forma%';"
```

### Passo 2 — Obter o próximo ID

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM equipamentos ORDER BY id DESC LIMIT 1;"
```

### Passo 3 — Criar o arquivo

```bash
cp docs/01-dominio/templates/equipamento-v1.md \
   dados/equipamentos/EQP-000003-forma-antiaderente-v1.md
```

### Passo 4 — Editar

```markdown
---
id: EQP-000003
tipo: equipamento
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: [seu-nome]
tags: [forno, antiaderente, panificacao]
---

# Forma Antiaderente

## Informações
- **Tipo:** Utensílio de forno
- **Material:** Alumínio com revestimento antiaderente
- **Capacidade:** 30–40 unidades médias (pão de queijo)

## Descrição
Forma com revestimento antiaderente para assar bolinhas de massa.
O antiaderente elimina a necessidade de untar, e a distribuição uniforme
de calor do alumínio garante cozimento homogêneo.

## Quando usar
Qualquer preparo que vai ao forno em formato de bolinhas ou unidades individuais.

## Cuidados
- Não usar esponjas abrasivas — danificam o revestimento.
- Temperatura máxima: verificar especificação do fabricante (geralmente 220°C).
```

### Passo 5 — Importar e commitar

```bash
scripts/importacao/importar.sh dados/equipamentos/EQP-000003-forma-antiaderente-v1.md

git add dados/equipamentos/EQP-000003-forma-antiaderente-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(eqp): adiciona EQP-000003 forma-antiaderente"
```

---

## Quando criar TEC vs. quando descrever na REC

| Situação | Ação |
|----------|------|
| Método genérico aplicável em várias receitas | Criar TEC — reutilizável |
| Detalhe específico de uma receita | Descrever no corpo da REC |
| Técnica com nome estabelecido na culinária | Criar TEC mesmo que use em uma receita por enquanto |
| Sequência de passos muito específica de uma receita | Manter na REC |

**Boas TECs:** Escaldamento, Emulsificação, Caramelização, Redução, Confit, Branqueamento  
**Não crie TEC para:** "misturar", "picar", "aquecer" — são genéricos demais para ter valor como entidade.
