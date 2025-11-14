@echo off
echo ======================================
echo    SCTEC - Iniciando Sistema
echo ======================================
echo.

REM Verificar Docker
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker nao esta rodando. Inicie o Docker Desktop e tente novamente.
    pause
    exit /b 1
)

echo OK Docker esta rodando
echo.

echo Construindo e iniciando containers...
docker-compose up --build -d

echo.
echo Aguardando servicos ficarem prontos (isso pode levar ate 1 minuto)...
timeout /t 15 /nobreak >nul

echo.
echo Status dos servicos:
docker-compose ps

echo.
echo ======================================
echo    Sistema Iniciado!
echo ======================================
echo.
echo Interface Web: http://localhost:5000
echo API Agendamento: http://localhost:5000/api/v1
echo API Coordenador: http://localhost:3000
echo.
echo Comandos uteis:
echo    Ver logs: docker-compose logs -f
echo    Ver logs do agendamento: docker-compose logs -f agendamento
echo    Ver logs do coordenador: docker-compose logs -f coordenador
echo    Parar: docker-compose stop
echo    Reiniciar: docker-compose restart
echo    Remover: docker-compose down
echo    Remover com volumes: docker-compose down -v
echo.
echo Health checks:
echo    curl http://localhost:3000/health
echo    curl http://localhost:5000/api/v1/time
echo.
pause
