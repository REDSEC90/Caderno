# Mapa de Relacionamentos do SOE-CCG

> Desenho completo do sistema no plano do domínio. Cada relacionamento documentado com nome, direção, cardinalidade, restrições e significado.

---

## Visão Geral

```
Experimento ──origina──→ Receita ──possui──→ Execução ──gera──→ Observação
     └──gera──→ Observação       │                └──gera──→ Observação
                                 ├──utiliza──→ Ingrediente
                                 ├──aplica───→ Técnica
                                 └──requer───→ Equipamento

Observação ──sobre──→ qualquer Entidade
```

---

## Relacionamentos Detalhados

---

### REL-001: Receita → Ingrediente

| Atributo | Valor |
|----------|-------|
| **Nome** | `utiliza` |
| **Origem** | Receita |
| **Destino** | Ingrediente |
| **Direção** | Receita referencia Ingrediente |
| **Cardinalidade** | N:N — uma Receita usa muitos Ingredientes; um Ingrediente é usado em muitas Receitas |
| **Obrigatório** | Sim — toda Receita deve ter ao menos um Ingrediente |
| **Expresso como** | Lista de IDs `ING-NNNNNN` com quantidade no campo `ingredientes` da Receita |
| **Restrições** | O `ING-NNNNNN` referenciado deve existir no sistema |
| **Significado** | "Esta Receita requer este Ingrediente para ser preparada" |
| **Impacto do arquivamento** | Ingrediente arquivado pode permanecer referenciado em Receitas históricas; Receitas novas recebem alerta |

---

### REL-002: Receita → Técnica

| Atributo | Valor |
|----------|-------|
| **Nome** | `aplica` |
| **Origem** | Receita |
| **Destino** | Técnica |
| **Direção** | Receita referencia Técnica |
| **Cardinalidade** | N:N — uma Receita pode aplicar muitas Técnicas; uma Técnica aparece em muitas Receitas |
| **Obrigatório** | Não |
| **Expresso como** | Lista de IDs `TEC-NNNNNN` no campo `tecnicas` da Receita |
| **Restrições** | O `TEC-NNNNNN` referenciado deve existir no sistema |
| **Significado** | "Esta Receita emprega este procedimento culinário" |

---

### REL-003: Receita → Equipamento

| Atributo | Valor |
|----------|-------|
| **Nome** | `requer` |
| **Origem** | Receita |
| **Destino** | Equipamento |
| **Direção** | Receita referencia Equipamento |
| **Cardinalidade** | N:N |
| **Obrigatório** | Não |
| **Expresso como** | Lista de IDs `EQP-NNNNNN` no campo `equipamentos` da Receita |
| **Significado** | "Esta Receita necessita deste equipamento para ser preparada" |

---

### REL-004: Execução → Receita

| Atributo | Valor |
|----------|-------|
| **Nome** | `pertence-a` |
| **Origem** | Execução |
| **Destino** | Receita |
| **Direção** | Execução referencia Receita |
| **Cardinalidade** | N:1 — muitas Execuções pertencem a uma Receita; uma Receita possui muitas Execuções |
| **Obrigatório** | Sim — toda Execução pertence a uma Receita |
| **Expresso como** | Campo `receita-id: REC-NNNNNN` na Execução |
| **Restrições** | Campo imutável após criação. O `REC-NNNNNN` deve existir. |
| **Significado** | "Esta Execução foi uma realização desta Receita" |

---

### REL-005: Execução → Ingrediente

| Atributo | Valor |
|----------|-------|
| **Nome** | `usa` |
| **Origem** | Execução |
| **Destino** | Ingrediente |
| **Direção** | Execução referencia Ingredientes efetivamente usados |
| **Cardinalidade** | N:N |
| **Obrigatório** | Não — pode diferir da Receita base |
| **Expresso como** | Lista de IDs `ING-NNNNNN` com quantidades reais em `ingredientes-usados` |
| **Significado** | "Nesta execução real, estes ingredientes foram efetivamente utilizados (pode incluir substituições)" |

---

### REL-006: Execução → Técnica

| Atributo | Valor |
|----------|-------|
| **Nome** | `aplica` |
| **Origem** | Execução |
| **Destino** | Técnica |
| **Cardinalidade** | N:N |
| **Obrigatório** | Não |
| **Expresso como** | Lista de IDs `TEC-NNNNNN` em `tecnicas-aplicadas` |
| **Significado** | "Nesta execução real, estas técnicas foram efetivamente empregadas" |

---

### REL-007: Execução → Equipamento

| Atributo | Valor |
|----------|-------|
| **Nome** | `utiliza` |
| **Origem** | Execução |
| **Destino** | Equipamento |
| **Cardinalidade** | N:N |
| **Obrigatório** | Não |
| **Expresso como** | Lista de IDs `EQP-NNNNNN` em `equipamentos-usados` |
| **Significado** | "Nesta execução real, estes equipamentos foram efetivamente usados" |

---

### REL-008: Execução → Observação

| Atributo | Valor |
|----------|-------|
| **Nome** | `gera` |
| **Origem** | Execução |
| **Destino** | Observação |
| **Direção** | Execução como contexto gerador de Observação |
| **Cardinalidade** | 1:N — uma Execução pode gerar muitas Observações |
| **Obrigatório** | Não |
| **Expresso como** | Campo `entidade-referenciada: EXE-NNNNNN` na Observação |
| **Significado** | "Esta percepção surgiu durante ou após esta execução específica" |

---

### REL-009: Observação → qualquer Entidade

| Atributo | Valor |
|----------|-------|
| **Nome** | `sobre` |
| **Origem** | Observação |
| **Destino** | Receita, Ingrediente, Técnica, Equipamento, Execução ou Experimento |
| **Direção** | Observação referencia a entidade sobre a qual se refere |
| **Cardinalidade** | N:1 — uma Observação é sobre uma entidade; uma entidade pode ter muitas Observações |
| **Obrigatório** | Não — Observação pode existir sem referência específica |
| **Expresso como** | Campos `entidade-referenciada: [ID]` e `tipo-entidade: [tipo]` na Observação |
| **Significado** | "Este aprendizado ou percepção se refere a esta entidade" |

---

### REL-010: Experimento → Receita (base)

| Atributo | Valor |
|----------|-------|
| **Nome** | `parte-de` |
| **Origem** | Experimento |
| **Destino** | Receita |
| **Direção** | Experimento referencia Receita que serviu de ponto de partida |
| **Cardinalidade** | N:1 |
| **Obrigatório** | Não — experimento pode não ter Receita base |
| **Expresso como** | Campo `receita-base-id: REC-NNNNNN` no Experimento |
| **Significado** | "Este experimento foi iniciado a partir desta Receita" |

---

### REL-011: Experimento → Receita (nova)

| Atributo | Valor |
|----------|-------|
| **Nome** | `origina` |
| **Origem** | Experimento |
| **Destino** | Receita |
| **Direção** | Experimento como gerador de nova Receita |
| **Cardinalidade** | 1:N — um experimento pode originar mais de uma Receita |
| **Obrigatório** | Não |
| **Expresso como** | Campo `incorporado-em: REC-NNNNNN` no Experimento |
| **Significado** | "Este experimento gerou conhecimento que foi formalizado nesta Receita" |

---

### REL-012: Experimento → Observação

| Atributo | Valor |
|----------|-------|
| **Nome** | `gera` |
| **Origem** | Experimento |
| **Destino** | Observação |
| **Cardinalidade** | 1:N |
| **Obrigatório** | Não |
| **Expresso como** | Campo `entidade-referenciada: EXP-NNNNNN` e `tipo-entidade: experimento` na Observação |
| **Significado** | "Esta observação surgiu durante o processo experimental" |

---

### REL-013: Receita → Categoria

| Atributo | Valor |
|----------|-------|
| **Nome** | `pertence-a` |
| **Origem** | Receita |
| **Destino** | Categoria (Catálogo) |
| **Cardinalidade** | N:N — uma Receita pode pertencer a muitas categorias |
| **Obrigatório** | Não |
| **Expresso como** | Lista de códigos de categoria em `categorias` |
| **Significado** | "Esta Receita pertence a esta categoria culinária" |

---

## Diagrama Completo de Relacionamentos

```
┌─────────────────────────────────────────────────────────────┐
│                    SOE-CCG — Mapa de Entidades              │
└─────────────────────────────────────────────────────────────┘

  EXPERIMENTO ──[parte-de]──→ RECEITA ←──[pertence-a]── EXECUÇÃO
       │                         │
       │                     [utiliza]
       │                     [aplica]
       │                     [requer]
       │                         │
       │                         ↓
       │                   INGREDIENTE
       │                   TÉCNICA
       │                   EQUIPAMENTO
       │
       └──[origina]──→ RECEITA (nova)
       │
       └──[gera]──→ OBSERVAÇÃO ──[sobre]──→ qualquer entidade

  EXECUÇÃO ──[usa]──────────→ INGREDIENTE
           ──[aplica]────────→ TÉCNICA
           ──[utiliza]───────→ EQUIPAMENTO
           ──[gera]──────────→ OBSERVAÇÃO

  OBSERVAÇÃO ──[sobre]──→ RECEITA
                        → EXECUÇÃO
                        → INGREDIENTE
                        → TÉCNICA
                        → EQUIPAMENTO
                        → EXPERIMENTO
```

---

## Princípio de Referência

Todo relacionamento usa identificadores permanentes, nunca nomes:

```
✅ CORRETO:
ingredientes:
  - id: ING-000042
    quantidade: 200g

❌ ERRADO:
ingredientes:
  - nome: Tomate Cereja
    quantidade: 200g
```

**Razão:** se o nome do Ingrediente mudar, todas as referências por nome precisariam ser atualizadas. Com IDs, o vínculo permanece intacto independentemente de renomeações.
