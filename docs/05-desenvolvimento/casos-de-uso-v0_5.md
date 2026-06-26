# Casos de Uso — SOE-CCG

> Documentação de todos os fluxos do usuário. Fase 11 do roadmap de maturidade.

---

## UC-001: Usuário Registra Nova Receita

**Ator:** Autor
**Pré-condição:** Autor tem acesso ao sistema e conhece a receita a registrar.
**Pós-condição:** Receita existe em `dados/receitas/` e no SQLite.

**Fluxo principal:**

1. Autor consulta `docs/04-padroes/identificadores.md` para obter o próximo `REC-NNNNNN`.
2. Autor copia `docs/01-dominio/templates/receita-v1.md` para `dados/receitas/REC-NNNNNN-[slug]-v1.md`.
3. Autor preenche o frontmatter: `id`, `titulo`, `status: rascunho`, datas, autor.
4. Autor verifica se cada Ingrediente já existe em `dados/ingredientes/`. Se não: cria registro de Ingrediente (UC-002) antes de continuar.
5. Autor preenche a tabela de Ingredientes com IDs referenciados + quantidades.
6. Autor repete para Técnicas e Equipamentos (UC-003, UC-004).
7. Autor escreve o `modo-de-preparo`.
8. Autor salva o arquivo.
9. Autor executa importador: `scripts/importacao/importar.sh [arquivo]`
10. Importador valida o esquema e insere no SQLite.
11. Autor atualiza tabela de sequência em `identificadores.md`.

**Fluxo alternativo — Ingrediente inexistente:**
- No passo 4, autor detecta que o Ingrediente não existe.
- Autor executa UC-002 para criar o Ingrediente.
- Retorna ao passo 5 com o novo ID.

**Pós-condição de falha:**
- Se importador rejeitar, o arquivo Markdown permanece como rascunho.
- Autor corrige os erros indicados e re-executa o importador.

---

## UC-002: Usuário Registra Ingrediente

**Ator:** Autor
**Pré-condição:** Nenhum Ingrediente com o mesmo conceito existe no sistema.

**Fluxo principal:**

1. Autor verifica em `dados/ingredientes/` se o Ingrediente já existe (evitar duplicatas).
2. Autor obtém próximo `ING-NNNNNN`.
3. Autor copia `docs/01-dominio/templates/ingrediente-v1.md`.
4. Autor preenche: `id`, `nome`, `tipo-ingrediente` (do catálogo), campos relevantes.
5. Autor salva em `dados/ingredientes/ING-NNNNNN-[slug]-v1.md`.
6. Autor executa importador.
7. Autor atualiza controle de IDs.

---

## UC-003: Usuário Registra Execução de Receita

**Ator:** Autor
**Pré-condição:** A Receita referenciada existe no sistema (`status: rascunho` ou superior).

**Fluxo principal:**

1. Autor obtém próximo `EXE-NNNNNN`.
2. Autor copia `docs/01-dominio/templates/execucao-v1.md`.
3. Autor preenche: `id`, `receita-id` (ID da Receita executada), `data-execucao`.
4. Autor registra ingredientes realmente utilizados (podem diferir da Receita).
5. Autor registra métricas observadas (tempo, peso final, temperaturas).
6. Autor registra avaliações: sabor, textura, aparência, geral.
7. Autor documenta desvios em relação à Receita (se houver).
8. Autor salva em `dados/execucoes/EXE-NNNNNN-[slug-receita]-execucao-N.md`.
9. Autor executa importador.
10. Sistema atualiza status da Receita de `rascunho` para `testada` (se for primeira execução).

**Fluxo alternativo — Registro posterior ao preparo:**
- Autor pode registrar a Execução horas ou dias após o preparo.
- `data-execucao` deve refletir quando o preparo ocorreu, não quando foi registrado.

---

## UC-004: Usuário Registra Observação

**Ator:** Autor
**Pré-condição:** Autor tem uma percepção ou aprendizado a registrar.

**Fluxo principal:**

1. Autor obtém próximo `OBS-NNNNNN`.
2. Autor copia `docs/01-dominio/templates/observacao-v1.md`.
3. Autor escreve o `conteudo` da observação em linguagem clara.
4. Autor referencia a entidade relacionada (se aplicável): `entidade-referenciada`, `tipo-entidade`.
5. Autor define `relevancia` (baixa, media, alta).
6. Autor salva em `dados/observacoes/OBS-NNNNNN-[slug-descritivo].md`.
7. Autor executa importador.

---

## UC-005: Usuário Consulta Técnica

**Ator:** Qualquer usuário
**Pré-condição:** Sistema disponível.

**Fluxo principal (via SQLite/CLI):**

```sql
-- Listar todas as técnicas ativas
SELECT id, nome, tipo_tecnica, dificuldade FROM tecnicas
WHERE status = 'ativo' ORDER BY nome;

-- Buscar técnica por nome
SELECT * FROM tecnicas WHERE nome LIKE '%fermentac%';

-- Ver receitas que usam determinada técnica
SELECT r.titulo, r.status
FROM receitas r
JOIN receita_tecnica rt ON rt.receita_id = r.id
WHERE rt.tecnica_id = 'TEC-000001';
```

**Fluxo alternativo (via Markdown direto):**
1. Navegar até `dados/tecnicas/`.
2. Abrir arquivo da técnica desejada.
3. Ler descrição, aplicações e notas.

---

## UC-006: Usuário Compara Versões de uma Receita

**Ator:** Autor / Qualquer usuário
**Pré-condição:** Receita possui mais de uma versão registrada.

**Fluxo principal:**

```bash
# Ver histórico de versões da Receita
git log --oneline dados/receitas/REC-000001-*.md

# Comparar versão atual com versão anterior
git diff [COMMIT-HASH-v1] dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Ver conteúdo de versão específica
git show [COMMIT-HASH]:dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

**Ou via arquivos múltiplos (quando versionamento formal criou v2):**
```bash
diff dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md \
     dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md
```

---

## UC-007: Usuário Importa Documento Externo

**Ator:** Autor
**Pré-condição:** Documento externo (texto, foto, receita de livro) a ser incorporado.

**Fluxo principal:**

1. Autor salva o documento original em `dados/importacao/[nome-original]`.
2. Autor cria um novo Registro apropriado (Receita, Técnica etc.) com base no conteúdo.
3. Autor preenche o campo `origem` com referência ao documento original.
4. Autor registra as entidades mencionadas no documento (Ingredientes, Técnicas).
5. Autor move o documento original para `dados/anexos/[ID-do-registro]/`.
6. Autor importa o Registro para o SQLite.

**Nota:** documentos importados nunca substituem o Registro estruturado — são complementos.

---

## UC-008: Usuário Exporta Catálogo

**Ator:** Autor
**Pré-condição:** SQLite atualizado.

**Fluxo principal:**

```bash
# Exportar todas as receitas ativas em CSV
sqlite3 -csv -header banco_de_dados/sqlite/soe-ccg.db \
  "SELECT * FROM vw_receitas_ativas;" > exports/receitas-$(date +%Y%m%d).csv

# Exportar ingredientes mais usados
sqlite3 -csv -header banco_de_dados/sqlite/soe-ccg.db \
  "SELECT * FROM vw_ingredientes_uso ORDER BY total_receitas DESC;" \
  > exports/ingredientes-uso-$(date +%Y%m%d).csv
```

---

## UC-009: Usuário Abre Experimento

**Ator:** Autor
**Pré-condição:** Autor tem hipótese a testar.

**Fluxo principal:**

1. Autor obtém próximo `EXP-NNNNNN`.
2. Autor copia `docs/01-dominio/templates/experimento-v1.md`.
3. Autor preenche: `titulo`, `hipotese`.
4. Autor referencia a Receita base (se existir): `receita-base-id`.
5. Autor define as `variaveis` a serem testadas.
6. Autor salva em `dados/experimentos/EXP-NNNNNN-[slug].md` com `status: aberto`.
7. Autor importa o Registro.

**Fluxo de conclusão (após realização):**
1. Autor edita o arquivo, preenche `resultado` e `conclusao`.
2. Autor muda `status` para `concluido`.
3. Se bem-sucedido: cria Receita nova (UC-001), referencia em `incorporado-em`.
4. Muda `status` para `incorporado`.
5. Se descartado: muda `status` para `descartado` (conclusão permanece).
6. Autor re-importa o Registro.

---

## UC-010: Usuário Arquiva Registro

**Ator:** Autor / Mantenedor
**Pré-condição:** Registro existe e há motivo para arquivamento.

**Fluxo principal:**

1. Autor abre o arquivo Markdown do Registro.
2. Autor muda `status` para `arquivado`.
3. Autor adiciona metadados de arquivamento:
   ```yaml
   data-arquivamento: 2026-06-26
   arquivado-por: nome-do-autor
   motivo-arquivamento: "Substituído por versão v2"
   ```
4. Autor salva e re-importa.
5. Sistema remove o Registro das consultas padrão.
6. Registro permanece acessível via consulta explícita.

**Verificação:** `git log` preserva todo o histórico mesmo após arquivamento.
