# 🎬 Quick Start - Demonstração Toggle

## 🚀 Uso Rápido

### Demonstração Completa (Recomendada)

```powershell
.\demo_comparacao.ps1
```

Isso vai:
1. Mostrar o PROBLEMA (SEM lock)
2. Pausar para análise
3. Mostrar a SOLUÇÃO (COM lock)
4. Exibir resumo comparativo

---

### Demonstração Individual

#### Apenas PROBLEMA:
```powershell
.\demo_sem_lock.ps1
python tests\test_concorrencia.py 10
```

#### Apenas SOLUÇÃO:
```powershell
.\demo_com_lock.ps1
python tests\test_com_lock.py 10
```

---

## 🔍 Verificar Modo Ativo

```powershell
docker-compose logs agendamento | Select-String "VERSÃO"
```

**Esperado:**
- `✅ Sistema usando VERSÃO COM LOCK` → Produção
- `⚠️ Sistema usando VERSÃO SEM LOCK` → Demonstração

---

## ⚙️ Toggle Manual

1. Editar `.env`:
   ```bash
   USE_LOCK=false  # SEM lock
   USE_LOCK=true   # COM lock
   ```

2. Reiniciar:
   ```powershell
   docker-compose down
   docker-compose up --build -d
   ```

---

## 📋 Resultado Esperado

### SEM LOCK (Problema)
- ❌ **2-10 agendamentos** criados
- ❌ Conflitos no banco
- ❌ Race condition

### COM LOCK (Solução)
- ✅ **1 agendamento** criado
- ✅ 9 conflitos HTTP 409
- ✅ Exclusão mútua funcionando

---

## 📚 Mais Informações

- **Guia Completo:** `GUIA_DEMONSTRACAO.md`
- **Documentação Técnica:** `docs/SISTEMA_TOGGLE.md`
