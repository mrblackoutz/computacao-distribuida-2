#!/bin/bash

echo "⏸️  Parando sistema SCTEC..."
docker-compose stop
echo "✅ Sistema parado."
echo ""
echo "Para iniciar novamente: ./start.sh ou start.bat"
echo "Para remover completamente: ./clean.sh"
