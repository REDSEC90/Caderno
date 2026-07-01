# Ciclo do Conhecimento — SOE-CCG

**Modelo Científico de Evolução do Conhecimento Gastronômico**

---

## 🔬 Ciclo Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    CICLO DO CONHECIMENTO                     │
└─────────────────────────────────────────────────────────────┘

1. OBSERVAÇÃO
   ↓
   "O doce de leite ficou muito escuro"
   OBS-000015
   ↓

2. HIPÓTESE
   ↓
   "Fogo alto demais causa caramelização excessiva
    e escurecimento não desejado"
   ↓

3. EXPERIMENTO
   ↓
   EXP-000042: Testar fogo baixo vs fogo médio
   Variáveis: temperatura, tempo, cor final
   ↓

4. EXECUÇÕES (evidência)
   ↓
   EXE-000123: Fogo baixo, 2h → cor âmbar (ideal)
   EXE-000124: Fogo médio, 1h30 → cor escura
   EXE-000125: Fogo baixo, 2h → cor âmbar (confirma)
   ↓

5. VALIDAÇÃO
   ↓
   Análise: 2 de 3 execuções com fogo baixo = sucesso
   Conclusão: Fogo baixo é consistentemente melhor
   ↓

6. ATUALIZAÇÃO DA RECEITA
   ↓
   REC-000001-v2:
   - Fogo baixo (não médio ou alto)
   - Tempo: ~2h
   - Resultado esperado: cor âmbar
   - Referência: EXP-000042
   ↓

7. NOVAS EXECUÇÕES
   ↓
   EXE-000156: Seguindo v2 → sucesso
   EXE-000157: Seguindo v2 → sucesso
   EXE-000158: Seguindo v2 → sucesso
   ↓

8. NOVAS OBSERVAÇÕES
   ↓
   OBS-000087: "Fogo baixo também evita queima no fundo"
   OBS-000088: "Mexer a cada 5min distribui calor melhor"
   ↓

9. NOVO CICLO
   ↓
   Hipótese: "Mexer a cada 5min melhora consistência"
   EXP-000043: Testar frequência de agitação
   ...
   ↓
   REC-000001-v3

───────────────────────────────────────────────────────────────

O ciclo se repete infinitamente.
Cada versão da receita é baseada em evidência acumulada.
```

---

## 📊 Modelo Formal

```
         ┌──────────────┐
         │  OBSERVAÇÃO  │
         │  (informal)  │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │   HIPÓTESE   │
         │  (testável)  │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │ EXPERIMENTO  │
         │  (planejado) │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  EXECUÇÕES   │
         │  (evidência) │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │  VALIDAÇÃO   │
         │  (análise)   │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │   RECEITA    │
         │ (consolidado)│
         └──────┬───────┘
                │
                └──────┐
                       │
         ┌─────────────▼────────────┐
         │  NOVAS EXECUÇÕES         │
         │  (confirmação/refinamento)│
         └─────────────┬────────────┘
                       │
         ┌─────────────▼────────────┐
         │  NOVAS OBSERVAÇÕES       │
         │  (descobertas)           │
         └─────────────┬────────────┘
                       │
                       │ (retorna ao ciclo)
                       │
         ┌─────────────▼────────────┐
         │    NOVA VERSÃO           │
         │    (evolução)            │
         └──────────────────────────┘
```

---

## 🗂️ Entidades Envolvidas

### Fase 1: Descoberta

```yaml
# OBS-000015
tipo: observacao
vinculada_a: [REC-000001, EXE-000120]
conteudo: "Doce ficou muito escuro. Suspeita: fogo alto."
data: 2026-06-20
```

### Fase 2: Hipótese

```yaml
# Registrada em OBS-000015 ou EXP-000042
hipotese: "Fogo alto causa caramelização excessiva"
testavel: sim
variavel: temperatura
```

### Fase 3: Experimento

```yaml
# EXP-000042
tipo: experimento
objetivo: "Testar relação fogo x cor final"
receita_base: REC-000001
status: em-andamento
variaveis:
  - nome: temperatura
    valores: [baixo, medio, alto]
  - nome: tempo
    valores: [1h30, 2h, 2h30]
```

### Fase 4: Execuções

```yaml
# EXE-000123
tipo: execucao
receita_id: REC-000001
experimento_id: EXP-000042
variacao: fogo-baixo
resultado: sucesso
metricas:
  tempo: 2h
  temperatura: ~85°C
  cor: ambar
  textura: cremosa

# EXE-000124
tipo: execucao
receita_id: REC-000001
experimento_id: EXP-000042
variacao: fogo-medio
resultado: parcial
metricas:
  tempo: 1h30
  temperatura: ~95°C
  cor: escura
  textura: cremosa
```

### Fase 5: Validação

```yaml
# Em EXP-000042
status: concluido
conclusao: |
  Fogo baixo (~85°C) produz cor âmbar desejada.
  Fogo médio (~95°C) escurece demais.
  Tempo ideal: 2h com fogo baixo.
evidencia:
  - EXE-000123: sucesso
  - EXE-000124: cor escura
  - EXE-000125: sucesso (confirmação)
```

### Fase 6: Receita Atualizada

```yaml
# REC-000001-v2
tipo: receita
versao: 2
receita_base_id: REC-000001
historico: |
  v2: Baseado em EXP-000042 (EXE-000123, 124, 125)
  Mudança: fogo alto → fogo baixo
  Razão: evitar escurecimento excessivo
conteudo:
  modo_preparo: |
    1. ...
    2. Aquecer em FOGO BAIXO (~85°C), nunca alto
    3. Manter fogo baixo durante todo o processo
    ...
```

---

## 🔄 Exemplo Real Completo

### Situação Inicial

```
REC-000001-v1: Doce de Leite
Modo de preparo: "Aquecer em fogo médio..."
```

### Execução 1

```
EXE-000120: Fogo médio
Resultado: doce ficou muito escuro
Observação: não está de acordo com o esperado
```

### Observação Gerada

```
OBS-000015: "Doce ficou escuro demais"
Hipótese: fogo alto ou tempo demais
```

### Experimento Planejado

```
EXP-000042: Testar diferentes intensidades de fogo
Variáveis:
  - Fogo baixo, médio, alto
  - Tempo fixo: 2h
  - Ingredientes: mesmos sempre
```

### Execuções do Experimento

```
EXE-000123: Fogo baixo → COR ÂMBAR (ideal) ✅
EXE-000124: Fogo médio → COR ESCURA ❌
EXE-000125: Fogo baixo → COR ÂMBAR (confirma) ✅
```

### Validação

```
Análise:
- 2 de 3 com fogo baixo = sucesso
- 1 de 1 com fogo médio = falha
Conclusão: fogo baixo é consistente
```

### Receita Atualizada

```
REC-000001-v2: Doce de Leite
Modo de preparo: "Aquecer em FOGO BAIXO (~85°C)..."
Referência: EXP-000042
```

### Novas Execuções (validação da v2)

```
EXE-000156: v2, fogo baixo → sucesso ✅
EXE-000157: v2, fogo baixo → sucesso ✅
EXE-000158: v2, fogo baixo → sucesso ✅
```

### Nova Observação

```
OBS-000087: "Fogo baixo também evita queima no fundo"
OBS-000088: "Mexer a cada 5min melhora ainda mais"
```

### Novo Ciclo

```
EXP-000043: Testar frequência de agitação
Variáveis: mexer a cada 5min vs 10min vs 15min
...
REC-000001-v3
```

---

## 📈 Benefícios do Ciclo

### 1. Conhecimento Baseado em Evidência

❌ **Sem ciclo:**
```
"Achei que ficou escuro, vou mudar a receita"
```

✅ **Com ciclo:**
```
"Executei 3 vezes com fogo baixo, todas deram certo.
 Executei 1 vez com fogo médio, deu errado.
 Logo, fogo baixo é melhor (evidência)."
```

### 2. Rastreabilidade Total

```
REC-000001-v2
  ↓ (baseado em)
EXP-000042
  ↓ (composto por)
[EXE-000123, EXE-000124, EXE-000125]
  ↓ (originado de)
OBS-000015
  ↓ (vinculada a)
EXE-000120
```

**Você pode rastrear:**
- Por que a receita mudou?
- Quais execuções justificam a mudança?
- Qual observação originou a hipótese?
- Qual experimento testou a hipótese?

### 3. Método Científico

```
Observação → Hipótese → Teste → Validação → Conclusão
```

**Não é opinião. É ciência aplicada à culinária.**

### 4. Evolução Incremental

```
v1 → observação → experimento → v2
v2 → nova observação → novo experimento → v3
v3 → refinamento → v4
...
```

**Cada versão é melhor que a anterior (baseado em evidência).**

### 5. Preservação do Conhecimento

```
REC-000001-v1 (mantido como histórico)
  ↓
REC-000001-v2 (evolução)
  ↓
REC-000001-v3 (refinamento)
```

**Histórico nunca é perdido. Evolução é rastreável.**

---

## 🎯 Diferencial: Culinária como Ciência

### Culinária Tradicional

```
Cozinheiro: "Achei que ficou escuro, vou usar fogo baixo"
(sem registro, sem evidência, sem rastreabilidade)
```

### Culinária com SOE-CCG

```
1. Observação: "Ficou escuro"
2. Hipótese: "Fogo alto causa isso"
3. Experimento: Testar fogo baixo vs médio vs alto
4. Execuções: 3x cada variação
5. Análise: Fogo baixo = sucesso consistente
6. Conclusão: Atualizar receita com evidência
7. Rastreabilidade: Tudo documentado
```

**Resultado:** Conhecimento consolidado, não opinião.

---

## 📚 Implementação Prática

### Como Usar o Ciclo

**1. Cozinhe e registre:**
```bash
cp templates/execucao-v1.md dados/execucoes/EXE-000200-doce-leite-2026-07-01-v1.md
# Preencher: resultado, tempo, observações
```

**2. Percebeu algo?**
```bash
cp templates/observacao-v1.md dados/observacoes/OBS-000100-doce-ficou-escuro-v1.md
# Vincular à execução
# Descrever observação
# Formular hipótese
```

**3. Quer testar?**
```bash
cp templates/experimento-v1.md dados/experimentos/EXP-000050-teste-fogo-v1.md
# Definir objetivo
# Listar variáveis
# Planejar execuções
```

**4. Execute o experimento:**
```bash
# Criar 3 execuções com variações
# EXE-000201, EXE-000202, EXE-000203
# Todas vinculadas ao EXP-000050
```

**5. Analise e conclua:**
```bash
# Atualizar EXP-000050
# status: concluido
# conclusao: ...
```

**6. Atualize a receita:**
```bash
cp dados/receitas/REC-000001-doce-leite-v1.md \
   dados/receitas/REC-000001-doce-leite-v2.md
# versao: 2
# receita_base_id: REC-000001
# historico: "v2 baseado em EXP-000050"
# Modificar modo de preparo
```

**7. Valide a nova versão:**
```bash
# Executar 3x a v2
# Confirmar consistência
# Se OK, v2 se torna receita ativa
```

---

## ✨ Conclusão

O **Ciclo do Conhecimento** transforma culinária em ciência.

Não é apenas cozinhar.  
**É aprender sistematicamente.**

Não é apenas registrar.  
**É evoluir com evidência.**

Não é apenas versionar.  
**É rastrear o porquê de cada mudança.**

**SOE-CCG não guarda receitas.**  
**SOE-CCG evolui conhecimento.**

---

**Documento:** `CICLO-DO-CONHECIMENTO.md`  
**Versão:** 1.0  
**Data:** 2026-07-01  
**Objetivo:** Formalizar o ciclo científico de evolução do conhecimento gastronômico
