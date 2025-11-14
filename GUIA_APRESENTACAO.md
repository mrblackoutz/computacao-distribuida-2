# 🎤 Guia de Apresentação do Projeto SCTEC

## 📋 Roteiro de Apresentação (15-20 minutos)

### 1. Introdução (2 minutos)

**O que dizer:**
> "Bom dia/tarde professor(a). Desenvolvemos o SCTEC - Sistema de Controle de Telescópio Espacial Compartilhado. Este projeto implementa todos os conceitos de Sistemas Distribuídos: exclusão mútua, sincronização de tempo, HATEOAS, logging distribuído e containerização com Docker."

**Mostrar:**
- Slide com arquitetura do sistema
- Mencionar as tecnologias: Flask (Python), Node.js, Docker, SQLite

---

### 2. Demonstração do Problema - Race Condition (3 minutos)

**O que explicar:**
> "Primeiro vamos demonstrar o PROBLEMA que sistemas distribuídos enfrentam: a condição de corrida. Quando múltiplos clientes tentam agendar o mesmo horário simultaneamente, sem controle de concorrência, o sistema aceita todos os agendamentos."

**Como demonstrar:**

```bash
# Terminal 1
cd servico-agendamento
python run.py

# Terminal 2 - Executar teste
python tests\test_concorrencia.py 10
```

**O que mostrar:**
1. Script dispara 10 requisições simultâneas
2. Múltiplos agendamentos são criados (2, 3 ou mais)
3. No banco de dados há registros duplicados
4. Logs mostram requisições entrelaçadas

**Frase-chave:**
> "Veja que foram criados X agendamentos para o mesmo horário. Isso seria catastrófico em produção - dois astrônomos achariam que têm acesso exclusivo ao telescópio no mesmo momento!"

---

### 3. Demonstração da Solução - Exclusão Mútua (4 minutos)

**O que explicar:**
> "Para resolver este problema, implementamos um Serviço Coordenador em Node.js que gerencia locks distribuídos. Quando um cliente quer criar um agendamento, ele primeiro precisa adquirir um lock exclusivo."

**Como demonstrar:**

```bash
# Terminal 1 - Coordenador
cd servico-coordenador
npm start

# Terminal 2 - Agendamento
cd servico-agendamento
python run.py

# Terminal 3 - Teste com lock
python tests\test_com_lock.py 10
```

**O que mostrar:**
1. Ambos serviços iniciando (Coordenador na porta 3000, Flask na porta 5000)
2. Script dispara 10 requisições simultâneas
3. **APENAS 1 SUCESSO (201 Created)**
4. **9 CONFLITOS (409 Conflict)**
5. Banco de dados tem apenas 1 registro

**Mostrar nos logs:**
- Terminal do Node.js: "Lock concedido" para 1, "Recurso já em uso" para os outros 9
- Terminal do Flask: Mensagens de "Lock adquirido" e "Falha ao adquirir lock"

**Frase-chave:**
> "Veja a diferença! Agora apenas 1 agendamento foi criado. Os outros 9 receberam 409 Conflict porque o recurso estava travado. É exatamente assim que deve funcionar!"

---

### 4. Interface Web e Sincronização de Tempo (3 minutos)

**O que explicar:**
> "Além da API, criamos uma interface web completa que implementa o Algoritmo de Cristian para sincronização de tempo entre cliente e servidor."

**Como demonstrar:**

```
Acessar: http://localhost:5000
```

**O que mostrar:**
1. **Painel de Sincronização de Tempo:**
   - Hora local do navegador
   - Hora do servidor (UTC)
   - Offset calculado
   - Latência de rede
   - Indicador visual de sincronização

2. **Funcionalidade Completa:**
   - Selecionar cientista
   - Criar agendamento
   - Agendamento aparece na lista automaticamente
   - Botão "Cancelar" aparece

3. **HATEOAS em Ação:**
   - Cancelar o agendamento
   - Botão "Cancelar" desaparece (status mudou para CANCELADO)
   - Explicar que o cliente usa os links `_links` da API

**Frase-chave:**
> "Veja como o botão de cancelar desapareceu. Isso é HATEOAS - o cliente não tem regra de negócio hardcoded, ele apenas mostra botões se o link existe na resposta da API."

---

### 5. Logging Distribuído (2 minutos)

**O que explicar:**
> "Todo o sistema possui logging estruturado com Correlation IDs que permitem rastrear uma requisição completa através de múltiplos serviços."

**Como demonstrar:**

```bash
# Abrir arquivo de log
cat servico-agendamento\logs\app.log | Select-String "correlation_id"

# Ou mostrar logs de auditoria
cat servico-agendamento\logs\audit.log | Select-Object -First 5
```

**O que mostrar:**
1. **Logs de Aplicação:** Formato texto com timestamp, nível, correlation_id
2. **Logs de Auditoria:** Formato JSON com eventos de negócio
3. **Rastreamento:** Mesmo correlation_id em Flask e Node.js

**Frase-chave:**
> "Com o Correlation ID, podemos rastrear toda a jornada de uma requisição, desde que chega no Flask, passa pelo Coordenador para pegar o lock, volta pro Flask e é salva no banco."

---

### 6. Docker e Orquestração (3 minutos)

**O que explicar:**
> "Todo o sistema está containerizado com Docker. Com um único comando, subimos ambos os microserviços com healthchecks, volumes persistentes e logs agregados."

**Como demonstrar:**

```bash
# Parar serviços locais primeiro
Ctrl+C nos terminais

# Iniciar com Docker
start.bat  # ou ./start.sh

# Ver status
docker-compose ps

# Ver logs agregados
docker-compose logs -f
```

**O que mostrar:**
1. **docker-compose.yml:**
   - 2 serviços (coordenador, agendamento)
   - Healthchecks configurados
   - Volumes para persistência
   - Networks para comunicação

2. **Logs agregados:**
   - `docker-compose logs -f` mostra ambos serviços
   - Criar um agendamento via interface
   - Logs aparecem em tempo real de ambos os serviços

3. **Healthchecks:**
   ```bash
   curl http://localhost:5000/health
   curl http://localhost:3000/health
   ```

**Frase-chave:**
> "Com Docker, qualquer pessoa pode rodar o sistema completo com um comando. Os healthchecks garantem que os serviços estão saudáveis antes de começar a receber requisições."

---

### 7. Documentação e Fechamento (2 minutos)

**O que explicar:**
> "Toda a implementação está documentada em 8 arquivos Markdown detalhados, totalizando mais de 80 páginas de documentação técnica."

**Como demonstrar:**

Abrir e mostrar rapidamente:
1. **README.md:** Visão geral do projeto
2. **MODELOS.md:** Entidades e regras de negócio
3. **API.md:** Especificação completa da API
4. **LOGGING.md:** Formato dos logs
5. **CHECKLIST_FINAL.md:** Validação de todos os requisitos

**Frase-chave:**
> "Cada decisão técnica está documentada. Temos especificação de API, diagramas de arquitetura, exemplos de uso, troubleshooting e um checklist completo de validação."

---

## 🎯 Pontos-Chave a Enfatizar

### Durante toda a apresentação, destacar:

1. **Os 3 Desafios Centrais:**
   - ✅ Condição de corrida → RESOLVIDA com locks distribuídos
   - ✅ Sincronização de tempo → RESOLVIDA com Algoritmo de Cristian
   - ✅ Logging/auditoria → RESOLVIDA com correlation IDs

2. **Conceitos de REST:**
   - ✅ Stateless (cada requisição independente)
   - ✅ URIs semânticas (/cientistas/{id})
   - ✅ Métodos HTTP corretos
   - ✅ **HATEOAS** (o mais importante!)

3. **Microserviços:**
   - ✅ Flask para lógica de negócio (o "cérebro")
   - ✅ Node.js para coordenação (o "porteiro")
   - ✅ Comunicação HTTP entre serviços

4. **Qualidade:**
   - ✅ Código limpo e organizado
   - ✅ Tratamento de erros robusto
   - ✅ Documentação profissional
   - ✅ Testes automatizados

---

## 💡 Respostas para Perguntas Comuns

### "Por que usar Node.js para o Coordenador?"
> "Node.js é orientado a eventos e não-bloqueante, tornando-o perfeito para gerenciar locks onde há muita concorrência. Enquanto o Flask cuida da lógica de negócio complexa, o Node.js faz apenas uma tarefa simples (gerenciar locks) mas com altíssima eficiência."

### "Como garantem que o lock sempre é liberado?"
> "Usamos try-finally em Python. Mesmo se der erro ao criar o agendamento, o finally garante que o unlock será chamado. Além disso, o Coordenador tem timeout de 30 segundos e limpeza automática de locks expirados."

### "Por que SQLite se é um sistema distribuído?"
> "SQLite foi escolhido para simplicidade no ambiente acadêmico. Em produção, usaríamos PostgreSQL ou MongoDB. Mas SQLite é suficiente para demonstrar os conceitos de sistemas distribuídos, que independem do banco usado."

### "O que é HATEOAS mesmo?"
> "Hypermedia as the Engine of Application State. Significa que o cliente não precisa saber regras de negócio - ele apenas mostra botões se os links existem na resposta. Por exemplo, o botão 'Cancelar' só aparece se `_links.cancelar` existe, e só existe se status=AGENDADO."

### "Como o Correlation ID funciona?"
> "Quando uma requisição chega no Flask, geramos um UUID único. Esse ID é usado em todos os logs daquela requisição. Quando o Flask chama o Coordenador, passa o mesmo ID. Assim, podemos rastrear toda a operação através de múltiplos serviços."

---

## ⚠️ Possíveis Problemas e Soluções

### Problema: SQLite não funciona no Docker Windows
**Solução já implementada:** 
> "Nosso sistema detecta automaticamente problemas de locking do SQLite em volumes Windows/WSL e faz fallback para /tmp. Veja aqui nos logs: `[DEBUG] Concurrent connections test FAILED: database is locked` seguido de `[DEBUG] Volume has issues, switching to /tmp`"

### Problema: Porta 5000 ou 3000 em uso
**Solução:**
```bash
# Windows
netstat -ano | findstr ":5000"
taskkill /PID <PID> /F

# Ou mudar porta no docker-compose.yml
ports:
  - "5001:5000"
```

### Problema: Docker não inicia
**Solução:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Checklist Pré-Apresentação

### 1 Dia Antes:
- [ ] Testar tudo funcionando
- [ ] Verificar Docker Desktop instalado
- [ ] Revisar documentação
- [ ] Preparar slides (opcional)
- [ ] Ensaiar apresentação

### 1 Hora Antes:
- [ ] Parar todos containers: `docker-compose down`
- [ ] Limpar logs: `rm -rf servico-agendamento/logs/*`
- [ ] Reiniciar Docker Desktop
- [ ] Testar uma vez completo

### 15 Minutos Antes:
- [ ] Abrir terminais necessários
- [ ] Abrir navegador em http://localhost:5000
- [ ] Abrir documentação (README, CHECKLIST_FINAL)
- [ ] Verificar conectividade de rede

### Durante Apresentação:
- [ ] Falar devagar e claramente
- [ ] Mostrar código quando explicar conceito
- [ ] Usar logs para provar funcionamento
- [ ] Demonstrar problema ANTES da solução
- [ ] Enfatizar HATEOAS e correlation IDs

---

## 🏆 Mensagem Final

**Fechamento sugerido:**
> "Implementamos todos os requisitos do projeto com excelência técnica. Demonstramos o problema da condição de corrida e implementamos a solução com locks distribuídos. Sincronizamos tempo com Algoritmo de Cristian. Criamos uma API RESTful completa com HATEOAS verdadeiro. Implementamos logging distribuído com rastreamento completo. E containerizamos tudo com Docker para facilitar o deploy."

> "Mais importante: entendemos profundamente cada conceito de Sistemas Distribuídos e conseguimos aplicar na prática. O projeto está completo, testado, documentado e pronto para uso."

> "Obrigado pela atenção. Estou à disposição para perguntas!"

---

**Tempo total estimado:** 15-20 minutos  
**Nível de confiança:** 💪 MÁXIMO  
**Resultado esperado:** ⭐⭐⭐⭐⭐ Nota 10!

Boa sorte! 🍀
