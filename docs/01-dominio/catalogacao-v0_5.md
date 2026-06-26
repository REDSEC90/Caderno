# Catalogação do SOE-CCG

Catalogação é o processo de classificar e organizar registros por meio de categorias, tags e atributos controlados.

---

## Princípios

- Catalogação nunca altera o registro original.
- Categorias e tags são aplicadas por referência.
- Um registro pode pertencer a múltiplas categorias.
- Catálogos controlados evitam duplicação semântica.

---

## Instrumentos de Catalogação

### Categorias

Agrupamentos hierárquicos e semânticos.

Definidos em `docs/01-dominio/catalogos/categorias.md`.

Exemplos: `confeitaria`, `técnicas-de-base`, `laticínios`.

### Tags

Rótulos livres para classificação transversal.

Definidas nos metadados de cada registro.

Exemplos: `sem-gluten`, `rapido`, `alta-precisao`.

### Status

Estado atual do registro dentro de seu ciclo de vida.

Definido em `docs/01-dominio/ciclo-de-vida.md`.

### Origem

Indica a procedência do conhecimento: próprio, adaptado, referência externa.

---

## Catálogos Controlados

Os catálogos controlados são listas de valores válidos que alimentarão tabelas no banco de dados.

Localização: `docs/01-dominio/catalogos/`

| Arquivo                  | Conteúdo                          |
|--------------------------|-----------------------------------|
| `categorias.md`          | Categorias disponíveis            |
| `unidades-medida.md`     | Unidades de medida aceitas        |
| `tipos-ingredientes.md`  | Classificação de ingredientes     |
| `tipos-tecnicas.md`      | Classificação de técnicas         |
| `tipos-equipamentos.md`  | Classificação de equipamentos     |
| `estados-receita.md`     | Estados válidos do ciclo de vida  |
