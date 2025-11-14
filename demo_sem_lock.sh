#!/bin/bash

# ============================================
# SCTEC - Demonstração da Entrega 2
# Sistema SEM LOCK (demonstra o problema)
# ============================================

echo ""
echo -e "\033[1;33m============================================\033[0m"
echo -e "\033[1;33m   ATIVANDO MODO SEM LOCK\033[0m"
echo -e "\033[1;33m   (Demonstração do Problema - Entrega 2)\033[0m"
echo -e "\033[1;33m============================================\033[0m"
echo ""

# Verificar se .env existe, caso contrário criar
if [ ! -f ".env" ]; then
    echo -e "\033[1;36m📝 Criando arquivo .env...\033[0m"
    cp .env.example .env
fi

# Atualizar USE_LOCK=false no .env
echo -e "\033[1;36m⚙️  Configurando USE_LOCK=false...\033[0m"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's/USE_LOCK=true/USE_LOCK=false/g' .env
else
    # Linux
    sed -i 's/USE_LOCK=true/USE_LOCK=false/g' .env
fi

echo -e "\033[1;32m✓ Configuração atualizada\033[0m"
echo ""

echo -e "\033[1;36m🐳 Reiniciando containers...\033[0m"
docker-compose down
docker-compose up --build -d

echo ""
echo -e "\033[1;36m⏳ Aguardando serviços iniciarem...\033[0m"
sleep 10

echo ""
echo -e "\033[1;32m============================================\033[0m"
echo -e "\033[1;32m   MODO SEM LOCK ATIVADO!\033[0m"
echo -e "\033[1;32m============================================\033[0m"
echo ""
echo -e "\033[1;31m⚠️  ATENÇÃO: Sistema agora está VULNERÁVEL a condição de corrida!\033[0m"
echo ""
echo -e "\033[1;36m📊 Status dos serviços:\033[0m"
docker-compose ps
echo ""
echo -e "\033[1;33m🧪 Para demonstrar o problema, execute:\033[0m"
echo -e "\033[0;37m   python tests/test_concorrencia.py 10\033[0m"
echo ""
echo -e "\033[1;33m📋 Resultado esperado:\033[0m"
echo -e "\033[0;37m   - MÚLTIPLOS agendamentos criados (2+)\033[0m"
echo -e "\033[0;37m   - Conflitos no banco de dados\033[0m"
echo -e "\033[0;37m   - Logs entrelaçados sem coordenação\033[0m"
echo ""
echo -e "\033[1;36m🔒 Para voltar ao modo COM LOCK:\033[0m"
echo -e "\033[0;37m   ./demo_com_lock.sh\033[0m"
echo ""
