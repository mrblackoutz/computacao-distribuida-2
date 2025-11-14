# ============================================
# SCTEC - Demonstração da Entrega 3
# Sistema COM LOCK (demonstra a solução)
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   ATIVANDO MODO COM LOCK" -ForegroundColor Green
Write-Host "   (Demonstração da Solução - Entrega 3)" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# Verificar se .env existe, caso contrário criar
if (-not (Test-Path ".env")) {
    Write-Host "📝 Criando arquivo .env..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
}

# Atualizar USE_LOCK=true no .env
Write-Host "⚙️  Configurando USE_LOCK=true..." -ForegroundColor Cyan
$content = Get-Content ".env" -Raw
$content = $content -replace "USE_LOCK=false", "USE_LOCK=true"
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
Write-Host "   MODO COM LOCK ATIVADO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Sistema agora está PROTEGIDO contra condição de corrida!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Status dos serviços:" -ForegroundColor Cyan
docker-compose ps
Write-Host ""
Write-Host "🧪 Para demonstrar a solução, execute:" -ForegroundColor Yellow
Write-Host "   python tests\test_com_lock.py 10" -ForegroundColor White
Write-Host ""
Write-Host "📋 Resultado esperado:" -ForegroundColor Yellow
Write-Host "   - APENAS 1 agendamento criado (✓)" -ForegroundColor White
Write-Host "   - 9 conflitos (409)" -ForegroundColor White
Write-Host "   - Logs mostram coordenação via lock/unlock" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Para demonstrar o problema novamente:" -ForegroundColor Cyan
Write-Host "   .\demo_sem_lock.ps1" -ForegroundColor White
Write-Host ""
