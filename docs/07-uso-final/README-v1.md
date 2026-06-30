# Manual Operacional — SOE-CCG
### Sistema de Organização e Evolução de Conhecimento Culinário Gastronômico

---

> **Este não é um documento de arquitetura.**
> É o manual de execução do sistema em produção cognitiva.
> Aqui não se descreve como o sistema foi projetado — aqui se diz exatamente o que fazer, em que ordem, por quê e como validar.

---

## Começa aqui

**Nunca usou o SOE?**
→ [`01-introducao/02-primeiros-passos-v1.md`](01-introducao/02-primeiros-passos-v1.md) — do zero ao primeiro registro em 15 minutos.

**Quer entender o sistema antes de usar?**
→ [`01-introducao/01-o-que-e-o-soe-v1.md`](01-introducao/01-o-que-e-o-soe-v1.md) — o que é, o que armazena, como funciona.

**Quer criar algo agora?**
→ [`10-cookbook/`](10-cookbook/) — exemplos copiáveis por tipo de entidade.

**Algo deu errado?**
→ [`09-troubleshooting/`](09-troubleshooting/) — diagnóstico por componente.

**Precisa de um comando rápido?**
→ [`07-referencia/cheat-sheet-v1.md`](07-referencia/cheat-sheet-v1.md) — consulta em 10 segundos.

---

## Estrutura do manual

```
01-introducao/      O que é, primeiros passos, mentalidade, glossário.
                    Leia uma vez antes de começar a usar.

02-operacao/        Ciclo de vida, criar, editar, remover, versionar.
                    O coração do manual.

03-validacao/       Pipeline completo: Parser → Resolver → Validador → FAA → Importador.
                    Cada componente com função, entrada, saída e erros.

04-consultas/       Como acessar o conhecimento: Markdown, SQLite, grafo.
                    Queries prontas. Navegação entre entidades.

05-fluxos/          Tutoriais end-to-end por tipo de tarefa.          ← seção mais usada
                    Cada fluxo: criar → validar → importar → verificar → commitar.

06-contribuicao/    Padrões, regras, ADRs, checklist seguro.

07-referencia/      Tabelas de entidades, relacionamentos, estados, comandos.  ← consulta rápida

08-agentes/         Protocolo para agentes automatizados e sistemas de IA.

09-troubleshooting/ Diagnóstico por componente: Parser, Resolver, FAA, SQLite.

10-cookbook/        Exemplos copiáveis prontos para uso.
```

---

## Rotas de leitura por perfil

### Primeira vez no sistema
```
01-introducao/01-o-que-e-o-soe-v1.md        ← o que é (10 min)
→ 01-introducao/02-primeiros-passos-v1.md   ← ver funcionando (15 min)
→ 01-introducao/03-como-pensar-no-soe-v1.md ← mudar a mentalidade (10 min)
→ 05-fluxos/07-fluxo-completo-v1.md         ← sessão real de trabalho (20 min)
→ 07-referencia/cheat-sheet-v1.md           ← manter aberto durante o trabalho
```

### Sessão de trabalho regular
```
07-referencia/cheat-sheet-v1.md
→ 10-cookbook/[tipo de entidade que vai criar]
→ 03-validacao/05-faa-v1.md   (ao final da sessão)
```

### Algo deu errado
```
09-troubleshooting/[componente que falhou]
→ 03-validacao/07-resolucao-de-erros-v1.md
→ 08-exemplos-reais-v1.md (ver o fluxo correto)
```

### Desenvolvedor / mantenedor
```
03-validacao/01-pipeline-completo-v1.md
→ 03-validacao/02-parser-v1.md ... 06-importador-v1.md
→ 06-contribuicao/
```

### Agente automatizado
```
08-agentes/01-protocolo-operacional-v1.md
→ 08-agentes/02-invariantes-v1.md
→ 07-referencia/comandos-v1.md
→ 07-referencia/cheat-sheet-v1.md
```

---

## Definição de "uso correto"

O sistema está sendo usado corretamente quando:

1. Todo conhecimento novo entra pelo sistema de arquivos (`dados/`) em formato Markdown.
2. Toda referência entre entidades usa identificadores canônicos (`ING-000001`, não `"Leite Integral"`).
3. O banco SQLite é sempre reconstruído a partir do Markdown — nunca editado diretamente.
4. O FAA é executado ao final de cada sessão de trabalho.
5. Todo estado novo é preservado em um commit git com mensagem descritiva.

Qualquer desvio dessas cinco regras quebra invariantes do sistema.

---

## Convenções deste manual

- Blocos `bash` são executáveis a partir da **raiz do repositório**
- `REC-000001`, `ING-000004` são identificadores de exemplos **reais** do sistema
- ⚠️ indica aviso operacional — algo que causa problemas sérios se ignorado
- ✅ indica verificação — como confirmar que um passo funcionou
- `CRÍTICO` indica regra inviolável — violação quebra invariantes do sistema
- Blocos `# Resultado esperado:` mostram o output correto de cada comando
