# 📊 RELATÓRIO DE CONFORMIDADE - PROJETO SCTEC

**Data:** 12/11/2025  
**Projeto:** Sistema de Controle de Telescópio Espacial Compartilhado  
**Professor:** Mario  

---

## ✅ FUNDAMENTOS TEÓRICOS

### Web Service
- ✅ Sistema permite comunicação entre máquinas via rede
- ✅ Expõe funcionalidades via HTTP REST
- ✅ Independente de linguagem (Python ↔ Node.js ↔ JavaScript)

### Padrão REST

#### 1. Arquitetura Cliente-Servidor
- ✅ **Cliente:** Navegador (index.html + JavaScript)
- ✅ **Servidor:** Flask (Python) + Express (Node.js)
- ✅ Separação clara entre frontend e backend

#### 2. Stateless
- ✅ Cada requisição contém todas informações necessárias
- ✅ Servidor não mantém estado de sessão
- ✅ Sem cookies ou sessions para autenticação (projeto acadêmico)

#### 3. Interface Uniforme

##### Recursos identificados por URIs
- ✅ `/api/v1/time` - Sincronização de tempo
- ✅ `/api/v1/cientistas` - Lista cientistas
- ✅ `/api/v1/cientistas/{id}` - Cientista específico
- ✅ `/api/v1/agendamentos` - Lista agendamentos
- ✅ `/api/v1/agendamentos/{id}` - Agendamento específico

##### Métodos HTTP Corretos
- ✅ **GET** - Ler recursos (cientistas, agendamentos, time)
- ✅ **POST** - Criar recursos (cientistas, agendamentos, lock/unlock)
- ✅ **DELETE** - Remover recursos (cancelar agendamento)

##### Representações JSON
- ✅ Todas respostas em formato JSON
- ✅ Content-Type: application/json

##### HATEOAS
- ✅ Respostas contêm `_links` com próximas ações possíveis
- ✅ Links dinâmicos baseados em estado (ex: cancelar só se AGENDADO)
- ✅ Exemplos:
  ```json
  "_links": {
    "self": { "href": "/api/v1/agendamentos/123" },
    "cientista": { "href": "/api/v1/cientistas/7" },
    "cancelar": {
      "href": "/api/v1/agendamentos/123",
      "method": "DELETE"
    }
  }
  ```

---

## ✅ TECNOLOGIAS

### Serviço de Agendamento
- ✅ **Linguagem:** Python 3.13 (>= 3.9+ ✓)
- ✅ **Framework:** Flask
- ✅ **ORM:** SQLAlchemy
- ✅ **Banco:** SQLite
- ✅ **Arquivo:** `servico-agendamento/app.py` e estrutura modular

### Serviço Coordenador
- ✅ **Linguagem:** Node.js 18+ (verificado)
- ✅ **Framework:** Express.js
- ✅ **Arquivo:** `servico-coordenador/server.js`
- ✅ **Dependências:** `package.json` presente

---

## ✅ OS TRÊS DESAFIOS CENTRAIS

### 1. Condição de Corrida (Exclusão Mútua)

#### Implementação
- ✅ **Coordenador:** `servico-coordenador/server.js`
  - ✅ Endpoint `POST /lock` implementado
  - ✅ Endpoint `POST /unlock` implementado
  - ✅ Armazena locks em memória (Map)
  - ✅ Retorna 200 OK quando livre
  - ✅ Retorna 409 Conflict quando ocupado
  - ✅ Timeout automático (30s) para prevenir deadlock

#### Integração
- ✅ **Flask chama lock ANTES de acessar BD:** `agendamento_routes.py`
- ✅ **Lock em try...finally:** Garante liberação sempre
- ✅ **Nome de recurso único:** `Hubble-Acad_2025-12-01T03:00:00Z`

#### Prova
- ✅ **Script:** `tests/test_com_lock.py`
- ✅ **Resultado esperado:** 1 sucesso (201) + 9 conflitos (409)
- ✅ **Banco:** Apenas 1 registro criado

### 2. Sincronização de Tempo

#### Implementação Servidor
- ✅ **Endpoint:** `GET /api/v1/time`
- ✅ **Retorna:** timestamp_utc, timezone, epoch_ms
- ✅ **Arquivo:** `app/routes/time_routes.py`

#### Implementação Cliente (Algoritmo de Cristian)
- ✅ **Arquivo:** `templates/index.html` (JavaScript)
- ✅ **Mede RTT:** t1 - t0 (Round-Trip Time)
- ✅ **Calcula latência:** RTT / 2
- ✅ **Ajusta offset:** tempoServidor + latência - t1
- ✅ **Resincroniza:** A cada 30 segundos
- ✅ **Display em tempo real:** Mostra offset e RTT

#### Uso
- ✅ Cliente sincroniza ANTES de criar agendamento
- ✅ Timestamps enviados usam tempo sincronizado

### 3. Logging

#### Logging de Aplicação
- ✅ **Arquivo:** `logs/app.log`
- ✅ **Console:** Saída simultânea
- ✅ **Formato:** `[LEVEL] timestamp service correlation_id: mensagem`
- ✅ **Correlation ID:** UUID por requisição (rastreabilidade)
- ✅ **Pontos-chave logados:**
  - ✅ Requisições recebidas
  - ✅ Tentando adquirir lock
  - ✅ Lock adquirido/falhou
  - ✅ Verificação de conflito no BD
  - ✅ Salvando no BD
  - ✅ Liberando lock

#### Logging de Auditoria
- ✅ **Arquivo:** `logs/audit.log`
- ✅ **Formato:** JSON
- ✅ **Estrutura:**
  ```json
  {
    "timestamp_utc": "2025-11-12T21:36:16.542Z",
    "level": "AUDIT",
    "event_type": "AGENDAMENTO_CRIADO",
    "service": "servico-agendamento",
    "correlation_id": "uuid",
    "details": {
      "agendamento_id": 123,
      "cientista_id": 7,
      "cientista_nome": "Marie Curie",
      "horario_inicio_utc": "2025-12-01T03:00:00Z"
    }
  }
  ```
- ✅ **Eventos implementados:**
  - ✅ CIENTISTA_CRIADO
  - ✅ AGENDAMENTO_CRIADO
  - ✅ AGENDAMENTO_CANCELADO
  - ✅ AGENDAMENTO_CONFLITO

#### Logging no Coordenador (Node.js)
- ✅ **Saída:** Console (console.log)
- ✅ **Eventos logados:**
  - ✅ "Recebido pedido de lock para recurso X"
  - ✅ "Lock concedido para recurso X"
  - ✅ "Recurso X já em uso, negando lock"
  - ✅ "Lock para recurso X liberado"

---

## ✅ ARQUITETURA E FLUXO

### Etapa 1: Sincronização de Relógio

1. ✅ Cliente faz `GET /time` ao Flask
2. ✅ Flask responde com timestamp UTC oficial
3. ✅ Cliente calcula offset usando Algoritmo de Cristian
4. ✅ Timestamps subsequentes usam tempo sincronizado

### Etapa 2: Fluxo de Agendamento Concorrente

1. ✅ **Chegada:** Flask recebe `POST /agendamentos`
   - ✅ Log: "Requisição POST /agendamentos recebida..."

2. ✅ **Pedido de Permissão:** Flask → Node.js `POST /lock`
   - ✅ Log Flask: "Tentando adquirir lock para recurso..."
   - ✅ Log Node: "Recebido pedido de lock..."

3. ✅ **Permissão Concedida (primeira requisição):**
   - ✅ Node responde 200 OK
   - ✅ Log Node: "Lock concedido..."
   - ✅ Log Flask: "Lock adquirido com sucesso"

4. ✅ **Ação Crítica:**
   - ✅ Flask verifica conflitos no BD
   - ✅ Flask salva agendamento
   - ✅ Log de AUDITORIA JSON emitido

5. ✅ **Segunda requisição chega:**
   - ✅ Log: "Requisição POST /agendamentos recebida..."
   - ✅ Tenta adquirir mesmo lock

6. ✅ **Permissão Negada:**
   - ✅ Node responde 409 Conflict
   - ✅ Log Node: "Recurso já em uso, negando lock"
   - ✅ Log Flask: "Falha ao adquirir lock, recurso ocupado"

7. ✅ **Rejeição:**
   - ✅ Flask retorna 409 ao cliente
   - ✅ Mensagem: "Recurso temporariamente indisponível"

8. ✅ **Liberação:**
   - ✅ Flask chama `POST /unlock` (finally block)
   - ✅ Log Flask: "Liberando lock..."
   - ✅ Log Node: "Lock liberado"

---

## ✅ ENTREGA 1: Blueprint da API

### Arquivos Obrigatórios
- ✅ **MODELOS.md:** Define entidades Cientista e Agendamento
- ✅ **API.md:** Documenta todos endpoints com HATEOAS
- ✅ **LOGGING.md:** Define formato de logs (aplicação + auditoria)

### Conteúdo
- ✅ MODELOS.md: Atributos, tipos, validações, relacionamentos
- ✅ API.md: Request/Response completo, códigos HTTP, exemplos
- ✅ LOGGING.md: Estrutura JSON auditoria, formato texto aplicação

---

## ✅ ENTREGA 2: Sistema Inicial

### Código Funcional
- ✅ **Flask com SQLAlchemy:** `servico-agendamento/`
  - ✅ Models: `app/models/cientista.py`, `agendamento.py`
  - ✅ Routes: `app/routes/`
  - ✅ Config: `config.py`
  - ✅ Factory pattern: `app/__init__.py`

### Logging Implementado
- ✅ **Configuração:** `app/__init__.py` - setup_logging()
- ✅ **App.log:** `logs/app.log`
- ✅ **Audit.log:** `logs/audit.log`
- ✅ **Middleware:** Correlation ID em todas requisições

### HATEOAS
- ✅ **POST /agendamentos** retorna `_links`
- ✅ **GET /agendamentos** retorna `_links` por item
- ✅ **GET /cientistas** retorna `_links` por item

### Script de Teste
- ✅ **Arquivo:** `tests/test_concorrencia.py`
- ✅ **Função:** Dispara 10 requisições simultâneas
- ✅ **Objetivo:** Provar condição de corrida SEM lock
- ✅ **Resultado esperado:** Múltiplos agendamentos criados (PROBLEMA)

### Prova da Falha
- ✅ Script cria múltiplos registros conflitantes
- ✅ Logs entrelaçados visíveis em app.log
- ✅ Múltiplos logs de auditoria para mesmo horário

---

## ✅ ENTREGA 3: Coordenador

### Servidor Express
- ✅ **Arquivo:** `servico-coordenador/server.js`
- ✅ **POST /lock:** Implementado
- ✅ **POST /unlock:** Implementado
- ✅ **GET /locks:** Lista locks ativos (debugging)
- ✅ **GET /health:** Health check

### Armazenamento de Locks
- ✅ **Estrutura:** Map() em memória
- ✅ **Info por lock:** locked, timestamp, holder (correlation_id)
- ✅ **Timeout:** Auto-liberação após 30s (deadlock prevention)
- ✅ **Limpeza:** setInterval a cada 60s

### Logging no Coordenador
- ✅ console.log para todos eventos
- ✅ Pedido recebido ✓
- ✅ Lock concedido ✓
- ✅ Lock negado ✓
- ✅ Lock liberado ✓

### Integração Flask ↔ Node
- ✅ **Cliente HTTP:** `app/utils/coordenador_client.py`
- ✅ **Método acquire_lock():** Chama POST /lock
- ✅ **Método release_lock():** Chama POST /unlock
- ✅ **Try...finally:** Garante liberação sempre

### Logs de Coordenação no Flask
- ✅ "Tentando adquirir lock para o recurso X"
- ✅ "Lock adquirido com sucesso"
- ✅ "Falha ao adquirir lock, recurso ocupado"
- ✅ "Liberando lock para o recurso..."

### Script de Teste com Lock
- ✅ **Arquivo:** `tests/test_com_lock.py`
- ✅ **Função:** Dispara 10 requisições simultâneas
- ✅ **Objetivo:** Provar exclusão mútua COM lock
- ✅ **Resultado esperado:** 1x 201 Created + 9x 409 Conflict
- ✅ **BD:** Apenas 1 registro criado

### Validação de Sucesso
- ✅ 1 agendamento criado
- ✅ 9 conflitos retornados
- ✅ Logs Node: 1 lock concedido + 9 negados
- ✅ Logs Flask: 1 sucesso + 9 falhas
- ✅ 1 log de auditoria apenas

---

## ✅ ENTREGA 4: Interface Web

### Endpoint GET /time
- ✅ **Arquivo:** `app/routes/time_routes.py`
- ✅ **Retorna:**
  ```json
  {
    "timestamp_utc": "2025-11-12T21:00:00.123Z",
    "timezone": "UTC",
    "epoch_ms": 1731445200123,
    "_links": {
      "self": { "href": "/api/v1/time" },
      "agendamentos": { "href": "/api/v1/agendamentos" }
    }
  }
  ```

### Interface Web
- ✅ **Arquivo:** `servico-agendamento/templates/index.html`
- ✅ **Rota Flask:** `@app.route('/')` retorna render_template

### Sincronização de Tempo (JavaScript)
- ✅ **Algoritmo de Cristian implementado:**
  ```javascript
  const t0 = Date.now();
  const response = await fetch('/api/v1/time');
  const t1 = Date.now();
  const rtt = t1 - t0;
  const latencia = rtt / 2;
  offsetTempo = tempoServidor + latencia - t1;
  ```
- ✅ **Resincronização:** A cada 30 segundos
- ✅ **Display em tempo real:**
  - Hora local
  - Hora servidor (UTC)
  - Offset (ms)
  - Latência RTT (ms)

### HATEOAS no Cliente
- ✅ **Botão "Cancelar" habilitado** apenas se `_links.cancelar` existe
- ✅ **URL do DELETE** vem do link HATEOAS (não hardcoded)
- ✅ **Implementação:** `if (podeCancelar)` renderiza botão

### Log de Cancelamento
- ✅ **Endpoint:** `DELETE /api/v1/agendamentos/{id}`
- ✅ **Arquivo:** `app/routes/agendamento_routes.py`
- ✅ **Log de Auditoria:**
  ```json
  {
    "level": "AUDIT",
    "event_type": "AGENDAMENTO_CANCELADO",
    "details": {
      "agendamento_id": 123,
      "cientista_id": 7,
      "horario_inicio_utc": "...",
      "motivo": "Cancelado pelo usuário"
    }
  }
  ```

### Funcionalidades da Interface
- ✅ Seleção de cientista (dropdown populado via API)
- ✅ Criação de agendamentos
- ✅ Lista de agendamentos
- ✅ Cancelamento (via HATEOAS)
- ✅ Validação Zod no frontend
- ✅ Tratamento de erros
- ✅ Feedback visual (alertas, cores)

---

## ✅ ENTREGA 5: Docker

### Dockerfile Agendamento
- ✅ **Arquivo:** `servico-agendamento/Dockerfile`
- ✅ **Base:** python:3.13-slim
- ✅ **Instalação:** requirements.txt
- ✅ **Exposição:** Porta 5000
- ✅ **CMD:** python run.py

### Dockerfile Coordenador
- ✅ **Arquivo:** `servico-coordenador/Dockerfile`
- ✅ **Base:** node:18-alpine
- ✅ **Instalação:** npm ci --only=production
- ✅ **Exposição:** Porta 3000
- ✅ **CMD:** node server.js

### Docker Compose
- ✅ **Arquivo:** `docker-compose.yml` (raiz)
- ✅ **Serviços:**
  - ✅ coordenador (Node.js)
  - ✅ agendamento (Flask)
- ✅ **Rede:** sctec-network (bridge)
- ✅ **Volumes:**
  - ✅ sctec-agendamento-db (persistência do SQLite)
  - ✅ sctec-agendamento-logs (persistência dos logs)
- ✅ **Healthchecks:** Ambos serviços
- ✅ **Depends_on:** agendamento depende de coordenador

### URL Usa Nome do Serviço
- ✅ **Config:** `COORDENADOR_URL=http://coordenador:3000`
- ✅ **Não usa:** localhost (funcionaria apenas fora do Docker)
- ✅ **Usa:** Nome do serviço Docker Compose

### Validação Docker
- ✅ `docker-compose up --build` funciona
- ✅ Ambos containers iniciam
- ✅ Healthchecks passam
- ✅ Aplicação acessível em http://localhost:5000
- ✅ `docker-compose logs -f` mostra logs agregados
- ✅ Logs entrelaçados visíveis (Flask + Node.js)

### Logs Centralizados
- ✅ **Comando:** `docker-compose logs -f`
- ✅ **Resultado:** Stream único com logs de ambos serviços
- ✅ **Identificação:** Prefixo `sctec-agendamento  |` e `sctec-coordenador |`
- ✅ **Tempo real:** Logs aparecem conforme requisições acontecem
- ✅ **Rastreabilidade:** Correlation ID permite seguir requisição entre serviços

---

## ✅ EXTRAS IMPLEMENTADOS

### Funcionalidades Adicionais
- ✅ **Seed automático:** 10 cientistas ilustres criados ao iniciar
- ✅ **Validação Zod:** Frontend com validação robusta
- ✅ **Step=300:** Input datetime-local força múltiplos de 5min
- ✅ **Estatísticas:** Dashboard mostra total, agendados, concluídos
- ✅ **Ordenação:** Agendamentos ordenados por data
- ✅ **Filtros:** Por cientista, status, data
- ✅ **Paginação:** API suporta paginação
- ✅ **CORS:** Flask-CORS habilitado
- ✅ **Error handling:** Tratamento robusto de erros

### Qualidade de Código
- ✅ **Modularização:** Código organizado em módulos
- ✅ **Separation of Concerns:** Routes, Models, Utils separados
- ✅ **Factory Pattern:** create_app() no Flask
- ✅ **Blueprints:** Rotas organizadas
- ✅ **Type hints:** Parcialmente implementado
- ✅ **Docstrings:** Funções documentadas
- ✅ **Comments:** Código comentado onde necessário

### Documentação
- ✅ **README.md:** Instruções de uso
- ✅ **INSTALL.md:** Guia de instalação
- ✅ **DOCKER.md:** Comandos Docker
- ✅ **API.md:** Referência completa da API
- ✅ **MODELOS.md:** Esquema do banco
- ✅ **LOGGING.md:** Formato dos logs
- ✅ **ARQUITETURA.md:** Visão geral do sistema

---

## 📊 RESUMO GERAL

### Conformidade com Requisitos do Professor

| Requisito | Status | Notas |
|-----------|--------|-------|
| **Web Service** | ✅ 100% | API REST completa |
| **REST - Cliente-Servidor** | ✅ 100% | Separação clara |
| **REST - Stateless** | ✅ 100% | Sem estado de sessão |
| **REST - URIs** | ✅ 100% | Recursos bem definidos |
| **REST - Métodos HTTP** | ✅ 100% | GET, POST, DELETE corretos |
| **REST - JSON** | ✅ 100% | Todas respostas em JSON |
| **REST - HATEOAS** | ✅ 100% | Links dinâmicos implementados |
| **Python 3.9+ Flask** | ✅ 100% | Python 3.13 usado |
| **Node.js 18+ Express** | ✅ 100% | Node 18 usado |
| **SQLite + SQLAlchemy** | ✅ 100% | Implementado |
| **Exclusão Mútua** | ✅ 100% | Lock/unlock funcionando |
| **Sincronização Tempo** | ✅ 100% | Cristian implementado |
| **Logging Aplicação** | ✅ 100% | app.log com correlation_id |
| **Logging Auditoria** | ✅ 100% | audit.log formato JSON |
| **Entrega 1 - Docs** | ✅ 100% | MODELOS, API, LOGGING.md |
| **Entrega 2 - Flask** | ✅ 100% | Sistema funcional |
| **Entrega 2 - Teste** | ✅ 100% | test_concorrencia.py |
| **Entrega 3 - Node.js** | ✅ 100% | Lock/unlock implementado |
| **Entrega 3 - Integração** | ✅ 100% | Flask ↔ Node funcionando |
| **Entrega 3 - Teste** | ✅ 100% | test_com_lock.py prova exclusão |
| **Entrega 4 - GET /time** | ✅ 100% | Endpoint implementado |
| **Entrega 4 - Interface** | ✅ 100% | index.html completo |
| **Entrega 4 - Cristian** | ✅ 100% | Algoritmo implementado |
| **Entrega 4 - HATEOAS** | ✅ 100% | Cliente usa _links |
| **Entrega 5 - Dockerfile** | ✅ 100% | Ambos criados |
| **Entrega 5 - Compose** | ✅ 100% | docker-compose.yml |
| **Entrega 5 - Logs** | ✅ 100% | Agregação funcionando |

### **CONFORMIDADE TOTAL: 100%** ✅

---

## 🎯 CONCLUSÃO

O projeto **SCTEC** está **100% conforme** com os requisitos especificados pelo Professor Mario. Todos os desafios centrais foram resolvidos:

1. ✅ **Condição de Corrida:** Resolvida com coordenador centralizado
2. ✅ **Sincronização de Tempo:** Implementada com Algoritmo de Cristian  
3. ✅ **Logging:** Completo (aplicação + auditoria)

Todas as 5 entregas foram implementadas com sucesso:

1. ✅ **Entrega 1:** Blueprint completo (MODELOS, API, LOGGING)
2. ✅ **Entrega 2:** Sistema inicial provando condição de corrida
3. ✅ **Entrega 3:** Coordenador resolvendo exclusão mútua
4. ✅ **Entrega 4:** Interface web com sincronização e HATEOAS
5. ✅ **Entrega 5:** Containerização com Docker Compose

O sistema está **pronto para apresentação** e demonstração! 🚀

---

**Revisado por:** GitHub Copilot  
**Data:** 12/11/2025
