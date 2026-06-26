# Decisão Arquitetural: Motor de Conhecimento

## Status

Aceita

## Identificador

ADR-0001

## Data

2026

---

# Contexto

Durante a definição da arquitetura do Caderno foi identificado que o projeto não deve ser modelado como um sistema de receitas, catálogo ou armazenamento de documentos.

Receitas representam apenas um dos possíveis domínios de conhecimento suportados pelo sistema.

O objetivo de longo prazo do projeto é permitir que diferentes tipos de conhecimento sejam armazenados, relacionados, pesquisados, versionados e evoluídos de forma uniforme.

Exemplos:

* Receitas
* Ingredientes
* Técnicas
* Equipamentos
* Procedimentos
* Fórmulas
* Referências
* Projetos
* Inventários
* Conhecimentos técnicos
* Conhecimentos científicos

Foi concluído que a arquitetura deve ser centrada em conhecimento e não em tipos específicos de conteúdo.

---

# Decisão

O núcleo do Caderno será um componente denominado:

Motor de Conhecimento

Toda informação inserida no sistema deverá passar pelo Motor de Conhecimento antes de ser persistida.

O Motor de Conhecimento será responsável por:

* Interpretar informações recebidas.
* Identificar entidades.
* Identificar relacionamentos.
* Reutilizar entidades existentes.
* Criar novas entidades quando necessário.
* Versionar alterações.
* Persistir conhecimento estruturado.

O banco de dados não armazenará apenas documentos.

O banco de dados armazenará uma rede de conhecimento composta por entidades e relacionamentos.

---

# Princípio Fundamental

O Caderno não armazena documentos.

O Caderno converte informação em conhecimento estruturado.

---

# Modelo Conceitual

Informação Bruta

↓

Motor de Conhecimento

↓

Entidades

*

Relacionamentos

↓

Banco de Conhecimento

↓

Consulta

---

# Fluxo Geral

Usuário

↓

Informação

↓

Validação

↓

Interpretação

↓

Extração de Entidades

↓

Detecção de Relacionamentos

↓

Persistência

↓

Consulta

---

# Exemplo

Entrada:

Pão Francês

Ingredientes:

* Farinha
* Água
* Fermento

Técnicas:

* Fermentação
* Sova

Equipamentos:

* Forno

---

Saída Estruturada:

Entidades:

* Pão Francês
* Farinha
* Água
* Fermento
* Fermentação
* Sova
* Forno

Relacionamentos:

* Pão Francês usa Farinha
* Pão Francês usa Água
* Pão Francês usa Fermento
* Pão Francês aplica Fermentação
* Pão Francês aplica Sova
* Pão Francês utiliza Forno

---

# Entidades

Entidades representam conceitos.

Exemplos:

* Receita
* Ingrediente
* Técnica
* Equipamento
* Procedimento
* Referência

Toda entidade possui:

* ID
* Tipo
* Título
* Descrição
* Metadados
* Data de Criação
* Data de Atualização
* Versão

---

# Relacionamentos

Relacionamentos representam conexões entre entidades.

Exemplos:

* usa
* aplica
* contém
* pertence
* referencia
* deriva

Estrutura:

Entidade A

↓

Relacionamento

↓

Entidade B

---

# Reutilização de Conhecimento

Antes de criar uma nova entidade o sistema deve verificar se ela já existe.

Exemplo:

Receita:

Bolo de Cenoura

Ingrediente:

Ovo

Se Ovo já existir:

Criar relacionamento.

Se Ovo não existir:

Criar entidade e relacionamento.

---

# Evolução de Conhecimento

Toda alteração deverá preservar histórico.

Exemplo:

Receita v1

↓

Receita v2

↓

Receita v3

Nenhuma informação deve ser perdida.

---

# Arquitetura Física Atual

.

├── banco_de_dados
├── codigo
├── dados
├── docs
├── scripts
└── testes

---

# Arquitetura Física Futura

.

├── banco_de_dados
│   ├── dados_iniciais
│   ├── esquemas
│   ├── migracoes
│   └── sqlite
│
├── codigo
│   └── caderno
│       ├── motor_de_conhecimento
│       │   ├── validacao
│       │   ├── interpretacao
│       │   ├── entidades
│       │   ├── relacionamentos
│       │   ├── historico
│       │   └── persistencia
│       │
│       ├── importacao
│       ├── exportacao
│       ├── busca
│       ├── extensoes
│       └── interface
│
├── dados
│   ├── importacao
│   ├── exportacao
│   ├── anexos
│   ├── imagens
│   └── temporario
│
├── docs
│
├── scripts
│
└── testes

---

# Componentes do Motor de Conhecimento

## Validação

Verifica integridade da entrada.

Responsabilidades:

* Campos obrigatórios
* Estrutura mínima
* Formatos aceitos

---

## Interpretação

Converte informação bruta em estrutura compreensível.

Responsabilidades:

* Identificação de tipos
* Classificação inicial

---

## Entidades

Gerencia conceitos persistentes.

Responsabilidades:

* Criação
* Atualização
* Reutilização

---

## Relacionamentos

Gerencia conexões entre entidades.

Responsabilidades:

* Criação
* Atualização
* Consulta

---

## Histórico

Gerencia evolução do conhecimento.

Responsabilidades:

* Versionamento
* Auditoria
* Recuperação

---

## Persistência

Responsável pela gravação definitiva.

Responsabilidades:

* SQLite
* Transações
* Integridade

---

# Visão de Longo Prazo

O Motor de Conhecimento deve ser independente do domínio.

O motor não deve conhecer receitas.

O motor não deve conhecer culinária.

O motor deve conhecer apenas:

* Entidades
* Relacionamentos
* Metadados
* Histórico

Novos domínios devem ser adicionados sem alterar o núcleo do sistema.

---

# Consequências

Benefícios:

* Alta escalabilidade conceitual.
* Reutilização de conhecimento.
* Expansão para novos domínios.
* Estrutura uniforme.
* Histórico consistente.
* Base para extensões futuras.

Custos:

* Modelagem inicial mais complexa.
* Necessidade de arquitetura bem definida.
* Necessidade de modelagem cuidadosa dos relacionamentos.

---

# Conclusão

O Caderno será desenvolvido como um sistema centrado em conhecimento.

Receitas representam apenas o primeiro domínio suportado.

O Motor de Conhecimento passa a ser o núcleo arquitetural do projeto e toda funcionalidade futura deverá ser compatível com este princípio.

