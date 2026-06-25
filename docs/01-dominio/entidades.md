# Entidades do SOE-CCG

As entidades são as categorias fundamentais de conhecimento do sistema.

Cada entidade possui definição, responsabilidades, atributos, restrições, relacionamentos e ciclo de vida próprios.

---

## Receita

**Definição:** Conjunto de conhecimento que descreve um prato ou preparação.

**Responsabilidade:** Representar o conhecimento, não um preparo específico.

**Relacionamentos:** possui Execuções, referencia Ingredientes, Técnicas e Equipamentos.

---

## Execução

**Definição:** Registro de um preparo real de uma receita em um momento específico.

**Responsabilidade:** Capturar o que aconteceu, não o que deveria acontecer.

**Relacionamentos:** pertence a uma Receita, pode conter Observações.

---

## Ingrediente

**Definição:** Insumo utilizado em receitas e execuções.

**Responsabilidade:** Ser uma entidade reutilizável e referenciável por múltiplas receitas.

**Relacionamentos:** referenciado por Receitas e Execuções.

---

## Técnica

**Definição:** Método ou procedimento culinário aplicável em preparações.

**Responsabilidade:** Centralizar o conhecimento sobre um procedimento para evitar duplicação.

**Relacionamentos:** referenciada por Receitas e Execuções.

---

## Equipamento

**Definição:** Utensílio ou aparelho utilizado no preparo de receitas.

**Responsabilidade:** Ser uma entidade reutilizável e referenciável.

**Relacionamentos:** referenciado por Receitas e Execuções.

---

## Observação

**Definição:** Nota, percepção ou descoberta vinculada a qualquer entidade.

**Responsabilidade:** Registrar conhecimento informal que não cabe em outros campos.

**Relacionamentos:** pode estar vinculada a qualquer entidade.

---

## Experimento

**Definição:** Tentativa deliberada de testar ou desenvolver conhecimento novo.

**Responsabilidade:** Registrar o processo de criação e evolução do conhecimento.

**Relacionamentos:** pode originar Receitas, pode conter Observações.

---

## Categoria

**Definição:** Agrupamento semântico utilizado para organizar entidades.

**Responsabilidade:** Facilitar navegação e consulta sem alterar os registros categorizados.

**Relacionamentos:** pode ser aplicada a Receitas, Ingredientes, Técnicas e Equipamentos.
