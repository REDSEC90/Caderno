# Plano de Execução — v1.0: Maturidade

**Data:** 2026-07-01  
**Objetivo:** Declarar o sistema oficialmente maduro — estável, documentado, auditado e com processos reprodutíveis.  
**Pré-requisito:** v0.9 entregue (hardening completo).

---

## O que significa "maduro"

Um sistema maduro não é necessariamente perfeito. É um sistema que:

- Funciona de forma confiável e previsível
- Pode ser mantido por qualquer colaborador sem conhecimento implícito
- Tem contratos explícitos que foram respeitados ao longo do tempo
- Tem histórico de decisões arquiteturais registrado
- Tem cobertura de testes que inspira confiança em mudanças
- Tem documentação que reflete o estado real do sistema
- Tem processos que podem ser executados sem intervenção manual

---

## Estado Esperado ao Entrar na v1.0 (pós v0.9)

| Componente               | Estado Esperado                              |
|--------------------------|----------------------------------------------|
| Arquitetura              | ✅ Congelada e auditada                      |
| Kernel                   | ✅ Estável, testado, observável, escalável   |
| Automação                | ✅ Pipeline, contratos, FAA contínuo         |
| Cobertura `codigo/`      | ✅ ≥ 90%                                     |
| Cobertura kernel/        | ✅ 100% métodos públicos                     |
| Segurança                | ✅ Validação de entrada, sem exposição       |
| Backup/recuperação       | ✅ Operacional e testado                     |
| Dívida técnica           | ✅ Baixa (documentada e gerenciada)          |

---

## Etapas da v1.0

### Etapa 1 — Auditoria final da documentação

**Objetivo:** Documentação reflete o sistema real. Nenhum documento obsoleto sem marcação explícita.

**Entregas:**
- Revisão de todos os documentos em `docs/` — marcar obsoletos com `status: arquivado`
- `docs/INDICE-MESTRE.md` — versão final, cobrindo 100% dos componentes
- `docs/MATRIZ-RASTREABILIDADE.md` — versão final, cobrindo todos os testes críticos
- CONTRIBUTING.md — guia de contribuição para novos colaboradores
- SECURITY.md — política de segurança e reporte de vulnerabilidades
- README.md raiz — atualizado para refletir v1.0

---

### Etapa 2 — Congelamento de contratos

**Objetivo:** Contratos públicos declarados estáveis e imutáveis para v1.0.

**Entregas:**
- `CONTRACTS_FREEZE.md` — lista todos os contratos públicos congelados com data e hash
- Contratos do `codigo/`: parser, validador, importador, ir
- Contratos do `kernel/`: ModuleRegistry, ServiceRegistry, KernelEventBus, LifecycleManager
- ADR-0005: decisão de congelamento de contratos públicos para v1.0
- Qualquer mudança após este ponto exige novo ADR e bump de versão

---

### Etapa 3 — Cobertura elevada

**Objetivo:** Cobertura que inspira confiança, não apenas número.

**Critérios:**
- `codigo/` — ≥ 90% (linhas e branches)
- `kernel/` — 100% dos métodos públicos
- Cenários críticos cobertos: importação com falha, parsing de arquivo inválido, ciclo estrutural
- Todos os golden files válidos e atualizados

---

### Etapa 4 — Auditoria arquitetural final (FAA)

**Objetivo:** Score ≥ 95 como sinal de maturidade.

**Entregas:**
- Rodar FAA completo
- Gerar `docs/99-referencias/FAA-v1.0-RELATORIO-FINAL.md`
- Score ≥ 95 ou justificativa documentada para cada ponto abaixo
- Zero inconsistências críticas
- Zero documentos sem versão explícita

---

### Etapa 5 — Validação de processos reprodutíveis

**Objetivo:** Qualquer colaborador consegue reproduzir o ambiente e rodar o sistema do zero.

**Entregas:**
- `scripts/instalacao/instalar.sh` — instala dependências e prepara ambiente
- `scripts/instalacao/verificar.sh` — verifica que o ambiente está correto
- Teste: ambiente limpo → rodar instalação → rodar todos os testes → todos passam
- Tempo de onboarding estimado: documentado no CONTRIBUTING.md

---

### Etapa 6 — Release v1.0

**Entregas:**
- Rodar pipeline completo uma última vez
- FAA score ≥ 95
- Todos os testes passando
- CHANGELOG.md com v1.0.0 — entrada detalhada celebrando a maturidade
- `CONTRACTS_FREEZE.md` publicado
- Tag `v1.0.0`
- `docs/99-referencias/FASE-1.0-RESUMO.md` — narrativa da jornada de v0.5 até v1.0

---

## Critérios de Conclusão (Definition of Done)

- [ ] Documentação 100% sincronizada com o sistema real
- [ ] CONTRIBUTING.md e SECURITY.md presentes
- [ ] README.md atualizado para v1.0
- [ ] `CONTRACTS_FREEZE.md` publicado
- [ ] ADR-0005 criado
- [ ] Cobertura `codigo/` ≥ 90% (linhas e branches)
- [ ] Cobertura `kernel/` 100% métodos públicos
- [ ] FAA score ≥ 95
- [ ] Processo de instalação reprodutível e documentado
- [ ] Zero inconsistências críticas
- [ ] Todos os testes passando
- [ ] Tag v1.0.0 criada
- [ ] Resumo narrativo da jornada publicado

---

## O que NÃO é v1.0

A v1.0 não significa fim do desenvolvimento. Significa que a base está madura o suficiente para receber novas funcionalidades sem risco de regressão. A visão de 5 anos descrita no `roadmap-master-v1.md` começa a se realizar a partir daqui.

---

**Documento:** `PLANO-v1.0.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
