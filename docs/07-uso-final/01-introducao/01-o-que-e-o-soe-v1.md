# O que é o SOE-CCG

> Visão prática — não filosófica. O que o sistema faz, com o que trabalha e por que existe.

---

## Em uma frase

O SOE-CCG é uma **plataforma de gestão de conhecimento culinário estruturado**, onde cada receita, ingrediente, técnica, equipamento, execução, observação e experimento é um objeto formal com identidade permanente, relacionamentos rastreáveis e histórico imutável.

---

## O que o sistema armazena

O SOE trabalha com sete tipos de objeto, chamados **entidades**:

| Entidade | O que é | Exemplo |
|----------|---------|---------|
| **Receita** | O conhecimento de como fazer um prato | Doce de Leite Artesanal |
| **Ingrediente** | Um insumo reutilizável por várias receitas | Leite Integral |
| **Técnica** | Um método culinário reutilizável | Redução por evaporação |
| **Equipamento** | Um utensílio ou aparelho | Panela de Fundo Grosso |
| **Execução** | O registro de um preparo real | Doce de leite feito em 25/06/2026 |
| **Observação** | Uma nota ou percepção vinculada a qualquer entidade | O bicarbonato acelera a reação de Maillard |
| **Experimento** | Uma hipótese sendo testada deliberadamente | Testar 300g de açúcar vs. 250g |

---

## O que são relacionamentos

Entidades se conectam através de **relacionamentos rastreáveis**. Uma Receita referencia os Ingredientes que usa. Uma Execução pertence a uma Receita. Uma Observação está vinculada a uma Execução.

Esses vínculos são registrados por **identificadores**, nunca por nomes:

```yaml
# Correto — usa ID permanente
ingredientes: [ING-000001, ING-000002]

# Errado — usa nome que pode mudar
ingredientes: [Leite Integral, Açúcar Refinado]
```

O conjunto de todas as entidades e seus relacionamentos forma o **grafo de conhecimento** do sistema.

---

## Onde os dados vivem

O sistema tem duas camadas físicas:

**Camada 1 — Markdown (fonte canônica)**
Arquivos `.md` em `dados/`. São legíveis por humanos, versionáveis por git, e independentes de qualquer software específico. São a fonte de verdade.

**Camada 2 — SQLite (índice derivado)**
Banco de dados em `banco_de_dados/sqlite/soe-ccg.db`. Existe para consultas rápidas e estruturadas. Pode ser reconstruído integralmente a partir dos arquivos Markdown a qualquer momento.

```
dados/ (Markdown)   →   validação   →   SQLite
      ↑                                    ↓
  fonte da verdade                    apenas consulta
```

⚠️ **O SQLite nunca é a origem.** Se houver qualquer divergência, o Markdown prevalece.

---

## O que são documentos

Além das entidades de dados, o SOE tem uma camada de **documentação formal** em `docs/`:

- Especificações de entidades (`docs/01-dominio/`)
- Padrões e políticas (`docs/04-padroes/`)
- Arquitetura (`docs/02-arquitetura/`)
- Este manual (`docs/07-uso/`)

A documentação em `docs/` descreve o sistema. Os dados em `dados/` são o conhecimento culinário.

---

## O que é o grafo de conhecimento

Quando todos os arquivos Markdown são parseados e seus relacionamentos resolvidos, o resultado é um **KnowledgeGraph** — uma estrutura em memória que representa todas as entidades e suas conexões.

Esse grafo é o objeto central de todo o pipeline de validação e importação. O Parser constrói o grafo. O Resolver resolve as referências. O Validador verifica consistência. O Importador persiste no SQLite.

---

## Por que esse design

Três razões práticas:

1. **Durabilidade.** Arquivos Markdown sobrevivem a qualquer mudança de tecnologia. O conhecimento culinário não depende de nenhum software específico para existir.

2. **Rastreabilidade.** Cada mudança é registrada pelo git. O histórico completo de qualquer receita ou ingrediente está sempre disponível.

3. **Consistência.** Identificadores permanentes garantem que renomear um ingrediente nunca quebra referências existentes.

---

## Próxima leitura

- Ver o sistema funcionando agora → [`02-primeiros-passos-v1.md`](02-primeiros-passos-v1.md)
- Mudar a mentalidade antes de operar → [`03-como-pensar-no-soe-v1.md`](03-como-pensar-no-soe-v1.md)
