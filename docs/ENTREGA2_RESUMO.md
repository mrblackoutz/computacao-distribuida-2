# Entrega 2 - Sistema Inicial (Demonstração do Problema)

## ✅ Objetivos Cumpridos

1. ✅ Implementar API RESTful completa em Flask
2. ✅ Criar modelos SQLAlchemy (Cientista, Agendamento)
3. ✅ Implementar sistema de logging (aplicação + auditoria)
4. ✅ Implementar todas as 8 rotas da API com HATEOAS
5. ✅ **Demonstrar condição de corrida** (problema a ser resolvido)

## 📁 Arquivos Implementados

### Configuração e Infraestrutura

- ✅ `servico-agendamento/requirements.txt` - Dependências Python
- ✅ `servico-agendamento/.env` - Variáveis de ambiente
- ✅ `servico-agendamento/config.py` - Configurações Flask
- ✅ `servico-agendamento/run.py` - Ponto de entrada da aplicação

### Aplicação Flask

- ✅ `app/__init__.py` - Factory pattern, setup de logging
- ✅ `app/utils/logger.py` - Sistema de logging com correlation_id
- ✅ `app/utils/middleware.py` - Middleware para requisições

### Modelos

- ✅ `app/models/cientista.py` - Modelo Cientista com validações
- ✅ `app/models/agendamento.py` - Modelo Agendamento com validações e detecção de conflitos

### Rotas da API

- ✅ `app/routes/__init__.py` - Blueprints Flask
- ✅ `app/routes/time_routes.py` - GET /api/v1/time
- ✅ `app/routes/cientista_routes.py` - CRUD de cientistas (4 endpoints)
- ✅ `app/routes/agendamento_routes.py` - CRUD de agendamentos (4 endpoints) **SEM LOCK**

### Testes

- ✅ `tests/test_concorrencia.py` - Script para demonstrar condição de corrida

### Documentação

- ✅ `INSTALL.md` - Guia completo de instalação e execução

## 🎯 Funcionalidades Implementadas

### API Endpoints

| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| GET | `/api/v1/time` | Timestamp do servidor | ✅ |
| GET | `/api/v1/cientistas` | Listar cientistas (paginado) | ✅ |
| POST | `/api/v1/cientistas` | Criar cientista | ✅ |
| GET | `/api/v1/cientistas/{id}` | Detalhes do cientista | ✅ |
| GET | `/api/v1/cientistas/{id}/agendamentos` | Agendamentos do cientista | ✅ |
| GET | `/api/v1/agendamentos` | Listar agendamentos (filtros) | ✅ |
| POST | `/api/v1/agendamentos` | Criar agendamento ⚠️ SEM LOCK | ✅ |
| GET | `/api/v1/agendamentos/{id}` | Detalhes do agendamento | ✅ |
| DELETE | `/api/v1/agendamentos/{id}` | Cancelar agendamento | ✅ |

### Validações Implementadas

**Cientista:**
- Nome obrigatório (mínimo 3 caracteres)
- Email obrigatório e único
- Instituição obrigatória
- País obrigatório

**Agendamento:**
- Duração entre 5-120 minutos
- Horários em múltiplos de 5 minutos
- Antecedência mínima de 24 horas
- Não permitir agendamento no passado
- Máximo 3 agendamentos ativos por cientista
- Verificação de conflitos de horário ⚠️ (sem lock - problema!)

### Sistema de Logging

**Logs de Aplicação (`logs/app.log`):**
```
[INFO] 2025-11-09T15:30:45.123Z servico-agendamento a1b2c3d4: Requisição POST /agendamentos recebida
[INFO] 2025-11-09T15:30:45.252Z servico-agendamento a1b2c3d4: Verificando conflitos no banco de dados
[INFO] 2025-11-09T15:30:45.280Z servico-agendamento a1b2c3d4: Salvando agendamento no BD
```

**Logs de Auditoria (`logs/audit.log`):**
```json
{"timestamp_utc":"2025-11-09T15:30:45.297Z","level":"AUDIT","event_type":"AGENDAMENTO_CRIADO","service":"servico-agendamento","correlation_id":"a1b2c3d4","details":{"agendamento_id":123,...}}
```

### HATEOAS

Todas as respostas incluem links para ações relacionadas:

```json
{
  "id": 123,
  "objeto_celeste": "NGC 1300",
  "_links": {
    "self": {"href": "http://localhost:5000/api/v1/agendamentos/123"},
    "cientista": {"href": "http://localhost:5000/api/v1/cientistas/7"},
    "cancelar": {
      "href": "http://localhost:5000/api/v1/agendamentos/123",
      "method": "DELETE"
    }
  }
}
```

## 🚨 Problema Demonstrado: Condição de Corrida

### O que acontece:

1. **10 threads** disparam requisições **simultaneamente**
2. Todas passam pela verificação de conflitos (banco ainda vazio)
3. **Múltiplas threads** salvam agendamentos para o mesmo horário
4. Banco fica com dados **inconsistentes**

### Resultado do Teste:

```
🚨 CONDIÇÃO DE CORRIDA DETECTADA! 3 agendamentos criados para o mesmo horário!

IDs dos agendamentos duplicados:
   - Thread 01: Agendamento ID 123
   - Thread 03: Agendamento ID 124  
   - Thread 07: Agendamento ID 125
```

### Por que acontece:

```
Thread A                    Thread B
   |                           |
   ├─ SELECT (conflitos)       |
   │  └─ Nenhum conflito       |
   |                           ├─ SELECT (conflitos)
   |                           │  └─ Nenhum conflito
   ├─ INSERT agendamento       |
   |                           ├─ INSERT agendamento
   ✓ Sucesso                   ✓ Sucesso (PROBLEMA!)
```

Ambas as threads verificam o banco **antes** da outra ter salvo, então ambas passam na verificação.

## 📊 Como Executar e Validar

### 1. Instalar e Rodar

```powershell
cd servico-agendamento
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

### 2. Executar Teste de Concorrência

```powershell
# Em outro terminal
python tests\test_concorrencia.py 10
```

### 3. Analisar Logs

```powershell
# Ver verificações de conflito
Select-String -Path servico-agendamento\logs\app.log -Pattern "verificação de conflito"

# Contar agendamentos criados
(Select-String -Path servico-agendamento\logs\audit.log -Pattern "AGENDAMENTO_CRIADO").Count
```

### 4. Verificar Banco de Dados

```powershell
# Instalar sqlite3 (se não tiver)
# Abrir banco
sqlite3 servico-agendamento\instance\telescopio.db

# Executar query
SELECT id, horario_inicio_utc, horario_fim_utc FROM agendamentos WHERE status = 'AGENDADO';
```

## 📈 Métricas da Implementação

- **Linhas de código Python**: ~1.500
- **Arquivos criados**: 18
- **Endpoints REST**: 9
- **Modelos de dados**: 2
- **Validações**: 15+
- **Tipos de log**: 2 (aplicação + auditoria)

## 🎓 Conceitos de Sistemas Distribuídos Demonstrados

1. ✅ **Race Condition** - Múltiplos processos acessando recurso compartilhado
2. ✅ **Logging Distribuído** - Correlation ID para rastrear requisições
3. ✅ **RESTful API** - Padrão REST com HATEOAS
4. ✅ **Stateless** - Servidor não mantém estado entre requisições
5. ⏳ **Exclusão Mútua** - A ser implementado na Entrega 3

## 🔜 Próxima Etapa: Entrega 3

Na Entrega 3, implementaremos o **Serviço Coordenador (Node.js)** para resolver a condição de corrida usando **locks distribuídos**.

**O que será implementado:**
- Serviço Node.js/Express com endpoints `/lock` e `/unlock`
- Gerenciamento de locks em memória (Map)
- Modificação do Flask para adquirir lock antes de criar agendamento
- Teste mostrando que apenas 1 agendamento é criado

**Resultado esperado:**
```
✓ Apenas 1 agendamento criado (exclusão mútua funcionando!)

Agendamento vencedor:
   Thread: 3
   ID: 123
   Tempo: 0.250s
```

---

**Entrega 2 concluída com sucesso!** 🎉

*Data: 2025-11-09*
