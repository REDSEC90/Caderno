# Manual Operacional — SOE-CCG
### Sistema de Organização e Evolução de Conhecimento Culinário Gastronômico

---

> **Este não é um documento de arquitetura.**
> É o manual de execução do sistema em produção cognitiva.
> Aqui não se descreve como o sistema foi projetado — aqui se diz exatamente o que fazer, em que ordem, por quê e como validar.

---

## Propósito

Este manual é a **fonte única de verdade operacional** do SOE-CCG.

Qualquer pessoa — ou agente automatizado — que precise interagir com o sistema deve conseguir fazê-lo lendo apenas este manual. Sem precisar ler código. Sem precisar ler documentação de arquitetura. Sem ambiguidade entre conceito e ação.

---

## Definição de "Uso Correto do SOE"

O sistema está sendo usado corretamente quando:

1. Todo conhecimento novo entra pelo sistema de arquivos (`dados/`) em formato Markdown.
2. Toda referência entre entidades usa identificadores canônicos (`ING-000001`, não `"Leite Integral"`).
3. O banco SQLite é sempre reconstruído a partir do Markdown — nunca editado diretamente.
4. O FAA é executado ao final de cada sessão de trabalho.
5. Todo estado novo é preservado em um commit git com mensagem descritiva.

Qualquer desvio dessas cinco regras quebra invariantes do sistema.

---

## Público-Alvo

### Usuário Operacional
Registra receitas, ingredientes, técnicas, execuções, observações e experimentos.
**Leitura:** `01-introducao/` → `05-fluxos/` → `07-referencia/cheat-sheet.md`

### Desenvolvedor
Mantém scripts, schemas, motores de validação, FAA, pipeline de importação.
**Leitura:** `01-introducao/` → `03-validacao/` → `06-contribuicao/`

### Mantenedor do Sistema
Audita saúde, evolui padrões, resolve conflitos arquiteturais, escreve ADRs.
**Leitura:** `02-operacao/` → `03-validacao/05-faa.md` → `06-contribuicao/`

### Agente Automatizado
Opera sobre o repositório de forma autônoma.
**Leitura:** `07-referencia/comandos.md` → `07-referencia/cheat-sheet.md` → `03-validacao/01-pipeline-completo.md`

---

## Estrutura do Manual

```
01-introducao/
│   O que é o sistema, como pensar nele, glossário completo.
│   Leia uma vez. Mude a mentalidade. Continue.
│
02-operacao/
│   Ciclo de vida do conhecimento. Criar, editar, remover, versionar.
│   O coração do manual. Contém pré-condições, execução, validação e impacto no grafo.
│
03-validacao/
│   O pipeline formal: Parser → Resolver → Validador → FAA → Importador.
│   Cada componente documentado com função, entrada, saída e erros.
│
04-consultas/
│   Como acessar o conhecimento: Markdown direto, SQLite, grafo.
│   Queries prontas. Navegação em relacionamentos indiretos.
│
05-fluxos/        ← A seção mais usada
│   Tutoriais completos end-to-end por tarefa.
│   Cada fluxo: decisão → criação → validação FAA → importação → consulta final.
│
06-contribuicao/
│   Governança. Quando escrever ADR. Quando modificar schema. Checklist seguro.
│
07-referencia/    ← Consulta em 10 segundos
│   Tabelas de entidades, relacionamentos, estados, comandos, cheat-sheet.
│
08-exemplos-reais.md
    Casos completos do mundo real, do zero à validação FAA.
    O melhor recurso para entender o sistema funcionando.
```

---

## Ordem de Leitura Recomendada

**Primeira vez no sistema:**
```
01-introducao/01-o-que-e-o-soe.md
→ 01-introducao/03-como-pensar-no-soe.md
→ 01-introducao/02-primeiros-passos.md
→ 05-fluxos/07-fluxo-completo.md
→ 07-referencia/cheat-sheet.md   (manter aberto durante o trabalho)
```

**Sessão de trabalho regular:**
```
07-referencia/cheat-sheet.md
→ 05-fluxos/[fluxo pertinente]
→ 03-validacao/05-faa.md (ao final)
```

**Resolvendo um problema:**
```
03-validacao/07-resolucao-de-erros.md
→ 08-exemplos-reais.md (seção correspondente)
```

---

## Convenções deste Manual

- Blocos `bash` são executáveis a partir da **raiz do repositório**
- `REC-000001`, `ING-000004` são identificadores de exemplos **reais** do sistema
- ⚠️ indica aviso operacional — algo que causa problemas sérios se ignorado
- ✅ indica verificação — como confirmar que um passo foi executado corretamente
- `CRÍTICO` indica regra inviolável — violação quebra invariantes do sistema
