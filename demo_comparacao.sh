#!/bin/bash

# ============================================
# SCTEC - Demonstração Comparativa
# Mostra PROBLEMA (sem lock) vs SOLUÇÃO (com lock)
# ============================================

echo ""
echo -e "\033[1;36m════════════════════════════════════════════════════════════════\033[0m"
echo -e "\033[1;36m   SCTEC - DEMONSTRAÇÃO COMPARATIVA\033[0m"
echo -e "\033[1;36m   Condição de Corrida: Problema vs Solução\033[0m"
echo -e "\033[1;36m════════════════════════════════════════════════════════════════\033[0m"
echo ""

# Criar .env se não existir
if [ ! -f ".env" ]; then
    cp .env.example .env
fi

# Detectar sistema operacional para sed
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_INPLACE="-i ''"
else
    SED_INPLACE="-i"
fi

# ============================================
# PARTE 1: DEMONSTRAÇÃO DO PROBLEMA (SEM LOCK)
# ============================================

echo -e "\033[1;31m┌──────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;31m│  PARTE 1: DEMONSTRAÇÃO DO PROBLEMA (ENTREGA 2)              │\033[0m"
echo -e "\033[1;31m│  Sistema SEM proteção de lock                               │\033[0m"
echo -e "\033[1;31m└──────────────────────────────────────────────────────────────┘\033[0m"
echo ""

echo -e "\033[1;33m⚙️  Configurando sistema SEM LOCK...\033[0m"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's/USE_LOCK=true/USE_LOCK=false/g' .env
else
    sed -i 's/USE_LOCK=true/USE_LOCK=false/g' .env
fi

echo -e "\033[1;33m🐳 Iniciando containers...\033[0m"
docker-compose down -v > /dev/null 2>&1
docker-compose up --build -d > /dev/null 2>&1
sleep 12

echo -e "\033[1;33m🧪 Executando teste de concorrência (10 threads)...\033[0m"
echo ""
python tests/test_concorrencia.py 10

echo ""
echo -e "\033[1;33mPressione ENTER para continuar com a SOLUÇÃO...\033[0m"
read

# ============================================
# PARTE 2: DEMONSTRAÇÃO DA SOLUÇÃO (COM LOCK)
# ============================================

echo ""
echo ""
echo -e "\033[1;32m┌──────────────────────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;32m│  PARTE 2: DEMONSTRAÇÃO DA SOLUÇÃO (ENTREGA 3)               │\033[0m"
echo -e "\033[1;32m│  Sistema COM proteção de lock (Coordenador)                 │\033[0m"
echo -e "\033[1;32m└──────────────────────────────────────────────────────────────┘\033[0m"
echo ""

echo -e "\033[1;36m⚙️  Configurando sistema COM LOCK...\033[0m"
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' 's/USE_LOCK=false/USE_LOCK=true/g' .env
else
    sed -i 's/USE_LOCK=false/USE_LOCK=true/g' .env
fi

echo -e "\033[1;36m🐳 Reiniciando containers...\033[0m"
docker-compose down -v > /dev/null 2>&1
docker-compose up --build -d > /dev/null 2>&1
sleep 12

echo -e "\033[1;36m🧪 Executando teste com lock (10 threads)...\033[0m"
echo ""
python tests/test_com_lock.py 10

# ============================================
# RESUMO FINAL
# ============================================

echo ""
echo ""
echo -e "\033[1;36m════════════════════════════════════════════════════════════════\033[0m"
echo -e "\033[1;36m   RESUMO DA DEMONSTRAÇÃO\033[0m"
echo -e "\033[1;36m════════════════════════════════════════════════════════════════\033[0m"
echo ""

echo -e "\033[1;31m📊 PROBLEMA (Entrega 2 - SEM LOCK):\033[0m"
echo -e "\033[0;37m   ❌ Múltiplos agendamentos criados simultaneamente\033[0m"
echo -e "\033[0;37m   ❌ Conflitos no banco de dados\033[0m"
echo -e "\033[0;37m   ❌ Race condition entre verificação e INSERT\033[0m"
echo ""

echo -e "\033[1;32m✅ SOLUÇÃO (Entrega 3 - COM LOCK):\033[0m"
echo -e "\033[0;37m   ✓ Apenas 1 agendamento criado\033[0m"
echo -e "\033[0;37m   ✓ Exclusão mútua garantida pelo coordenador\033[0m"
echo -e "\033[0;37m   ✓ Sistema consistente e confiável\033[0m"
echo ""

echo -e "\033[1;36m🔍 ARQUITETURA DA SOLUÇÃO:\033[0m"
echo -e "\033[0;37m   • Serviço Coordenador (Node.js)\033[0m"
echo -e "\033[0;37m   • Endpoints: POST /lock e POST /unlock\033[0m"
echo -e "\033[0;37m   • Flask chama coordenador antes de acessar BD\033[0m"
echo -e "\033[0;37m   • Lock liberado em bloco try...finally\033[0m"
echo ""

echo -e "\033[1;33m📚 CONCEITOS DEMONSTRADOS:\033[0m"
echo -e "\033[0;37m   1. Condição de Corrida (Race Condition)\033[0m"
echo -e "\033[0;37m   2. Exclusão Mútua (Mutual Exclusion)\033[0m"
echo -e "\033[0;37m   3. Coordenador Centralizado\033[0m"
echo -e "\033[0;37m   4. Microserviços (Flask + Node.js)\033[0m"
echo -e "\033[0;37m   5. Logging e Observabilidade\033[0m"
echo ""

echo -e "\033[1;36m════════════════════════════════════════════════════════════════\033[0m"
echo ""
