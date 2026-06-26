# Escopo do SOE-CCG

## Dentro do Escopo

- Registro e versionamento de receitas como conhecimento.
- Registro de execuções vinculadas a receitas.
- Catalogação de ingredientes, técnicas e equipamentos.
- Registro de observações e experimentos.
- Relacionamento entre entidades por identificadores permanentes.
- Preservação permanente do histórico de todos os registros.
- Exportação e importação de conhecimento em Markdown.
- Consulta via SQLite como mecanismo derivado.

## Fora do Escopo

- Interface gráfica (fase atual).
- API pública (fase atual).
- Compartilhamento ou sincronização em nuvem.
- Funcionalidades sociais ou colaborativas.
- Planejamento de cardápios ou listas de compras.

## Fronteiras do Sistema

O SOE-CCG opera localmente.

O conhecimento reside em arquivos Markdown dentro de `dados/`.

O banco de dados SQLite é gerado a partir desses arquivos e pode ser reconstruído a qualquer momento.

Nenhuma funcionalidade do sistema depende exclusivamente do banco de dados.
