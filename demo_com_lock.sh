#!/bin/bash

# ============================================
# SCTEC - Demonstração da Entrega 3
# Sistema COM LOCK (demonstra a solução)
# ============================================

echo ""
echo -e "\033[1;32m============================================\033[0m"
echo -e "\033[1;32m   ATIVANDO MODO COM LOCK\033[0m"
echo -e "\033[1;32m   (Demonstração da Solução - Entrega 3)\033[0m"
echo -e "\033[1;32m============================================\033[0m"
echo ""

# Verificar se .env existe, caso contrário criar
if [ ! -f ".env" ]; then
    echo -e "\033[1;36m📝 Criando arquivo .env...\033[0m"
    cp .env.example .env
fi

# Atualizar USE_LOCK=true no .env
echo -e "\033[1;36m⚙️  Configurando USE_LOCK=true...\033[0m"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's/USE_LOCK=false/USE_LOCK=true/g' .env
else
    # Linux
    sed -i 's/USE_LOCK=false/USE_LOCK=true/g' .env
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
echo -e "\033[1;32m   MODO COM LOCK ATIVADO!\033[0m"
echo -e "\033[1;32m============================================\033[0m"
echo ""
echo -e "\033[1;32m✅ Sistema agora está PROTEGIDO contra condição de corrida!\033[0m"
echo ""
echo -e "\033[1;36m📊 Status dos serviços:\033[0m"
docker-compose ps
echo ""
echo -e "\033[1;33m🧪 Para demonstrar a solução, execute:\033[0m"
echo -e "\033[0;37m   python tests/test_com_lock.py 10\033[0m"
echo ""
echo -e "\033[1;33m📋 Resultado esperado:\033[0m"
echo -e "\033[0;37m   - APENAS 1 agendamento criado (✓)\033[0m"
echo -e "\033[0;37m   - 9 conflitos (409)\033[0m"
echo -e "\033[0;37m   - Logs mostram coordenação via lock/unlock\033[0m"
echo ""
echo -e "\033[1;36m⚠️  Para demonstrar o problema novamente:\033[0m"
echo -e "\033[0;37m   ./demo_sem_lock.sh\033[0m"
echo ""
