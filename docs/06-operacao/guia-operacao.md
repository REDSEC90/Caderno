# Guia de Operação — SOE-CCG

> Procedimentos de backup, manutenção, monitoramento e recuperação do sistema.

---

## 1. Princípio Operacional

O SOE-CCG tem duas camadas independentes:

| Camada | Localização | Natureza | Perda aceitável? |
|--------|-------------|----------|-----------------|
| Conhecimento | `dados/` (Markdown + git) | Permanente | **Nunca** |
| Índice | `banco_de_dados/sqlite/` | Derivado | Sim — reconstruível |

**Toda operação de backup prioriza `dados/`.** O banco SQLite pode ser perdido e reconstruído a qualquer momento.

---

## 2. Backup

### 2.1 Backup do Conhecimento (git)

O repositório git é o backup primário dos arquivos Markdown. Todo commit é um snapshot do estado do conhecimento.

**Operação manual:**
```bash
cd /path/to/SOE-CCG
git add dados/
git commit -m "backup: snapshot $(date +%Y-%m-%d)"
git push origin main
```

**Recomendação:** pelo menos 1 commit por sessão de trabalho.

### 2.2 Backup do Banco SQLite

O banco SQLite é derivado e pode ser reconstruído. Backup opcional mas recomendado para conveniência:

```bash
# Backup do banco
cp banco_de_dados/sqlite/soe-ccg.db \
   banco_de_dados/sqlite/backups/soe-ccg-$(date +%Y%m%d).db
```

**O banco não deve ser commitado no git** — apenas os arquivos Markdown.

### 2.3 Backup Externo

Recomendado: sincronizar `dados/` com serviço de armazenamento externo (nuvem, HD externo):

```bash
# Exemplo com rsync
rsync -avz dados/ /mnt/backup-externo/SOE-CCG/dados/
rsync -avz docs/  /mnt/backup-externo/SOE-CCG/docs/
```

---

## 3. Reconstrução do Banco

Se o banco SQLite for corrompido ou perdido, reconstruir a partir dos arquivos Markdown:

```bash
# 1. Remover banco corrompido
rm banco_de_dados/sqlite/soe-ccg.db

# 2. Recriar esquema
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

# 3. Importar todos os dados
scripts/importacao/importar-todos.sh
```

**Garantia:** nenhuma informação é perdida porque o Markdown é a fonte de verdade.

---

## 4. Manutenção

### 4.1 Verificação de Integridade

Executar periodicamente para garantir consistência entre Markdown e SQLite:

```bash
scripts/manutencao/verificar-integridade.sh
```

Verifica:
- Todo Markdown em `dados/` tem entrada correspondente no SQLite
- Todo ID no SQLite tem arquivo Markdown correspondente
- Nenhum ID está duplicado
- Todos os IDs referenciados existem

### 4.2 Atualização do Controle de IDs

Após criar novos registros, atualizar a tabela de controle de sequência:

```
docs/04-padroes/identificadores.md → tabela "Controle de Sequência"
```

### 4.3 Limpeza de Importação

Arquivos processados em `dados/importacao/` devem ser movidos para destino final ou arquivados:

```bash
# Após processamento bem-sucedido
mv dados/importacao/arquivo-processado.md dados/[entidade]/[ID]-[slug]-v1.md
```

---

## 5. Resolução de Conflitos Markdown vs SQLite

Se houver divergência entre um arquivo Markdown e o SQLite:

**O Markdown prevalece sempre.**

Processo de resolução:
```bash
# 1. Identificar o arquivo em conflito
grep -r "[ID]" dados/

# 2. Verificar estado no SQLite
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT * FROM [tabela] WHERE id = '[ID]';"

# 3. Re-importar o arquivo Markdown
scripts/importacao/importar.sh dados/[entidade]/[arquivo].md

# 4. Verificar resolução
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT * FROM [tabela] WHERE id = '[ID]';"
```

---

## 6. Recuperação de Versões Anteriores

Para recuperar uma versão anterior de um Registro:

```bash
# Ver histórico do arquivo
git log --oneline dados/receitas/REC-000001-*.md

# Ver conteúdo de versão específica
git show [COMMIT-HASH]:dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Restaurar versão anterior (cria novo commit)
git checkout [COMMIT-HASH] -- dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
git commit -m "restore: REC-000001 versão anterior de [data]"
```

---

## 7. Monitoramento

### 7.1 Estatísticas do Sistema

```sql
-- Contagem por entidade
SELECT 'receitas' as entidade, COUNT(*) as total FROM receitas
UNION ALL SELECT 'ingredientes', COUNT(*) FROM ingredientes
UNION ALL SELECT 'tecnicas', COUNT(*) FROM tecnicas
UNION ALL SELECT 'equipamentos', COUNT(*) FROM equipamentos
UNION ALL SELECT 'execucoes', COUNT(*) FROM execucoes
UNION ALL SELECT 'observacoes', COUNT(*) FROM observacoes
UNION ALL SELECT 'experimentos', COUNT(*) FROM experimentos;

-- Receitas por status
SELECT status, COUNT(*) FROM receitas GROUP BY status;

-- Últimas execuções
SELECT r.titulo, e.data_execucao, e.avaliacao_geral
FROM execucoes e
JOIN receitas r ON r.id = e.receita_id
ORDER BY e.data_execucao DESC LIMIT 10;
```

### 7.2 Saúde do Sistema

Indicadores de saúde a verificar periodicamente:

- [ ] Número de registros sem `atualizado-em` atual (esquecimentos)
- [ ] IDs referenciados que não existem no sistema
- [ ] Receitas em `rascunho` por mais de 30 dias
- [ ] Experimentos `abertos` por mais de 90 dias sem atualização
- [ ] Diferença entre contagem Markdown e SQLite (sinal de dessincronização)

---

## 8. Procedimento de Emergência

Em caso de perda total do sistema:

```
1. Clonar repositório git (se houver remoto)
   git clone [URL] SOE-CCG

2. Reconstruir banco SQLite (Seção 3)

3. Verificar integridade (Seção 4.1)

4. Se repositório perdido mas backup externo existir:
   rsync -avz /mnt/backup-externo/SOE-CCG/ ./SOE-CCG/
   git init && git add . && git commit -m "restore: recuperação de backup"
```

**O conhecimento é recuperável enquanto os arquivos Markdown existirem.**

---

## 9. Checklist de Manutenção Semanal

- [ ] Commitar todos os arquivos novos ou alterados
- [ ] Atualizar controle de IDs em `identificadores.md`
- [ ] Verificar Experimentos `abertos` e atualizar status se concluídos
- [ ] Verificar Execuções `registradas` e completar campos faltantes
- [ ] Sincronizar backup externo
