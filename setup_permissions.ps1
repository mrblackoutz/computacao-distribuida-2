# ============================================
# Script para verificar permissões (Windows)
# No Windows PowerShell, scripts são executáveis
# mas podem precisar de ExecutionPolicy
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Verificação de Scripts - Windows" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar ExecutionPolicy atual
$policy = Get-ExecutionPolicy
Write-Host "ExecutionPolicy atual: " -NoNewline
if ($policy -eq "Restricted") {
    Write-Host $policy -ForegroundColor Red
    Write-Host ""
    Write-Host "⚠️  ExecutionPolicy está RESTRITA!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para permitir execução de scripts, execute (como Administrador):" -ForegroundColor Yellow
    Write-Host "   Set-ExecutionPolicy RemoteSigned" -ForegroundColor White
    Write-Host ""
    Write-Host "Ou execute scripts com bypass:" -ForegroundColor Yellow
    Write-Host "   powershell -ExecutionPolicy Bypass -File .\start.ps1" -ForegroundColor White
} else {
    Write-Host $policy -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ ExecutionPolicy permite execução de scripts!" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Scripts Disponíveis" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Listar scripts .ps1 e .bat
Write-Host "📜 Scripts BAT (executar diretamente):" -ForegroundColor Yellow
Get-ChildItem -Filter "*.bat" | ForEach-Object {
    Write-Host "   • $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "📜 Scripts PowerShell (executar com .\script.ps1):" -ForegroundColor Yellow
Get-ChildItem -Filter "*.ps1" | Where-Object { $_.Name -ne "setup_permissions.ps1" } | ForEach-Object {
    Write-Host "   • $($_.Name)" -ForegroundColor White
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Como Usar" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Scripts BAT:" -ForegroundColor Yellow
Write-Host "   start.bat" -ForegroundColor White
Write-Host "   stop.bat" -ForegroundColor White
Write-Host "   clean.bat" -ForegroundColor White
Write-Host ""

Write-Host "Scripts PowerShell:" -ForegroundColor Yellow
Write-Host "   .\start.ps1" -ForegroundColor White
Write-Host "   .\demo_sem_lock.ps1" -ForegroundColor White
Write-Host "   .\demo_com_lock.ps1" -ForegroundColor White
Write-Host "   .\demo_comparacao.ps1" -ForegroundColor White
Write-Host ""

Write-Host "Se houver erro de ExecutionPolicy:" -ForegroundColor Yellow
Write-Host "   powershell -ExecutionPolicy Bypass -File .\script.ps1" -ForegroundColor White
Write-Host ""

Write-Host "============================================" -ForegroundColor Green
Write-Host ""
