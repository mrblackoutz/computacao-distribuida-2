@echo off
echo ATENCAO: Isso ira remover todos os containers, volumes e dados!
echo.
set /p confirm="Tem certeza? (S/N): "
if /i "%confirm%"=="S" (
    echo Removendo sistema SCTEC...
    docker-compose down -v
    echo Sistema removido completamente.
    echo.
    echo Volumes removidos:
    echo   - sctec-agendamento-db (banco de dados^)
    echo   - sctec-agendamento-logs (logs^)
    echo.
    echo Para iniciar novamente: start.bat
) else (
    echo Operacao cancelada.
)
pause
