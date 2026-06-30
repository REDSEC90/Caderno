# Boas Práticas

> O que sempre fazer e o que nunca fazer. Consulta rápida.

---

## Nunca

| Proibido | Por quê |
|----------|---------|
| ✗ Deletar arquivos de `dados/` | Destrói o registro histórico. Arquivar em vez disso. |
| ✗ Alterar o campo `id` de uma entidade | Quebra todas as referências existentes. |
| ✗ Reutilizar um ID (mesmo de entidade arquivada) | Contamina referências históricas. |
| ✗ Editar o banco SQLite diretamente | O banco é derivado. Mudanças diretas serão sobrescritas na próxima importação. |
| ✗ Referenciar entidades por nome em vez de ID | Nomes mudam. IDs não. |
| ✗ Commitar o arquivo `soe-ccg.db` | O banco é derivado e reconstruível. |
| ✗ Criar duplicatas de conceitos existentes | Divide o grafo e torna consultas inconsistentes. |
| ✗ Pular a etapa de verificação de existência antes de criar | A causa mais comum de duplicatas. |
| ✗ Criar uma Receita sem verificar se os ingredientes existem | Causa referências quebradas no Resolver. |

---

## Sempre

| Prática | Por quê |
|---------|---------|
| ✅ Verificar duplicatas antes de criar | Grafo limpo, consultas confiáveis. |
| ✅ Atualizar `atualizado-em` a cada edição | Rastreabilidade temporal. |
| ✅ Atualizar a tabela de controle de IDs imediatamente | Evita conflitos se outra pessoa criar ao mesmo tempo. |
| ✅ Executar o Parser antes de importar | Detecta erros cedo. |
| ✅ Rodar o FAA ao final de cada sessão | Garante saúde sistêmica. |
| ✅ Fazer commit de cada sessão | Snapshot do conhecimento. |
| ✅ Usar mensagens de commit descritivas | O `git log` é o diário do sistema. |
| ✅ Criar dependências antes de referenciar | ING e TEC antes da REC que os usa. |
| ✅ Registrar Execuções de cada preparo | Conhecimento prático vale tanto quanto a Receita. |
| ✅ Criar OBS para descobertas relevantes | Observações são o vetor de aprendizado do sistema. |

---

## Granularidade Recomendada

**Ingredientes:** prefira granularidade fina.
- `manteiga-sem-sal` e `manteiga-com-sal` são entidades distintas.
- `leite-integral` e `leite-semidesnatado` são entidades distintas.
- Não crie `laticinio-generico` — perde poder de consulta.

**Técnicas:** documente o método, não a aplicação.
- TEC descreve "como" de forma geral. A REC descreve "como" nesse contexto específico.
- Uma boa TEC é reutilizável em múltiplas REC.

**Execuções:** registre mesmo execuções imperfeitas.
- Uma EXE com avaliação 4/10 e desvios documentados tem mais valor que uma EXE não registrada.
- O campo `desvios` é onde fica o aprendizado real.

**Observações:** capture insights imediatamente.
- O momento mais produtivo para criar uma OBS é durante ou logo após um preparo.
- Insights não registrados são perdidos.

---

## Checklist de Saída de Sessão

Ao finalizar qualquer sessão de trabalho:

```
[ ] Todos os novos arquivos estão em dados/
[ ] Frontmatters preenchidos e válidos (nenhum campo YYYY-MM-DD literal)
[ ] Controle de IDs (identificadores-v1.md) atualizado
[ ] Parser executado sem erros em todos os novos arquivos
[ ] Importador rodou com sucesso
[ ] Auditoria FAA: sem novas falhas críticas
[ ] git status limpo (ou commit feito)
[ ] git push realizado (se trabalhando com remoto)
```

---

## Próxima leitura

- Consultar referência rápida → [`../07-referencia/cheat-sheet-v1.md`](../07-referencia/cheat-sheet-v1.md)
- Regras para contribuidores → [`../06-contribuicao/02-regras-v1.md`](../06-contribuicao/02-regras-v1.md)
