# Política de Revisão

> Como registros são aprovados, alterados e auditados.

---

## Princípio

Conhecimento de qualidade requer validação. A política de revisão garante que registros atendam aos padrões do SOE-CCG antes de se tornarem ativos.

---

## Ciclo de Aprovação

### Quando revisão é necessária

**Obrigatória para:**
- Novos registros de entidades principais (Receita, Ingrediente, Técnica)
- Alterações estruturais em registros ativos
- Mudanças em catálogos oficiais
- Criação de novos templates ou esquemas

**Opcional para:**
- Observações pessoais
- Execuções de receitas
- Rascunhos em desenvolvimento

### Fluxo de revisão

```
[Criação] → [Rascunho] → [Submissão para Revisão] → [Revisão] → [Aprovação/Rejeição]
                                                          ↓
                                                      [Ativo] / [Rascunho]
```

---

## Responsáveis

### Papéis

| Papel | Responsabilidade | Permissões |
|-------|------------------|------------|
| **Autor** | Cria e edita registro | Criar rascunho, submeter para revisão |
| **Revisor** | Valida conformidade e qualidade | Aprovar, rejeitar, solicitar mudanças |
| **Mantenedor** | Cuida do domínio | Revisar, aprovar, editar diretamente |
| **Administrador** | Governa o sistema | Todas as permissões |

### Quem pode aprovar

**Registros simples:**
- Qualquer revisor designado

**Registros críticos:**
- Mínimo 2 revisores (mantenedores)

**Mudanças estruturais:**
- Consenso entre mantenedores do domínio

---

## Critérios de Revisão

### Checklist obrigatório

- [ ] Conformidade com esquema da entidade
- [ ] Conformidade com template
- [ ] Metadados completos e corretos
- [ ] Identificador válido e único
- [ ] Relacionamentos íntegros (IDs referenciados existem)
- [ ] Tags adequadas
- [ ] Formatação Markdown correta
- [ ] Legibilidade humana preservada
- [ ] Sem informações sensíveis não autorizadas

### Critérios de qualidade

- [ ] Informação é precisa
- [ ] Informação é completa (dentro do escopo)
- [ ] Redação é clara
- [ ] Não há duplicação com registros existentes
- [ ] Origem e autoria estão documentadas

---

## Rastreabilidade

### Metadados de revisão

```yaml
revisao:
  submetido_em: 2026-06-15T10:00:00Z
  submetido_por: autor@example.com
  revisores:
    - nome: revisor1@example.com
      decisao: aprovado
      data: 2026-06-16T14:30:00Z
      comentario: "Conforme. Pequenos ajustes de formatação aplicados."
    - nome: revisor2@example.com
      decisao: aprovado
      data: 2026-06-16T15:00:00Z
  status_final: aprovado
  aprovado_em: 2026-06-16T15:00:00Z
```

### Histórico de revisões

Cada rodada de revisão é registrada:

```yaml
historico_revisoes:
  - rodada: 1
    data: 2026-06-10T10:00:00Z
    decisao: mudancas_solicitadas
    comentarios:
      - "Falta informar origem da receita"
      - "Quantidade de ingrediente ING-0042 está ambígua"
  - rodada: 2
    data: 2026-06-15T10:00:00Z
    decisao: aprovado
    comentarios:
      - "Todas as solicitações atendidas"
```

---

## Processo de Alteração

### Alteração em registro ativo

Registros ativos podem ser editados:

**Mudanças menores:**
- Correção tipográfica
- Esclarecimento de redação
- Adição de tag

Podem ser aplicadas diretamente pelo autor ou mantenedor. Não exigem nova revisão.

**Mudanças significativas:**
- Alteração de ingrediente
- Mudança em modo de preparo
- Alteração de relacionamento

Registro volta para estado `revisao`. Após aprovação, retorna a `ativo`.

### Versionamento de conteúdo

Git preserva todas as alterações. Cada commit representa uma versão do registro.

Alterações maiores podem justificar nova versão do registro (REC-0042-v1 → REC-0042-v2).

---

## Rejeição

### Quando um registro é rejeitado

Motivos comuns:
- Não atende ao esquema
- Informação incorreta ou incompleta
- Duplica registro existente
- Formatação inadequada
- Falta de origem/autoria

### Processo de rejeição

1. Revisor registra decisão de rejeição
2. Comentários explicam os motivos
3. Registro volta ao estado `rascunho`
4. Autor recebe notificação
5. Autor pode corrigir e resubmeter

### Rejeição não é exclusão

Registro rejeitado permanece no sistema (como rascunho). Pode ser corrigido e resubmetido quantas vezes necessário.

---

## Auditoria

### O que é auditado

- Quem criou o registro
- Quando foi criado
- Quem submeteu para revisão
- Quem revisou
- Decisão de cada revisor
- Quando foi aprovado ou rejeitado
- Quem alterou após aprovação
- Histórico completo de mudanças

### Logs de auditoria

```yaml
auditoria:
  - acao: criacao
    usuario: autor@example.com
    data: 2026-06-10T09:00:00Z
  - acao: submissao_revisao
    usuario: autor@example.com
    data: 2026-06-10T10:00:00Z
  - acao: revisao
    usuario: revisor1@example.com
    decisao: mudancas_solicitadas
    data: 2026-06-11T14:00:00Z
  - acao: edicao
    usuario: autor@example.com
    data: 2026-06-12T09:30:00Z
  - acao: resubmissao_revisao
    usuario: autor@example.com
    data: 2026-06-12T10:00:00Z
  - acao: revisao
    usuario: revisor1@example.com
    decisao: aprovado
    data: 2026-06-13T11:00:00Z
  - acao: ativacao
    usuario: sistema
    data: 2026-06-13T11:00:00Z
```

---

## Reversão

### Quando uma mudança é revertida

Motivos:
- Erro identificado após aprovação
- Informação descoberta como incorreta
- Alteração acidental

### Processo de reversão

1. Identificar versão correta (commit no git)
2. Justificar reversão
3. Aplicar reversão
4. Registrar na auditoria
5. Notificar autor original (se aplicável)

Reversão gera novo commit. Histórico nunca é reescrito.

---

## Comentários de Revisão

### Estrutura de comentário

```yaml
comentario:
  revisor: revisor@example.com
  data: 2026-06-15T14:00:00Z
  tipo: mudanca_solicitada
  secao: "Ingredientes"
  descricao: "Quantidade de sal está em gramas, mas deveria ser em colheres (padrão para temperos)"
  sugestao: "Alterar '10g sal' para '2 colheres de chá de sal'"
```

### Tipos de comentário

- `informativo` — observação, não bloqueia aprovação
- `sugestao` — melhoria opcional
- `mudanca_solicitada` — correção necessária antes de aprovar
- `bloqueante` — erro crítico, impede aprovação

---

## Revisão Automatizada

### Validações automáticas

Antes da revisão humana, sistema valida automaticamente:

- [ ] Esquema é respeitado
- [ ] Metadados obrigatórios presentes
- [ ] Identificador único
- [ ] Markdown válido
- [ ] Referências existem (IDs de relacionamentos)

Se falhar, submissão é rejeitada automaticamente antes de chegar ao revisor.

### Complementaridade

Validação automatizada verifica **conformidade técnica**.

Revisão humana verifica **qualidade e semântica**.

Ambas são necessárias.

---

## Exemplos

### Exemplo 1: Receita aprovada na primeira rodada

```yaml
id: REC-0156
nome: Pão de Queijo Mineiro
estado: ativo
revisao:
  submetido_em: 2026-06-10T10:00:00Z
  revisores:
    - nome: revisor@example.com
      decisao: aprovado
      data: 2026-06-11T14:00:00Z
      comentario: "Receita bem documentada e conforme."
  aprovado_em: 2026-06-11T14:00:00Z
```

---

### Exemplo 2: Ingrediente com mudanças solicitadas

```yaml
id: ING-0312
nome: Tomate Italiano
estado: revisao
historico_revisoes:
  - rodada: 1
    data: 2026-06-10T14:00:00Z
    decisao: mudancas_solicitadas
    comentarios:
      - tipo: mudanca_solicitada
        descricao: "Falta especificar a origem (nacional/importado)"
      - tipo: sugestao
        descricao: "Considere adicionar sazonalidade"
```

Autor corrige e reenvia.

---

### Exemplo 3: Observação sem revisão

```yaml
id: OBS-0890
tipo: Observacao
estado: ativo
criado_por: usuario@example.com
criado_em: 2026-06-15T19:00:00Z
revisao: nao_requerida
```

Observações pessoais não exigem revisão. Tornam-se ativas automaticamente.

---

## Governança

### Configuração de revisão obrigatória

Definida por tipo de entidade:

```yaml
politica_revisao:
  Receita: obrigatoria
  Ingrediente: obrigatoria
  Tecnica: obrigatoria
  Equipamento: obrigatoria
  Execucao: opcional
  Observacao: opcional
  Experimento: opcional
```

### Quem define revisores

- Mantenedores do domínio designam revisores
- Sistema pode sugerir revisor com base em especialidade (tags)

---

## Resumo

- Revisão valida conformidade e qualidade
- Fluxo: rascunho → submissão → revisão → aprovação/rejeição
- Papéis: autor, revisor, mantenedor, administrador
- Mudanças menores não exigem nova revisão
- Mudanças significativas voltam ao estado `revisao`
- Toda decisão é auditada
- Reversões são permitidas e rastreadas
- Validação automática complementa revisão humana
- Rejeição não é exclusão — registro pode ser corrigido
