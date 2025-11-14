#!/bin/bash

# ============================================
# Script para configurar permissões de execução
# Execute este script após clonar o repositório
# ============================================

echo "🔧 Configurando permissões de execução..."
echo ""

# Tornar scripts principais executáveis
chmod +x start.sh
chmod +x stop.sh
chmod +x clean.sh

# Tornar scripts de demonstração executáveis
chmod +x demo_sem_lock.sh
chmod +x demo_com_lock.sh
chmod +x demo_comparacao.sh

echo "✅ Permissões configuradas com sucesso!"
echo ""
echo "Scripts disponíveis:"
echo "  • ./start.sh           - Iniciar sistema"
echo "  • ./stop.sh            - Parar sistema"
echo "  • ./clean.sh           - Limpar tudo"
echo "  • ./demo_sem_lock.sh   - Demo sem lock (problema)"
echo "  • ./demo_com_lock.sh   - Demo com lock (solução)"
echo "  • ./demo_comparacao.sh - Demo comparativa"
echo ""
