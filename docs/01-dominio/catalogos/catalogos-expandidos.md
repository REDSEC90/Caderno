# Catálogos Expandidos do SOE-CCG

> Valores padronizados faltantes: Classificações, Escalas, Materiais, Métodos e Vocabulário Controlado.

---

## Catálogo: Classificações de Receitas

Classificações complementam as categorias, indicando características transversais de uma Receita.

| Código | Classificação | Descrição |
|--------|--------------|-----------|
| `CLS-VEGET` | Vegetariano | Sem carnes ou derivados de abate |
| `CLS-VEGANO` | Vegano | Sem produtos de origem animal |
| `CLS-GLUTEN` | Sem glúten | Não contém glúten |
| `CLS-LACTOSE` | Sem lactose | Não contém lactose |
| `CLS-JEJUM` | Jejum intermitente | Compatível com protocolos de jejum |
| `CLS-BAIXO-CAL` | Baixa caloria | Menos de 300kcal por porção |
| `CLS-LOW-CARB` | Low-carb | Baixo teor de carboidratos |
| `CLS-FUNCIONAL` | Funcional | Ingredientes com propriedade funcional reconhecida |
| `CLS-CONGELAVEL` | Congelável | Pode ser congelado sem perda significativa |
| `CLS-CONSERVA` | Conserva | Preservação prolongada por processo químico ou físico |
| `CLS-FERMENTADO` | Fermentado | Processo de fermentação como etapa central |
| `CLS-CRIANCA` | Para crianças | Adaptado para público infantil |
| `CLS-RAPIDO` | Rápido | Pronto em até 30 minutos |
| `CLS-ECONOMICO` | Econômico | Ingredientes acessíveis e custo baixo |
| `CLS-GOURMET` | Gourmet | Ingredientes premium ou técnica elaborada |

---

## Catálogo: Escalas de Avaliação

Valores padronizados para campos de avaliação em Execuções.

### Escala numérica (1–10)

Usada nos campos `avaliacao-sabor`, `avaliacao-textura`, `avaliacao-aparencia`, `avaliacao-geral`.

| Valor | Interpretação |
|-------|---------------|
| 1–2 | Inaceitável — não repetir |
| 3–4 | Insatisfatório — alterações necessárias |
| 5–6 | Aceitável — melhorias desejáveis |
| 7–8 | Bom — resultado satisfatório |
| 9–10 | Excelente — referência para futuras execuções |

### Escala descritiva de dificuldade

Usada no campo `dificuldade` de Receitas.

| Valor | Interpretação |
|-------|---------------|
| `baixa` | Executável por iniciantes; sem técnicas complexas; menos de 30 min de atenção ativa |
| `media` | Requer alguma experiência; 1–2 técnicas específicas; entre 30 min e 2h |
| `alta` | Requer habilidade culinária; técnicas precisas; mais de 2h ou múltiplas etapas críticas |

### Escala de relevância

Usada no campo `relevancia` de Observações.

| Valor | Interpretação |
|-------|---------------|
| `baixa` | Curiosidade ou detalhe menor, improvável impacto em futuras execuções |
| `media` | Informação útil que pode influenciar ajustes pontuais |
| `alta` | Descoberta relevante que deve ser considerada em qualquer futura execução |

---

## Catálogo: Materiais de Equipamentos

Valores padronizados para o campo `material` de Equipamentos.

| Código | Material |
|--------|----------|
| `MAT-ACO-INOX` | Aço inoxidável |
| `MAT-FERRO-FUND` | Ferro fundido |
| `MAT-ALUMINIO` | Alumínio |
| `MAT-TEFLON` | Antiaderente (teflon) |
| `MAT-CERAMICA` | Cerâmica |
| `MAT-VIDRO` | Vidro |
| `MAT-PLASTICO` | Plástico/polímero |
| `MAT-MADEIRA` | Madeira |
| `MAT-SILICONE` | Silicone |
| `MAT-COBRE` | Cobre |
| `MAT-BARRO` | Barro/argila |
| `MAT-PEDRA` | Pedra |

---

## Catálogo: Métodos Culinários

Valores padronizados para contextualizar Técnicas por método geral de preparo.

| Código | Método | Descrição |
|--------|--------|-----------|
| `MET-CALOR-SECO` | Calor seco | Assar, grelhar, tostar — sem líquido |
| `MET-CALOR-UMIDO` | Calor úmido | Cozinhar, vaporizar, escalfar — com líquido ou vapor |
| `MET-FRITURA` | Fritura | Imersão em óleo quente (funda ou superficial) |
| `MET-FERMENTACAO` | Fermentação | Transformação por microrganismos |
| `MET-EMULSIFICACAO` | Emulsificação | Mistura estável de líquidos imiscíveis |
| `MET-REDUCAO` | Redução | Evaporação de líquido por calor para concentrar |
| `MET-GELIFICACAO` | Gelificação | Solidificação por agente gelificante ou temperatura |
| `MET-CURAR` | Cura | Preservação por sal, açúcar, fumaça ou combinações |
| `MET-MARINAR` | Marinada | Imersão em líquido aromatizante por tempo |
| `MET-FRIO` | Preparo a frio | Sem aplicação de calor |
| `MET-MISTO` | Método misto | Combinação de dois ou mais métodos |

---

## Catálogo: Estados Complementares

### Estados de Ingrediente (complementa `ciclo-de-vida.md`)

| Estado | Significado |
|--------|-------------|
| `ativo` | Disponível para referência |
| `descontinuado` | Não mais recomendado para novos registros, mantido para histórico |
| `arquivado` | Fora de uso, preservado |

### Estados de Experimento

| Estado | Significado |
|--------|-------------|
| `aberto` | Em andamento |
| `concluido` | Finalizado com resultado documentado |
| `incorporado` | Resultado absorvido por Receita ou entidade |
| `descartado` | Concluído sem aproveitamento, mantido no histórico |

### Estados de Observação

| Estado | Significado |
|--------|-------------|
| `ativo` | Válida e consultável |
| `arquivado` | Superada ou inválida, preservada |
| `obsoleto` | Substituída por versão mais precisa, estado final |

---

## Vocabulário Controlado

Termos padronizados para uso em Tags, evitando proliferação de variantes.

### Tags de contexto temporal

| Tag | Uso |
|-----|-----|
| `inverno` | Preparo ou ingrediente típico de inverno |
| `verao` | Preparo ou ingrediente típico de verão |
| `natal` | Relacionado a culinária natalina |
| `pascoa` | Relacionado a culinária pascal |
| `festa` | Adequado para celebrações |
| `cotidiano` | Para o dia a dia |
| `fim-de-semana` | Preparo adequado para fins de semana |

### Tags de origem culinária

| Tag | Uso |
|-----|-----|
| `brasileira` | Culinária brasileira |
| `italiana` | Culinária italiana |
| `francesa` | Culinária francesa |
| `japonesa` | Culinária japonesa |
| `mineira` | Culinária de Minas Gerais |
| `nordestina` | Culinária do Nordeste brasileiro |
| `caseira` | Culinária doméstica, sem origem regional específica |

### Tags de tipo de preparo

| Tag | Uso |
|-----|-----|
| `doce` | Sabor predominantemente doce |
| `salgado` | Sabor predominantemente salgado |
| `entrada` | Servido como entrada |
| `sobremesa` | Servido como sobremesa |
| `bebida` | Preparação líquida para consumo |
| `molho` | Preparação complementar |
| `conserva` | Preservação de alimentos |
| `panificacao` | Pães, bolos e produtos assados |
| `confeitaria` | Doces e sobremesas elaboradas |

### Tags de experiência pessoal

| Tag | Uso |
|-----|-----|
| `favorito` | Receita ou preparo favorito |
| `a-repetir` | Vale repetir em breve |
| `a-melhorar` | Resultado satisfatório mas com espaço para melhoria |
| `a-experimentar` | Ainda não executado, deseja tentar |
| `referencia` | Referência técnica ou de qualidade |

---

## Nota sobre Evolução dos Catálogos

Catálogos são extensíveis mas fechados no momento da definição formal. Para adicionar novos valores:

1. Propor adição com justificativa.
2. Verificar que não há valor existente que atenda.
3. Seguir a convenção de codificação do catálogo.
4. Atualizar o catálogo com versão incrementada.
5. Documentar a adição no histórico de mudanças.

Valores nunca são removidos de catálogos — apenas marcados como `[DEPRECADO]`.
