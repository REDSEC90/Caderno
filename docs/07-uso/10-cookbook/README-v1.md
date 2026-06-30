# Cookbook — SOE-CCG

> Exemplos prontos para copiar. Sem narrativa, sem contexto extra — só o procedimento.

---

## Índice

| Arquivo | O que faz | Tempo |
|---------|-----------|-------|
| [`01-criar-ingrediente-v1.md`](01-criar-ingrediente-v1.md) | Criar um ING do zero | ~5 min |
| [`02-criar-receita-v1.md`](02-criar-receita-v1.md) | Criar uma REC com relacionamentos completos | ~15 min |
| [`03-criar-tecnica-equipamento-v1.md`](03-criar-tecnica-equipamento-v1.md) | Criar TEC ou EQP | ~5 min |
| [`04-executar-faa-v1.md`](04-executar-faa-v1.md) | Executar o FAA e interpretar resultados | ~3 min |
| [`05-criar-execucao-v1.md`](05-criar-execucao-v1.md) | Registrar EXE e criar OBS | ~10 min |

---

## Ordem de criação (sempre seguir)

```
EQP → TEC → ING → REC → EXE → OBS / EXP
```

Entidades que aparecem primeiro na ordem devem existir antes das que aparecem depois.  
Uma REC não pode referenciar um ING que ainda não existe.

---

## Quando usar o cookbook vs. os fluxos

**Use o cookbook** quando souber o que quer criar e precisar só do procedimento.

**Use os fluxos** (`05-fluxos/`) quando quiser entender o contexto completo de uma sessão de trabalho ou o raciocínio por trás de cada passo.
