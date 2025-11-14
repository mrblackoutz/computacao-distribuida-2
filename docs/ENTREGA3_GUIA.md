# Entrega 3 - Serviço Coordenador e Exclusão Mútua

## 🎯 Objetivo

Resolver a **condição de corrida** demonstrada na Entrega 2 através de um **serviço coordenador** que implementa exclusão mútua usando locks distribuídos.

## 📋 O que foi implementado

### 1. Serviço Coordenador (Node.js/Express)

**Arquivo:** `servico-coordenador/server.js`

- **Porta:** 3000
- **Armazenamento:** Map em memória (locks)
- **Endpoints:**
  - `POST /lock` - Adquire lock para um recurso
  - `POST /unlock` - Libera lock de um recurso
  - `GET /locks` - Lista todos os locks ativos (debug)
  - `GET /health` - Health check

**Funcionalidades:**
- Lock com timeout de 30 segundos (prevenção de deadlock)
- Limpeza periódica de locks expirados (a cada 60s)
- Retorna 409 Conflict quando recurso já está travado
- Logging detalhado de todas as operações

### 2. Cliente Python para o Coordenador

**Arquivo:** `servico-agendamento/app/utils/coordenador_client.py`

**Classe:** `CoordenadorClient`

Métodos:
- `acquire_lock(recurso)` → retorna (bool, mensagem)
- `release_lock(recurso)` → retorna (bool, mensagem)
- `check_health()` → retorna bool

**Função utilitária:**
- `gerar_nome_recurso_agendamento(inicio, fim)` → gera nome único do recurso

Exemplo de nome: `Hubble-Acad_2025-12-01T03:00:00Z`

### 3. Integração com Flask

**Modificado:** `servico-agendamento/app/routes/agendamento_routes.py`

**Mudança no fluxo de POST /agendamentos:**

```python
# Antes (Entrega 2):
validar dados → verificar conflitos no BD → salvar

# Agora (Entrega 3):
validar dados → ADQUIRIR LOCK → verificar conflitos no BD → salvar → LIBERAR LOCK
```

**Try-Finally garantido:**
```python
try:
    # Operações no banco de dados
finally:
    # SEMPRE libera o lock
    coordenador.release_lock(nome_recurso)
```

### 4. Script de Teste COM Lock

**Arquivo:** `tests/test_com_lock.py`

Testa o sistema COM locks funcionando:
- Dispara N requisições simultâneas para o mesmo horário
- **Resultado esperado:** 1 sucesso (201), N-1 conflitos (409)
- Verifica banco de dados (deve ter exatamente 1 agendamento)
- Compara com Entrega 2 (que tinha múltiplos sucessos)

## 🚀 Como Executar

### Passo 1: Instalar dependências do Node.js

```powershell
cd servico-coordenador
npm install
```

### Passo 2: Iniciar o Serviço Coordenador

**Terminal 1:**
```powershell
cd servico-coordenador
npm start
```

Saída esperada:
```
==================================================
   Serviço Coordenador - SCTEC
   Porta: 3000
   Ambiente: development
   Lock Timeout: 30000ms
==================================================
```

### Passo 3: Iniciar o Serviço de Agendamento

**Terminal 2:**
```powershell
cd servico-agendamento
.\venv\Scripts\Activate.ps1  # ou venv\Scripts\activate no CMD
python run.py
```

Saída esperada:
```
 * Running on http://0.0.0.0:5000
```

### Passo 4: Executar Teste COM Lock

**Terminal 3:**
```powershell
python tests\test_com_lock.py 10
```

## 📊 Resultado Esperado

```
================================================================================
TESTE COM LOCK - ENTREGA 3
================================================================================

Verificando serviços...
✓ Serviço de Agendamento: OK
✓ Serviço Coordenador: OK

1. Criando cientista de teste...
   Cientista criado: ID 1

2. Horário alvo: 2025-11-11T03:00:00Z - 2025-11-11T03:30:00Z

3. Disparando 10 requisições simultâneas...

--------------------------------------------------------------------------------
✓ [Thread 03] Status: 201 - Tempo: 0.152s
✗ [Thread 00] Status: 409 - Tempo: 0.148s
   └─ Motivo: Recurso temporariamente indisponível
✗ [Thread 01] Status: 409 - Tempo: 0.150s
   └─ Motivo: Recurso temporariamente indisponível
[... mais 7 linhas de 409 ...]
--------------------------------------------------------------------------------

================================================================================
RESULTADOS
================================================================================

✓ Sucessos (201):         1
✗ Recursos ocupados (409): 9
⚠ Outros erros:           0
⚠ Falhas de rede:         0

⏱ Tempo total: 0.156s
⏱ Tempo médio por requisição: 0.150s

🎉 SUCESSO! Apenas 1 agendamento criado (exclusão mútua funcionando!)

Agendamento vencedor:
   Thread: 3
   ID: 1
   Tempo: 0.152s

================================================================================
VERIFICAÇÃO NO BANCO DE DADOS
================================================================================

Agendamentos no banco: 1

✓ Banco de dados consistente (1 agendamento)
```

## 🔍 Análise dos Logs

### Logs do Coordenador (Terminal 1):

```
[INFO] 2025-11-10T15:30:45.123Z POST /lock
[INFO] Recebido pedido de lock para recurso: Hubble-Acad_2025-11-11T03:00:00Z
[INFO] Lock concedido para recurso: Hubble-Acad_2025-11-11T03:00:00Z (holder: a1b2c3d4)

[INFO] 2025-11-10T15:30:45.125Z POST /lock
[INFO] Recebido pedido de lock para recurso: Hubble-Acad_2025-11-11T03:00:00Z
[INFO] Recurso Hubble-Acad_2025-11-11T03:00:00Z já está em uso (holder: a1b2c3d4). Negando lock.

[... 8 mais negações ...]

[INFO] 2025-11-10T15:30:45.300Z POST /unlock
[INFO] Recebido pedido de unlock para recurso: Hubble-Acad_2025-11-11T03:00:00Z
[INFO] Lock liberado para recurso: Hubble-Acad_2025-11-11T03:00:00Z
```

### Logs da Aplicação (servico-agendamento/logs/app.log):

```
[INFO] 2025-11-10T15:30:45.120Z servico-agendamento a1b2c3d4: Requisição POST /agendamentos recebida
[INFO] 2025-11-10T15:30:45.122Z servico-agendamento a1b2c3d4: Tentando adquirir lock para o recurso Hubble-Acad_2025-11-11T03:00:00Z
[INFO] 2025-11-10T15:30:45.130Z servico-agendamento a1b2c3d4: Lock adquirido com sucesso
[INFO] 2025-11-10T15:30:45.132Z servico-agendamento a1b2c3d4: Iniciando verificação de conflito no BD
[INFO] 2025-11-10T15:30:45.150Z servico-agendamento a1b2c3d4: Salvando novo agendamento no BD
[INFO] 2025-11-10T15:30:45.155Z servico-agendamento a1b2c3d4: Agendamento criado com ID 1
[INFO] 2025-11-10T15:30:45.160Z servico-agendamento a1b2c3d4: Liberando lock para o recurso...

[INFO] 2025-11-10T15:30:45.121Z servico-agendamento e5f6g7h8: Requisição POST /agendamentos recebida
[INFO] 2025-11-10T15:30:45.123Z servico-agendamento e5f6g7h8: Tentando adquirir lock para o recurso Hubble-Acad_2025-11-11T03:00:00Z
[WARNING] 2025-11-10T15:30:45.131Z servico-agendamento e5f6g7h8: Falha ao adquirir lock: Recurso já está travado
```

### Logs de Auditoria (servico-agendamento/logs/audit.log):

```json
{"timestamp_utc":"2025-11-10T15:30:45.155Z","level":"AUDIT","event_type":"AGENDAMENTO_CRIADO","service":"servico-agendamento","correlation_id":"a1b2c3d4-e5f6-7890-abcd-ef1234567890","details":{"agendamento_id":1,"cientista_id":1,"cientista_nome":"Grace Hopper","horario_inicio_utc":"2025-11-11T03:00:00Z","horario_fim_utc":"2025-11-11T03:30:00Z","objeto_celeste":"Teste Lock Thread 3"}}

{"timestamp_utc":"2025-11-10T15:30:45.131Z","level":"AUDIT","event_type":"AGENDAMENTO_CONFLITO","service":"servico-agendamento","correlation_id":"e5f6g7h8-i9j0-1234-5678-9abcdef01234","details":{"cientista_id":1,"horario_inicio_utc":"2025-11-11T03:00:00Z","motivo":"Lock não disponível"}}
```

## 📈 Comparação com Entrega 2

| Aspecto | Entrega 2 (SEM Lock) | Entrega 3 (COM Lock) |
|---------|---------------------|---------------------|
| **Requisições simultâneas** | 10 | 10 |
| **Sucessos (201)** | 5-10 (variável) | **1** |
| **Conflitos (409)** | 0-5 | **9** |
| **Agendamentos no BD** | 5-10 (PROBLEMA!) | **1** (CORRETO!) |
| **Consistência** | ❌ Inconsistente | ✅ Consistente |
| **Race Condition** | ❌ Presente | ✅ Resolvida |

## 🎓 Conceitos Aplicados

### 1. Exclusão Mútua
- Apenas 1 thread pode acessar a seção crítica (BD) por vez
- Implementado via locks do coordenador

### 2. Coordenador Centralizado
- Serviço dedicado para gerenciar acesso a recursos
- Ponto único de controle (trade-off: single point of failure)

### 3. Try-Finally Pattern
- Garante liberação do lock mesmo em caso de erro
- Previne deadlocks por exceções não tratadas

### 4. Timeout de Lock
- Auto-liberação após 30 segundos
- Previne bloqueios permanentes se cliente falhar

### 5. Correlation ID
- Rastreamento distribuído de requisições
- Permite correlacionar logs entre serviços

## 🧪 Testes Adicionais

### Teste com carga maior:
```powershell
python tests\test_com_lock.py 50
```

### Teste de timeout (simular falha):
1. Modifique `acquire_lock()` para não liberar o lock
2. Execute o teste
3. Aguarde 30 segundos
4. Execute novamente (deve funcionar após timeout)

### Verificar locks ativos:
```powershell
curl http://localhost:3000/locks
```

## ✅ Critérios de Validação

- [x] Serviço coordenador implementado em Node.js
- [x] Cliente Python para comunicação com coordenador
- [x] Locks adquiridos ANTES de acessar banco de dados
- [x] Locks sempre liberados (try-finally)
- [x] Timeout de 30s implementado
- [x] Apenas 1 agendamento criado em teste simultâneo
- [x] Logs mostram tentativas de lock
- [x] Correlation IDs presentes em todos os logs
- [x] Script de teste automatizado

## 🐛 Troubleshooting

### Erro: "Serviço Coordenador: OFFLINE"
```powershell
# Verificar se Node.js está instalado
node --version

# Instalar dependências
cd servico-coordenador
npm install

# Iniciar serviço
npm start
```

### Erro: "CoordenadorClient" is not defined
```powershell
# Garantir que venv está ativado
cd servico-agendamento
.\venv\Scripts\Activate.ps1
```

### Teste falha com múltiplos sucessos
- Verificar se coordenador está rodando (porta 3000)
- Verificar URL em `.env`: `COORDENADOR_URL=http://localhost:3000`
- Verificar logs do coordenador para ver se recebe requisições

### Locks não são liberados
- Aguardar 30 segundos (timeout automático)
- Ou reiniciar serviço coordenador: `Ctrl+C` e `npm start`

## 📚 Próximos Passos

**Entrega 4:** Interface web com sincronização de tempo (Algoritmo de Cristian)

**Entrega 5:** Containerização com Docker Compose

---

**Data de conclusão:** 2025-11-10
**Status:** ✅ Completo
