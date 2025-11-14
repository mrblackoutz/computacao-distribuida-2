# ============================================
# SCTEC - Demonstração Comparativa
# Mostra PROBLEMA (sem lock) vs SOLUÇÃO (com lock)
# ============================================

Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   SCTEC - DEMONSTRAÇÃO COMPARATIVA" -ForegroundColor Cyan
Write-Host "   Condição de Corrida: Problema vs Solução" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Criar .env se não existir
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

# ============================================
# PARTE 1: DEMONSTRAÇÃO DO PROBLEMA (SEM LOCK)
# ============================================

Write-Host "┌──────────────────────────────────────────────────────────────┐" -ForegroundColor Red
Write-Host "│  PARTE 1: DEMONSTRAÇÃO DO PROBLEMA (ENTREGA 2)              │" -ForegroundColor Red
Write-Host "│  Sistema SEM proteção de lock                               │" -ForegroundColor Red
Write-Host "└──────────────────────────────────────────────────────────────┘" -ForegroundColor Red
Write-Host ""

Write-Host "⚙️  Configurando sistema SEM LOCK..." -ForegroundColor Yellow
$content = Get-Content ".env" -Raw
$content = $content -replace "USE_LOCK=true", "USE_LOCK=false"
$content | Set-Content ".env" -NoNewline

Write-Host "🐳 Iniciando containers..." -ForegroundColor Yellow
docker-compose down -v | Out-Null
docker-compose up --build -d | Out-Null
Start-Sleep -Seconds 12

Write-Host "🧪 Executando teste de concorrência (10 threads)..." -ForegroundColor Yellow
Write-Host ""
python tests\test_concorrencia.py 10

Write-Host ""
Write-Host "Pressione qualquer tecla para continuar com a SOLUÇÃO..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# ============================================
# PARTE 2: DEMONSTRAÇÃO DA SOLUÇÃO (COM LOCK)
# ============================================

Write-Host ""
Write-Host ""
Write-Host "┌──────────────────────────────────────────────────────────────┐" -ForegroundColor Green
Write-Host "│  PARTE 2: DEMONSTRAÇÃO DA SOLUÇÃO (ENTREGA 3)               │" -ForegroundColor Green
Write-Host "│  Sistema COM proteção de lock (Coordenador)                 │" -ForegroundColor Green
Write-Host "└──────────────────────────────────────────────────────────────┘" -ForegroundColor Green
Write-Host ""

Write-Host "⚙️  Configurando sistema COM LOCK..." -ForegroundColor Cyan
$content = Get-Content ".env" -Raw
$content = $content -replace "USE_LOCK=false", "USE_LOCK=true"
$content | Set-Content ".env" -NoNewline

Write-Host "🐳 Reiniciando containers..." -ForegroundColor Cyan
docker-compose down -v | Out-Null
docker-compose up --build -d | Out-Null
Start-Sleep -Seconds 12

Write-Host "🧪 Executando teste com lock (10 threads)..." -ForegroundColor Cyan
Write-Host ""
python tests\test_com_lock.py 10

# ============================================
# RESUMO FINAL
# ============================================

Write-Host ""
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   RESUMO DA DEMONSTRAÇÃO" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 PROBLEMA (Entrega 2 - SEM LOCK):" -ForegroundColor Red
Write-Host "   ❌ Múltiplos agendamentos criados simultaneamente" -ForegroundColor White
Write-Host "   ❌ Conflitos no banco de dados" -ForegroundColor White
Write-Host "   ❌ Race condition entre verificação e INSERT" -ForegroundColor White
Write-Host ""

Write-Host "✅ SOLUÇÃO (Entrega 3 - COM LOCK):" -ForegroundColor Green
Write-Host "   ✓ Apenas 1 agendamento criado" -ForegroundColor White
Write-Host "   ✓ Exclusão mútua garantida pelo coordenador" -ForegroundColor White
Write-Host "   ✓ Sistema consistente e confiável" -ForegroundColor White
Write-Host ""

Write-Host "🔍 ARQUITETURA DA SOLUÇÃO:" -ForegroundColor Cyan
Write-Host "   • Serviço Coordenador (Node.js)" -ForegroundColor White
Write-Host "   • Endpoints: POST /lock e POST /unlock" -ForegroundColor White
Write-Host "   • Flask chama coordenador antes de acessar BD" -ForegroundColor White
Write-Host "   • Lock liberado em bloco try...finally" -ForegroundColor White
Write-Host ""

Write-Host "📚 CONCEITOS DEMONSTRADOS:" -ForegroundColor Yellow
Write-Host "   1. Condição de Corrida (Race Condition)" -ForegroundColor White
Write-Host "   2. Exclusão Mútua (Mutual Exclusion)" -ForegroundColor White
Write-Host "   3. Coordenador Centralizado" -ForegroundColor White
Write-Host "   4. Microserviços (Flask + Node.js)" -ForegroundColor White
Write-Host "   5. Logging e Observabilidade" -ForegroundColor White
Write-Host ""

Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
