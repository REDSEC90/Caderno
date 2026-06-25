# Política de Conflito

> Como conflitos entre regras ou camadas são resolvidos.

---

## Definição

Um **conflito** ocorre quando:

1. Duas regras da mesma camada se contradizem
2. Uma decisão de camada inferior contraria camada superior
3. Uma evolução de entidade quebra um contrato estabelecido
4. Dois registros reivindicam autoridade sobre o mesmo conhecimento
5. Um esquema novo invalida registros antigos válidos

Conflitos não resolvidos geram ambiguidade. Ambiguidade viola o objetivo fundamental do roadmap de maturidade.

---

## Hierarquia

### Ordem de precedência entre camadas

```
Filosofia
    ↓
Constituição
    ↓
Governança
    ↓
Linguagem
    ↓
Domínio
    ↓
Contratos
    ↓
Implementação
```

**Regra fundamental:** camada superior sempre prevalece sobre camada inferior.

### Exemplos de aplicação

**Conflito Implementação vs Domínio:**
- Código diz que Ingrediente não tem campo `sazonalidade`
- Domínio diz que Ingrediente deve ter `sazonalidade`
- **Resolução:** Domínio prevalece. Código está errado.

**Conflito Domínio vs Constituição:**
- Domínio propõe que relacionamentos usem nomes
- Constituição diz que relacionamentos usam IDs
- **Resolução:** Constituição prevalece. Proposta de domínio é inválida.

**Conflito Governança vs Filosofia:**
- Governança propõe que SQLite seja fonte primária
- Filosofia diz que Markdown é formato canônico
- **Resolução:** Filosofia prevalece. Governança violaria axioma.

---

## Detecção

### Como conflitos são identificados

**Durante especificação:**
- Revisão cruzada de documentos
- Validação de consistência entre camadas
- Checklist de maturidade (FASE 12)

**Durante implementação:**
- Código tentando violar regra de camada superior
- Testes detectando comportamento incompatível com domínio
- Validação de conformidade arquitetural

**Durante operação:**
- Registro não pode ser criado porque regras conflitam
- Dois padrões aplicáveis geram resultado diferente
- Auditoria identifica decisão inconsistente

---

## Resolução

### Processo padrão de resolução

1. **Identificar camadas envolvidas** — qual camada estabeleceu cada regra?
2. **Aplicar hierarquia** — camada superior prevalece
3. **Ajustar camada inferior** — corrigir regra que viola hierarquia
4. **Documentar decisão** — registrar conflito e resolução
5. **Propagar correção** — atualizar documentação e implementação afetadas

---

## Conflitos Especiais

### Quando a Constituição é contraditória

**Cenário:** duas leis fundamentais da Constituição entram em conflito.

**Exemplo hipotético:**
- Lei 4: "Markdown é formato canônico"
- Lei 6: "Nenhuma informação exclusiva no banco de dados"
- Conflito: metadado de auditoria gerado pelo banco seria exclusivo?

**Resolução:**
1. Mantenedores do projeto analisam
2. Verifica-se qual lei está mais próxima da Filosofia
3. Filosofia é árbitro final
4. Constituição é emendada para eliminar contradição

**Quem decide:** consenso entre mantenedores, validado contra Filosofia.

Este é o conflito mais grave possível e exige processo formal.

---

### Quando Entidade evolui quebrando Contrato

**Cenário:** domínio gastronômico muda, entidade precisa evoluir, mas contrato estabelecido seria violado.

**Exemplo concreto:**
- Contrato v1 de Ingrediente: campo `tipo` é enum com 3 valores
- Domínio evolui: surgem 5 novos tipos de ingredientes
- Contrato seria quebrado se enum mudar

**Resolução:**

**Opção A — Versionamento (preferencial):**
- Contrato v1 permanece válido
- Contrato v2 criado com novos tipos
- Registros v1 continuam válidos
- Novos registros usam v2

**Opção B — Extensão compatível:**
- Contrato v1.1 adiciona novos valores ao enum
- Mudança é compatível (apenas adiciona, não remove)
- Registros v1 continuam válidos sob v1.1

**Decisão:** depende se mudança é compatível ou não. Se incompatível, versionamento é obrigatório (Opção A).

---

### Quando dois Esquemas conflitam

**Cenário:** esquema de duas entidades define campos relacionados de forma inconsistente.

**Exemplo concreto:**
- Esquema de Receita: campo `tempo_preparo` em minutos (número)
- Esquema de Execução: campo `tempo_preparo` em string livre ("30 min a 1h")

**Resolução:**
1. Identificar qual esquema foi definido primeiro
2. Avaliar qual tipagem é mais correta para o domínio
3. Padronizar ambos
4. Versionar esquemas se necessário

**Princípio:** consistência entre entidades relacionadas é obrigatória.

---

### Quando Implementação não consegue atender Domínio

**Cenário:** requisito do domínio é tecnicamente inviável na implementação atual.

**Exemplo hipotético:**
- Domínio exige busca semântica avançada
- Implementação SQLite não suporta nativamente

**Resolução:**

**Opção A — Implementação melhora:**
- Adicionar extensão ou biblioteca ao SQLite
- Implementar funcionalidade em camada acima do banco

**Opção B — Domínio é esclarecido:**
- Requisito era ambíguo
- Busca simples já atende
- Domínio é refinado para ser mais preciso

**Nunca permitido:** mudar o domínio para ser mais fácil de implementar se isso compromete o conhecimento.

**Princípio:** se implementação não consegue atender, implementação muda ou é substituída. Domínio não é negociável.

---

## Conflitos entre Registros

### Quando dois registros representam o mesmo conhecimento

**Cenário:** dois registros de Ingrediente chamados "Tomate" existem.

**IDs diferentes:**
- `ING-0042` — Tomate
- `ING-0156` — Tomate

**Resolução:**

1. **Verificar se são realmente duplicados:**
   - São o mesmo ingrediente? → duplicação
   - São variedades diferentes (Tomate Cereja vs Tomate Italiano)? → não é duplicação

2. **Se duplicação confirmada:**
   - Registro mais antigo ou mais completo permanece ativo
   - Registro duplicado é marcado como `arquivado`
   - Metadado `duplicado_de: ING-0042` adicionado ao arquivado
   - Referências ao duplicado são migradas (opcional, mas recomendado)

3. **Se não é duplicação:**
   - Nomes são diferenciados
   - `Tomate Cereja`, `Tomate Italiano`
   - Ambos permanecem ativos

---

### Quando dois esquemas reivindicam autoridade

**Cenário:** existe `esquema-receita-v1.md` e alguém cria `esquema-receita-v1-alternativo.md`.

**Resolução:**

Apenas um esquema por versão é oficial.

1. Revisar ambos
2. Avaliar qual está mais conforme à Governança e Domínio
3. Eleger o oficial
4. Outro é movido para `docs/98-rascunhos/` ou descartado

**Princípio:** não pode haver ambiguidade sobre qual esquema é válido.

---

## Documentação de Conflitos

### Registro de Decisão Arquitetural (ADR)

Conflitos resolvidos devem gerar ADR documentando:

```markdown
# ADR-XXXX: Resolução de Conflito entre [A] e [B]

## Contexto

[descrição do conflito]

## Camadas envolvidas

- Camada X: [regra]
- Camada Y: [regra conflitante]

## Análise

[como hierarquia foi aplicada]

## Decisão

[qual regra prevaleceu e por quê]

## Consequências

[o que foi alterado para resolver]

## Referências

[links para documentos afetados]
```

---

## Prevenção

### Como evitar conflitos

**Durante especificação:**
- Revisão cruzada entre camadas antes de finalizar
- Checklist de consistência na FASE 12
- Validação de que camadas inferiores não contradizem superiores

**Durante governança:**
- Política de Conflito aplicada desde o início
- Toda nova regra validada contra hierarquia
- Mudanças estruturais passam por revisão de múltiplos mantenedores

**Durante implementação:**
- Testes de conformidade arquitetural
- Validação automática contra domínio
- Code review verifica aderência

---

## Casos Extremos

### Quando Filosofia está errada

**Cenário hipotético:** um axioma da Filosofia se mostra fundamentalmente incorreto após anos de uso.

**Exemplo fictício:** "Markdown é formato canônico" se mostra inviável para tipos específicos de conhecimento que surgiram.

**Resolução:**

Este é um evento extraordinário que exige:
1. Análise profunda do impacto
2. Consenso amplo entre mantenedores
3. Período de discussão pública
4. Emenda filosófica formal
5. Roadmap de transição (pode levar anos)

**Critério:** Filosofia só muda se comprovado que viola objetivo maior de preservação do conhecimento por décadas.

Mudança filosófica é última opção. Antes disso, todas as alternativas devem ser esgotadas.

---

## Escalação

### Quando não há consenso

1. **Nível 1:** Discussão entre envolvidos
2. **Nível 2:** Mantenedores do domínio mediam
3. **Nível 3:** Administradores aplicam hierarquia formalmente
4. **Nível 4:** Comunidade vota (apenas para conflitos sem resolução clara por hierarquia)

**Nível 4 é raro.** Maioria dos conflitos resolve-se pela hierarquia.

---

## Exemplos Completos

### Exemplo 1: Código vs Domínio

**Conflito:**
```python
# Código implementa:
class Receita:
    def add_ingrediente(self, nome: str):
        self.ingredientes.append(nome)  # usa nome

# Domínio especifica:
Relacionamento Receita-Ingrediente: usa ID, nunca nome
```

**Resolução:**
- Domínio (camada superior) prevalece
- Código está errado
- Correção:
```python
def add_ingrediente(self, ingrediente_id: str):
    self.ingredientes.append(ingrediente_id)
```

---

### Exemplo 2: Esquema novo invalida registros antigos

**Conflito:**
- `esquema-receita-v2` adiciona campo obrigatório `categoria`
- Registros v1 não têm esse campo

**Resolução (pela Política de Esquemas):**
- Não é conflito, é evolução natural
- Registros v1 permanecem válidos sob esquema v1
- Registros novos usam v2
- Sistema aceita ambas versões

**Não há conflito porque Governança já prevê convivência de versões.**

---

### Exemplo 3: Duas políticas conflitantes

**Conflito:**
- Política de Templates: "mudança menor não exige nova versão"
- Política de Versionamento: "toda mudança deve ser versionada"

**Resolução:**
- Esclarecer que "versão" em cada contexto significa coisas diferentes
- Política de Templates: versão do template (v1, v2)
- Política de Versionamento: versão do registro (controlada por git)
- Após esclarecimento, não há conflito

---

## Resumo

- Conflitos ocorrem quando regras se contradizem
- Hierarquia define precedência: Filosofia > Constituição > Governança > Domínio > Implementação
- Camada superior sempre prevalece
- Conflitos na Constituição são resolvidos por Filosofia
- Evolução quebrando contrato: versionamento resolve
- Registros duplicados: o mais antigo/completo permanece
- Conflitos geram ADR documentando resolução
- Prevenção: revisão cruzada e validação de consistência
- Mudança filosófica é extraordinária e exige consenso amplo
