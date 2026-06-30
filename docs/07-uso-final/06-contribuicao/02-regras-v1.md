# Regras de Contribuição

> O que é permitido, o que é proibido e por quê.

---

## Regras Invioláveis (CRÍTICO)

Violar qualquer uma destas regras quebra invariantes do sistema:

| Regra | Razão |
|-------|-------|
| Nunca editar o SQLite diretamente | O banco é derivado. Edições são sobrescritas na próxima importação |
| Nunca reutilizar um ID | Contamina referências históricas. IDs de entidades arquivadas são eternamente reservados |
| Nunca alterar o campo `id` de uma entidade existente | Quebra todas as arestas que apontam para esse ID |
| Nunca deletar arquivos de `dados/` | Arquivar (`status: arquivado`) em vez de deletar |
| Nunca referenciar entidades por nome em campos de relacionamento | Nomes mudam. IDs não |
| Nunca commitar `soe-ccg.db` | O banco é derivado e reconstruível a qualquer momento |
| Nunca criar entidade sem verificar se já existe | Duplicatas corrompem o grafo |

---

## Regras de Processo

| Regra | Contexto |
|-------|---------|
| Verificar existência antes de criar | Obrigatório para ING, TEC, EQP |
| Criar dependências antes de referenciar | ING/TEC/EQP antes da REC que os usa |
| Rodar FAA ao final de cada sessão | Detecta problemas antes do commit |
| Atualizar `identificadores-v1.md` imediatamente | Evita conflitos de ID em trabalho paralelo |
| Atualizar `atualizado-em` a cada edição | Rastreabilidade temporal |
| Reimportar após qualquer edição de Markdown | SQLite deve refletir estado atual |

---

## O que Requer Revisão por Pares

Mudanças que afetam todo o sistema requerem revisão antes de serem mergeadas:

- Alterações no esquema SQLite (`banco_de_dados/esquemas/schema-sqlite-v1.sql`)
- Alterações no Parser, Resolver ou Validador (`codigo/`)
- Criação de novos motores de auditoria FAA
- Alterações em políticas em `docs/04-padroes/`
- Qualquer ADR nova

Mudanças que podem ser feitas diretamente:
- Criar/editar entidades em `dados/`
- Criar/editar documentação em `docs/07-uso/`
- Criar novas tags (com adição ao catálogo)
