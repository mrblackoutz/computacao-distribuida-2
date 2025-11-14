# Guia de Teste Final - SCTEC

## 🎯 Objetivo

Este guia contém os passos exatos para validar que todas as funcionalidades do SCTEC estão funcionando corretamente no ambiente Docker.

---

## ⚙️ Pré-requisitos

Antes de começar, verifique:

- [ ] Docker Desktop instalado e rodando
- [ ] Portas 3000 e 5000 livres
- [ ] Terminal PowerShell (Windows) ou Bash (Linux/Mac)
- [ ] Navegador web moderno (Chrome, Firefox, Edge)

**Verificar Docker:**
```powershell
docker --version
docker-compose --version
docker info
```

---

## 📋 Roteiro de Testes

### Teste 1: Deploy do Sistema com Docker

**Objetivo:** Verificar que o sistema sobe corretamente com Docker Compose

**Passos:**

1. **Iniciar o sistema:**
   ```powershell
   # Windows
   .\start.bat
   
   # Ou manualmente:
   docker-compose up --build -d
   ```

2. **Aguardar inicialização (15-30 segundos)**

3. **Verificar status dos containers:**
   ```powershell
   docker-compose ps
   ```

4. **Resultado esperado:**
   ```
   NAME                  STATUS              PORTS
   sctec-coordenador     Up (healthy)       0.0.0.0:3000->3000/tcp
   sctec-agendamento     Up (healthy)       0.0.0.0:5000->5000/tcp
   ```

5. **Verificar logs iniciais:**
   ```powershell
   docker-compose logs
   ```

**✅ Critérios de sucesso:**
- [ ] Ambos containers com status "Up (healthy)"
- [ ] Nenhum erro nos logs
- [ ] Portas 3000 e 5000 expostas

**❌ Se falhar:**
- Ver: [Troubleshooting](#troubleshooting)

---

### Teste 2: Health Checks dos Serviços

**Objetivo:** Confirmar que ambos os serviços estão respondendo

**Passos:**

1. **Testar Coordenador:**
   ```powershell
   curl http://localhost:3000/health
   
   # Ou no navegador:
   # http://localhost:3000/health
   ```

   **Resposta esperada:**
   ```json
   {
     "status": "healthy",
     "service": "servico-coordenador",
     "timestamp": "2025-01-XX...",
     "locks_ativos": 0
   }
   ```

2. **Testar Serviço de Agendamento:**
   ```powershell
   curl http://localhost:5000/api/v1/time
   ```

   **Resposta esperada:**
   ```json
   {
     "timestamp_utc": "2025-01-XX...",
     "timezone": "UTC",
     "epoch_ms": 1234567890123,
     "_links": {
       "self": {"href": "http://localhost:5000/api/v1/time"},
       "agendamentos": {"href": "..."},
       "cientistas": {"href": "..."}
     }
   }
   ```

**✅ Critérios de sucesso:**
- [ ] Coordenador retorna 200 OK com JSON válido
- [ ] Agendamento retorna 200 OK com timestamp UTC
- [ ] HATEOAS links presentes na resposta

---

### Teste 3: Interface Web

**Objetivo:** Validar interface do usuário e sincronização de tempo

**Passos:**

1. **Abrir no navegador:**
   ```
   http://localhost:5000
   ```

2. **Verificar componentes visuais:**
   - [ ] Título "SCTEC" visível
   - [ ] Painel de sincronização de tempo carregado
   - [ ] 4 campos de tempo visíveis:
     - Hora Local do Navegador
     - Hora do Servidor (UTC)
     - Diferença (ms)
     - Latência de Rede (ms)

3. **Observar sincronização:**
   - [ ] Indicador muda de "Sincronizando..." para "Sincronizado"
   - [ ] Offset calculado e exibido (pode ser negativo ou positivo)
   - [ ] RTT (latência) exibido em ms
   - [ ] Relógios atualizam a cada segundo

4. **Verificar formulário:**
   - [ ] Dropdown "Cientista" carrega cientistas (ou mostra "vazio")
   - [ ] Campo "Horário de Início" aceita datetime
   - [ ] Dropdown "Duração" tem opções de 5 a 120 min
   - [ ] Campos "Objeto Celeste" e "Observações" editáveis
   - [ ] Botão "Agendar Observação" habilitado

5. **Verificar lista de agendamentos:**
   - [ ] Área "Meus Agendamentos" visível
   - [ ] Mensagem inicial (vazia ou com agendamentos)

**✅ Critérios de sucesso:**
- [ ] Página carrega sem erros no console (F12)
- [ ] Sincronização de tempo funcionando
- [ ] Formulário interativo

---

### Teste 4: Criar Cientista via API

**Objetivo:** Testar CRUD de cientistas

**Passos:**

1. **Criar cientista:**
   ```powershell
   curl -X POST http://localhost:5000/api/v1/cientistas `
     -H "Content-Type: application/json" `
     -d '{
       "nome": "Marie Curie",
       "email": "marie.curie@test.com",
       "instituicao": "Universidade de Paris",
       "pais": "França",
       "especialidade": "Radioastronomia"
     }'
   ```

2. **Resultado esperado:**
   ```json
   {
     "id": 1,
     "nome": "Marie Curie",
     "email": "marie.curie@test.com",
     "instituicao": "Universidade de Paris",
     "pais": "França",
     "especialidade": "Radioastronomia",
     "ativo": true,
     "data_cadastro": "2025-XX-XX...",
     "_links": {
       "self": {"href": "http://localhost:5000/api/v1/cientistas/1"},
       "agendamentos": {"href": "..."},
       "criar_agendamento": {"href": "...", "method": "POST"}
     }
   }
   ```

3. **Verificar HATEOAS:**
   - [ ] Link "self" presente
   - [ ] Link "agendamentos" presente
   - [ ] Link "criar_agendamento" com method POST

4. **Atualizar interface:**
   - Recarregue http://localhost:5000
   - [ ] Dropdown "Cientista" agora mostra "Marie Curie"

**✅ Critérios de sucesso:**
- [ ] Status 201 Created
- [ ] Cientista retornado com ID
- [ ] HATEOAS completo
- [ ] Aparece na interface

---

### Teste 5: Criar Agendamento COM Locks (Teste Crítico!)

**Objetivo:** Validar exclusão mútua funcionando em ambiente containerizado

**Passos:**

1. **Calcular horário futuro (25h a partir de agora):**
   ```python
   # Python (se tiver instalado):
   python -c "from datetime import datetime, timedelta; print((datetime.utcnow() + timedelta(hours=25)).replace(microsecond=0, second=0).isoformat() + 'Z')"
   ```
   
   **Exemplo de resultado:** `2025-01-15T14:30:00Z`
   
   **OU** use um horário fixo longe no futuro: `2025-12-31T10:00:00Z`

2. **Criar agendamento:**
   ```powershell
   curl -X POST http://localhost:5000/api/v1/agendamentos `
     -H "Content-Type: application/json" `
     -d '{
       "cientista_id": 1,
       "horario_inicio_utc": "2025-12-31T10:00:00Z",
       "horario_fim_utc": "2025-12-31T10:30:00Z",
       "objeto_celeste": "NGC 1300",
       "observacoes": "Teste de agendamento"
     }'
   ```

3. **Resultado esperado:**
   ```json
   {
     "id": 1,
     "cientista_id": 1,
     "cientista_nome": "Marie Curie",
     "horario_inicio_utc": "2025-12-31T10:00:00Z",
     "horario_fim_utc": "2025-12-31T10:30:00Z",
     "objeto_celeste": "NGC 1300",
     "observacoes": "Teste de agendamento",
     "status": "AGENDADO",
     "data_criacao": "2025-XX-XX...",
     "_links": {
       "self": {"href": "..."},
       "cientista": {"href": "..."},
       "cancelar": {"href": "...", "method": "DELETE"}
     }
   }
   ```

4. **Verificar logs do coordenador:**
   ```powershell
   docker-compose logs coordenador | Select-String "lock"
   ```
   
   **Deve conter:**
   ```
   [INFO] ... Recebido pedido de lock para recurso: Hubble-Acad_2025-12-31T10:00:00Z
   [INFO] ... Lock concedido para recurso: Hubble-Acad_2025-12-31T10:00:00Z
   [INFO] ... Lock liberado para recurso: Hubble-Acad_2025-12-31T10:00:00Z
   ```

5. **Verificar logs do agendamento:**
   ```powershell
   docker-compose logs agendamento | Select-String "lock"
   ```
   
   **Deve conter:**
   ```
   [INFO] ... Tentando adquirir lock para o recurso: Hubble-Acad_2025-12-31T10:00:00Z
   [INFO] ... Lock adquirido com sucesso
   [INFO] ... Liberando lock
   ```

6. **Verificar audit log:**
   ```powershell
   docker exec sctec-agendamento cat logs/audit.log | Select-String "AGENDAMENTO_CRIADO"
   ```

**✅ Critérios de sucesso:**
- [ ] Status 201 Created
- [ ] Agendamento criado no banco
- [ ] Lock adquirido e liberado nos logs
- [ ] Evento de auditoria registrado
- [ ] Link "cancelar" presente

---

### Teste 6: Exclusão Mútua - Tentativa Duplicada

**Objetivo:** Provar que o lock impede agendamentos duplicados

**Passos:**

1. **Tentar criar EXATAMENTE o mesmo agendamento novamente:**
   ```powershell
   curl -X POST http://localhost:5000/api/v1/agendamentos `
     -H "Content-Type: application/json" `
     -d '{
       "cientista_id": 1,
       "horario_inicio_utc": "2025-12-31T10:00:00Z",
       "horario_fim_utc": "2025-12-31T10:30:00Z",
       "objeto_celeste": "Teste duplicado",
       "observacoes": "Deve falhar"
     }'
   ```

2. **Resultado esperado:**
   ```json
   {
     "error": "Conflito de horário",
     "conflitos": [
       {
         "id": 1,
         "horario_inicio_utc": "2025-12-31T10:00:00Z",
         "horario_fim_utc": "2025-12-31T10:30:00Z",
         ...
       }
     ]
   }
   ```

3. **Status esperado:** `409 Conflict`

**✅ Critérios de sucesso:**
- [ ] Status 409 Conflict
- [ ] Mensagem de erro clara
- [ ] Lista de conflitos retornada
- [ ] Apenas 1 agendamento no banco (não duplicou)

---

### Teste 7: Interface Web - Criar e Cancelar

**Objetivo:** Validar fluxo completo via interface

**Passos:**

1. **Abrir interface:** http://localhost:5000

2. **Selecionar cientista:** "Marie Curie"

3. **Preencher formulário:**
   - Horário de Início: Data futura (ex: 31/12/2025 15:00)
   - Duração: 30 minutos
   - Objeto Celeste: "Andrômeda M31"
   - Observações: "Teste via interface"

4. **Clicar em "Agendar Observação"**

5. **Verificar:**
   - [ ] Alerta verde "Agendamento criado com sucesso!"
   - [ ] Card do agendamento aparece na lista
   - [ ] Status: "AGENDADO" (verde)
   - [ ] Botão "Cancelar Agendamento" visível

6. **Clicar em "Cancelar Agendamento"**

7. **Confirmar cancelamento**

8. **Verificar:**
   - [ ] Alerta laranja "Agendamento cancelado com sucesso"
   - [ ] Status muda para "CANCELADO" (vermelho)
   - [ ] Botão "Cancelar" desaparece (HATEOAS!)
   - [ ] Motivo do cancelamento exibido

**✅ Critérios de sucesso:**
- [ ] Agendamento criado via interface
- [ ] Aparece na lista automaticamente
- [ ] Cancelamento funciona
- [ ] HATEOAS: botão desaparece após cancelar

---

### Teste 8: Concorrência Extrema (Script Automatizado)

**Objetivo:** Validar exclusão mútua sob alta carga

**Pré-requisito:** Python instalado localmente

**Passos:**

1. **Ativar ambiente Python:**
   ```powershell
   cd servico-agendamento
   .\venv\Scripts\Activate.ps1
   cd ..
   ```

2. **Executar teste de concorrência COM lock:**
   ```powershell
   python tests/test_com_lock.py 20
   ```

3. **Aguardar execução (10-30 segundos)**

4. **Resultado esperado:**
   ```
   ✓ Sucessos (201):         1
   ✗ Recursos ocupados (409): 19
   
   🎉 SUCESSO! Apenas 1 agendamento criado
   
   Agendamentos no banco: 1
   ```

**✅ Critérios de sucesso:**
- [ ] Apenas 1 sucesso (201 Created)
- [ ] 19 conflitos (409)
- [ ] Banco de dados com apenas 1 registro
- [ ] Sistema permanece estável

**🔥 Teste extremo (50 threads):**
```powershell
python tests/test_com_lock.py 50
```

**Resultado esperado:** 1 sucesso, 49 conflitos

---

### Teste 9: Persistência de Volumes

**Objetivo:** Verificar que dados sobrevivem a reinicializações

**Passos:**

1. **Verificar agendamentos atuais:**
   ```powershell
   curl http://localhost:5000/api/v1/agendamentos
   ```
   
   **Anotar:** Quantidade de agendamentos

2. **Parar containers:**
   ```powershell
   docker-compose stop
   ```

3. **Reiniciar containers:**
   ```powershell
   docker-compose start
   ```

4. **Aguardar health checks (15-30s)**

5. **Verificar agendamentos novamente:**
   ```powershell
   curl http://localhost:5000/api/v1/agendamentos
   ```

6. **Comparar:**
   - [ ] Mesma quantidade de agendamentos
   - [ ] Mesmos IDs
   - [ ] Mesmos dados

**✅ Critérios de sucesso:**
- [ ] Dados persistiram após restart
- [ ] Nenhuma perda de informação

---

### Teste 10: Comunicação Inter-Containers

**Objetivo:** Validar que containers se comunicam via network

**Passos:**

1. **Executar comando dentro do container de agendamento:**
   ```powershell
   docker exec sctec-agendamento curl http://coordenador:3000/health
   ```

2. **Resultado esperado:**
   ```json
   {
     "status": "healthy",
     "service": "servico-coordenador",
     ...
   }
   ```

3. **Verificar DNS reverso:**
   ```powershell
   docker exec sctec-coordenador wget -qO- http://agendamento:5000/api/v1/time
   ```

**✅ Critérios de sucesso:**
- [ ] Containers se encontram por nome (DNS)
- [ ] Comunicação HTTP funciona
- [ ] Não há erros de rede

---

### Teste 11: Logs Agregados

**Objetivo:** Validar rastreamento distribuído com correlation IDs

**Passos:**

1. **Criar um agendamento via interface ou API**

2. **Observar logs em tempo real:**
   ```powershell
   docker-compose logs -f
   ```

3. **Procurar por correlation_id:**
   - [ ] Mesmo UUID aparece em logs do coordenador E agendamento
   - [ ] Sequência visível: requisição → lock → verificação → save → unlock → resposta

4. **Exemplo esperado:**
   ```
   agendamento  | [INFO] ... a1b2c3d4-...: Requisição POST /agendamentos recebida
   agendamento  | [INFO] ... a1b2c3d4-...: Tentando adquirir lock
   coordenador  | [INFO] ... Recebido pedido de lock...
   coordenador  | [INFO] ... Lock concedido...
   agendamento  | [INFO] ... a1b2c3d4-...: Lock adquirido com sucesso
   agendamento  | [INFO] ... a1b2c3d4-...: Salvando agendamento
   agendamento  | [INFO] ... a1b2c3d4-...: Liberando lock
   ```

**✅ Critérios de sucesso:**
- [ ] Correlation ID presente em todas as linhas
- [ ] Mesmo ID em ambos os serviços
- [ ] Sequência lógica visível

---

### Teste 12: Validação de Regras de Negócio

**Objetivo:** Confirmar que validações estão funcionando

**Testes a executar:**

1. **Duração muito curta (< 5 min):**
   ```powershell
   curl -X POST http://localhost:5000/api/v1/agendamentos `
     -H "Content-Type: application/json" `
     -d '{
       "cientista_id": 1,
       "horario_inicio_utc": "2025-12-31T12:00:00Z",
       "horario_fim_utc": "2025-12-31T12:03:00Z",
       "objeto_celeste": "Teste"
     }'
   ```
   
   **Esperado:** `400 Bad Request` - "Duração mínima: 5 minutos"

2. **Duração muito longa (> 2h):**
   - Fim: 3 horas depois do início
   - **Esperado:** `400 Bad Request` - "Duração máxima: 120 minutos"

3. **Não múltiplo de 5 minutos:**
   - Início: 10:07 (não termina em 0 ou 5)
   - **Esperado:** `400 Bad Request` - "múltiplos de 5 minutos"

4. **No passado:**
   - Início: `2020-01-01T10:00:00Z`
   - **Esperado:** `400 Bad Request` - "Não é possível agendar no passado"

5. **Antecedência < 24h:**
   - Início: daqui 2 horas
   - **Esperado:** `400 Bad Request` - "Antecedência mínima: 24 horas"

**✅ Critérios de sucesso:**
- [ ] Todas as validações retornam 400
- [ ] Mensagens de erro descritivas

---

## 🧹 Limpeza e Finalização

### Parar sistema (preserva dados):
```powershell
.\stop.bat
# ou
docker-compose stop
```

### Remover tudo (incluindo volumes):
```powershell
.\clean.bat
# ou
docker-compose down -v
```

### Ver uso de disco:
```powershell
docker system df
```

---

## 🐛 Troubleshooting

### Problema: Container não inicia

**Solução:**
```powershell
# Ver logs de erro
docker-compose logs coordenador
docker-compose logs agendamento

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Porta em uso

**Solução:**
```powershell
# Ver o que está usando
netstat -ano | findstr ":5000"
netstat -ano | findstr ":3000"

# Matar processo (substitua PID)
taskkill /PID 12345 /F
```

### Problema: Health check falha

**Solução:**
```powershell
# Verificar logs detalhados
docker inspect sctec-agendamento
docker inspect sctec-coordenador

# Testar manualmente
docker exec sctec-agendamento curl http://localhost:5000/api/v1/time
docker exec sctec-coordenador wget -qO- http://localhost:3000/health
```

### Problema: Containers não se comunicam

**Solução:**
```powershell
# Verificar network
docker network inspect sctec-network

# Reiniciar com network limpa
docker-compose down
docker network prune
docker-compose up -d
```

---

## ✅ Checklist Final

Marque conforme completa os testes:

- [ ] Teste 1: Deploy com Docker ✓
- [ ] Teste 2: Health checks ✓
- [ ] Teste 3: Interface web ✓
- [ ] Teste 4: Criar cientista ✓
- [ ] Teste 5: Criar agendamento ✓
- [ ] Teste 6: Exclusão mútua ✓
- [ ] Teste 7: Interface completa ✓
- [ ] Teste 8: Concorrência extrema ✓
- [ ] Teste 9: Persistência ✓
- [ ] Teste 10: Comunicação inter-containers ✓
- [ ] Teste 11: Logs agregados ✓
- [ ] Teste 12: Validações de negócio ✓

**Status geral:** ___/12 testes passaram

---

## 📸 Evidências Sugeridas

Para documentação final, capture:

1. Screenshot: `docker-compose ps` (containers healthy)
2. Screenshot: Interface web funcionando
3. Screenshot: Painel de sincronização de tempo
4. Log: Saída do `test_com_lock.py` mostrando 1 sucesso
5. Log: `docker-compose logs` mostrando correlation IDs
6. Screenshot: Agendamento sendo cancelado via interface

---

## 🎉 Conclusão

Após completar todos os testes, você terá validado:

✅ Sistema containerizado funcional  
✅ Exclusão mútua sob alta concorrência  
✅ Sincronização de tempo (Algoritmo de Cristian)  
✅ HATEOAS funcionando dinamicamente  
✅ Logging distribuído com rastreamento  
✅ Persistência de dados  
✅ Comunicação inter-serviços  
✅ Validações de regras de negócio  

**O sistema está PRONTO PARA PRODUÇÃO (em ambiente acadêmico)!**

---

**Última atualização:** 2025  
**Versão:** 1.0.0
