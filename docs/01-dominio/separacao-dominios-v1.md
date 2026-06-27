# Separação de Domínios

> Distinção essencial entre domínio gastronômico e domínio do sistema.

---

## Por que separar?

O SOE-CCG opera em **dois planos conceituais distintos**:

1. **Domínio Gastronômico** — o problema que estamos resolvendo
2. **Domínio do Sistema** — a solução que estamos construindo

Confundir esses planos gera ambiguidade e impede implementação clara.

---

## Domínio Gastronômico

### O que é

O conjunto de **conceitos culinários** que existem independentemente do SOE-CCG.

Esses conceitos existiam antes do sistema e continuarão existindo após ele.

### Conceitos principais

**Ingrediente (gastronômico):**
Um insumo alimentício usado em preparações. Ex: tomate, sal, farinha.

**Técnica (gastronômica):**
Um método de preparo ou transformação. Ex: refogar, assar, emulsionar.

**Equipamento (gastronômico):**
Um utensílio ou aparelho usado no preparo. Ex: panela, forno, batedeira.

**Receita (gastronômica):**
Uma definição de prato: ingredientes, técnicas, passos. Existe no plano do conhecimento.

**Execução (gastronômica):**
Um preparo real de uma receita. Acontece no plano físico, em momento específico.

**Observação (gastronômica):**
Uma percepção sobre qualquer aspecto culinário. Ex: "o bolo ficou seco", "sal realça doçura".

**Experimento (gastronômico):**
Uma tentativa deliberada de testar hipótese ou desenvolver conhecimento novo. Ex: "dobrar fermento melhora textura?".

---

## Domínio do Sistema

### O que é

O conjunto de **conceitos computacionais** que o SOE-CCG define para organizar conhecimento gastronômico.

Esses conceitos existem apenas dentro do SOE-CCG e servem para estruturar, versionar, relacionar e consultar conhecimento.

### Conceitos principais

**Registro:**
Unidade mínima de conhecimento no sistema. Todo conhecimento gastronômico é armazenado como registro.

**Entidade:**
Categoria de registro. Define atributos, regras, estados, ciclo de vida. Ex: a entidade "Ingrediente" no sistema representa o conceito gastronômico "ingrediente".

**Identificador:**
Código permanente atribuído a um registro. Ex: `ING-0042`, `REC-0156`. Conceito técnico do sistema, não gastronômico.

**Esquema:**
Definição formal dos campos de uma entidade. Conceito de validação e estruturação técnica.

**Template:**
Modelo de estrutura Markdown para escrever registros. Conceito de formatação técnica.

**Versão:**
Estado imutável de um registro em momento específico. Conceito de controle de mudanças.

**Histórico:**
Conjunto ordenado de versões. Conceito de rastreabilidade.

**Estado:**
Fase do ciclo de vida de um registro (rascunho, ativo, arquivado). Conceito de governança.

**Relacionamento (sistêmico):**
Ligação entre dois registros por identificadores. Conceito de integridade referencial.

**Metadado:**
Informação sobre o registro (data de criação, autor, versão de esquema). Conceito de catalogação técnica.

**Catálogo:**
Conjunto padronizado de valores reutilizáveis. Ex: unidades de medida, tipos de ingredientes. Conceito de normalização.

**Tag:**
Marcador livre para classificação. Conceito de organização.

---

## Relação entre os Domínios

### Mapeamento

| Conceito Gastronômico | Implementado como (Sistema) |
|-----------------------|------------------------------|
| Ingrediente (tomate) | Entidade Ingrediente, Registro ING-0042 |
| Técnica (refogar) | Entidade Técnica, Registro TEC-0023 |
| Receita (bolo de cenoura) | Entidade Receita, Registro REC-0089 |
| Execução (preparo de 15/jun) | Entidade Execução, Registro EXE-0345 |
| Observação (bolo ficou seco) | Entidade Observação, Registro OBS-0890 |

### Fluxo

```
Conceito Gastronômico
    ↓
Modelado como Entidade
    ↓
Estruturado por Esquema e Template
    ↓
Registrado como Registro
    ↓
Identificado por ID
    ↓
Versionado e Auditado
    ↓
Relacionado com outros Registros
    ↓
Consultado via SQLite
```

---

## Exemplos de Ambiguidade Resolvida

### Ambiguidade 1: "Versão"

**Confuso:**
"A receita tem versão 2."

**Claro:**
- **Domínio gastronômico:** "A receita foi reformulada (conhecimento evoluiu)."
- **Domínio do sistema:** "O registro REC-0089 está em sua segunda versão de esquema (v2)."

São coisas diferentes. Primeira é evolução do conhecimento. Segunda é evolução da estrutura de dados.

---

### Ambiguidade 2: "Relacionamento"

**Confuso:**
"Receita se relaciona com ingrediente."

**Claro:**
- **Domínio gastronômico:** "Uma receita utiliza ingredientes (conceito culinário)."
- **Domínio do sistema:** "O registro REC-0089 referencia ING-0042 por identificador (conceito de integridade referencial)."

---

### Ambiguidade 3: "Estado"

**Confuso:**
"A receita está ativa."

**Claro:**
- **Domínio gastronômico:** "A receita é preparada regularmente (conhecimento em uso)."
- **Domínio do sistema:** "O registro REC-0089 está no estado 'ativo' do ciclo de vida (não arquivado)."

---

## Aplicação na Documentação

### Ao especificar Entidades

Sempre responder:

1. **Conceito gastronômico:** o que este conceito significa no mundo real da culinária?
2. **Conceito do sistema:** como o SOE-CCG modela este conceito como entidade?
3. **Mapeamento:** como um se traduz no outro?

---

### Exemplo: Ingrediente

**Domínio gastronômico:**
Ingrediente é qualquer insumo alimentício usado em preparações. Possui nome, origem, características (sólido/líquido), sazonalidade, etc.

**Domínio do sistema:**
Ingrediente é uma Entidade no SOE-CCG. Cada ingrediente é um Registro com identificador único (ING-XXXX), metadados padronizados, esquema versionado, e pode ser referenciado por Receitas e Execuções.

**Mapeamento:**
O conceito gastronômico "tomate italiano" é representado pelo registro `ING-0042` na entidade Ingrediente, obedecendo ao esquema v1 e ao template v1.

---

## Teste de Clareza

Ao escrever documentação, pergunte:

1. Estou falando do conceito culinário ou do conceito técnico do sistema?
2. Um desenvolvedor que não cozinha entende o conceito técnico?
3. Um chef que não programa entende o conceito gastronômico?

Se as respostas forem ambíguas, a separação de domínios está confusa.

---

## Resumo

| Aspecto | Domínio Gastronômico | Domínio do Sistema |
|---------|----------------------|--------------------|
| **O que é** | Conceitos culinários | Conceitos computacionais |
| **Existe onde** | Mundo real | Dentro do SOE-CCG |
| **Exemplos** | Ingrediente, receita, técnica | Registro, entidade, identificador, esquema |
| **Objetivo** | Conhecimento a preservar | Mecanismo de preservação |
| **Durabilidade** | Permanente (décadas, séculos) | Temporário (pode ser reimplementado) |
| **Especificado por** | Especialistas culinários | Arquitetos de sistema |

O SOE-CCG existe para servir o domínio gastronômico. O domínio gastronômico não se adapta ao sistema. O sistema se adapta ao domínio gastronômico.
