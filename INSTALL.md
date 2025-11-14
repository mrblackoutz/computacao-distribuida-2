# Guia de Instalação e Execução - Entrega 2

## Pré-requisitos

- Python 3.9+ instalado
- pip instalado
- Terminal/PowerShell

## Passo 1: Criar Ambiente Virtual

```powershell
# Navegar para o diretório do serviço
cd servico-agendamento

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ou (Windows CMD)
venv\Scripts\activate.bat

# Ou (Linux/Mac)
source venv/bin/activate
```

## Passo 2: Instalar Dependências

```powershell
# Com o ambiente virtual ativado
pip install -r requirements.txt
```

## Passo 3: Executar o Servidor

```powershell
# Ainda no diretório servico-agendamento
python run.py
```

O servidor irá iniciar em: http://localhost:5000

## Passo 4: Testar a API

### Opção 1: Endpoint /time

Abra o navegador em: http://localhost:5000/api/v1/time

Ou use curl:
```powershell
curl http://localhost:5000/api/v1/time
```

### Opção 2: Criar um Cientista

```powershell
curl -X POST http://localhost:5000/api/v1/cientistas `
  -H "Content-Type: application/json" `
  -d '{
    \"nome\": \"Marie Curie\",
    \"email\": \"marie.curie@sorbonne.fr\",
    \"instituicao\": \"Universidade de Paris\",
    \"pais\": \"França\",
    \"especialidade\": \"Radioastronomia\"
  }'
```

### Opção 3: Listar Cientistas

```powershell
curl http://localhost:5000/api/v1/cientistas
```

## Passo 5: Testar Condição de Corrida

**Em um NOVO terminal** (mantendo o servidor rodando):

```powershell
# Navegar para a raiz do projeto
cd ..

# Executar teste (10 threads simultâneas)
python tests\test_concorrencia.py

# Ou com mais threads
python tests\test_concorrencia.py 20
```

## Resultado Esperado (Entrega 2)

❌ **PROBLEMA**: Múltiplos agendamentos serão criados para o mesmo horário!

Exemplo de saída:
```
🚨 CONDIÇÃO DE CORRIDA DETECTADA! 3 agendamentos criados para o mesmo horário!

IDs dos agendamentos duplicados:
   - Thread 01: Agendamento ID 123
   - Thread 03: Agendamento ID 124
   - Thread 07: Agendamento ID 125
```

## Analisando os Logs

### Logs de Aplicação

```powershell
# Ver todas as verificações de conflito
Select-String -Path servico-agendamento\logs\app.log -Pattern "verificação de conflito"

# Ver todas as tentativas de salvar
Select-String -Path servico-agendamento\logs\app.log -Pattern "Salvando novo agendamento"
```

### Logs de Auditoria

```powershell
# Ver todos os agendamentos criados
Select-String -Path servico-agendamento\logs\audit.log -Pattern "AGENDAMENTO_CRIADO"

# Contar quantos foram criados
(Select-String -Path servico-agendamento\logs\audit.log -Pattern "AGENDAMENTO_CRIADO").Count
```

## Troubleshooting

### Erro: "Import flask could not be resolved"

Certifique-se de que o ambiente virtual está ativado:
```powershell
.\venv\Scripts\Activate.ps1
```

### Erro: "Port 5000 is already in use"

Mate o processo que está usando a porta 5000:
```powershell
# Encontrar o processo
netstat -ano | findstr :5000

# Matar o processo (substitua <PID> pelo número encontrado)
taskkill /PID <PID> /F
```

### Erro: "No module named 'app'"

Certifique-se de estar no diretório correto:
```powershell
cd servico-agendamento
python run.py
```

## Estrutura de Arquivos Gerados

Após executar pela primeira vez:

```
servico-agendamento/
├── logs/
│   ├── app.log          # Logs de aplicação
│   └── audit.log        # Logs de auditoria (JSON)
├── instance/
│   └── telescopio.db    # Banco de dados SQLite
└── ...
```

## Próximos Passos

Na **Entrega 3**, implementaremos o Serviço Coordenador (Node.js) para resolver a condição de corrida usando locks distribuídos.
