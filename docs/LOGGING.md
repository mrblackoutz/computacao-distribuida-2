# Sistema de Logging - SCTEC

## Visão Geral

O sistema de logging do SCTEC serve dois propósitos principais:

1. **Logging de Aplicação**: Para depuração e monitoramento técnico
2. **Logging de Auditoria**: Para rastreabilidade de negócio e compliance

---

## 1. Logs de Auditoria (JSON)

### Estrutura Base

Todos os logs de auditoria são escritos em formato JSON estruturado para facilitar análise e indexação.

```json
{
  "timestamp_utc": "2025-11-09T15:30:45.123Z",
  "level": "AUDIT",
  "event_type": "TIPO_DO_EVENTO",
  "service": "servico-agendamento",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "details": {
    // Dados específicos do evento
  }
}
```

### Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `timestamp_utc` | String (ISO8601) | Timestamp exato do evento em UTC |
| `level` | String | Sempre "AUDIT" para logs de auditoria |
| `event_type` | String | Tipo do evento (ver lista abaixo) |
| `service` | String | Nome do serviço que gerou o log |
| `correlation_id` | String (UUID) | ID para rastrear requisição completa |
| `details` | Object | Detalhes específicos do evento |

---

## 2. Eventos de Auditoria

### 2.1. CIENTISTA_CRIADO

Registrado quando um novo cientista é cadastrado no sistema.

```json
{
  "timestamp_utc": "2025-11-09T15:30:45.123Z",
  "level": "AUDIT",
  "event_type": "CIENTISTA_CRIADO",
  "service": "servico-agendamento",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "details": {
    "cientista_id": 7,
    "nome": "Marie Curie",
    "email": "marie.curie@sorbonne.fr",
    "instituicao": "Universidade de Paris",
    "pais": "França"
  }
}
```

### 2.2. AGENDAMENTO_CRIADO

Registrado quando um agendamento é criado com sucesso.

```json
{
  "timestamp_utc": "2025-11-09T15:30:45.123Z",
  "level": "AUDIT",
  "event_type": "AGENDAMENTO_CRIADO",
  "service": "servico-agendamento",
  "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "details": {
    "agendamento_id": 123,
    "cientista_id": 7,
    "cientista_nome": "Marie Curie",
    "horario_inicio_utc": "2025-12-01T03:00:00Z",
    "horario_fim_utc": "2025-12-01T03:30:00Z",
    "objeto_celeste": "NGC 1300",
    "duracao_minutos": 30
  }
}
```

### 2.3. AGENDAMENTO_CANCELADO

Registrado quando um agendamento é cancelado.

```json
{
  "timestamp_utc": "2025-11-10T10:15:30.456Z",
  "level": "AUDIT",
  "event_type": "AGENDAMENTO_CANCELADO",
  "service": "servico-agendamento",
  "correlation_id": "b2c3d4e5-f6g7-8901-bcde-f12345678901",
  "details": {
    "agendamento_id": 123,
    "cientista_id": 7,
    "cientista_nome": "Marie Curie",
    "horario_inicio_utc": "2025-12-01T03:00:00Z",
    "horario_fim_utc": "2025-12-01T03:30:00Z",
    "motivo": "Conflito de agenda - necessidade de rescheduling"
  }
}
```

### 2.4. AGENDAMENTO_CONFLITO

Registrado quando uma tentativa de agendamento falha por conflito de horário ou lock.

```json
{
  "timestamp_utc": "2025-11-09T15:30:45.200Z",
  "level": "AUDIT",
  "event_type": "AGENDAMENTO_CONFLITO",
  "service": "servico-agendamento",
  "correlation_id": "c3d4e5f6-g7h8-9012-cdef-123456789012",
  "details": {
    "cientista_id": 8,
    "cientista_nome": "Albert Einstein",
    "horario_inicio_utc": "2025-12-01T03:00:00Z",
    "horario_fim_utc": "2025-12-01T03:30:00Z",
    "motivo": "Lock não disponível",
    "conflitos_com": [123]
  }
}
```

### 2.5. CIENTISTA_ATUALIZADO

Registrado quando dados de um cientista são atualizados.

```json
{
  "timestamp_utc": "2025-11-09T16:00:00.789Z",
  "level": "AUDIT",
  "event_type": "CIENTISTA_ATUALIZADO",
  "service": "servico-agendamento",
  "correlation_id": "d4e5f6g7-h8i9-0123-defg-234567890123",
  "details": {
    "cientista_id": 7,
    "campos_alterados": ["especialidade", "instituicao"],
    "valores_anteriores": {
      "especialidade": "Radioastronomia",
      "instituicao": "Universidade de Paris"
    },
    "valores_novos": {
      "especialidade": "Astrofísica Nuclear",
      "instituicao": "Sorbonne Université"
    }
  }
}
```

### 2.6. CIENTISTA_DESATIVADO

Registrado quando um cientista é desativado (soft delete).

```json
{
  "timestamp_utc": "2025-11-09T17:00:00.123Z",
  "level": "AUDIT",
  "event_type": "CIENTISTA_DESATIVADO",
  "service": "servico-agendamento",
  "correlation_id": "e5f6g7h8-i9j0-1234-efgh-345678901234",
  "details": {
    "cientista_id": 7,
    "nome": "Marie Curie",
    "email": "marie.curie@sorbonne.fr",
    "motivo": "Término de contrato"
  }
}
```

---

## 3. Logs de Aplicação (Texto)

### Formato Padrão

```
[LEVEL] timestamp_utc service correlation_id: mensagem
```

### Exemplo:
```
[INFO] 2025-11-09T15:30:45.123Z servico-agendamento a1b2c3d4: Requisição POST /agendamentos recebida
```

### Níveis de Log

| Nível | Quando Usar | Exemplo |
|-------|-------------|---------|
| **DEBUG** | Informações detalhadas para debugging | Valores de variáveis, estados intermediários |
| **INFO** | Fluxo normal da aplicação | Requisições recebidas, operações iniciadas |
| **WARNING** | Situações incomuns mas recuperáveis | Validações falhadas, timeouts recuperados |
| **ERROR** | Erros que impedem operações específicas | Falha ao conectar BD, timeout de serviço |
| **CRITICAL** | Falhas graves do sistema | Sistema não pode iniciar, BD inacessível |

---

## 4. Exemplo de Fluxo Completo com Logs

### Cenário: Criação de Agendamento com Sucesso

#### Terminal do Serviço de Agendamento (Flask)

```
[INFO] 2025-11-09T15:30:45.100Z servico-agendamento a1b2c3d4: Requisição POST /agendamentos recebida
[INFO] 2025-11-09T15:30:45.102Z servico-agendamento a1b2c3d4: Validando dados do agendamento
[INFO] 2025-11-09T15:30:45.105Z servico-agendamento a1b2c3d4: Cientista ID 7 encontrado e ativo
[INFO] 2025-11-09T15:30:45.107Z servico-agendamento a1b2c3d4: Tentando adquirir lock para recurso Hubble-Acad_2025-12-01T03:00:00Z
[INFO] 2025-11-09T15:30:45.250Z servico-agendamento a1b2c3d4: Lock adquirido com sucesso
[INFO] 2025-11-09T15:30:45.252Z servico-agendamento a1b2c3d4: Verificando conflitos no banco de dados
[INFO] 2025-11-09T15:30:45.275Z servico-agendamento a1b2c3d4: Nenhum conflito encontrado
[INFO] 2025-11-09T15:30:45.280Z servico-agendamento a1b2c3d4: Salvando agendamento no banco de dados
[INFO] 2025-11-09T15:30:45.295Z servico-agendamento a1b2c3d4: Agendamento criado com ID 123
[INFO] 2025-11-09T15:30:45.300Z servico-agendamento a1b2c3d4: Liberando lock para recurso Hubble-Acad_2025-12-01T03:00:00Z
[INFO] 2025-11-09T15:30:45.305Z servico-agendamento a1b2c3d4: Resposta 201 enviada
```

#### Terminal do Serviço Coordenador (Node.js)

```
[INFO] 2025-11-09T15:30:45.108Z POST /lock
[INFO] 2025-11-09T15:30:45.109Z Recebido pedido de lock para recurso: Hubble-Acad_2025-12-01T03:00:00Z
[INFO] 2025-11-09T15:30:45.110Z Lock concedido para recurso: Hubble-Acad_2025-12-01T03:00:00Z (holder: a1b2c3d4)
[INFO] 2025-11-09T15:30:45.301Z POST /unlock
[INFO] 2025-11-09T15:30:45.302Z Recebido pedido de unlock para recurso: Hubble-Acad_2025-12-01T03:00:00Z
[INFO] 2025-11-09T15:30:45.303Z Lock liberado para recurso: Hubble-Acad_2025-12-01T03:00:00Z
```

#### Arquivo de Auditoria (audit.log)

```json
{"timestamp_utc":"2025-11-09T15:30:45.297Z","level":"AUDIT","event_type":"AGENDAMENTO_CRIADO","service":"servico-agendamento","correlation_id":"a1b2c3d4-e5f6-7890-abcd-ef1234567890","details":{"agendamento_id":123,"cientista_id":7,"cientista_nome":"Marie Curie","horario_inicio_utc":"2025-12-01T03:00:00Z","horario_fim_utc":"2025-12-01T03:30:00Z","objeto_celeste":"NGC 1300","duracao_minutos":30}}
```

---

### Cenário: Tentativa de Agendamento com Conflito

#### Terminal do Serviço de Agendamento (Flask)

```
[INFO] 2025-11-09T15:30:46.100Z servico-agendamento b2c3d4e5: Requisição POST /agendamentos recebida
[INFO] 2025-11-09T15:30:46.102Z servico-agendamento b2c3d4e5: Validando dados do agendamento
[INFO] 2025-11-09T15:30:46.105Z servico-agendamento b2c3d4e5: Cientista ID 8 encontrado e ativo
[INFO] 2025-11-09T15:30:46.107Z servico-agendamento b2c3d4e5: Tentando adquirir lock para recurso Hubble-Acad_2025-12-01T03:00:00Z
[INFO] 2025-11-09T15:30:46.110Z servico-agendamento b2c3d4e5: Falha ao adquirir lock - recurso ocupado
[WARNING] 2025-11-09T15:30:46.112Z servico-agendamento b2c3d4e5: Conflito detectado - lock não disponível
[INFO] 2025-11-09T15:30:46.115Z servico-agendamento b2c3d4e5: Resposta 409 enviada
```

#### Terminal do Serviço Coordenador (Node.js)

```
[INFO] 2025-11-09T15:30:46.108Z POST /lock
[INFO] 2025-11-09T15:30:46.109Z Recebido pedido de lock para recurso: Hubble-Acad_2025-12-01T03:00:00Z
[INFO] 2025-11-09T15:30:46.109Z Recurso Hubble-Acad_2025-12-01T03:00:00Z já está em uso (holder: a1b2c3d4). Negando lock.
```

#### Arquivo de Auditoria (audit.log)

```json
{"timestamp_utc":"2025-11-09T15:30:46.113Z","level":"AUDIT","event_type":"AGENDAMENTO_CONFLITO","service":"servico-agendamento","correlation_id":"b2c3d4e5-f6g7-8901-bcde-f12345678901","details":{"cientista_id":8,"cientista_nome":"Albert Einstein","horario_inicio_utc":"2025-12-01T03:00:00Z","horario_fim_utc":"2025-12-01T03:30:00Z","motivo":"Lock não disponível","conflitos_com":[123]}}
```

---

## 5. Correlation ID

### Propósito

O `correlation_id` é um UUID gerado para cada requisição HTTP e propagado através de todos os logs relacionados, permitindo rastrear o fluxo completo de uma operação distribuída.

### Geração

```python
import uuid
from flask import g

def get_correlation_id():
    if 'correlation_id' not in g:
        g.correlation_id = str(uuid.uuid4())
    return g.correlation_id
```

### Propagação

O correlation_id é:
1. Gerado no início da requisição (middleware)
2. Adicionado a todos os logs da requisição
3. Incluído no header da resposta: `X-Correlation-ID`
4. Enviado para serviços downstream (coordenador)

### Exemplo de Rastreamento

Com correlation_id `a1b2c3d4`, podemos filtrar todos os logs:

```bash
# Logs de aplicação
cat logs/app.log | grep a1b2c3d4

# Logs de auditoria
cat logs/audit.log | jq 'select(.correlation_id == "a1b2c3d4")'
```

---

## 6. Configuração de Logging

### Python (Flask)

```python
import logging
import os

def setup_logging(app):
    # Criar diretório
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Formato
    log_format = '[%(levelname)s] %(asctime)s %(name)s %(correlation_id)s: %(message)s'
    
    # Handler para arquivo
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Configurar
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
```

### Node.js (Express)

```javascript
function log(level, message) {
    const timestamp = new Date().toISOString();
    console.log(`[${level}] ${timestamp} ${message}`);
}

// Uso
log('INFO', 'Recebido pedido de lock para recurso: ' + recurso);
```

---

## 7. Rotação e Retenção de Logs

### Política de Rotação

**Logs de Aplicação (app.log)**:
- Rotação diária
- Manter últimos 30 dias
- Compressão após 7 dias
- Arquivo máximo: 100MB

**Logs de Auditoria (audit.log)**:
- Rotação semanal
- Manter últimos 365 dias (compliance)
- Compressão após 30 dias
- Arquivo máximo: 500MB

### Implementação (logrotate)

```
/caminho/para/logs/app.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    maxsize 100M
}

/caminho/para/logs/audit.log {
    weekly
    rotate 52
    compress
    delaycompress
    missingok
    notifempty
    maxsize 500MB
}
```

---

## 8. Análise de Logs

### Comandos Úteis

**Buscar por correlation_id**:
```bash
grep "a1b2c3d4" logs/app.log
```

**Contar eventos de auditoria por tipo**:
```bash
cat logs/audit.log | jq -r '.event_type' | sort | uniq -c
```

**Agendamentos criados hoje**:
```bash
cat logs/audit.log | jq 'select(.event_type == "AGENDAMENTO_CRIADO" and .timestamp_utc | startswith("2025-11-09"))'
```

**Últimos 10 conflitos**:
```bash
cat logs/audit.log | jq 'select(.event_type == "AGENDAMENTO_CONFLITO")' | tail -10
```

### Ferramentas de Análise

- **jq**: Processamento de JSON (logs de auditoria)
- **grep/awk/sed**: Processamento de texto (logs de aplicação)
- **ELK Stack** (futuro): Elasticsearch + Logstash + Kibana
- **Grafana** (futuro): Visualização de métricas

---

## 9. Monitoramento e Alertas (Futuro)

### Métricas Importantes

1. **Taxa de conflitos**: `AGENDAMENTO_CONFLITO / AGENDAMENTO_CRIADO`
2. **Tempo de lock**: Tempo entre acquire e release
3. **Taxa de cancelamento**: `AGENDAMENTO_CANCELADO / AGENDAMENTO_CRIADO`
4. **Erros 5xx**: Frequência de erros internos

### Alertas Sugeridos

- Taxa de conflitos > 10%
- Tempo médio de lock > 500ms
- Erros 5xx > 5/min
- Disk usage de logs > 80%

---

## 10. Compliance e Segurança

### Dados Sensíveis

**NUNCA** logar:
- Senhas ou tokens de autenticação
- Dados pessoais sensíveis (CPF, RG, etc.)
- Informações financeiras

**Sempre** logar:
- Quem fez (cientista_id/nome)
- O quê (ação executada)
- Quando (timestamp UTC)
- Resultado (sucesso/falha)

### Imutabilidade

Logs de auditoria devem ser:
- Append-only (nunca modificar ou deletar)
- Com checksum/hash para detectar adulteração
- Armazenados em sistema separado (futuro)

---

*Última atualização: 2025-11-09*
