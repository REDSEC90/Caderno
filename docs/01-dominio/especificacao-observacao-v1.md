# Especificação de Entidade: Observação

> Aplicação do template canônico à entidade Observação do SOE-CCG.

---

## 1. Identidade

**Definição formal:**
Observação é o registro de uma percepção, descoberta, nota ou aprendizado vinculado a qualquer entidade do sistema, capturando conhecimento informal que não cabe nos campos estruturados de outras entidades.

**Categoria gastronômica:**
Na culinária, observações são insights que surgem durante ou após o preparo: "o bicarbonato acelerou o processo", "fogo baixo produziu resultado mais uniforme", "sal no fim realçou o sabor diferentemente". São o conhecimento emergente que transforma cozinheiros em especialistas.

**Categoria no sistema:**
Observação é uma entidade de anotação livre com identificador `OBS-NNNNNN` que pode ser vinculada a Receitas, Execuções, Ingredientes, Técnicas ou Equipamentos.

---

## 2. Responsabilidade

**Propósito principal:**
Capturar conhecimento qualitativo que surge da experiência prática sem forçar estrutura artificial sobre ele.

**Responsabilidades explícitas:**
- Registrar percepções, conclusões e aprendizados.
- Vincular insight ao contexto que o gerou.
- Acumular conhecimento tácito ao longo do tempo.
- Servir de base para evolução de Receitas e descoberta de padrões.

---

## 3. Limites

**Esta entidade NÃO:**
- Registra dados estruturados de uma execução (isso pertence a Execução).
- Substitui a evolução formal de uma Receita (mudanças de formulação geram nova versão da Receita).
- É obrigatória — Receitas e Execuções existem independentemente de Observações.

**Fronteira com Execução:**
Execução registra o que aconteceu (fatos, métricas). Observação registra o que se aprendeu ou percebeu. Uma Execução tem estrutura rígida; uma Observação é livre.

**Fronteira com Experimento:**
Observação é passiva — registra o que foi percebido. Experimento é ativo — registra uma tentativa deliberada de testar hipótese. Uma Observação pode inspirar um Experimento; um Experimento pode gerar Observações.

---

## 4. Atributos

Referência ao esquema: `docs/01-dominio/esquemas/esquema-observacao-v1.md`

**Campos obrigatórios:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente. Formato: `OBS-NNNNNN` |
| `tipo` | string | Valor fixo: `observacao` |
| `schema-version` | string | Versão do esquema |
| `versao` | string | Versão do registro |
| `status` | string | Estado do ciclo de vida |
| `criado-em` | date | Data de criação |
| `atualizado-em` | date | Data da última atualização |
| `autor` | string | Identificador do autor |
| `conteudo` | text | O texto da observação |

**Campos opcionais:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `entidade-referenciada` | string | ID da entidade sobre a qual a observação se refere |
| `tipo-entidade` | string | Tipo da entidade referenciada (`receita`, `execucao`, `ingrediente`, `tecnica`, `equipamento`) |
| `contexto` | text | Situação em que a observação surgiu |
| `tags` | list | Marcadores livres |
| `relevancia` | string | `baixa`, `media`, `alta` |

---

## 5. Estados

| Estado | Significado |
|--------|-------------|
| `ativo` | Observação válida e consultável |
| `arquivado` | Observação superada ou inválida, preservada no histórico |
| `obsoleto` | Substituída por versão mais precisa |

---

## 6. Relacionamentos

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| `sobre` | Receita | N:1 | Observação pode se referir a uma Receita |
| `sobre` | Execução | N:1 | Observação pode se referir a uma Execução |
| `sobre` | Ingrediente | N:1 | Observação pode se referir a um Ingrediente |
| `sobre` | Técnica | N:1 | Observação pode se referir a uma Técnica |
| `sobre` | Equipamento | N:1 | Observação pode se referir a um Equipamento |

---

## 7. Restrições

1. O `id` é imutável após criação.
2. Uma Observação pode existir sem referenciar nenhuma entidade (observação geral).
3. O `conteudo` deve ser suficientemente descritivo para ser compreensível sem contexto adicional.
4. Observações não exigem revisão — tornam-se ativas automaticamente ao serem criadas.

---

## 8. Ciclo de Vida

**Nascimento:** Nasce quando o usuário registra uma percepção. Campo mínimo: `conteudo`. Nasce como `ativo`.

**Evolução:** Observações são raramente editadas. Quando uma observação está errada, ela é arquivada e uma nova é criada.

**Arquivamento:** Observação arquivada quando superada por novo aprendizado ou quando identificada como imprecisa.
