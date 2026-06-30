# OBSERVAÇÃO — NECESSIDADE DE LIMPEZA E CONSOLIDAÇÃO

## Status do Sistema
O SOE-CCG encontra-se em um estado de alta maturidade estrutural, porém ainda não consolidado em termos de autoridade única, redundância de regras e coerência entre camadas.

O sistema é funcional, mas ainda não está em condição ideal para **tag de versão estável definitiva** sem risco de divergência futura.

---

## 1. SITUAÇÃO ATUAL

O sistema apresenta:

- Microkernel funcional em `kernel/`
- Pipeline de processamento (parser → IR → resolver → validador)
- Estrutura de domínio altamente detalhada em `dados/`
- Sistema de auditoria avançado (FAA)
- Documentação extensa e bem segmentada em `docs/`

Entretanto, essas camadas ainda operam com **sobreposição parcial de responsabilidades**.

---

## 2. PROBLEMAS IDENTIFICADOS

### 2.1 Duplicação de regras e contratos
Regras de domínio e validação existem simultaneamente em:

- `kernel-docs/`
- `docs/01-dominio/`
- `scripts/auditoria/`

➡ Isso cria múltiplas fontes de verdade para o mesmo conceito.

---

### 2.2 FAA como sistema paralelo
O sistema FAA evoluiu para além de auditoria, contendo:

- estado próprio
- lógica de priorização
- planejamento interno

➡ Isso cria risco de divergência com o Kernel.

---

### 2.3 Falta de autoridade única formal
Não existe uma definição absolutamente rígida de:

- quem é o "detentor final da verdade"
- se o Kernel ou IR é a camada superior de autoridade

---

### 2.4 IR parcialmente acoplado
A camada de IR ainda não está isolada como fronteira formal do sistema.

Alguns módulos ainda acessam dados e lógica fora do pipeline estruturado.

---

### 2.5 Redundância documental
Há sobreposição entre:

- documentação técnica (kernel-docs)
- documentação de domínio (docs)
- lógica operacional (scripts)

---

## 3. IMPACTO SISTÊMICO

Se não houver consolidação:

- divergência de regras entre camadas
- inconsistência de validação
- dificuldade de manutenção futura
- risco de “duas versões do sistema coexistindo”

---

## 4. CONDIÇÃO PARA TAG DE VERSÃO ESTÁVEL

Para que uma versão estável possa ser oficialmente tagada, é necessário:

### 4.1 Consolidação de autoridade
Definir explicitamente:

- Kernel como executor final
- IR como fronteira estrutural do sistema
- FAA como camada de observação apenas

---

### 4.2 Unificação de contratos
Todos os contratos devem existir em uma única camada formal:

- `kernel/contracts/`

---

### 4.3 Redução de duplicidade
Eliminar ou unificar:

- contratos duplicados em `docs/`
- regras redundantes em `scripts/auditoria/`

---

### 4.4 Isolamento do pipeline IR
Garantir pipeline único e obrigatório:

INPUT → PARSER → IR → RESOLVER → VALIDATOR → STORAGE

Sem exceções de acesso paralelo.

---

### 4.5 Congelamento de expansão
Durante a fase de consolidação:

- não adicionar novos módulos
- não expandir FAA
- não introduzir novas entidades de domínio

---

## 5. CONCLUSÃO

O sistema encontra-se em estado:

> funcionalmente avançado, mas arquiteturalmente não consolidado

Portanto:

- NÃO é recomendado o lançamento de versão estável ainda
- é necessária uma fase de limpeza e alinhamento estrutural
- após consolidação, o sistema estará apto para tag estável com baixa dívida técnica

---

## 6. DECISÃO ARQUITETURAL

Esta observação define uma fase obrigatória de:

> CONSOLIDAÇÃO ANTES DE RELEASE

até que:

- autoridade única esteja definida
- redundâncias sejam removidas
- pipeline IR esteja isolado
- FAA esteja restrito à observação

---
