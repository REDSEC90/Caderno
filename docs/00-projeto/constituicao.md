# Constituição do SOE-CCG

> Autoridade máxima do Sistema de Registro, Organização, Evolução e Consulta de Conhecimento Gastronômico.

Todos os demais documentos, decisões e implementações deverão obedecer esta constituição.

---

## O que é conhecimento?

Conhecimento é toda informação sobre ingredientes, técnicas, equipamentos, receitas, execuções, experimentos e observações que possui valor permanente independentemente da tecnologia utilizada para armazená-la.

## O que é um registro?

Um registro é a unidade mínima de conhecimento. Todo registro possui identidade permanente, metadados padronizados e formato canônico em Markdown.

## O que é uma entidade?

Uma entidade é uma categoria de registro com definição, atributos, responsabilidades, restrições, relacionamentos e ciclo de vida próprios.

## O que é um relacionamento?

Um relacionamento é uma ligação entre dois registros, expressa sempre por identificadores permanentes, nunca por nomes.

## O que é uma versão?

Uma versão é um estado imutável de um registro em um momento específico. Versões anteriores nunca são destruídas.

## O que é um histórico?

Um histórico é o conjunto ordenado de todas as versões de um registro desde sua criação.

## O que é um identificador?

Um identificador é um código permanente atribuído a um registro no momento de sua criação. Nunca muda. Nunca é reutilizado.

## O que nunca pode mudar?

- O identificador de um registro.
- O histórico de versões.
- O formato canônico: Markdown.
- A separação entre conhecimento e implementação.

## O que pode evoluir?

- O nome de um registro.
- Os atributos de um registro.
- Os templates.
- Os esquemas, mediante versionamento explícito.
- A implementação técnica.

## Qual é a fonte oficial do conhecimento?

Os arquivos Markdown contidos em `dados/` são a fonte oficial e permanente do conhecimento.

O banco de dados SQLite é apenas um mecanismo de consulta derivado dessa fonte.

---

## Leis Fundamentais

1. Todo registro possui identificador permanente.
2. Todo registro possui metadados padronizados.
3. Todo conhecimento possui origem registrada.
4. Markdown é o formato canônico.
5. SQLite é apenas um mecanismo de consulta.
6. Nenhuma informação deve existir exclusivamente no banco de dados.
7. Toda alteração relevante gera histórico.
8. Relacionamentos utilizam identificadores, nunca nomes.
9. O conhecimento é permanente. A implementação é temporária.
10. Toda implementação é consequência do domínio. Nunca o contrário.
