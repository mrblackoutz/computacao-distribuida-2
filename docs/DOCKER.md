# Guia Docker - SCTEC

## 🎯 Objetivo

Containerizar todo o sistema SCTEC usando Docker e Docker Compose, permitindo deployment consistente, isolamento de dependências e fácil orquestração dos microserviços.

## 📋 Pré-requisitos

### Software Necessário

- **Docker Desktop** 24.0+
  - Windows: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
  - Mac: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
  - Linux: Docker Engine + Docker Compose

- **Recursos do Sistema**
  - RAM: Mínimo 4GB (recomendado 8GB)
  - Disco: 5GB livres
  - CPU: 2+ cores

### Portas Necessárias

- `3000`: Serviço Coordenador
- `5000`: Serviço de Agendamento

**Verificar se estão livres:**
```powershell
# Windows PowerShell
netstat -ano | findstr ":3000"
netstat -ano | findstr ":5000"
```

```bash
# Linux/Mac
lsof -i :3000
lsof -i :5000
```

## 🏗️ Arquitetura dos Containers

```
┌─────────────────────────────────────────┐
│         Docker Compose                  │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐   ┌───────────────┐  │
│  │ Coordenador  │   │  Agendamento  │  │
│  │ (Node.js)    │   │  (Flask)      │  │
│  │ Port: 3000   │←──│  Port: 5000   │  │
│  └──────────────┘   └───────────────┘  │
│         │                    │         │
│         │              ┌─────┴─────┐   │
│         │              │  Volumes  │   │
│         │              │  - DB     │   │
│         │              │  - Logs   │   │
│         │              └───────────┘   │
│         │                              │
│    ┌────┴────────┐                     │
│    │   Network   │                     │
│    │ sctec-net   │                     │
│    └─────────────┘                     │
└─────────────────────────────────────────┘
```

## 🚀 Início Rápido

### Opção 1: Scripts Automatizados (Recomendado)

**Linux/Mac:**
```bash
chmod +x start.sh stop.sh clean.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

### Opção 2: Comandos Manuais

```bash
# Build e iniciar
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose stop

# Remover
docker-compose down
```

## 📦 Detalhes dos Dockerfiles

### Dockerfile - Serviço de Agendamento (Python)

**Localização:** `servico-agendamento/Dockerfile`

```dockerfile
FROM python:3.13-slim

# Dependências do sistema
RUN apt-get update && apt-get install -y gcc

# Dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código da aplicação
COPY . .

# Diretórios
RUN mkdir -p logs instance

EXPOSE 5000

# Health check
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/v1/time')"

CMD ["python", "run.py"]
```

**Características:**
- ✅ Imagem base: `python:3.13-slim` (~150MB)
- ✅ Multi-stage não necessário (aplicação simples)
- ✅ Health check automático
- ✅ Logs unbuffered (`PYTHONUNBUFFERED=1`)
- ✅ .dockerignore para otimizar build

### Dockerfile - Serviço Coordenador (Node.js)

**Localização:** `servico-coordenador/Dockerfile`

```dockerfile
FROM node:18-alpine

# Dependências
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Código
COPY . .

EXPOSE 3000

# Health check
HEALTHCHECK CMD wget --spider http://localhost:3000/health

# Segurança: usuário não-root
USER node

CMD ["node", "server.js"]
```

**Características:**
- ✅ Imagem base: `node:18-alpine` (~170MB)
- ✅ Alpine = menor tamanho
- ✅ Health check com wget
- ✅ Roda como usuário não-root
- ✅ Cache de layers otimizado

## 🔧 docker-compose.yml

**Localização:** raiz do projeto

### Serviço Coordenador

```yaml
coordenador:
  build: ./servico-coordenador
  container_name: sctec-coordenador
  ports:
    - "3000:3000"
  environment:
    - NODE_ENV=production
    - PORT=3000
  networks:
    - sctec-network
  healthcheck:
    interval: 30s
    timeout: 10s
    retries: 3
  restart: unless-stopped
  logging:
    max-size: "10m"
    max-file: "3"
```

### Serviço de Agendamento

```yaml
agendamento:
  build: ./servico-agendamento
  container_name: sctec-agendamento
  ports:
    - "5000:5000"
  environment:
    - COORDENADOR_URL=http://coordenador:3000
    # ... outras vars
  volumes:
    - agendamento-db:/app/instance
    - agendamento-logs:/app/logs
  networks:
    - sctec-network
  depends_on:
    coordenador:
      condition: service_healthy
  restart: unless-stopped
```

**Recursos Importantes:**

1. **depends_on com condition:**
   - Agendamento só inicia após Coordenador estar healthy
   - Evita erros de conexão na inicialização

2. **Volumes nomeados:**
   - Dados persistem entre restarts
   - Fácil backup/restore

3. **Network bridge:**
   - Comunicação entre containers
   - DNS automático (coordenador → IP do container)

4. **Restart policy:**
   - `unless-stopped`: reinicia exceto se parado manualmente
   - Garante alta disponibilidade

5. **Logging:**
   - Rotação automática (10MB, 3 arquivos)
   - Evita disco cheio

## 📊 Comandos Essenciais

### Gerenciamento Básico

```bash
# Iniciar (build se necessário)
docker-compose up -d

# Iniciar com rebuild forçado
docker-compose up --build -d

# Parar
docker-compose stop

# Parar e remover containers
docker-compose down

# Parar, remover e deletar volumes
docker-compose down -v
```

### Logs

```bash
# Todos os serviços (tempo real)
docker-compose logs -f

# Serviço específico
docker-compose logs -f agendamento
docker-compose logs -f coordenador

# Últimas 100 linhas
docker-compose logs --tail=100

# Sem seguir (snapshot)
docker-compose logs

# Filtrar por timestamp
docker-compose logs --since="2025-11-10T15:00:00"
```

### Status e Diagnóstico

```bash
# Status dos containers
docker-compose ps

# Uso de recursos (CPU, RAM, I/O)
docker stats

# Inspecionar container
docker inspect sctec-agendamento
docker inspect sctec-coordenador

# Health check status
docker inspect --format='{{.State.Health.Status}}' sctec-agendamento
```

### Acesso aos Containers

```bash
# Shell interativo - Agendamento (bash)
docker exec -it sctec-agendamento /bin/bash

# Shell interativo - Coordenador (sh, pois Alpine)
docker exec -it sctec-coordenador /bin/sh

# Executar comando único
docker exec sctec-agendamento python -c "print('Hello')"

# Ver arquivos
docker exec sctec-agendamento ls -la /app
```

### Volumes

```bash
# Listar volumes
docker volume ls

# Inspecionar volume
docker volume inspect sctec-agendamento-db
docker volume inspect sctec-agendamento-logs

# Backup do banco de dados
docker run --rm \
  -v sctec-agendamento-db:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/backup-$(date +%Y%m%d).tar.gz -C /data .

# Restaurar backup
docker run --rm \
  -v sctec-agendamento-db:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/backup-20251110.tar.gz -C /data

# Remover volumes órfãos
docker volume prune
```

### Network

```bash
# Listar networks
docker network ls

# Inspecionar network
docker network inspect sctec-network

# Testar conectividade entre containers
docker exec sctec-agendamento ping coordenador
docker exec sctec-coordenador wget -O- http://agendamento:5000/api/v1/time
```

## 🔍 Troubleshooting

### Problema: Porta já em uso

**Sintoma:**
```
Error: Bind for 0.0.0.0:5000 failed: port is already allocated
```

**Solução:**
```powershell
# Windows: Ver quem está usando
netstat -ano | findstr ":5000"

# Matar processo
taskkill /PID <PID> /F

# Ou: Mudar porta no docker-compose.yml
ports:
  - "5001:5000"  # Host:Container
```

### Problema: Container não inicia

**Sintoma:**
```
docker-compose ps
sctec-agendamento   Exit 1
```

**Diagnóstico:**
```bash
# Ver logs de erro
docker-compose logs agendamento

# Ver últimas linhas
docker logs sctec-agendamento --tail=50

# Tentar iniciar manualmente para debug
docker run -it --rm sctec_agendamento /bin/bash
```

### Problema: Health check falha

**Sintoma:**
```
sctec-agendamento   unhealthy
```

**Diagnóstico:**
```bash
# Ver status detalhado
docker inspect --format='{{json .State.Health}}' sctec-agendamento | jq

# Testar health check manualmente
docker exec sctec-agendamento \
  python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/v1/time')"
```

### Problema: Comunicação entre containers falha

**Sintoma:**
```
requests.exceptions.ConnectionError: Failed to establish connection to http://coordenador:3000
```

**Diagnóstico:**
```bash
# Verificar se estão na mesma network
docker network inspect sctec-network

# Testar DNS
docker exec sctec-agendamento nslookup coordenador
docker exec sctec-agendamento ping -c 3 coordenador

# Testar conectividade HTTP
docker exec sctec-agendamento curl http://coordenador:3000/health
```

**Solução:**
```bash
# Recriar network
docker-compose down
docker network prune
docker-compose up -d
```

### Problema: Volumes não persistem dados

**Sintoma:**
Dados são perdidos após `docker-compose down`

**Causa:**
Usou `docker-compose down -v` (remove volumes)

**Solução:**
```bash
# Usar apenas stop (mantém volumes)
docker-compose stop

# Ou down sem -v
docker-compose down  # volumes permanecem
```

### Problema: Build falha

**Sintoma:**
```
ERROR: failed to solve: process "/bin/sh -c pip install -r requirements.txt" did not complete successfully
```

**Soluções:**
```bash
# Rebuild sem cache
docker-compose build --no-cache

# Build com mais output
docker-compose build --progress=plain

# Build apenas um serviço
docker-compose build agendamento
```

### Problema: Permissões (Linux)

**Sintoma:**
```
PermissionError: [Errno 13] Permission denied: '/app/logs/app.log'
```

**Solução:**
```dockerfile
# No Dockerfile, adicionar antes do CMD:
RUN chmod -R 777 logs instance
```

## 🔒 Segurança

### Variáveis de Ambiente Sensíveis

**NÃO fazer:**
```yaml
environment:
  - SECRET_KEY=minha-chave-secreta  # ❌ Exposto
```

**FAZER:**
```yaml
environment:
  - SECRET_KEY=${SECRET_KEY}  # ✅ Usa variável do host
```

**Criar `.env` (gitignored):**
```bash
SECRET_KEY=chave-super-secreta-aleatoria-123456
DATABASE_PASSWORD=senha-forte-aqui
```

### Usuário Não-Root

O Coordenador já roda como `USER node`. Para agendamento:

```dockerfile
# Adicionar no Dockerfile
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser
```

### Scan de Vulnerabilidades

```bash
# Scan de segurança
docker scan sctec_agendamento
docker scan sctec_coordenador

# Atualizar imagens base
docker pull python:3.13-slim
docker pull node:18-alpine
docker-compose build --pull
```

## 📈 Monitoramento

### Logs Estruturados

```bash
# Exportar logs para arquivo
docker-compose logs > logs-$(date +%Y%m%d).txt

# Análise de erros
docker-compose logs | grep ERROR

# Filtrar por correlation_id
docker-compose logs agendamento | grep "a1b2c3d4"
```

### Métricas

```bash
# Uso de recursos
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Disco usado por imagens
docker system df

# Limpar recursos não utilizados
docker system prune -a
```

## 🚢 Deploy em Produção

### Checklist

- [ ] Trocar `SECRET_KEY` por valor forte
- [ ] Configurar `FLASK_ENV=production`
- [ ] Habilitar HTTPS (Nginx/Traefik na frente)
- [ ] Backup automático de volumes
- [ ] Monitoramento (Prometheus/Grafana)
- [ ] Logging centralizado (ELK Stack)
- [ ] Limites de recursos (CPU/RAM)
- [ ] Replicação do Coordenador (HA)
- [ ] Banco de dados externo (PostgreSQL)

### Limites de Recursos

```yaml
services:
  agendamento:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          memory: 256M
```

## ✅ Validação da Entrega 5

### Teste 1: Build Successful
```bash
docker-compose build
# ✅ Ambas imagens buildadas sem erros
```

### Teste 2: Containers Healthy
```bash
docker-compose up -d
sleep 30
docker-compose ps
# ✅ Ambos com status "healthy"
```

### Teste 3: Comunicação Inter-Container
```bash
docker exec sctec-agendamento curl http://coordenador:3000/health
# ✅ {"status":"healthy",...}
```

### Teste 4: Persistência de Dados
```bash
# Criar cientista
curl -X POST http://localhost:5000/api/v1/cientistas -H "Content-Type: application/json" -d '{"nome":"Test","email":"test@test.com","instituicao":"Test","pais":"BR"}'

# Restart
docker-compose restart agendamento

# Verificar se ainda existe
curl http://localhost:5000/api/v1/cientistas
# ✅ Cientista ainda está lá
```

### Teste 5: Logs Agregados
```bash
docker-compose logs -f
# ✅ Ver logs de ambos serviços entrelaçados
```

### Teste 6: Health Checks
```bash
docker inspect --format='{{.State.Health.Status}}' sctec-agendamento
docker inspect --format='{{.State.Health.Status}}' sctec-coordenador
# ✅ Ambos retornam "healthy"
```

---

**Data de conclusão:** 2025-11-10  
**Status:** ✅ Completo
