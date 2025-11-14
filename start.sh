#!/bin/bash

echo "======================================"
echo "   SCTEC - Iniciando Sistema"
echo "======================================"
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Inicie o Docker Desktop e tente novamente."
    exit 1
fi

echo "✓ Docker está rodando"
echo ""

# Build e start
echo "📦 Construindo e iniciando containers..."
docker-compose up --build -d

# Aguardar serviços ficarem saudáveis
echo ""
echo "⏳ Aguardando serviços ficarem prontos (isso pode levar até 1 minuto)..."
sleep 15

# Verificar status
echo ""
echo "📊 Status dos serviços:"
docker-compose ps

echo ""
echo "======================================"
echo "   Sistema Iniciado!"
echo "======================================"
echo ""
echo "🌐 Interface Web: http://localhost:5000"
echo "🔗 API Agendamento: http://localhost:5000/api/v1"
echo "🔗 API Coordenador: http://localhost:3000"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs: docker-compose logs -f"
echo "   Ver logs do agendamento: docker-compose logs -f agendamento"
echo "   Ver logs do coordenador: docker-compose logs -f coordenador"
echo "   Parar: docker-compose stop"
echo "   Reiniciar: docker-compose restart"
echo "   Remover: docker-compose down"
echo "   Remover com volumes: docker-compose down -v"
echo ""
echo "🔍 Health checks:"
echo "   curl http://localhost:3000/health"
echo "   curl http://localhost:5000/api/v1/time"
echo ""
