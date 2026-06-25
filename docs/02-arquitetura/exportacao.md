# Exportação

Define como o conhecimento do SOE-CCG pode ser exportado.

---

## Princípio

O conhecimento já existe em formato exportável por natureza.

Os arquivos Markdown em `dados/` são o formato canônico e portável.

Exportação é o processo de selecionar, organizar e empacotar esse conhecimento para uso externo.

---

## Formatos de Exportação

| Formato    | Descrição                                              |
|------------|--------------------------------------------------------|
| Markdown   | Cópia direta de arquivos de `dados/`                   |
| JSON       | Derivado do SQLite, útil para integração               |
| CSV        | Derivado do SQLite, útil para planilhas                |
| ZIP        | Pacote de arquivos Markdown para portabilidade total   |

---

## Escopos de Exportação

- Exportação total: todos os registros de todas as entidades.
- Exportação por tipo: todos os registros de uma entidade específica.
- Exportação por filtro: registros selecionados por categoria, tag ou status.
- Exportação de um único registro: por ID.

---

## Regras

- Exportação nunca remove nem altera registros originais.
- Exportações em Markdown são sempre fiéis ao arquivo original.
- Exportações em JSON e CSV são derivadas do SQLite e podem ser recriadas.
- O formato Markdown é o único que garante portabilidade total e independência tecnológica.
