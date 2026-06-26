# Especificação de Entidade: Execução

> Aplicação do template canônico à entidade Execução do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Execução é o registro de um preparo real de uma Receita em um momento específico, capturando o que aconteceu, não o que deveria acontecer.

**Categoria gastronômica:**
Na culinária, executar uma receita é cozinhá-la de fato: na cozinha, com ingredientes reais, em um dia e horário específicos. Cada preparo é único e pode diferir da receita original.

**Categoria no sistema:**
Execução é o registro histórico e descritivo que vincula uma Receita à realidade vivida. Possui identificador `EXE-NNNNNN` e é sempre filha de uma Receita.

---

## 2. Responsabilidade

**Propósito principal:**
Separar o conhecimento prescritivo (Receita) do conhecimento empírico (o que realmente aconteceu quando se cozinhou), permitindo que o histórico de preparos enriqueça o conhecimento sem alterar a Receita base.

**Responsabilidades explícitas:**
- Registrar data, hora e contexto do preparo.
- Capturar desvios em relação à Receita (substituições, ajustes).
- Registrar métricas observadas (tempo real, temperatura, peso final).
- Registrar resultado e avaliação da execução.
- Servir de base para Observações vinculadas ao preparo.

---

## 3. Limites

**Esta entidade NÃO:**
- Altera a Receita (mudanças na Receita geram nova versão da Receita, não uma Execução).
- Substitui Observações livres (Observação é entidade separada para registros qualitativos mais ricos).
- Representa experimentos controlados (isso pertence a Experimento).

**Fronteira com Receita:**
Receita é prescritiva e imutável no preparo. Execução é descritiva e única. Se durante uma execução o cozinheiro percebe que a receita precisa mudar, isso gera uma nova versão da Receita — não uma anotação na Execução.

**Fronteira com Observação:**
Observação é um registro isolado de uma percepção qualquer. Execução é um registro estruturado de um preparo completo. Uma Execução pode gerar múltiplas Observações vinculadas.

---

## 4. Atributos

Referência ao esquema: `docs/01-dominio/esquemas/esquema-execucao-v1.md`

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `EXE-NNNNNN` |
| `tipo` | string | Valor fixo: `execucao` |
| `schema-version` | string | Versão do esquema |
| `versao` | string | Versão do registro |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação do registro |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `receita-id` | string | ID da Receita executada. Formato: `REC-NNNNNN` |
| `data-execucao` | date | Data em que o preparo ocorreu |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `hora-inicio` | string | Horário de início do preparo |
| `hora-fim` | string | Horário de término do preparo |
| `tempo-total` | string | Duração real do preparo |
| `ingredientes-usados` | list | IDs de Ingredientes com quantidades reais (pode diferir da Receita) |
| `tecnicas-aplicadas` | list | IDs de Técnicas efetivamente aplicadas |
| `equipamentos-usados` | list | IDs de Equipamentos utilizados |
| `desvios` | text | Diferenças em relação à Receita base |
| `resultado` | text | Descrição do resultado obtido |
| `avaliacao-sabor` | string | Nota de 1 a 10 ou descritivo |
| `avaliacao-textura` | string | Nota de 1 a 10 ou descritivo |
| `avaliacao-aparencia` | string | Nota de 1 a 10 ou descritivo |
| `avaliacao-geral` | string | Nota de 1 a 10 ou descritivo |
| `peso-final` | string | Quantidade produzida na execução |
| `contexto` | text | Circunstâncias relevantes do preparo |
| `tags` | list | Marcadores livres |
| `notas` | text | Observações livres |

---

## 5. Estados

| Estado | Significado |
|--------|-------------|
| `registrada` | Preparo documentado, dados em preenchimento |
| `revisada` | Dados conferidos e complementados |
| `consolidada` | Registro encerrado, sem alterações futuras |

**Diagrama de transição:**
```
[registrada] → [revisada] → [consolidada]
```

**Regras:**
- `registrada` → `revisada`: usuário confere e complementa dados após o preparo.
- `revisada` → `consolidada`: usuário declara o registro encerrado.

---

## 6. Eventos

| Evento | Descrição | Gatilho |
|--------|-----------|---------|
| `criacao` | Execução registrada | Usuário documenta preparo |
| `complementacao` | Campos opcionais preenchidos | Usuário adiciona dados pós-preparo |
| `vinculo-observacao` | Observação vinculada à Execução | Usuário registra nova Observação sobre este preparo |
| `consolidacao` | Registro encerrado | Usuário consolida |

---

## 7. Relacionamentos

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| `pertence-a` | Receita | N:1 | Toda Execução pertence a uma Receita |
| `usa` | Ingrediente | N:N | Ingredientes reais utilizados |
| `aplica` | Técnica | N:N | Técnicas efetivamente aplicadas |
| `utiliza` | Equipamento | N:N | Equipamentos efetivamente usados |
| `gera` | Observação | 1:N | Execuções podem gerar Observações |

---

## 8. Dependências

**Dependências obrigatórias:**
- `Receita`: toda Execução deve referenciar uma Receita existente.

**Dependências opcionais:**
- `Ingrediente`, `Técnica`, `Equipamento`: quando registrados na execução.

---

## 9. Restrições

1. O `id` é imutável após criação.
2. `receita-id` é imutável após criação — uma Execução sempre pertence à mesma Receita.
3. A `receita-id` deve referenciar uma Receita existente no sistema.
4. Execuções consolidadas não recebem alterações de conteúdo — apenas metadados de sistema.
5. `data-execucao` deve ser igual ou anterior à `criado-em`.

---

## 10. Ciclo de Vida

**Nascimento:** Uma Execução nasce quando o usuário registra um preparo ocorrido. O campo mínimo além dos metadados é `receita-id` e `data-execucao`. Nasce em estado `registrada`.

**Evolução:** O usuário complementa dados nos dias seguintes ao preparo (métricas, avaliações, notas). Ao concluir, transita para `revisada` e depois `consolidada`.

**Arquivamento:** Execuções não são normalmente arquivadas — fazem parte do histórico permanente. Somente em casos de registro duplicado ou erro de criação são arquivadas.
