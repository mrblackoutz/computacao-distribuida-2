#!/bin/bash

echo "⚠️  ATENÇÃO: Isso irá remover todos os containers, volumes e dados!"
echo ""
read -p "Tem certeza? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]
then
    echo "🗑️  Removendo sistema SCTEC..."
    docker-compose down -v
    echo "✅ Sistema removido completamente."
    echo ""
    echo "Volumes removidos:"
    echo "  - sctec-agendamento-db (banco de dados)"
    echo "  - sctec-agendamento-logs (logs)"
    echo ""
    echo "Para iniciar novamente: ./start.sh"
else
    echo "❌ Operação cancelada."
fi
