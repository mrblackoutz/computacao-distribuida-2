# 📊 Paridade de Scripts - Windows ↔ Linux/Mac

## ✅ Tabela Completa de Paridade

| Script | Windows (.bat) | Windows (.ps1) | Linux/Mac (.sh) | Status |
|--------|----------------|----------------|-----------------|--------|
| **Iniciar Sistema** | ✅ start.bat | ➖ | ✅ start.sh | ✅ Completo |
| **Parar Sistema** | ✅ stop.bat | ➖ | ✅ stop.sh | ✅ Completo |
| **Limpar Tudo** | ✅ clean.bat | ➖ | ✅ clean.sh | ✅ Completo |
| **Setup Permissões** | ✅ setup_permissions.bat | ✅ setup_permissions.ps1 | ✅ setup_permissions.sh | ✅ Completo |
| **Demo Sem Lock** | ➖ | ✅ demo_sem_lock.ps1 | ✅ demo_sem_lock.sh | ✅ Completo |
| **Demo Com Lock** | ➖ | ✅ demo_com_lock.ps1 | ✅ demo_com_lock.sh | ✅ Completo |
| **Demo Comparação** | ➖ | ✅ demo_comparacao.ps1 | ✅ demo_comparacao.sh | ✅ Completo |

**Legenda:**
- ✅ = Arquivo existe
- ➖ = Não necessário (formato alternativo disponível)

## 📝 Observações

### Scripts de Sistema (start, stop, clean)

**Windows:**
- Versão `.bat` (preferida - mais simples)
- Não há `.ps1` correspondente (não necessário)

**Linux/Mac:**
- Versão `.sh` (única opção)

### Scripts de Demonstração (demo_*)

**Windows:**
- Versão `.ps1` (preferida - mais recursos)
- Não há `.bat` correspondente (PowerShell é mais poderoso)

**Linux/Mac:**
- Versão `.sh` (única opção)

### Scripts de Setup

**Windows:**
- Versão `.bat` (simples, direta)
- Versão `.ps1` (mais informativa, verifica ExecutionPolicy)

**Linux/Mac:**
- Versão `.sh` (configura chmod +x)

## 🎯 Resumo de Arquivos

### Total de Scripts

- **Windows BAT**: 4 arquivos
  - start.bat
  - stop.bat
  - clean.bat
  - setup_permissions.bat

- **Windows PowerShell**: 4 arquivos
  - demo_sem_lock.ps1
  - demo_com_lock.ps1
  - demo_comparacao.ps1
  - setup_permissions.ps1

- **Linux/Mac Bash**: 7 arquivos
  - start.sh
  - stop.sh
  - clean.sh
  - demo_sem_lock.sh
  - demo_com_lock.sh
  - demo_comparacao.sh
  - setup_permissions.sh

**Total Geral**: 15 scripts

## 📖 Guia de Uso por Plataforma

### Windows

**Opção 1: Scripts BAT (Simples)**
```cmd
REM Gerenciamento do sistema
start.bat
stop.bat
clean.bat
setup_permissions.bat
```

**Opção 2: Scripts PowerShell (Demonstrações)**
```powershell
# Demonstrações didáticas
.\demo_sem_lock.ps1
.\demo_com_lock.ps1
.\demo_comparacao.ps1
.\setup_permissions.ps1
```

**Se houver erro de ExecutionPolicy:**
```powershell
powershell -ExecutionPolicy Bypass -File .\demo_sem_lock.ps1
```

### Linux/Mac

**Primeira vez (configurar permissões):**
```bash
chmod +x *.sh
# ou
./setup_permissions.sh
```

**Uso normal:**
```bash
# Gerenciamento do sistema
./start.sh
./stop.sh
./clean.sh

# Demonstrações didáticas
./demo_sem_lock.sh
./demo_com_lock.sh
./demo_comparacao.sh
```

## 🔍 Diferenças de Implementação

### Cores e Formatação

**Windows BAT:**
- Sem cores (texto simples)
- Foco em funcionalidade

**Windows PowerShell:**
- Cores via `Write-Host -ForegroundColor`
- Interface rica e informativa

**Linux/Mac Bash:**
- Cores via códigos ANSI `\033[1;XXm`
- Interface equivalente ao PowerShell

### Comandos de Sistema

| Tarefa | Windows BAT/PS1 | Linux/Mac Bash |
|--------|-----------------|----------------|
| Pausa | `pause` / `Read-Host` | `read` |
| Esperar | `timeout /t 10` / `Start-Sleep 10` | `sleep 10` |
| Limpar tela | `cls` / `Clear-Host` | `clear` |
| Copiar | `copy` / `Copy-Item` | `cp` |
| Editar arquivo | PowerShell string replace | `sed -i` |

### Edição de .env

**Windows PowerShell:**
```powershell
$content = Get-Content ".env" -Raw
$content = $content -replace "USE_LOCK=true", "USE_LOCK=false"
$content | Set-Content ".env" -NoNewline
```

**Linux/Mac Bash:**
```bash
# Linux
sed -i 's/USE_LOCK=true/USE_LOCK=false/g' .env

# macOS
sed -i '' 's/USE_LOCK=true/USE_LOCK=false/g' .env
```

## ✅ Status de Conformidade

- ✅ **Paridade funcional**: 100%
  - Todas as funcionalidades disponíveis em ambas plataformas
  
- ✅ **Scripts básicos**: Completos
  - start, stop, clean presentes em todas plataformas
  
- ✅ **Scripts de demonstração**: Completos
  - demo_sem_lock, demo_com_lock, demo_comparacao
  
- ✅ **Scripts de setup**: Completos
  - setup_permissions para Windows e Linux/Mac
  
- ✅ **Documentação**: Completa
  - DEMO_SCRIPTS.md, SCRIPTS_CHECKLIST.md, PARIDADE_SCRIPTS.md

## 🎯 Recomendações de Uso

### Para Desenvolvimento Local

**Windows:**
```cmd
start.bat          # Inicia o sistema rapidamente
stop.bat           # Para o sistema
.\demo_comparacao.ps1  # Demonstração completa
```

**Linux/Mac:**
```bash
./start.sh         # Inicia o sistema
./stop.sh          # Para o sistema
./demo_comparacao.sh   # Demonstração completa
```

### Para Apresentações

**Todas as plataformas:**
```
Usar demo_comparacao (mostra problema + solução automaticamente)
```

### Para CI/CD

**Todas as plataformas:**
```bash
# Detectar SO e usar script apropriado
if [ "$OS" = "Windows_NT" ]; then
    start.bat
else
    ./start.sh
fi
```

---

**Criado em**: 14 de novembro de 2025  
**Projeto**: SCTEC - Sistema de Controle de Telescópio Espacial Compartilhado  
**Status**: ✅ 100% Completo e Funcional
