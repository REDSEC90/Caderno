# Filosofia do SOE-CCG

> Axiomas fundamentais que governam todas as decisões do sistema.

---

## Axioma 1: Papel do Conhecimento

**Enunciado:**

Conhecimento gastronômico existe independentemente de qualquer sistema computacional. O SOE-CCG apenas o registra, organiza e preserva.

**Consequências:**

1. O conhecimento precede a implementação.
2. A perda de um sistema não pode causar perda de conhecimento.
3. Todo conhecimento deve ser representável em formato legível por humanos.
4. Nenhuma operação do sistema pode alterar o significado do conhecimento registrado.

**Implicação arquitetural:**

Markdown como formato canônico. Qualquer outro formato é derivado.

---

## Axioma 2: Fonte da Verdade

**Enunciado:**

Toda informação possui uma única localização oficial. Representações derivadas existem apenas para eficiência de consulta, nunca como origem.

**Consequências:**

1. Arquivos Markdown em `dados/` são a fonte oficial.
2. SQLite é índice derivado, não fonte.
3. Conflito entre Markdown e SQLite: Markdown prevalece sempre.
4. Toda informação no banco de dados deve ter origem rastreável no Markdown.

**Implicação arquitetural:**

Fluxo unidirecional: Markdown → Validador → SQLite. Nunca o contrário.

---

## Axioma 3: Papel do Markdown

**Enunciado:**

Markdown é o formato canônico porque é simultaneamente legível por humanos, processável por máquinas, versionável por sistemas de controle de versão e durável através de décadas.

**Consequências:**

1. Todo registro gastronômico deve ser representável em Markdown sem perda semântica.
2. Se uma informação não pode ser expressa em Markdown, ela não pertence ao conhecimento permanente.
3. Ferramentas podem ler Markdown. Ferramentas não podem exigir formatos proprietários.
4. O SOE-CCG sobrevive sem banco de dados. Não sobrevive sem Markdown.

**Implicação arquitetural:**

Qualquer feature que exija formato não-Markdown para funcionar é arquiteturalmente inválida.

---

## Axioma 4: Papel do SQLite

**Enunciado:**

SQLite é um **mecanismo de consulta**, não um armazenamento primário. Seu papel é acelerar buscas e relacionamentos, não preservar conhecimento.

**Consequências:**

1. O banco de dados pode ser destruído e reconstruído a partir do Markdown sem perda.
2. Nenhuma informação pode existir exclusivamente no banco de dados.
3. Sincronização ocorre de Markdown para SQLite, nunca o inverso.
4. SQLite é opcional. Um sistema que apenas lê Markdown já é funcional, embora lento.

**Implicação arquitetural:**

O sistema possui duas camadas independentes:
- Camada de preservação (Markdown)
- Camada de consulta (SQLite)

A primeira pode existir sem a segunda. A segunda não pode existir sem a primeira.

---

## Axioma 5: Papel da Implementação

**Enunciado:**

Implementação é temporária. Conhecimento é permanente. Toda decisão arquitetural deve favorecer a durabilidade do conhecimento sobre a conveniência da implementação.

**Consequências:**

1. Tecnologias mudam. Formatos de arquivo mudam. O conhecimento registrado não muda.
2. Se uma biblioteca, linguagem ou framework desaparecer, o conhecimento permanece acessível.
3. Conveniência para desenvolvedores é secundária. Preservação para décadas é primária.
4. Features que facilitam implementação mas comprometem preservação são inaceitáveis.

**Implicação arquitetural:**

Escolhas técnicas priorizam:
1. Formatos abertos sobre proprietários
2. Padrões amplamente suportados sobre otimizações específicas
3. Legibilidade humana sobre compactação binária
4. Simplicidade sobre performance

---

## Consequências Filosóficas

### 1. O Sistema Não Cria Conhecimento

O SOE-CCG não inventa receitas, ingredientes ou técnicas. Ele registra o que já existe ou foi criado por humanos.

Implicação: metadados de autoria e origem são obrigatórios.

### 2. O Sistema Não Interpreta Conhecimento

O SOE-CCG não decide se uma receita é "boa" ou "ruim". Ele registra observações que humanos fazem.

Implicação: avaliações e opiniões são Observações, não propriedades de Receitas.

### 3. O Sistema Não Impede Evolução

Se uma entidade precisa de um campo que não existe, o esquema deve evoluir, não o conhecimento ser descartado.

Implicação: versionamento de esquemas é obrigatório e compatibilidade retroativa é prioritária.

### 4. O Sistema Não Depende de Contexto Externo

Um registro deve ser compreensível por si só. Dependências externas (links quebrados, referências a sistemas terceiros) comprometem durabilidade.

Implicação: tudo que é essencial deve estar dentro do sistema. Referências externas são opcionais.

### 5. A Implementação Serve o Domínio

Código não define o que é uma Receita. O domínio gastronômico define. O código apenas implementa essa definição.

Implicação: domínio é especificado antes do código. Código que contraria domínio está errado, não o domínio.

---

## Teste Filosófico

Toda decisão arquitetural deve responder:

1. **Preservação**: se esta tecnologia desaparecer, o conhecimento permanece acessível?
2. **Independência**: o conhecimento pode ser lido sem este sistema?
3. **Durabilidade**: daqui a 20 anos, esta escolha ainda faz sentido?
4. **Prioridade**: esta decisão favorece conhecimento ou implementação?

Se qualquer resposta for insatisfatória, a decisão contraria a filosofia.

---

## Relação com a Constituição

A Constituição deriva desta filosofia.

As 10 Leis Fundamentais são consequências diretas destes 5 axiomas.

Toda política, padrão e implementação deve obedecer:

```
Filosofia → Constituição → Governança → Especificações → Implementação
```

Contradição filosófica é o erro mais grave possível no SOE-CCG. Mais grave que bugs, mais grave que performance, mais grave que conveniência.

Filosofia é imutável. Tudo o resto pode evoluir.
