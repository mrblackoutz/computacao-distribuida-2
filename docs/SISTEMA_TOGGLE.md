# 🎓 Sistema de Toggle: COM Lock vs SEM Lock

## 📋 Resumo da Implementação

Este documento descreve a implementação do sistema de **toggle** entre a versão **COM lock** (Entrega 3 - solução) e **SEM lock** (Entrega 2 - demonstração do problema).

---

## 🏗️ Arquitetura da Solução

### Arquivos Criados/Modificados

#### 1. **Rotas Duplicadas**

**`agendamento_routes.py`** (COM LOCK - Produção)
- ✅ Usa `CoordenadorClient` para adquirir lock
- ✅ Fluxo: lock → verificar → salvar → unlock (try...finally)
- ✅ Logs: "Tentando adquirir lock", "Lock adquirido", etc
- ✅ Retorna 409 quando recurso ocupado

**`agendamento_routes_sem_lock.py`** (SEM LOCK - Demonstração)
- ❌ NÃO usa coordenador
- ❌ Apenas verificação no BD (race condition possível)
- ⚠️ Logs: "RACE CONDITION WINDOW", "MODO SEM LOCK"
- ⚠️ Permite múltiplos agendamentos simultâneos

#### 2. **Sistema de Toggle** (`app/routes/__init__.py`)

```python
# Importar rota baseado na variável USE_LOCK
USE_LOCK = os.getenv('USE_LOCK', 'true').lower() in ('true', '1', 'yes', 'on')

if USE_LOCK:
    print("✅ Sistema usando VERSÃO COM LOCK (Entrega 3)")
    from app.routes import agendamento_routes
else:
    print("⚠️ Sistema usando VERSÃO SEM LOCK (Entrega 2)")
    from app.routes import agendamento_routes_sem_lock
```

**Como funciona:**
1. Lê variável de ambiente `USE_LOCK`
2. Se `true`: importa `agendamento_routes.py` (COM lock)
3. Se `false`: importa `agendamento_routes_sem_lock.py` (SEM lock)
4. Imprime mensagem no console indicando modo ativo

#### 3. **Docker Compose** (`docker-compose.yml`)

Adicionada variável de ambiente:

```yaml
environment:
  - USE_LOCK=${USE_LOCK:-true}
```

**Default:** `true` (sistema COM lock)
**Override:** via arquivo `.env` ou CLI

#### 4. **Arquivo de Configuração** (`.env`)

```bash
# true  = COM lock (Produção)
# false = SEM lock (Demonstração)
USE_LOCK=true
```

---

## 🚀 Como Usar

### Opção 1: Scripts PowerShell Automatizados

#### Demonstrar PROBLEMA (SEM LOCK)
```powershell
.\demo_sem_lock.ps1
python tests\test_concorrencia.py 10
```

**Resultado esperado:**
- 🔴 Múltiplos agendamentos criados
- 🔴 Conflitos no banco
- 🔴 Logs mostram race condition

---

#### Demonstrar SOLUÇÃO (COM LOCK)
```powershell
.\demo_com_lock.ps1
python tests\test_com_lock.py 10
```

**Resultado esperado:**
- 🟢 Apenas 1 agendamento criado
- 🟢 9 conflitos HTTP 409
- 🟢 Logs mostram coordenação

---

#### Demonstração COMPARATIVA (Recomendado!)
```powershell
.\demo_comparacao.ps1
```

**O que faz:**
1. Executa sistema SEM lock + teste
2. Pausa para análise
3. Executa sistema COM lock + teste
4. Mostra resumo comparativo

---

### Opção 2: Toggle Manual

#### Passo 1: Editar `.env`
```bash
# Para demonstrar PROBLEMA:
USE_LOCK=false

# Para demonstrar SOLUÇÃO:
USE_LOCK=true
```

#### Passo 2: Reiniciar containers
```powershell
docker-compose down
docker-compose up --build -d
```

#### Passo 3: Verificar modo ativo
```powershell
docker-compose logs agendamento | Select-String "VERSÃO"
```

**Saída esperada:**
- COM LOCK: `✅ Sistema usando VERSÃO COM LOCK`
- SEM LOCK: `⚠️ Sistema usando VERSÃO SEM LOCK`

---

## 🔍 Diferenças Técnicas

### Código COM LOCK (agendamento_routes.py)

```python
# Gerar nome do recurso
nome_recurso = gerar_nome_recurso_agendamento(inicio, fim)

# Adquirir lock
coordenador = CoordenadorClient()
lock_adquirido, mensagem = coordenador.acquire_lock(nome_recurso)

if not lock_adquirido:
    return jsonify({'error': 'Recurso temporariamente indisponível'}), 409

try:
    # Verificar conflitos
    conflitos = Agendamento.check_conflicts(inicio, fim)
    
    # Salvar agendamento
    db.session.add(agendamento)
    db.session.commit()
    
finally:
    # SEMPRE liberar lock
    coordenador.release_lock(nome_recurso)
```

---

### Código SEM LOCK (agendamento_routes_sem_lock.py)

```python
# ⚠️ SEM LOCK - Apenas verificação no banco

# Verificar conflitos
conflitos = Agendamento.check_conflicts(inicio, fim)

# ⚠️ PONTO CRÍTICO: Race condition possível aqui!
# Entre a verificação e o INSERT, outra thread pode criar agendamento

# Salvar agendamento
db.session.add(agendamento)
db.session.commit()
```

**Problema:** Janela de tempo entre `check_conflicts()` e `db.session.commit()` permite race condition.

---

## 📊 Análise de Logs

### Logs SEM LOCK

```
[INFO] Criando novo agendamento (MODO SEM LOCK)
[WARNING] ⚠️ Sistema rodando SEM proteção de lock!
[INFO] Iniciando verificação de conflito no BD (SEM LOCK - UNSAFE!)
[WARNING] ⚠️ RACE CONDITION WINDOW: Entre verificação e INSERT
[INFO] Salvando novo agendamento no BD
```

**Logs de Auditoria:**
```json
{
  "event_type": "AGENDAMENTO_CRIADO",
  "details": {
    "agendamento_id": 123,
    "modo": "SEM_LOCK"
  }
}
```

---

### Logs COM LOCK

```
[INFO] Criando novo agendamento
[INFO] Tentando adquirir lock para o recurso: Hubble-Acad_2025-11-13T23:20:00Z
[INFO] Lock adquirido com sucesso
[INFO] Iniciando verificação de conflito no BD
[INFO] Salvando novo agendamento no BD
[INFO] Liberando lock para o recurso: Hubble-Acad_2025-11-13T23:20:00Z
```

**Coordenador (Node.js):**
```
[INFO] Recebido pedido de lock para recurso: Hubble-Acad_2025-11-13T23:20:00Z
[INFO] Lock concedido para recurso: Hubble-Acad_2025-11-13T23:20:00Z
[INFO] Recebido pedido de lock...
[INFO] Recurso já está em uso, negando lock
[INFO] Lock liberado
```

---

## 🎯 Casos de Uso

### Para Apresentação ao Professor

**Roteiro sugerido:**

1. **Demonstrar PROBLEMA** (3 min)
   ```powershell
   .\demo_sem_lock.ps1
   python tests\test_concorrencia.py 10
   ```
   - Mostrar múltiplos agendamentos criados
   - Explicar race condition
   - Apontar logs de warning

2. **Demonstrar SOLUÇÃO** (3 min)
   ```powershell
   .\demo_com_lock.ps1
   python tests\test_com_lock.py 10
   ```
   - Mostrar apenas 1 agendamento
   - Explicar exclusão mútua
   - Mostrar coordenação nos logs

3. **Explicar Arquitetura** (2 min)
   - Desenhar fluxo: Cliente → Flask → Coordenador
   - Explicar endpoints /lock e /unlock
   - Destacar try...finally

---

### Para Desenvolvimento/Debug

```powershell
# Testar versão SEM lock localmente
$env:USE_LOCK="false"
python servico-agendamento/run.py

# Testar versão COM lock localmente
$env:USE_LOCK="true"
python servico-agendamento/run.py
```

---

## ✅ Checklist de Validação

Antes de apresentar, verificar:

- [ ] Arquivo `.env` existe
- [ ] Scripts `.ps1` têm permissão de execução
- [ ] Docker Desktop rodando
- [ ] Modo SEM LOCK cria múltiplos agendamentos
- [ ] Modo COM LOCK cria apenas 1 agendamento
- [ ] Logs mostram diferença clara entre modos
- [ ] Interface web funciona em ambos modos

---

## 🐛 Troubleshooting

### Problema: Sistema sempre usa COM LOCK

**Causa:** `.env` não está sendo lido

**Solução:**
```powershell
# Verificar se .env existe
Test-Path .env

# Recriar se necessário
Copy-Item .env.example .env

# Rebuild containers
docker-compose down
docker-compose up --build -d
```

---

### Problema: Logs não mostram mensagem de modo

**Causa:** `__init__.py` não foi modificado

**Solução:**
```powershell
# Verificar conteúdo
Get-Content servico-agendamento\app\routes\__init__.py

# Deve conter: USE_LOCK = os.getenv('USE_LOCK', 'true')
```

---

### Problema: Script PowerShell não executa

**Causa:** Política de execução restritiva

**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `agendamento_routes.py` | Versão COM lock (produção) |
| `agendamento_routes_sem_lock.py` | Versão SEM lock (demonstração) |
| `app/routes/__init__.py` | Sistema de toggle |
| `docker-compose.yml` | Configuração USE_LOCK |
| `.env` | Variável de ambiente |
| `.env.example` | Template de configuração |
| `demo_sem_lock.ps1` | Script para modo SEM LOCK |
| `demo_com_lock.ps1` | Script para modo COM LOCK |
| `demo_comparacao.ps1` | Demonstração comparativa |
| `GUIA_DEMONSTRACAO.md` | Guia completo de uso |

---

## 🎓 Conceitos Demonstrados

### Entrega 2 (SEM LOCK)

✅ **Demonstra:**
- Condição de corrida (race condition)
- Check-then-act problem
- Logs de aplicação
- Logs de auditoria JSON

❌ **Problema:**
- Múltiplos agendamentos simultâneos
- Inconsistência no banco de dados

---

### Entrega 3 (COM LOCK)

✅ **Demonstra:**
- Exclusão mútua (mutual exclusion)
- Coordenador centralizado
- Comunicação entre microserviços
- Lock/unlock pattern
- Try...finally para garantir liberação

✅ **Solução:**
- Apenas 1 agendamento criado
- Consistência garantida
- Sistema confiável

---

## 🎉 Conclusão

Este sistema de toggle permite:

1. ✅ **Demonstrar PROBLEMA** da Entrega 2
2. ✅ **Demonstrar SOLUÇÃO** da Entrega 3
3. ✅ **Contrastar** ambas abordagens
4. ✅ **Validar** aprendizado
5. ✅ **Apresentar** de forma didática

**Modo padrão:** `USE_LOCK=true` (produção)  
**Modo didático:** `USE_LOCK=false` (demonstração)

🚀 **Sistema pronto para apresentação!**
