# Diagrama Mestre

Visão geral da arquitetura do SOE-CCG.

---

## Camadas do Sistema

```
┌─────────────────────────────────────────────────────┐
│                      AUTOR                          │
└─────────────────────┬───────────────────────────────┘
                      │ escreve
                      ▼
┌─────────────────────────────────────────────────────┐
│                  dados/                             │
│         (Markdown — fonte oficial)                  │
│                                                     │
│  receitas/      execucoes/     ingredientes/        │
│  tecnicas/      equipamentos/  observacoes/         │
│  experimentos/  anexos/        importacao/          │
└─────────────────────┬───────────────────────────────┘
                      │ lê e valida
                      ▼
┌─────────────────────────────────────────────────────┐
│               IMPORTADOR                            │
│         (scripts/importacao/)                       │
└─────────────────────┬───────────────────────────────┘
                      │ insere
                      ▼
┌─────────────────────────────────────────────────────┐
│               banco_de_dados/                       │
│         (SQLite — mecanismo de consulta)            │
└─────────────────────┬───────────────────────────────┘
                      │ consulta
                      ▼
┌─────────────────────────────────────────────────────┐
│                  codigo/                            │
│              (regras e lógica)                      │
└─────────────────────┬───────────────────────────────┘
                      │ expõe
                      ▼
┌─────────────────────────────────────────────────────┐
│               INTERFACE / API                       │
│              (fase futura)                          │
└─────────────────────────────────────────────────────┘
```

---

## Estrutura de Diretórios

```
SOE-CCG/
│
├── README.md
├── LICENSE
│
├── docs/
│   ├── 00-projeto/
│   ├── 01-dominio/
│   ├── 02-arquitetura/
│   ├── 03-modelagem/
│   ├── 04-padroes/
│   ├── 05-desenvolvimento/
│   ├── 06-operacao/
│   ├── 98-rascunhos/
│   └── 99-referencias/
│
├── dados/
│   ├── receitas/
│   ├── execucoes/
│   ├── ingredientes/
│   ├── tecnicas/
│   ├── equipamentos/
│   ├── observacoes/
│   ├── experimentos/
│   ├── anexos/
│   └── importacao/
│
├── banco_de_dados/
│   ├── esquemas/
│   ├── migracoes/
│   ├── seeds/
│   └── sqlite/
│
├── scripts/
│   ├── importacao/
│   ├── instalacao/
│   ├── copia_seguranca/
│   └── manutencao/
│
├── codigo/
├── testes/
└── recursos/
    ├── imagens/
    ├── videos/
    ├── audios/
    └── documentos/
```

---

## Lei Arquitetural

O banco de dados pode ser destruído e reconstruído a qualquer momento.

O conhecimento em `dados/` nunca pode ser destruído.
