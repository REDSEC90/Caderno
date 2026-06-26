# Especificação de Entidade: Experimento

> Aplicação do template canônico à entidade Experimento do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Experimento é o registro de uma tentativa deliberada de testar uma hipótese ou desenvolver conhecimento novo sobre algum aspecto culinário, com resultado documentado.

**Categoria gastronômica:**
Na culinária, um experimento é uma preparação com objetivo científico: "e se dobrar o fermento?", "qual temperatura produz melhor caramelização?", "a adição de bicarbonato muda a textura?". É o preparo orientado à descoberta, não à produção.

**Categoria no sistema:**
Experimento é a entidade que captura o processo investigativo, com identificador `EXP-NNNNNN`. Pode originar Receitas (se bem-sucedido) e gera Observações ao longo do processo.

---

## 2. Responsabilidade

**Propósito principal:**
Registrar o processo de criação e evolução do conhecimento, separando a fase exploratória da fase consolidada (Receita).

**Responsabilidades explícitas:**
- Registrar a hipótese investigada.
- Documentar o processo experimental.
- Registrar o resultado e conclusão.
- Vincular ao conhecimento que originou (Receita base, se houver).
- Indicar se o resultado foi incorporado a uma Receita.

---

## 3. Limites

**Esta entidade NÃO:**
- Substitui Receitas consolidadas.
- Serve como registro de execuções rotineiras (isso pertence a Execução).
- É obrigatória para a criação de Receitas — Receitas podem nascer diretamente.

**Fronteira com Execução:**
Execução registra "o que fiz desta receita". Experimento registra "o que testei para descobrir algo novo".

**Fronteira com Receita:**
Quando o experimento é concluído e o resultado validado, o conhecimento pode ser incorporado em uma Receita. O Experimento permanece como registro histórico do processo.

---

## 4. Atributos

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `EXP-NNNNNN` |
| `tipo` | string | Valor fixo: `experimento` |
| `schema-version` | string | Versão do esquema |
| `versao` | string | Versão do registro |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `titulo` | string | Nome do experimento |
| `hipotese` | text | O que está sendo testado e por quê |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `receita-base-id` | string | ID da Receita que serviu de ponto de partida |
| `variaveis` | text | O que foi alterado em relação ao estado base |
| `processo` | text | Descrição do processo experimental |
| `resultado` | text | O que foi observado |
| `conclusao` | text | O que foi aprendido |
| `incorporado-em` | string | ID da Receita que incorporou o resultado |
| `tags` | list | Marcadores livres |
| `notas` | text | Observações adicionais |

---

## 5. Estados

| Estado | Significado |
|--------|-------------|
| `aberto` | Em andamento, sem resultado definitivo |
| `concluido` | Finalizado com resultado documentado |
| `incorporado` | Resultado absorvido por uma Receita ou entidade |
| `descartado` | Concluído sem aproveitamento, mantido no histórico |

**Diagrama de transição:**
```
[aberto] → [concluido] → [incorporado]
                       → [descartado]
```

---

## 6. Relacionamentos

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| `parte-de` | Receita (base) | N:1 | Experimento pode ter uma Receita como ponto de partida |
| `origina` | Receita (nova) | 1:N | Experimento bem-sucedido pode originar Receitas |
| `gera` | Observação | 1:N | Processo experimental gera Observações |

---

## 7. Restrições

1. O `id` é imutável após criação.
2. Estado `incorporado` exige `incorporado-em` preenchido.
3. Estado `descartado` exige `conclusao` preenchido, mesmo que negativa.
4. Experimentos descartados permanecem no histórico com valor informativo.

---

## 8. Ciclo de Vida

**Nascimento:** Nasce com a formulação de uma hipótese. Campo mínimo: `titulo` e `hipotese`. Nasce em estado `aberto`.

**Evolução:** Resultado é registrado conforme o experimento progride. Conclusão é formalizada ao final.

**Encerramento:** Ao concluir, o Experimento transita para `incorporado` (se gerou Receita) ou `descartado` (se não gerou). Nunca é arquivado antes de concluído.
