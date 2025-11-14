# 🎬 Guia de Demonstração - SCTEC

Este guia mostra como demonstrar o **problema** da condição de corrida (Entrega 2) e sua **solução** com exclusão mútua (Entrega 3).

---

## 📋 Índice

1. [Toggle Manual](#toggle-manual)
2. [Scripts Automatizados](#scripts-automatizados)
3. [Demonstração Comparativa](#demonstração-comparativa)
4. [Análise de Logs](#análise-de-logs)

---

## 🔧 Toggle Manual

### Passo 1: Criar arquivo `.env`

Se não existir, crie baseado no exemplo:

```powershell
Copy-Item .env.example .env
```

### Passo 2: Editar `.env`

Abra o arquivo `.env` e encontre a linha:

```bash
USE_LOCK=true
```

**Para demonstrar o PROBLEMA:**
```bash
USE_LOCK=false  # Sistema SEM lock
```

**Para demonstrar a SOLUÇÃO:**
```bash
USE_LOCK=true   # Sistema COM lock
```

### Passo 3: Reiniciar sistema

```powershell
docker-compose down
docker-compose up --build -d
```

---

## 🚀 Scripts Automatizados

### Opção A: Demonstração do Problema (SEM LOCK)

```powershell
.\demo_sem_lock.ps1
```

**O que faz:**
- ✅ Configura `USE_LOCK=false`
- ✅ Reinicia containers
- ✅ Mostra instruções de teste

**Depois execute:**
```powershell
python tests\test_concorrencia.py 10
```

**Resultado esperado:**
- ❌ **MÚLTIPLOS** agendamentos criados (2+)
- ❌ Conflitos no banco de dados
- ❌ Logs mostram race condition

---

### Opção B: Demonstração da Solução (COM LOCK)

```powershell
.\demo_com_lock.ps1
```

**O que faz:**
- ✅ Configura `USE_LOCK=true`
- ✅ Reinicia containers
- ✅ Mostra instruções de teste

**Depois execute:**
```powershell
python tests\test_com_lock.py 10
```

**Resultado esperado:**
- ✅ **APENAS 1** agendamento criado
- ✅ 9 conflitos (HTTP 409)
- ✅ Logs mostram coordenação via lock/unlock

---

### Opção C: Demonstração Comparativa (RECOMENDADA!)

```powershell
.\demo_comparacao.ps1
```

**O que faz:**
1. 🔴 **Parte 1:** Executa sistema SEM lock + teste
2. ⏸️ Pausa para análise
3. 🟢 **Parte 2:** Executa sistema COM lock + teste
4. 📊 Mostra resumo comparativo

**Vantagens:**
- ✅ Demonstra problema e solução em sequência
- ✅ Contraste claro entre as duas versões
- ✅ Resumo didático ao final
- ✅ Ideal para apresentações

---

## 📊 Comparação de Resultados

### Cenário: 10 requisições simultâneas para o mesmo horário

| Métrica | SEM LOCK (Problema) | COM LOCK (Solução) |
|---------|---------------------|-------------------|
| **Agendamentos criados** | 2-10 (múltiplos ❌) | 1 (único ✅) |
| **Conflitos HTTP 409** | 0-8 | 9 |
| **Estado do BD** | INCONSISTENTE ❌ | CONSISTENTE ✅ |
| **Logs** | Entrelaçados 🔴 | Coordenados 🟢 |
| **Race condition** | SIM ❌ | NÃO ✅ |

---

## 🔍 Análise de Logs

### Logs do Sistema SEM LOCK

```powershell
# Ver logs de aplicação
docker-compose logs agendamento | Select-String "verificação de conflito"

# Ver logs de auditoria
docker exec sctec-agendamento cat logs/audit.log | Select-String "AGENDAMENTO_CRIADO"
```

**O que observar:**
- ⚠️ Múltiplos logs `"Iniciando verificação de conflito"` simultâneos
- ⚠️ Vários eventos `AGENDAMENTO_CRIADO` para o mesmo horário
- ⚠️ Mensagem: `"RACE CONDITION WINDOW: Entre verificação e INSERT"`

---

### Logs do Sistema COM LOCK

```powershell
# Ver logs do Flask (agendamento)
docker-compose logs agendamento | Select-String "lock"

# Ver logs do Node.js (coordenador)
docker-compose logs coordenador
```

**O que observar:**
- ✅ Log: `"Tentando adquirir lock para o recurso"`
- ✅ 1x `"Lock concedido"` no coordenador
- ✅ 9x `"Recurso já está em uso, negando lock"`
- ✅ Log: `"Lock liberado"` ao final

---

## 🎯 Roteiro de Apresentação

### 1. Introdução (2 min)
- Explicar o problema: Telescópio espacial compartilhado
- Desafio: Evitar agendamentos simultâneos no mesmo horário

### 2. Demonstração do Problema (3 min)
```powershell
.\demo_sem_lock.ps1
python tests\test_concorrencia.py 10
```
- Mostrar múltiplos agendamentos criados
- Explicar race condition
- Mostrar logs entrelaçados

### 3. Demonstração da Solução (3 min)
```powershell
.\demo_com_lock.ps1
python tests\test_com_lock.py 10
```
- Mostrar apenas 1 agendamento criado
- Explicar exclusão mútua
- Mostrar coordenação nos logs

### 4. Arquitetura (2 min)
- Desenhar diagrama: Cliente → Flask → Coordenador → BD
- Explicar fluxo: lock → verificar → salvar → unlock
- Destacar try...finally para garantir liberação

### 5. Conclusão (1 min)
- Conceitos demonstrados:
  - ✅ Condição de corrida
  - ✅ Exclusão mútua
  - ✅ Coordenador centralizado
  - ✅ Microserviços
  - ✅ Observabilidade via logs

---

## 🛠️ Troubleshooting

### Problema: Script não executa

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: Containers não iniciam

**Solução:**
```powershell
docker-compose down -v
docker-compose up --build -d
```

### Problema: USE_LOCK não muda comportamento

**Verificar:**
1. Arquivo `.env` existe?
2. Variável está correta? (`true` ou `false`)
3. Fez rebuild? (`--build`)

**Debug:**
```powershell
# Ver logs de inicialização
docker-compose logs agendamento | Select-String "VERSÃO"
```

**Esperado:**
- COM LOCK: `"✅ Sistema usando VERSÃO COM LOCK"`
- SEM LOCK: `"⚠️ Sistema usando VERSÃO SEM LOCK"`

---

## 📚 Referências

- **Código SEM lock:** `servico-agendamento/app/routes/agendamento_routes_sem_lock.py`
- **Código COM lock:** `servico-agendamento/app/routes/agendamento_routes.py`
- **Coordenador:** `servico-coordenador/server.js`
- **Toggle logic:** `servico-agendamento/app/routes/__init__.py`

---

## ✅ Checklist de Demonstração

Antes de apresentar, verifique:

- [ ] Arquivo `.env` existe
- [ ] Docker Desktop rodando
- [ ] Containers iniciados: `docker-compose ps`
- [ ] Ambos healthy: `docker inspect sctec-agendamento sctec-coordenador`
- [ ] Interface acessível: http://localhost:5000
- [ ] Teste SEM lock funciona
- [ ] Teste COM lock funciona
- [ ] Scripts PowerShell executam sem erros

---

🎉 **Sistema pronto para demonstração!**
