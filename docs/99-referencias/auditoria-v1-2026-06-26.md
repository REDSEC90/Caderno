# Relatório de Auditoria Arquitetural — FAA v1

**Data:** 2026-06-26 17:16  
**Pontuação geral:** 92.2%  
**Decisão arquitetural:** ✅ APROVADO  
**Baseline:** 70/71 artefatos (99%)  

## Grupos de Maturidade

| Grupo | % | Status |
|-------|---|--------|
| fundacao | 100% | ✅ |
| arquitetura | 100% | ✅ |
| dominio_especificacoes | 100% | ✅ |
| dominio_contratos | 100% | ✅ |
| dominio_templates | 100% | ✅ |
| dominio_esquemas | 86% | ✅ |
| governanca | 100% | ✅ |
| modelagem | 100% | ✅ |
| linguagem_dominio | 100% | ✅ |

## Resumo por Motor

| Motor | Pontuação | Falhas | Avisos |
|-------|-----------|--------|--------|
| Baseline | 100.0% | 0 | 0 |
| Estrutura | 83.3% | 0 | 11 |
| Filosofia | 100.0% | 0 | 0 |
| Domínio | 96.7% | 1 | 0 |
| Cobertura | 100.0% | 0 | 0 |
| Maturidade | 100.0% | 0 | 0 |
| Semântica | 92.9% | 0 | 2 |
| Dados | 100.0% | 0 | 0 |
| Integridade | 100.0% | 0 | 0 |
| Padrões | 50.0% | 0 | 11 |
| Escalabilidade | 100.0% | 0 | 0 |
| Dependências | 83.3% | 0 | 1 |

**Total:** 118 ✅ · 25 ⚠️ · 1 ❌

## Estrutura

- ⚠️  **[EST-003]** Nomenclatura fora do padrão: ING-000003-sal-refinado.md
  - Evidência: `dados/ingredientes/ING-000003-sal-refinado.md`
  - Sugestão: Padrão esperado: ING-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: ING-000001-leite-integral.md
  - Evidência: `dados/ingredientes/ING-000001-leite-integral.md`
  - Sugestão: Padrão esperado: ING-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: ING-000004-bicarbonato-sodio.md
  - Evidência: `dados/ingredientes/ING-000004-bicarbonato-sodio.md`
  - Sugestão: Padrão esperado: ING-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: ING-000002-acucar-refinado.md
  - Evidência: `dados/ingredientes/ING-000002-acucar-refinado.md`
  - Sugestão: Padrão esperado: ING-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: TEC-000001-reducao.md
  - Evidência: `dados/tecnicas/TEC-000001-reducao.md`
  - Sugestão: Padrão esperado: TEC-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: TEC-000003-agitacao-continua.md
  - Evidência: `dados/tecnicas/TEC-000003-agitacao-continua.md`
  - Sugestão: Padrão esperado: TEC-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: TEC-000002-caramelizacao.md
  - Evidência: `dados/tecnicas/TEC-000002-caramelizacao.md`
  - Sugestão: Padrão esperado: TEC-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: EQP-000001-panela-fundo-grosso.md
  - Evidência: `dados/equipamentos/EQP-000001-panela-fundo-grosso.md`
  - Sugestão: Padrão esperado: EQP-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: EQP-000002-colher-silicone.md
  - Evidência: `dados/equipamentos/EQP-000002-colher-silicone.md`
  - Sugestão: Padrão esperado: EQP-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: EXE-000001-doce-leite-v1-execucao1.md
  - Evidência: `dados/execucoes/EXE-000001-doce-leite-v1-execucao1.md`
  - Sugestão: Padrão esperado: EXE-NNNNNN-slug-vN.md
- ⚠️  **[EST-003]** Nomenclatura fora do padrão: OBS-000001-bicarbonato-efeito.md
  - Evidência: `dados/observacoes/OBS-000001-bicarbonato-efeito.md`
  - Sugestão: Padrão esperado: OBS-NNNNNN-slug-vN.md

## Domínio

- ❌ **[DOM-001]** experimento/esquema: AUSENTE
  - Evidência: `docs/01-dominio/esquemas/esquema-experimento-v1.md`
  - Sugestão: Criar: docs/01-dominio/esquemas/esquema-experimento-v1.md

## Semântica

- ⚠️  **[SEM-002]** Termo proibido 'salvar' encontrado fora da seção de proibição
  - Evidência: `docs/01-dominio/linguagem-soe-ccg-v0_5.md`
  - Sugestão: Substituir pelo termo correto
- ⚠️  **[SEM-004]** Glossário: ~0 entradas
  - Evidência: `docs/00-projeto/glossario-v1.md`

## Padrões

- ⚠️  **[PAD-001]** Nome fora do padrão: ING-000001-leite-integral.md
  - Evidência: `dados/ingredientes/ING-000001-leite-integral.md`
  - Sugestão: Padrão: ING-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: ING-000002-acucar-refinado.md
  - Evidência: `dados/ingredientes/ING-000002-acucar-refinado.md`
  - Sugestão: Padrão: ING-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: ING-000003-sal-refinado.md
  - Evidência: `dados/ingredientes/ING-000003-sal-refinado.md`
  - Sugestão: Padrão: ING-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: ING-000004-bicarbonato-sodio.md
  - Evidência: `dados/ingredientes/ING-000004-bicarbonato-sodio.md`
  - Sugestão: Padrão: ING-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: TEC-000001-reducao.md
  - Evidência: `dados/tecnicas/TEC-000001-reducao.md`
  - Sugestão: Padrão: TEC-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: TEC-000002-caramelizacao.md
  - Evidência: `dados/tecnicas/TEC-000002-caramelizacao.md`
  - Sugestão: Padrão: TEC-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: TEC-000003-agitacao-continua.md
  - Evidência: `dados/tecnicas/TEC-000003-agitacao-continua.md`
  - Sugestão: Padrão: TEC-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: EQP-000001-panela-fundo-grosso.md
  - Evidência: `dados/equipamentos/EQP-000001-panela-fundo-grosso.md`
  - Sugestão: Padrão: EQP-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: EQP-000002-colher-silicone.md
  - Evidência: `dados/equipamentos/EQP-000002-colher-silicone.md`
  - Sugestão: Padrão: EQP-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: EXE-000001-doce-leite-v1-execucao1.md
  - Evidência: `dados/execucoes/EXE-000001-doce-leite-v1-execucao1.md`
  - Sugestão: Padrão: EXE-NNNNNN-slug-vN.md
- ⚠️  **[PAD-001]** Nome fora do padrão: OBS-000001-bicarbonato-efeito.md
  - Evidência: `dados/observacoes/OBS-000001-bicarbonato-efeito.md`
  - Sugestão: Padrão: OBS-NNNNNN-slug-vN.md

## Dependências

- ⚠️  **[DEP-003]** Registro isolado (sem referências): REC-000001
  - Sugestão: Verificar se o registro tem relacionamentos não documentados
