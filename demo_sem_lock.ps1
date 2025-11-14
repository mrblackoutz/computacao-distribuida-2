# ============================================
# SCTEC - Demonstração da Entrega 2
# Sistema SEM LOCK (demonstra o problema)
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "   ATIVANDO MODO SEM LOCK" -ForegroundColor Yellow
Write-Host "   (Demonstração do Problema - Entrega 2)" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# Verificar se .env existe, caso contrário criar
if (-not (Test-Path ".env")) {
    Write-Host "📝 Criando arquivo .env..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
}

# Atualizar USE_LOCK=false no .env
Write-Host "⚙️  Configurando USE_LOCK=false..." -ForegroundColor Cyan
$content = Get-Content ".env" -Raw
$content = $content -replace "USE_LOCK=true", "USE_LOCK=false"
$content | Set-Content ".env" -NoNewline

Write-Host "✓ Configuração atualizada" -ForegroundColor Green
Write-Host ""

Write-Host "🐳 Reiniciando containers..." -ForegroundColor Cyan
docker-compose down
docker-compose up --build -d

Write-Host ""
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   MODO SEM LOCK ATIVADO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  ATENÇÃO: Sistema agora está VULNERÁVEL a condição de corrida!" -ForegroundColor Red
Write-Host ""
Write-Host "📊 Status dos serviços:" -ForegroundColor Cyan
docker-compose ps
Write-Host ""
Write-Host "🧪 Para demonstrar o problema, execute:" -ForegroundColor Yellow
Write-Host "   python tests\test_concorrencia.py 10" -ForegroundColor White
Write-Host ""
Write-Host "📋 Resultado esperado:" -ForegroundColor Yellow
Write-Host "   - MÚLTIPLOS agendamentos criados (2+)" -ForegroundColor White
Write-Host "   - Conflitos no banco de dados" -ForegroundColor White
Write-Host "   - Logs entrelaçados sem coordenação" -ForegroundColor White
Write-Host ""
Write-Host "🔒 Para voltar ao modo COM LOCK:" -ForegroundColor Cyan
Write-Host "   .\demo_com_lock.ps1" -ForegroundColor White
Write-Host ""
