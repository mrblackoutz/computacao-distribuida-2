@echo off
REM ============================================
REM Script para verificar permissões (Windows)
REM No Windows, não há necessidade de chmod
REM ============================================

echo.
echo ============================================
echo   Verificação de Scripts - Windows
echo ============================================
echo.

echo No Windows, os scripts PowerShell e BAT são executáveis por padrão.
echo.

echo Scripts disponíveis:
echo   • start.bat / start.ps1       - Iniciar sistema
echo   • stop.bat / stop.ps1         - Parar sistema  
echo   • clean.bat / clean.ps1       - Limpar tudo
echo   • demo_sem_lock.ps1           - Demo sem lock (problema)
echo   • demo_com_lock.ps1           - Demo com lock (solução)
echo   • demo_comparacao.ps1         - Demo comparativa
echo.

echo Para executar scripts BAT:
echo   start.bat
echo.

echo Para executar scripts PowerShell:
echo   .\start.ps1
echo   ou
echo   powershell -ExecutionPolicy Bypass -File .\start.ps1
echo.

echo ============================================
echo.

pause
