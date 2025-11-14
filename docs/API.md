# Especificação da API - SCTEC

## Visão Geral

API RESTful para o Sistema de Controle de Telescópio Espacial Compartilhado (SCTEC).

**Base URL**: `/api/v1`  
**Formato**: JSON  
**Encoding**: UTF-8  
**Timezone**: UTC

---

## Princípios REST

1. **Cliente-Servidor**: Separação clara entre cliente e servidor
2. **Stateless**: Cada requisição contém todas as informações necessárias
3. **HATEOAS**: Respostas incluem links para ações possíveis
4. **Métodos HTTP**: GET (ler), POST (criar), PUT (atualizar), DELETE (remover)
5. **Códigos de Status**: Uso semântico correto dos códigos HTTP

---

## Cabeçalhos Comuns

### Request Headers

```http
Content-Type: application/json
Accept: application/json
```

### Response Headers

```http
Content-Type: application/json; charset=utf-8
X-Correlation-ID: <uuid>
```

---

## 1. Endpoint: Tempo do Servidor

### GET /time

Retorna o timestamp oficial do servidor para sincronização de relógio.

**Autenticação**: Não requerida

**Query Parameters**: Nenhum

**Request**:
```http
GET /api/v1/time HTTP/1.1
```

**Response Success (200 OK)**:
```json
{
  "timestamp_utc": "2025-11-09T15:30:45.123456Z",
  "timezone": "UTC",
  "epoch_ms": 1731166245123,
  "_links": {
    "self": {
      "href": "/api/v1/time"
    },
    "agendamentos": {
      "href": "/api/v1/agendamentos"
    },
    "cientistas": {
      "href": "/api/v1/cientistas"
    }
  }
}
```

**Códigos de Status**:
- `200 OK`: Sucesso
- `500 Internal Server Error`: Erro interno do servidor

---

## 2. Endpoints: Cientistas

### GET /cientistas

Lista todos os cientistas cadastrados com paginação.

**Autenticação**: Não requerida (futuramente: Bearer token)

**Query Parameters**:
- `page` (integer, default=1): Número da página
- `per_page` (integer, default=20, max=100): Itens por página
- `ativo` (boolean, optional): Filtrar por status ativo/inativo

**Request**:
```http
GET /api/v1/cientistas?page=1&per_page=20&ativo=true HTTP/1.1
```

**Response Success (200 OK)**:
```json
{
  "cientistas": [
    {
      "id": 1,
      "nome": "Marie Curie",
      "email": "marie.curie@sorbonne.fr",
      "instituicao": "Universidade de Paris",
      "pais": "França",
      "especialidade": "Radioastronomia",
      "ativo": true,
      "data_cadastro": "2025-11-09T10:30:00Z",
      "_links": {
        "self": {
          "href": "/api/v1/cientistas/1"
        },
        "agendamentos": {
          "href": "/api/v1/cientistas/1/agendamentos"
        },
        "criar_agendamento": {
          "href": "/api/v1/agendamentos",
          "method": "POST"
        }
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 45,
    "total_pages": 3
  },
  "_links": {
    "self": {
      "href": "/api/v1/cientistas?page=1&per_page=20"
    },
    "next": {
      "href": "/api/v1/cientistas?page=2&per_page=20"
    },
    "last": {
      "href": "/api/v1/cientistas?page=3&per_page=20"
    }
  }
}
```

**Códigos de Status**:
- `200 OK`: Sucesso
- `400 Bad Request`: Parâmetros inválidos
- `500 Internal Server Error`: Erro interno

---

### POST /cientistas

Cria um novo cientista.

**Autenticação**: Não requerida (futuramente: Bearer token com permissões admin)

**Request**:
```http
POST /api/v1/cientistas HTTP/1.1
Content-Type: application/json

{
  "nome": "Alan Turing",
  "email": "alan.turing@manchester.ac.uk",
  "instituicao": "University of Manchester",
  "pais": "Reino Unido",
  "especialidade": "Computação Quântica Astrofísica"
}
```

**Response Success (201 Created)**:
```json
{
  "id": 42,
  "nome": "Alan Turing",
  "email": "alan.turing@manchester.ac.uk",
  "instituicao": "University of Manchester",
  "pais": "Reino Unido",
  "especialidade": "Computação Quântica Astrofísica",
  "ativo": true,
  "data_cadastro": "2025-11-09T15:45:00Z",
  "_links": {
    "self": {
      "href": "/api/v1/cientistas/42"
    },
    "agendamentos": {
      "href": "/api/v1/cientistas/42/agendamentos"
    },
    "atualizar": {
      "href": "/api/v1/cientistas/42",
      "method": "PUT"
    },
    "desativar": {
      "href": "/api/v1/cientistas/42",
      "method": "DELETE"
    }
  }
}
```

**Response Error (400 Bad Request)**:
```json
{
  "error": "Dados inválidos",
  "details": [
    "Nome deve ter no mínimo 3 caracteres",
    "Email inválido"
  ]
}
```

**Response Error (409 Conflict)**:
```json
{
  "error": "Email já cadastrado",
  "email": "alan.turing@manchester.ac.uk"
}
```

**Códigos de Status**:
- `201 Created`: Cientista criado com sucesso
- `400 Bad Request`: Dados inválidos
- `409 Conflict`: Email já existe
- `422 Unprocessable Entity`: Regra de negócio violada
- `500 Internal Server Error`: Erro interno

---

### GET /cientistas/{id}

Obtém detalhes de um cientista específico.

**Autenticação**: Não requerida

**Path Parameters**:
- `id` (integer, required): ID do cientista

**Request**:
```http
GET /api/v1/cientistas/1 HTTP/1.1
```

**Response Success (200 OK)**:
```json
{
  "id": 1,
  "nome": "Marie Curie",
  "email": "marie.curie@sorbonne.fr",
  "instituicao": "Universidade de Paris",
  "pais": "França",
  "especialidade": "Radioastronomia",
  "ativo": true,
  "data_cadastro": "2025-11-09T10:30:00Z",
  "_links": {
    "self": {
      "href": "/api/v1/cientistas/1"
    },
    "agendamentos": {
      "href": "/api/v1/cientistas/1/agendamentos"
    },
    "criar_agendamento": {
      "href": "/api/v1/agendamentos",
      "method": "POST"
    }
  }
}
```

**Response Error (404 Not Found)**:
```json
{
  "error": "Cientista não encontrado"
}
```

**Códigos de Status**:
- `200 OK`: Sucesso
- `404 Not Found`: Cientista não encontrado
- `500 Internal Server Error`: Erro interno

---

### GET /cientistas/{id}/agendamentos

Lista todos os agendamentos de um cientista.

**Autenticação**: Não requerida

**Path Parameters**:
- `id` (integer, required): ID do cientista

**Query Parameters**:
- `status` (string, optional): Filtrar por status (AGENDADO, CANCELADO, CONCLUIDO)

**Request**:
```http
GET /api/v1/cientistas/1/agendamentos?status=AGENDADO HTTP/1.1
```

**Response Success (200 OK)**:
```json
{
  "cientista_id": 1,
  "cientista_nome": "Marie Curie",
  "agendamentos": [
    {
      "id": 123,
      "cientista_id": 1,
      "cientista_nome": "Marie Curie",
      "horario_inicio_utc": "2025-12-01T03:00:00Z",
      "horario_fim_utc": "2025-12-01T03:30:00Z",
      "objeto_celeste": "NGC 1300",
      "observacoes": "Estudo de estrutura espiral",
      "status": "AGENDADO",
      "data_criacao": "2025-11-09T15:30:45Z",
      "_links": {
        "self": {
          "href": "/api/v1/agendamentos/123"
        },
        "cientista": {
          "href": "/api/v1/cientistas/1"
        },
        "cancelar": {
          "href": "/api/v1/agendamentos/123",
          "method": "DELETE"
        }
      }
    }
  ],
  "total": 3,
  "_links": {
    "self": {
      "href": "/api/v1/cientistas/1/agendamentos"
    },
    "cientista": {
      "href": "/api/v1/cientistas/1"
    }
  }
}
```

**Códigos de Status**:
- `200 OK`: Sucesso
- `404 Not Found`: Cientista não encontrado
- `500 Internal Server Error`: Erro interno

---

## 3. Endpoints: Agendamentos

### GET /agendamentos

Lista agendamentos com filtros e paginação.

**Autenticação**: Não requerida

**Query Parameters**:
- `page` (integer, default=1): Número da página
- `per_page` (integer, default=20, max=100): Itens por página
- `cientista_id` (integer, optional): Filtrar por cientista
- `status` (string, optional): Filtrar por status
- `data_inicio` (datetime ISO8601, optional): Filtrar agendamentos a partir desta data
- `data_fim` (datetime ISO8601, optional): Filtrar agendamentos até esta data

**Request**:
```http
GET /api/v1/agendamentos?cientista_id=1&status=AGENDADO&page=1 HTTP/1.1
```

**Response Success (200 OK)**:
```json
{
  "agendamentos": [
    {
      "id": 123,
      "cientista_id": 1,
      "cientista_nome": "Marie Curie",
      "horario_inicio_utc": "2025-12-01T03:00:00Z",
      "horario_fim_utc": "2025-12-01T03:30:00Z",
      "objeto_celeste": "NGC 1300",
      "observacoes": "Estudo de estrutura espiral",
      "status": "AGENDADO",
      "data_criacao": "2025-11-09T15:30:45Z",
      "_links": {
        "self": {
          "href": "/api/v1/agendamentos/123"
        },
        "cientista": {
          "href": "/api/v1/cientistas/1"
        },
        "cancelar": {
          "href": "/api/v1/agendamentos/123",
          "method": "DELETE"
        }
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 15,
    "total_pages": 1
  },
  "_links": {
    "self": {
      "href": "/api/v1/agendamentos?page=1"
    }
  }
}
```

**Códigos de Status**:
- `200 OK`: Sucesso
- `400 Bad Request`: Parâmetros inválidos
- `500 Internal Server Error`: Erro interno

---

### POST /agendamentos

Cria um novo agendamento (OPERAÇÃO CRÍTICA - usa lock).

**Autenticação**: Não requerida (futuramente: Bearer token)

**Request**:
```http
POST /api/v1/agendamentos HTTP/1.1
Content-Type: application/json

{
  "cientista_id": 1,
  "horario_inicio_utc": "2025-12-01T03:00:00Z",
  "horario_fim_utc": "2025-12-01T03:30:00Z",
  "objeto_celeste": "NGC 1300 - Galáxia Espiral Barrada",
  "observacoes": "Análise de formação estelar no núcleo galáctico"
}
```

**Validações Automáticas**:
1. `cientista_id` existe e está ativo
2. Horários são válidos (formato ISO8601 UTC)
3. `horario_fim_utc` > `horario_inicio_utc`
4. Duração entre 5 minutos e 2 horas
5. Horários são múltiplos de 5 minutos
6. Não é no passado
7. Antecedência mínima de 24 horas
8. Sem conflitos de horário
9. Cientista não atingiu limite de 3 agendamentos ativos

**Response Success (201 Created)**:
```json
{
  "id": 123,
  "cientista_id": 1,
  "cientista_nome": "Marie Curie",
  "horario_inicio_utc": "2025-12-01T03:00:00Z",
  "horario_fim_utc": "2025-12-01T03:30:00Z",
  "objeto_celeste": "NGC 1300 - Galáxia Espiral Barrada",
  "observacoes": "Análise de formação estelar no núcleo galáctico",
  "status": "AGENDADO",
  "data_criacao": "2025-11-09T15:30:45Z",
  "_links": {
    "self": {
      "href": "/api/v1/agendamentos/123"
    },
    "cientista": {
      "href": "/api/v1/cientistas/1"
    },
    "cancelar": {
      "href": "/api/v1/agendamentos/123",
      "method": "DELETE"
    }
  }
}
```

**Response Error (400 Bad Request)**:
```json
{
  "error": "Dados inválidos",
  "details": [
    "Duração mínima: 5 minutos",
    "Horários devem ser múltiplos de 5 minutos"
  ]
}
```

**Response Error (404 Not Found)**:
```json
{
  "error": "Cientista não encontrado"
}
```

**Response Error (409 Conflict - Horário)**:
```json
{
  "error": "Conflito de horário",
  "conflitos": [
    {
      "id": 122,
      "cientista_nome": "Albert Einstein",
      "horario_inicio_utc": "2025-12-01T02:45:00Z",
      "horario_fim_utc": "2025-12-01T03:15:00Z"
    }
  ]
}
```

**Response Error (409 Conflict - Lock)**:
```json
{
  "error": "Recurso temporariamente indisponível",
  "detalhes": "Recurso já está travado"
}
```

**Response Error (422 Unprocessable Entity)**:
```json
{
  "error": "Limite de 3 agendamentos ativos atingido"
}
```

**Códigos de Status**:
- `201 Created`: Agendamento criado com sucesso
- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Cientista não encontrado
- `409 Conflict`: Conflito de horário ou lock não disponível
- `422 Unprocessable Entity`: Regra de negócio violada
- `500 Internal Server Error`: Erro interno

---

### GET /agendamentos/{id}

Obtém detalhes de um agendamento específico.

**Autenticação**: Não requerida

**Path Parameters**:
- `id` (integer, required): ID do agendamento

**Request**:
```http
GET /api/v1/agendamentos/123 HTTP/1.1
```

**Response Success (200 OK)**:
```json
{
  "id": 123,
  "cientista_id": 1,
  "cientista_nome": "Marie Curie",
  "horario_inicio_utc": "2025-12-01T03:00:00Z",
  "horario_fim_utc": "2025-12-01T03:30:00Z",
  "objeto_celeste": "NGC 1300",
  "observacoes": "Estudo de estrutura espiral",
  "status": "AGENDADO",
  "data_criacao": "2025-11-09T15:30:45Z",
  "_links": {
    "self": {
      "href": "/api/v1/agendamentos/123"
    },
    "cientista": {
      "href": "/api/v1/cientistas/1"
    },
    "cancelar": {
      "href": "/api/v1/agendamentos/123",
      "method": "DELETE"
    }
  }
}
```

**Response para Agendamento Cancelado (200 OK)**:
```json
{
  "id": 120,
  "cientista_id": 1,
  "cientista_nome": "Marie Curie",
  "horario_inicio_utc": "2025-11-30T20:00:00Z",
  "horario_fim_utc": "2025-11-30T20:30:00Z",
  "objeto_celeste": "M87",
  "observacoes": "Estudo do jato relativístico",
  "status": "CANCELADO",
  "data_criacao": "2025-11-08T10:00:00Z",
  "data_cancelamento": "2025-11-09T14:30:00Z",
  "motivo_cancelamento": "Condições atmosféricas desfavoráveis previstas",
  "_links": {
    "self": {
      "href": "/api/v1/agendamentos/120"
    },
    "cientista": {
      "href": "/api/v1/cientistas/1"
    }
  }
}
```

**Nota**: O link "cancelar" só aparece se status = AGENDADO (HATEOAS condicional).

**Códigos de Status**:
- `200 OK`: Sucesso
- `404 Not Found`: Agendamento não encontrado
- `500 Internal Server Error`: Erro interno

---

### DELETE /agendamentos/{id}

Cancela um agendamento (soft delete).

**Autenticação**: Não requerida (futuramente: Bearer token)

**Path Parameters**:
- `id` (integer, required): ID do agendamento

**Request**:
```http
DELETE /api/v1/agendamentos/123 HTTP/1.1
Content-Type: application/json

{
  "motivo": "Conflito de agenda - necessidade de rescheduling"
}
```

**Request Body** (opcional):
- `motivo` (string, optional): Justificativa do cancelamento

**Response Success (200 OK)**:
```json
{
  "id": 123,
  "cientista_id": 1,
  "cientista_nome": "Marie Curie",
  "horario_inicio_utc": "2025-12-01T03:00:00Z",
  "horario_fim_utc": "2025-12-01T03:30:00Z",
  "objeto_celeste": "NGC 1300",
  "observacoes": "Estudo de estrutura espiral",
  "status": "CANCELADO",
  "data_criacao": "2025-11-09T15:30:45Z",
  "data_cancelamento": "2025-11-10T10:15:30Z",
  "motivo_cancelamento": "Conflito de agenda - necessidade de rescheduling",
  "_links": {
    "self": {
      "href": "/api/v1/agendamentos/123"
    },
    "cientista": {
      "href": "/api/v1/cientistas/1"
    }
  }
}
```

**Response Error (404 Not Found)**:
```json
{
  "error": "Agendamento não encontrado"
}
```

**Response Error (422 Unprocessable Entity)**:
```json
{
  "error": "Agendamento com status CANCELADO não pode ser cancelado"
}
```

**Códigos de Status**:
- `200 OK`: Agendamento cancelado com sucesso
- `404 Not Found`: Agendamento não encontrado
- `422 Unprocessable Entity`: Agendamento não pode ser cancelado (status != AGENDADO)
- `500 Internal Server Error`: Erro interno

---

## 4. HATEOAS - Hypermedia as the Engine of Application State

### Princípios

1. **Descoberta**: Cliente não precisa conhecer URLs antecipadamente
2. **Navegação**: Links guiam o cliente pelas ações possíveis
3. **Estado Condicional**: Links aparecem/desaparecem baseado no estado do recurso

### Estrutura de Links

```json
{
  "_links": {
    "nome_da_acao": {
      "href": "/caminho/completo",
      "method": "GET|POST|PUT|DELETE" // opcional, default=GET
    }
  }
}
```

### Exemplos de Links Condicionais

**Agendamento com status AGENDADO**:
```json
{
  "_links": {
    "self": { "href": "/api/v1/agendamentos/123" },
    "cientista": { "href": "/api/v1/cientistas/1" },
    "cancelar": { "href": "/api/v1/agendamentos/123", "method": "DELETE" }
  }
}
```

**Agendamento com status CANCELADO**:
```json
{
  "_links": {
    "self": { "href": "/api/v1/agendamentos/123" },
    "cientista": { "href": "/api/v1/cientistas/1" }
    // Nota: link "cancelar" não aparece
  }
}
```

---

## 5. Tratamento de Erros

### Estrutura Padrão de Erro

```json
{
  "error": "Mensagem de erro principal",
  "details": ["Detalhe 1", "Detalhe 2"], // opcional
  "codigo": "CODIGO_ERRO", // opcional
  "timestamp": "2025-11-09T15:30:45Z" // opcional
}
```

### Códigos de Status HTTP

| Código | Significado | Quando Usar |
|--------|-------------|-------------|
| 200 | OK | Sucesso (GET, PUT, DELETE) |
| 201 | Created | Recurso criado (POST) |
| 204 | No Content | Sucesso sem corpo de resposta |
| 400 | Bad Request | Dados de entrada inválidos |
| 404 | Not Found | Recurso não encontrado |
| 409 | Conflict | Conflito de estado (email duplicado, horário conflitante) |
| 422 | Unprocessable Entity | Regra de negócio violada |
| 500 | Internal Server Error | Erro inesperado do servidor |
| 503 | Service Unavailable | Serviço temporariamente indisponível |

---

## 6. Versionamento da API

**Estratégia**: URL Path Versioning

- Versão atual: `v1`
- URL: `/api/v1/...`
- Futura: `/api/v2/...`

**Política**:
- Versões antigas mantidas por 12 meses após lançamento de nova versão
- Breaking changes exigem nova versão
- Adições compatíveis podem ser feitas na versão atual

---

## 7. Rate Limiting (Futuro)

**Headers de Resposta**:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1731166245
```

**Limites Planejados**:
- Sem autenticação: 100 requisições/hora
- Com autenticação: 1000 requisições/hora
- Burst: 20 requisições/minuto

---

## 8. Exemplos de Fluxos Completos

### Fluxo 1: Criar Cientista e Agendar Observação

```bash
# 1. Criar cientista
POST /api/v1/cientistas
{
  "nome": "Carl Sagan",
  "email": "carl.sagan@cornell.edu",
  "instituicao": "Cornell University",
  "pais": "Estados Unidos"
}
# Resposta: 201, cientista_id = 50

# 2. Verificar horários disponíveis
GET /api/v1/agendamentos?data_inicio=2025-12-01T00:00:00Z&data_fim=2025-12-02T00:00:00Z

# 3. Sincronizar tempo
GET /api/v1/time

# 4. Criar agendamento
POST /api/v1/agendamentos
{
  "cientista_id": 50,
  "horario_inicio_utc": "2025-12-01T15:00:00Z",
  "horario_fim_utc": "2025-12-01T15:45:00Z",
  "objeto_celeste": "Pale Blue Dot - Júpiter",
  "observacoes": "Análise atmosférica"
}
# Resposta: 201, agendamento_id = 150

# 5. Consultar agendamentos do cientista
GET /api/v1/cientistas/50/agendamentos
```

### Fluxo 2: Conflito de Agendamento

```bash
# Cientista 1 tenta agendar
POST /api/v1/agendamentos
{
  "cientista_id": 1,
  "horario_inicio_utc": "2025-12-01T10:00:00Z",
  "horario_fim_utc": "2025-12-01T10:30:00Z",
  "objeto_celeste": "Andromeda"
}
# Resposta: 201 Created

# Cientista 2 tenta agendar horário conflitante
POST /api/v1/agendamentos
{
  "cientista_id": 2,
  "horario_inicio_utc": "2025-12-01T10:15:00Z",
  "horario_fim_utc": "2025-12-01T10:45:00Z",
  "objeto_celeste": "Orion Nebula"
}
# Resposta: 409 Conflict
```

---

*Última atualização: 2025-11-09*
