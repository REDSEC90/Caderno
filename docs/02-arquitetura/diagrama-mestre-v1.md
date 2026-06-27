╔══════════════════════════════════════════════════════════════╗
║                         CADERNO                             ║
║              Sistema de Conhecimento Estruturado            ║
╚══════════════════════════════════════════════════════════════╝

Missão:
    Armazenar, organizar, relacionar, pesquisar,
    preservar e evoluir conhecimento.

Princípio Fundamental:

    Tudo é Conhecimento.

        Receita
        Ingrediente
        Técnica
        Equipamento
        Procedimento
        Referência
        Fórmula
        Anotação

    são apenas diferentes formas de conhecimento.


═══════════════════════════════════════════════════════════════
                     VISÃO GERAL DO SISTEMA
═══════════════════════════════════════════════════════════════


                  ┌───────────────────┐
                  │     USUÁRIO       │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │     CADERNO       │
                  └─────────┬─────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼

  Armazenar         Relacionar          Consultar

         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼

                 Conhecimento Organizado



═══════════════════════════════════════════════════════════════
                   MODELO CONCEITUAL
═══════════════════════════════════════════════════════════════


                    ┌──────────────┐
                    │Conhecimento  │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼

    Receita         Ingrediente         Técnica

        │                  │                  │
        └──────────┬───────┴──────────┬───────┘
                   │                  │
                   ▼                  ▼

              Equipamento       Referência


Todo objeto armazenado é um registro.

Todo registro possui:

    ID
    Tipo
    Título
    Descrição
    Metadados
    Relacionamentos
    Histórico



═══════════════════════════════════════════════════════════════
                 ARQUITETURA FÍSICA
═══════════════════════════════════════════════════════════════


Projeto
│
├── banco_de_dados
├── codigo
├── dados
├── docs
├── scripts
└── testes



═══════════════════════════════════════════════════════════════
                  FLUXO DE ENTRADA
═══════════════════════════════════════════════════════════════


              Usuário fornece informação
                           │
                           ▼

                 Informação Bruta
                           │
                           ▼

                      Validação
                           │
                           ▼

                    Estruturação
                           │
                           ▼

                  Registro Interno
                           │
                           ▼

                   Banco de Dados



Exemplos:

Receita
Texto
JSON
Markdown
Importação
Extensão



═══════════════════════════════════════════════════════════════
                 FLUXO DE CONHECIMENTO
═══════════════════════════════════════════════════════════════


Receita
│
├── utiliza Ingrediente
├── utiliza Técnica
├── utiliza Equipamento
└── pertence Categoria



Exemplo:


Pão Francês
│
├── Farinha
├── Água
├── Fermentação
├── Sova
└── Forno


O sistema não armazena apenas texto.

O sistema armazena relações.



═══════════════════════════════════════════════════════════════
                   FLUXO DE CONSULTA
═══════════════════════════════════════════════════════════════


Pesquisa
│
▼

Motor de Busca
│
▼

Banco de Dados
│
▼

Relacionamentos
│
▼

Resultados



Exemplos:


"O que usa fermentação?"

      ▼

Receitas encontradas
Técnicas encontradas
Ingredientes relacionados



═══════════════════════════════════════════════════════════════
                 FLUXO DE EVOLUÇÃO
═══════════════════════════════════════════════════════════════


Registro
│
▼

Edição
│
▼

Nova Versão
│
▼

Histórico


Exemplo:


Receita v1
   │
   ▼
Receita v2
   │
   ▼
Receita v3


Nenhuma informação é perdida.



═══════════════════════════════════════════════════════════════
                FLUXO DE IMPORTAÇÃO
═══════════════════════════════════════════════════════════════


Arquivo
│
├── JSON
├── CSV
├── Markdown
└── YAML
│
▼

Importador
│
▼

Validador
│
▼

Conversor
│
▼

Registro Interno



═══════════════════════════════════════════════════════════════
                FLUXO DE EXPORTAÇÃO
═══════════════════════════════════════════════════════════════


Registro
│
▼

Exportador
│
├── JSON
├── Markdown
├── HTML
└── PDF
│
▼

Arquivo Final



═══════════════════════════════════════════════════════════════
                    VISÃO FUTURA
═══════════════════════════════════════════════════════════════


                     Núcleo
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼

   Receitas      Inventário       Conhecimento

      │                 │                 │

      ▼                 ▼                 ▼

   Extensões       Extensões       Extensões



═══════════════════════════════════════════════════════════════
                    PRINCÍPIO FINAL
═══════════════════════════════════════════════════════════════


O Caderno não armazena arquivos.

O Caderno não armazena páginas.

O Caderno não armazena textos.

O Caderno armazena conhecimento estruturado.

Conhecimento pode ser criado,
relacionado,
pesquisado,
evoluído,
exportado
e preservado.
