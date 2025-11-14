# SCTEC - Sistema de Controle de Telescópio Espacial Compartilhado

Sistema distribuído para agendamento de observações em telescópio espacial acadêmico, desenvolvido como projeto da disciplina de Computação Distribuída.

## 🎯 Objetivos do Projeto

Este projeto demonstra na prática os principais conceitos de **Sistemas Distribuídos**:

- ✅ **API RESTful** com HATEOAS (Hypermedia as the Engine of Application State)
- ✅ **Exclusão Mútua** via coordenador centralizado com locks distribuídos
- ✅ **Sincronização de Tempo** usando Algoritmo de Cristian
- ✅ **Logging Distribuído** com correlation IDs
- ✅ **Containerização** com Docker e orquestração com Docker Compose
- ✅ **Microserviços** com comunicação inter-serviços

## 🏗️ Arquitetura

### Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                        Cliente Web                          │
│              (Interface HTML/CSS/JavaScript)                │
└────────────┬────────────────────────────────────────────────┘
             │
             │ HTTP REST
             │
┌────────────▼────────────────────────────────────────────────┐
│              Serviço de Agendamento (Flask)                 │
│                    Port: 5000                               │
├─────────────────────────────────────────────────────────────┤
│  - CRUD de Cientistas e Agendamentos                        │
│  - Validação de Regras de Negócio                          │
│  - HATEOAS Links Dinâmicos                                 │
│  - Logging (App + Audit)                                   │
│  - Sincronização de Tempo (endpoint /time)                │
└──────┬──────────────────────────────┬───────────────────────┘
       │                              │
       │ HTTP (Lock/Unlock)           │ SQLAlchemy
       │                              │
┌──────▼──────────────────┐    ┌──────▼──────────────┐
│  Serviço Coordenador    │    │   SQLite Database   │
│      (Node.js)          │    │                     │
│    Port: 3000           │    │ - cientistas        │
├─────────────────────────┤    │ - agendamentos      │
│ - POST /lock            │    └─────────────────────┘
│ - POST /unlock          │
│ - GET /locks (debug)    │
│ - GET /health           │
│ - Timeout 30s           │
│ - Cleanup automático    │
└─────────────────────────┘
```

### Microserviços

#### 1. Serviço de Agendamento (Python/Flask)
- **Porta:** 5000
- **Responsabilidades:**
  - API RESTful principal
  - Gerenciamento de cientistas e agendamentos
  - Persistência em SQLite
  - Logging estruturado (aplicação + auditoria)
  - Sincronização de tempo (endpoint `/api/v1/time`)
  - Interface web

#### 2. Serviço Coordenador (Node.js/Express)
- **Porta:** 3000
- **Responsabilidades:**
  - Controle de locks (exclusão mútua)
  - Gerenciamento de recursos compartilhados
  - Alta performance para concorrência
  - Timeout automático de locks (30s)
  - Limpeza periódica de locks expirados

### Comunicação

- **Protocolo:** HTTP/REST
- **Formato:** JSON
- **Discovery:** HATEOAS (links nas respostas da API)
- **Rastreamento:** Correlation IDs em todos os logs

## 🚀 Início Rápido

### Opção 1: Docker (Recomendado) 🐳

**Pré-requisitos:**
- Docker Desktop instalado
- Portas 3000 e 5000 livres

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Acessar:**
- 🌐 Interface Web: http://localhost:5000
- 🔗 API Agendamento: http://localhost:5000/api/v1
- 🔗 API Coordenador: http://localhost:3000

**Ver logs:**
```bash
docker-compose logs -f
```

**Parar:**
```bash
docker-compose stop
# ou
stop.bat   # Windows
./stop.sh  # Linux/Mac
```

### Opção 2: Desenvolvimento Local

**Pré-requisitos:**
- Python 3.13+
- Node.js 18+

**Terminal 1 - Serviço Coordenador:**
```bash
cd servico-coordenador
npm install
npm start
```

**Terminal 2 - Serviço de Agendamento:**
```bash
cd servico-agendamento
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
python run.py
```

**Terminal 3 - Acessar:**
```
http://localhost:5000
```

## 📚 Documentação Completa

### Entregas do Projeto

| Entrega | Status | Descrição | Documentação |
|---------|--------|-----------|--------------|
| **1** | ✅ | Blueprint da API | [MODELOS.md](docs/MODELOS.md), [API.md](docs/API.md), [LOGGING.md](docs/LOGGING.md), [ARQUITETURA.md](docs/ARQUITETURA.md) |
| **2** | ✅ | Sistema Inicial (demonstra race condition) | [ENTREGA2_RESUMO.md](docs/ENTREGA2_RESUMO.md), [INSTALL.md](INSTALL.md) |
| **3** | ✅ | Serviço Coordenador (resolve race condition) | [ENTREGA3_GUIA.md](docs/ENTREGA3_GUIA.md) |
| **4** | ✅ | Interface Web + Sincronização de Tempo | [ENTREGA4_GUIA.md](docs/ENTREGA4_GUIA.md) |
| **5** | ✅ | Containerização com Docker | [DOCKER.md](docs/DOCKER.md) |

### Documentos Principais

- **[MODELOS.md](docs/MODELOS.md)** - Entidades, atributos, relacionamentos, regras de negócio
- **[API.md](docs/API.md)** - Especificação completa da API RESTful com HATEOAS
- **[LOGGING.md](docs/LOGGING.md)** - Formato de logs de aplicação e auditoria
- **[ARQUITETURA.md](docs/ARQUITETURA.md)** - Diagramas de arquitetura e sequência
- **[DOCKER.md](docs/DOCKER.md)** - Guia completo de containerização
- **[INSTALL.md](INSTALL.md)** - Instalação passo a passo (desenvolvimento local)

## 🧪 Testes

### Teste 1: Demonstração do Problema (Race Condition)

**Sem lock - Entrega 2:**
```bash
# Com ambiente local ativo
python tests\test_concorrencia.py 10
```

**Resultado esperado:** Múltiplos agendamentos criados para o mesmo horário (PROBLEMA!)

### Teste 2: Demonstração da Solução (Exclusão Mútua)

**Com lock - Entrega 3:**
```bash
# Com ambos serviços rodando
python tests\test_com_lock.py 10
```

**Resultado esperado:** Apenas 1 agendamento criado, 9 recusados (SOLUÇÃO!)

### Teste 3: Interface Web

1. Acesse http://localhost:5000
2. Observe o painel de sincronização de tempo
3. Crie um agendamento
4. Veja-o aparecer na lista automaticamente
5. Cancele um agendamento
6. Observe o status mudar

### Teste 4: Carga Simultânea

```bash
# 50 requisições simultâneas
python tests\test_com_lock.py 50
```

**Resultado esperado:** Apenas 1 sucesso, 49 conflitos, sistema permanece consistente

---

## 🎬 Demonstração: Problema vs Solução

### Sistema de Toggle COM/SEM Lock

Este projeto implementa um **sistema de toggle** que permite alternar entre:

- **🔴 Versão SEM LOCK** (Entrega 2) - Demonstra o **PROBLEMA** da condição de corrida
- **🟢 Versão COM LOCK** (Entrega 3) - Demonstra a **SOLUÇÃO** com exclusão mútua

### Demonstração Rápida

#### Opção 1: Comparação Lado a Lado (Recomendada)

```powershell
.\demo_comparacao.ps1
```

Executa automaticamente:
1. Sistema SEM lock → Teste → Mostra múltiplos agendamentos criados ❌
2. Sistema COM lock → Teste → Mostra apenas 1 agendamento ✅
3. Resumo comparativo

#### Opção 2: Demonstrações Individuais

**Demonstrar PROBLEMA (SEM LOCK):**
```powershell
.\demo_sem_lock.ps1
python tests\test_concorrencia.py 10
```

**Demonstrar SOLUÇÃO (COM LOCK):**
```powershell
.\demo_com_lock.ps1
python tests\test_com_lock.py 10
```

### Como Funciona

O toggle é controlado pela variável de ambiente `USE_LOCK` no arquivo `.env`:

```bash
# Arquivo: .env
USE_LOCK=true   # COM lock (Produção) ✅
# ou
USE_LOCK=false  # SEM lock (Demonstração do problema) ⚠️
```

Ao iniciar, o sistema exibe qual versão está ativa:

```
✅ Sistema usando VERSÃO COM LOCK (Entrega 3 - Produção)
# ou
⚠️ Sistema usando VERSÃO SEM LOCK (Entrega 2 - Demonstração do problema)
```

### Comparação de Resultados

| Métrica | SEM LOCK ❌ | COM LOCK ✅ |
|---------|------------|------------|
| **Agendamentos criados** | 2-10 | 1 |
| **Conflitos HTTP 409** | 0-8 | 9 |
| **Estado do BD** | INCONSISTENTE | CONSISTENTE |
| **Race condition** | SIM | NÃO |

### Documentação Completa

- 📖 **Quick Start:** `QUICK_START_TOGGLE.md`
- 📖 **Guia Completo:** `GUIA_DEMONSTRACAO.md`
- 📖 **Documentação Técnica:** `docs/SISTEMA_TOGGLE.md`

---

## 🎓 Conceitos Aplicados

### 1. Exclusão Mútua
- **Problema:** Condição de corrida permite múltiplos agendamentos no mesmo horário
- **Solução:** Lock distribuído no Coordenador garante que apenas 1 cliente acessa o recurso por vez
- **Implementação:** try-finally garante liberação do lock mesmo em caso de erro

### 2. Algoritmo de Cristian (Sincronização de Tempo)
- **Problema:** Relógios cliente e servidor dessincronizados
- **Solução:** Cliente calcula offset baseado no RTT (Round-Trip Time)
- **Fórmula:** `Offset = (TempoServidor + RTT/2) - TempoCliente`
- **Implementação:** JavaScript na interface web

### 3. HATEOAS (Hypermedia as the Engine of Application State)
- **Conceito:** Cliente descobre ações disponíveis através dos links fornecidos pela API
- **Exemplo:** Botão "Cancelar" aparece apenas se `_links.cancelar` existe na resposta
- **Benefício:** Cliente não precisa conhecer regras de negócio do servidor

### 4. Logging Distribuído
- **Correlation ID:** UUID gerado por requisição, propaga entre serviços
- **Logs de Aplicação:** Eventos técnicos (INFO, WARNING, ERROR)
- **Logs de Auditoria:** Eventos de negócio em JSON (quem fez o quê, quando)

### 5. Microserviços
- **Separação de Responsabilidades:** Cada serviço tem uma função específica
- **Comunicação:** HTTP/REST entre serviços
- **Escalabilidade:** Serviços podem escalar independentemente

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.13** - Serviço de Agendamento
- **Flask 3.0** - Framework web
- **SQLAlchemy 3.1** - ORM
- **SQLite** - Banco de dados

### Coordenação
- **Node.js 18** - Serviço Coordenador
- **Express 4.18** - Framework web

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização (gradientes, animações)
- **JavaScript** - Lógica (Algoritmo de Cristian)
- **Zod** - Validação de formulários (type-safe schemas)

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração

## 📈 Estatísticas do Projeto

- **Linhas de código:** ~5000+
- **Arquivos Python:** 20+
- **Arquivos JavaScript:** 2
- **Endpoints API:** 9
- **Documentação:** 8 arquivos Markdown
- **Testes:** 2 scripts automatizados
- **Containers:** 2
- **Volumes:** 2 (banco de dados + logs)

## 🎓 Regras de Negócio

- ⏱ **Duração:** 5 minutos (mínimo) a 2 horas (máximo)
- 📅 **Granularidade:** Múltiplos de 5 minutos
- ⏰ **Antecedência:** Mínimo 24 horas
- 🔢 **Limite:** Máximo 3 agendamentos ativos por cientista
- 🕐 **Timezone:** Todos os horários em UTC
- ❌ **Cancelamento:** Apenas agendamentos com status AGENDADO

## 🐛 Troubleshooting

### Docker não inicia

```bash
# Verificar se Docker Desktop está rodando
docker info

# Ver logs de erro
docker-compose logs

# Rebuild completo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Porta em uso

```powershell
# Windows: Ver o que está usando a porta
netstat -ano | findstr ":5000"
netstat -ano | findstr ":3000"

# Matar processo
taskkill /PID <PID> /F
```

```bash
# Linux/Mac: Ver e matar
lsof -ti:5000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Coordenador offline

```bash
# Verificar status
docker-compose ps

# Reiniciar apenas coordenador
docker-compose restart coordenador

# Ver logs
docker-compose logs -f coordenador
```

### Banco de dados corrompido

```bash
# Remover volume e reiniciar
docker-compose down -v
docker-compose up -d
```

## 📖 Próximos Passos (Melhorias Futuras)

- [ ] **Autenticação:** JWT tokens para cientistas
- [ ] **Autorização:** Permissões por papel (admin, cientista)
- [ ] **PostgreSQL:** Migrar de SQLite para produção
- [ ] **Redis:** Locks distribuídos com expiração automática
- [ ] **WebSockets:** Atualização em tempo real da interface
- [ ] **Kubernetes:** Deploy em cluster
- [ ] **Prometheus:** Métricas de performance
- [ ] **Grafana:** Dashboards de monitoramento
- [ ] **CI/CD:** GitHub Actions para testes e deploy
- [ ] **Testes Unitários:** Cobertura completa

## 👥 Autor

Desenvolvido para a disciplina de **Computação Distribuída**

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.
