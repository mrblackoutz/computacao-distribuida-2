# 🎬 Scripts de Demonstração - SCTEC

Scripts para demonstrar o **problema** (condição de corrida) e a **solução** (exclusão mútua com lock).

## 📋 Scripts Disponíveis

### Windows (PowerShell)
- `demo_sem_lock.ps1` - Demonstra o PROBLEMA (Entrega 2)
- `demo_com_lock.ps1` - Demonstra a SOLUÇÃO (Entrega 3)
- `demo_comparacao.ps1` - Demonstração comparativa completa

### Linux/Mac (Bash)
- `demo_sem_lock.sh` - Demonstra o PROBLEMA (Entrega 2)
- `demo_com_lock.sh` - Demonstra a SOLUÇÃO (Entrega 3)
- `demo_comparacao.sh` - Demonstração comparativa completa

## 🚀 Como Usar

### Windows

```powershell
# Demonstrar o PROBLEMA (múltiplos agendamentos criados)
.\demo_sem_lock.ps1

# Demonstrar a SOLUÇÃO (apenas 1 agendamento criado)
.\demo_com_lock.ps1

# Demonstração COMPLETA (problema + solução)
.\demo_comparacao.ps1
```

### Linux/Mac

**Primeira vez (configurar permissões):**
```bash
chmod +x *.sh
# ou
./setup_permissions.sh
```

**Depois:**
```bash
# Demonstrar o PROBLEMA (múltiplos agendamentos criados)
./demo_sem_lock.sh

# Demonstrar a SOLUÇÃO (apenas 1 agendamento criado)
./demo_com_lock.sh

# Demonstração COMPLETA (problema + solução)
./demo_comparacao.sh
```

## 📊 O Que Cada Script Faz

### `demo_sem_lock` (Entrega 2 - PROBLEMA)

1. Configura `USE_LOCK=false` no `.env`
2. Reinicia containers
3. Instrui a executar `test_concorrencia.py`
4. **Resultado esperado**: MÚLTIPLOS agendamentos criados (condição de corrida)

**Saída esperada:**
```
✓ Sucessos (201):  3-5 (ou mais)
✗ Conflitos (409): 5-7
🚨 CONDIÇÃO DE CORRIDA DETECTADA!
```

### `demo_com_lock` (Entrega 3 - SOLUÇÃO)

1. Configura `USE_LOCK=true` no `.env`
2. Reinicia containers
3. Instrui a executar `test_com_lock.py`
4. **Resultado esperado**: APENAS 1 agendamento criado (exclusão mútua)

**Saída esperada:**
```
✓ Sucessos (201):  1
✗ Conflitos (409): 9
🎉 SUCESSO! Exclusão mútua funcionando!
```

### `demo_comparacao` (Demonstração Completa)

1. Executa **PARTE 1**: Sistema SEM lock (problema)
   - Aguarda pressionar tecla para continuar
2. Executa **PARTE 2**: Sistema COM lock (solução)
3. Mostra **RESUMO** comparativo

**Ideal para apresentações!**

## 🔍 Como Funciona o Toggle

Os scripts modificam a variável `USE_LOCK` no arquivo `.env`:

```bash
# SEM LOCK (Problema - Entrega 2)
USE_LOCK=false
# Sistema NÃO chama coordenador
# Múltiplos agendamentos são criados

# COM LOCK (Solução - Entrega 3)
USE_LOCK=true
# Sistema CHAMA coordenador para lock/unlock
# Apenas 1 agendamento é criado
```

O arquivo `app/routes/__init__.py` lê essa variável e importa a rota correta:

```python
import os

use_lock = os.getenv('USE_LOCK', 'true').lower() == 'true'

if use_lock:
    from app.routes import agendamento_routes  # COM LOCK
else:
    from app.routes import agendamento_routes_sem_lock  # SEM LOCK
```

## 📝 Logs a Observar

### Durante modo SEM LOCK:
```bash
# Ver logs do Flask
docker-compose logs -f agendamento

# Buscar por múltiplos "AGENDAMENTO_CRIADO"
docker exec sctec-agendamento cat logs/audit.log | grep AGENDAMENTO_CRIADO
```

### Durante modo COM LOCK:
```bash
# Ver coordenação entre serviços
docker-compose logs -f

# Buscar por "Lock concedido" e "Lock negado"
docker-compose logs coordenador | grep -i lock
```

## ⚙️ Variáveis de Ambiente

O sistema suporta as seguintes variáveis no `.env`:

```bash
# Modo de operação
USE_LOCK=true              # true = COM lock, false = SEM lock

# URLs dos serviços
COORDENADOR_URL=http://coordenador:3000

# Configurações Flask
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta

# Banco de dados
DATABASE_URI=sqlite:///instance/telescopio.db
```

## 🎯 Para Apresentações

**Roteiro recomendado:**

1. **Inicie com `demo_comparacao`**
   - Mostra problema e solução sequencialmente
   - Mais didático e visual

2. **Ou demonstre separadamente:**
   ```bash
   # Primeiro mostrar o problema
   ./demo_sem_lock.sh
   python tests/test_concorrencia.py 10
   
   # Depois mostrar a solução
   ./demo_com_lock.sh
   python tests/test_com_lock.py 10
   ```

3. **Mostre os logs durante execução:**
   ```bash
   # Terminal separado com logs ao vivo
   docker-compose logs -f
   ```

## 🔧 Troubleshooting

### "Permission denied" (Linux/Mac)
```bash
chmod +x demo_*.sh
# ou
./setup_permissions.sh
```

### "Cannot find .env.example"
```bash
# Criar .env manualmente
echo "USE_LOCK=true" > .env
echo "COORDENADOR_URL=http://coordenador:3000" >> .env
```

### Containers não iniciam
```bash
# Limpar tudo e reconstruir
docker-compose down -v
docker-compose up --build -d
```

### Teste não mostra múltiplos agendamentos no modo SEM LOCK
- Verifique se `.env` tem `USE_LOCK=false`
- Verifique se containers foram reconstruídos
- Aumente o número de threads: `python tests/test_concorrencia.py 20`

## 📚 Conceitos Demonstrados

1. **Condição de Corrida (Race Condition)**
   - Múltiplas threads acessam recurso compartilhado
   - Verificação e modificação não são atômicas
   - Resultado: inconsistência nos dados

2. **Exclusão Mútua (Mutual Exclusion)**
   - Apenas uma thread acessa recurso crítico por vez
   - Implementado via coordenador centralizado
   - Resultado: consistência garantida

3. **Arquitetura de Microserviços**
   - Serviço de Agendamento (Flask/Python)
   - Serviço Coordenador (Express/Node.js)
   - Comunicação via HTTP/REST

4. **Observabilidade**
   - Logs de aplicação (app.log)
   - Logs de auditoria (audit.log)
   - Correlation IDs para rastreamento

---

**Desenvolvido para o projeto SCTEC - Sistema de Controle de Telescópio Espacial Compartilhado**
