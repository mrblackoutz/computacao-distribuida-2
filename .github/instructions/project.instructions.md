---
applyTo: '**'
---
A TAREFA AGORA É IMPLEMENTAR TODO ESSE PROJETO, E SÓ PARAR QUANDO TERMINAR:

<projeto>
Atividade Computação Distribuída
 Web Services e Containers
 Prof Mario
 Laboratório
 Sistema de Controle de Telescópio Espacial Compartilhado (SCTEC)
 Vocês foram contratados para desenvolver o núcleo do sistema de agendamento do novo telescópio espacial acadêmico. Cientistas do mundo todo competirão por tempo de observação neste equipamento, que custa milhões de dólares por hora para operar.
 Nosso desafio não é apenas criar uma API de agendamento, mas garantir que ela seja justa, consistente, à prova de falhas em um ambiente de altíssima concorrência. Primeiro vamos entender os conceitos e as ferramentas que nos permitirão construir a solução.
 Fundamentos teóricos
 O que é um Web Service?
 Um Web Service é um sistema projetado para permitir a comunicação entre diferentes máquinas através de uma rede. Ele expõe funcionalidades que podem ser requisitadas por outras aplicações, independentemente da linguagem ou sistema operacional.
 O que são APIs e o Padrão REST?
 API(Application Programming Interface): É um contrato,um conjunto de regras que permite que diferentes aplicações se comuniquem. A API define quais funcionalidades estão disponíveis, que dados são necessários e o que será recebido como resposta. REST(REpresentational State Transfer): É um estilo de arquitetura para a criação de WebServices.
API RESTful
 1. Arquitetura Cliente-Servidor: Cliente (quem pede) e servidor (quem responde) são separados.
 2. Stateless (sem estado): Cada requisição contém toda a informação necessária para ser processada. O servidor não guarda o “contexto” do cliente.
 3. Interface uniforme: Esta é a restrição mais importante do REST.
 • Recursos são identificados por URIs: /telescopios/hubble, /agendamentos/123.
 • Uso dos Métodos HTTP: GET (ler), POST (criar), PUT (atualizar), DELETE (remover).
 • Representações: Os recursos são trocados em um formato como JSON.
 • HATEOAS(Hypermedia as the Engine of Application State): Este é o nível mais alto de maturidade REST.Significa que a resposta do servidor não deve conter apenas os dados do recurso, mas também links para as próximas ações possíveis que podem ser executadas sobre aquele recurso.
 Ferramentas: Flask e Node.js
 Flask (Python): É um “microframework” para desenvolvimento web em Python. Usaremos o Flask para construir nosso Serviço de Agendamento. Ele é excelente para criar APIs RESTful de forma rápida e limpa, cuidando da lógica de negócio principal e da comunicação com o banco de dados. Ele será o “cérebro” do nosso sistema. Node.js (JavaScript): É um ambiente de execução de JavaScript no lado do servidor. Sua principal característica é a arquitetura orientada a eventos e I/O (Entrada/Saída) não-bloqueante. Isso o torna extremamente eficiente para tarefas que envolvem muitas conexões simultâneas ou tempo de espera, como gerenciar locks. Usaremos o Node.js para construir nosso Serviço Coordenador, o “porteiro” rápido e eficiente do nosso sistema.
 Os três desafios centrais
 1. Condição de corrida (exclusão mútua): O que acontece se dois astrônomos, um em SãoPaulo e outro em Tóquio, conseguirem agendar o telescópio para o mesmo slot das 03:00 às 03:05 UTC? A garantia de que apenas um comando de agendamento pode ser processado por vez para um mesmo horário é a definição de exclusão mútua neste contexto.
2. A Ilusão do tempo (sincronização de relógio): Se o relógio do astrônomo de São Paulo está 2 segundos adiantado e o de Tóquio está 1 segundo atrasado, como o sistema pode determinar quem clicou em “reservar” primeiro? Um sistema distribuído sem uma noção de tempo unificada é caótico e não confiável.
 3. A memória do sistema (logging): Se um agendamento for contestado, como podemos provar quem o fez e quando? Se o sistema falhar, como podemos rastrear a sequência de eventos que levou ao erro? Em nosso sistema, o logging servirá para:
 • Logging de aplicação(depuração): Registros de eventos de baixo nível que ajudam os desenvolvedores a entenderem o fluxo do código. Ex: “Conexão como banco de dados estabelecida”, “Requisição recebida na rota /agendamentos”.
 • Logging de auditoria (negócio): Uma trilha de eventos importantes do ponto de vista do negócio. É um registro imutável de quem fez o quê e quando. Ex: “Cientista ‘Marie Curie’ (ID: 7) criou o agendamento (ID: 123) para ohorário’2025-12-01T03:00:00Z”. Isso é fundamental para resolver disputas.
 Arquitetura e Tecnologias
 Serviço de Agendamento (API Principal):
 • Linguagem/Framework: Python 3.9+ com Flask.
 • BancodeDados: SQLite (para simplicidade inicial) com SQLAlchemy.
 • Responsabilidade: Gerenciar a agenda, os cientistas e a persistência dos dados.
 É afonte autoritativa do estado da agenda. Serviço de Travamento e Sincronia (Coordenador):
 • Linguagem/Framework: Node.js 18+ com Express.js.
 • Responsabilidade: Atuar como um coordenador centralizado para garantir a exclusão mútua (serviço de “lock”) e, posteriormente, ajudar na disseminação de eventos em tempo real.
 Preparação do Ambiente (Setup Inicial)
 Antes da primeira entrega, vocês devem preparar suas máquinas.
 1. Instalar as Ferramentas:
 • Instale Python 3.9+.
 • Instale Node.js 18+.
 • Instale Docker Desktop.
 • Um cliente de API como Postman ou Insomnia.

 2. Estrutura de pastas do projeto (sugestão):
sctec-projeto/
├━━servico-agendamento/ (Python/Flask)
|   ├venv/
|   ├app.py
|   └━requirements.txt
└━━servico-coordenador/
    ├node_modules/
    ├server.js
    └━package. json (Node.js/Express)

 Figura 1: Estrutura de pastas do projeto
 3. Configuração Inicial (Serviço de Agendamento):
 # Dentro da pasta /servico-agendamento
 python-m venv venv
 source venv/bin/activate # No Windows: venv\Scripts\activate
 pip install Flask Flask-SQLAlchemy
 # salvar a lista de todas as bibliotecas instaladas
 pip freeze > requirements.txt
 4. Configuração inicial (Serviço Coordenador):
 # Dentro da pasta /servico-coordenador
 npm init-y
 npm install express
 Como os serviços colaboram Antes de iniciar, é crucial entender a “divisão de trabalho” em nossa arquitetura de microserviços. Teremos dois sistemas independentes que conversam entre si para atingir umobjetivocomum. PensenelescomooCérebroeoPorteirodeumaoperação crítica.

1. O Cérebro- Serviço de Agendamento (Python/Flask):
 • Responsabilidade: Lidar com toda a lógica de negócio complexa. Ele sabe o que é um cientista, o que é um agendamento e como persistir essas informações no banco de dados. Ele é a fonte de verdade sobre o “estado” da agenda do telescópio.
 • Em Ação: Quando recebe um pedido para criar um agendamento, ele é responsável por validar os dados, verificar as regras de negócio e, finalmente, salvar o registro no banco de dados.
 2. O Porteiro - Serviço Coordenador (Node.js/Express):
 • Responsabilidade: Executar uma única tarefa de forma extremamente rápida e eficiente: controlar o acesso. Ele não sabe nada sobre telescópios ou cientistas. Sua única função é dizer “pode passar” ou “espere, tem alguém na sua frente”. Ele gerencia uma fila invisível para garantir que apenas uma operação crítica aconteça por vez.
 • Em Ação: Ele expõe uma API simples para “travar” (lock) um recurso e depois “destravar” (unlock). Sua natureza leve e orientada a eventos (Node.js) é perfeita para essa tarefa de alta concorrência.

 O fluxo de uma requisição: Sincronização e Concorrência
 Para que o agendamento seja justo, o sistema resolve dois desafios em duas etapas:
 Etapa 1: Sincronização do relógio (garantindo um pedido justo)
 Imagine que o relógio do computador de um cientista em São Paulo está 2 segundos adiantado.
 1. Busca da Verdade: Antes de permitir o agendamento, o cliente (navegador) faz uma requisição GET /time ao Cérebro (Flask).
 • [LOGGING no Cérebro (Flask):] Um Log de Aplicação é gerado, ex: "INFO: Requisição recebida em GET /time do IP 1.2.3.4".
 2. Cálculo: O Cérebro responde com seu tempo oficial (a “fonte da verdade”). O cliente (usando o Algoritmo de Cristian) calcula e ajusta seu relógio local, compensando a latência da rede.
 3. Resultado: Agora, o cliente sabe a hora exata. Quando o cientista clica para reservar o horário 03:00:00Z, o timestamp enviado na requisição é o correto (baseado no tempo doservidor), e não o horário adiantado da máquina local (03:00:02Z).

Etapa 2: O Fluxo de uma Requisição de Agendamento Concorrente (Resolvendo a Disputa) Agora, imagine que duas requisições (de São Paulo e de Tóquio), ambas com o timestamp sincronizado e justo (ex: 03:00:00Z), chegam ao Cérebro (Flask) quase simultaneamente. O fluxo para resolver a disputa será o seguinte:
 1. Chegada: O Cérebro (Flask) recebe a primeira requisição POST /agendamentos (com timestamp já sincronizado).
 • [LOGGINGnoCérebro(Flask):] LogdeAplicação: "INFO: Requisição POST /agendamentos recebida para o recurso Hubble-Acad_2025-12-01T03:00:00Z".
 2. Pedido de Permissão (Exclusão Mútua): Antes de tocar no banco de dados, o Cérebro pausa e faz uma chamada de rede para o Porteiro (Node.js): “Quero acesso exclusivo ao recurso telescopio-1_2025-12-01T03:00:00Z. Posso?”.
 • [LOGGING no Cérebro (Flask):] Log de Aplicação: "INFO: Tentando adquirir lock para o recurso Hubble-Acad_2025-12-01T03:00:00Z".
 3. Permissão Concedida: O Porteiro, vendo que ninguém mais pediu acesso a esse recurso, responde “Sim, podepassar”(HTTP200OK)e anota que o recurso agora está travado.
 • [LOGGING no Porteiro (Node.js):] "Recebido pedido de lock para recurso Hubble-Acad_2025-12-01T03:00:00Z".
 • O Porteiro vê que o recurso está livre e o trava.
 • [LOGGING no Porteiro (Node.js):] "Lock concedido para recurso Hubble-Acad_2025-12-01T03:00:00Z".
 • O Porteiro responde “HTTP 200 OK” para o Flask.
 4. Ação Crítica: Com a permissão em mãos, o Cérebro (Flask) executa sua lógica crítica: verifica a disponibilidade no banco de dados e salva o novo agendamento.
 • [LOGGING no Cérebro (Flask):] Log de Aplicação: "INFO: Lock adquirido com sucesso para o recurso Hubble-Acad_2025-12-01T03:00:00Z".
 • O Cérebro salva o agendamento no banco de dados.
 • [LOGGING no Cérebro (Flask):] Log de AUDITORIA (JSON): {"level": "AUDIT", "event_type": "AGENDAMENTO_CRIADO", "agendamento_id": 123, ...}.
 5. Chegada da segunda requisição: Enquanto o Cérebro está ocupado,a segunda requisição (também com timestamp justo) chega. Ela também pede permissão ao Porteiro para o mesmo recurso.
 • [LOGGING no Cérebro (Flask):] "INFO: Requisição POST /agendamentos recebida para o recurso Hubble-Acad_2025-12-01T03:00:00Z.".
 • O Cérebro(Flask)chamaoPorteiro(Node.js)pedindo um lock para o mesmo recurso.
 • [LOGGING no Cérebro (Flask):] Um Log de Aplicação é gerado, ex: "INFO: Tentando adquirir lock para o recurso Hubble-Acad_2025-12-01T03:00:00Z".
 6. Permissão Negada: OPorteirovêqueorecursojáestátravadoeresponde“Não, espere. Recurso ocupado”(HTTP409Conflict). OCérebro(Flask), a o receber essa resposta, rejeita a segunda requisição
 • [LOGGING no Porteiro (Node.js):] "Recebido pedido de lock...".
 • O Porteiro vê que o recurso já está travado.
 • [LOGGING no Porteiro (Node.js):] "Recurso ... já em uso, negando lock.".
 • O Porteiro responde “HTTP 409 Conflict” para o Flask.
 7. Rejeição: O Cérebro (Flask) recebe o “Conflict” e rejeita a segunda requisição.
 • [LOGGING no Cérebro (Flask):] "INFO: Falha ao adquirir lock..., recurso ocupado.".
 • O Cérebro retorna o erro 409 ao segundo cliente.
 8. Liberação: Após o Cérebro(Flask) terminar sua operação com sucesso, ele envia um último comando ao Porteiro: “Obrigado, já terminei. Pode liberar o recurso”.
 O Porteiro então remove a trava.
 • [LOGGING no Cérebro(Flask):] "INFO: Liberando lock para o recurso...".
 • [LOGGING no Porteiro (Node.js):] "Recebido pedido de unlock... Lock liberado.".
 Essa colaboração garante que a Sincronização de Relógio torne os pedidos justos,e a Exclusão Mútua escolha apenas um vencedor. Ainda registra tudo no Logging (Etapa 3)
 Entregas do projeto em etapas
 Entrega 1: O Blueprint da API
 • Objetivo: Compreender que um bom software começa com um bom design. Aprender a pensar em uma API como um contrato e a projetar a observabilidade do sistema desde o início, definindo o formato dos logs de auditoria.
 
• Descrição: Nesta fase, vocês atuarão como arquitetos de software, focados puramente na especificação.
 • Passo apasso:
 1. Crie um arquivo chamado MODELOS.md para definir as entidades.
 2. Crie um arquivo chamado API.md para descrever cada endpoint, incluindo HATEOAS.
 3. Design de Log: Defina a estrutura dos logs de auditoria em LOGGING.md.
 Exemplo:
 {
 "timestamp_utc": "2025-10-26T18:00:05.123Z",
 "level": "AUDIT",
 "event_type": "AGENDAMENTO_CRIADO",
 "service": "servico-agendamento",
 "details": {
 "agendamento_id": 123,
 "cientista_id": 7,
 "horario_inicio_utc": "2025-12-01T03:00:00Z"
 }
 }
 4. Logs de aplicação (exemplo)
 – INFO:2025-10-26T18:00:04.500Z:servico-agendamento:Requisição recebida para POST /agendamentos
 – INFO:2025-10-26T18:00:04.505Z:servico-agendamento:Tentando adquirir lock para o recurso Hubble-Acad_2025-12-01T03:00:00Z
 – INFO:2025-10-26T18:00:05.120Z:servico-agendamento:Lock adquirido com sucesso
 – INFO:2025-10-26T18:00:05.122Z:servico-agendamento:Iniciando verificação de conflito no BD
 – INFO:2025-10-26T18:00:05.123Z:servico-agendamento:Salvando novo agendamento no BD
 – INFO:2025-10-26T18:00:04800Z:servico-agendamento:Requisição
 recebida para POST /agendamentos
 – INFO:2025-10-26T18:00:04.805Z:servico-agendamento:Tentando adquirir lock para o recurso Hubble-Acad_2025-12-01T03:00:00Z
 – INFO:2025-10-26T18:00:05.121Z:servico-agendamento:Falha ao adquirir lock, recurso ocupado
 • Critérios de Avaliação:
– Arquivo MODELOS.md completo.
– Arquivo API.md detalhando endpoints e respostas HATEOAS.
– Seção ouarquivo definindo o formato padrão para os logs.
 Entrega 2: O Sistema inicial (e a prova da falha nos logs)
 • Objetivo: Traduzir a especificação em código funcional, implementar uma API RESTful básica em Flask e usar os logs de aplicação e auditoria para provar visualmente a existência de uma condição de corrida.
 • Passo apasso:
 1. Implemente o “Cérebro” (Serviço de Agendamento) em Flask/SQLAlchemy
 de forma simples.
 2. Implementação de logging:
 – Configure o módulo logging do Python para escrever em app.log e no console.
 – Adicione logs de aplicação (nível INFO) em pontos-chave: “Requisição recebida para POST /agendamentos”, “Iniciando verificação de conflito no BD”, “Salvando novo agendamento no BD”.
 – Após salvar com sucesso no banco, emita um log de auditoria (nível WARNING ou um nível customizado AUDIT) no formato JSON definido na Entrega/Parte 1.
 3. Implemente a rota POST /agendamentos e os links HATEOAS.
 4. Crie um script de teste de estresse que dispare 10 requisições simultâneas.
 • ComoValidar o Sucesso:
 1. Execute o script de teste de estresse.
 2. Consulte o banco de dados e veja os múltiplos registros conflitantes.
 3. Examine app.log. Você deverá ver os logs entrelaçados e múltiplos logs de auditoria para o mesmo horário.
 • Critérios de avaliação:
 – Código funcional do serviço Flask com HATEOAS.
 – Script de teste que prova a condição de corrida.
 – Arquivo de log que mostra os logs entrelaçados e duplicados.
 Entrega/Parte 3: O Coordenador (e seus próprios registros)
 • Objetivo: Entender a arquitetura de microserviços, a comunicação inter-serviços e implementar o padrão de Coordenador Centralizado.
 • Passo apasso:
 1. Implemente o servidor Express com os endpoints POST /lock e POST /unlock.
 2. Logging no Coordenador: Adicione logs de console (console.log) no serviço Node.js para registrar eventos importantes: “Recebido pedido de lock para o recurso X”, “Lock concedido para o recurso X”, “Recurso X já está em uso, negando lock”, “Lock para o recurso X liberado”.
 3. Modifique a rota no Flask para chamar o serviço de lock antes da operação de BD, garantindo a liberação em um bloco try...finally.
 4. Logging da Coordenação: No serviço Flask, adicione logs de aplicação que registrem a comunicação: “Tentando adquirir lock para o recurso X”, “Lock adquirido com sucesso”, “Falha ao adquirir lock, recurso ocupado”.
 • Como validar o sucesso:
 1. Inicie ambos os servidores e execute o script de teste.
 2. O resultado deve ser uma requisição 201 Created e nove 409 Conflict.
 3. O banco de dados deve ter apenas um registro.
 4. Observe os terminais: o log do Node.js deve mostrar um lock concedido e nove negados. O log do Flask deve mostrar um sucesso, nove falhas e apenas um log de auditoria.
 • Critérios de avaliação:
 – Código funcional de ambos os serviços.
 – O teste de estresse prova que a exclusão mútua foi implementada.
 – Os logs de ambososserviços refletem a lógica de coordenação.
 Entrega/Parte 4: A fonte da verdade e o cliente inteligente
 • Objetivo: Compreender asincronização de tempo cliente-servidor e o HATEOAS.
 • Passo apasso:
 1. Crie o endpoint GET /time no Flask.
 2. Crie a interface web (index.html) com JavaScript que implementa algum algoritmo para sincronizar o tempo.
 3. Faça o cliente usar os links HATEOAS da resposta para habilitar e executar a ação de cancelamento.
 4. Logando a nova interação: Adicione um log de auditoria para o evento de cancelamento no endpoint correspondente do Flask. O log de aplicação também deve registrar as chamadas ao endpoint /time.
 • Critérios de avaliação:
 – Endpoint /time funcionando e cliente web implementado.
 – O cliente sincroniza o tempo e usa HATEOAS para o cancelamento.
 – Ao cancelar, um novo log de auditoria AGENDAMENTO_CANCELADO deve aparecer no app.log.
 Entrega 5: Orquestração com Docker (e logs centralizados)
 • Objetivo: Aprender os fundamentos de conteinerização com Docker e orquestração com Docker Compose.
 • Passo apasso:
 1. Crie um Dockerfile para o servico-agendamento (Python/Flask).
 2. Crie um Dockerfile para o servico-coordenador (Node.js/Express).
 3. Naraiz, crie um docker-compose.yml para conectar os dois serviços.
 4. Modifique a URL noFlask para usar o nome do serviço do Docker Compose (ex: http://servico-coordenador:3000).
 • Comovalidar o sucesso:
 1. Na raiz do projeto, execute docker-compose up--build. Os dois contêineres devem iniciar.
 2. Validação de Logs Orquestrados: Em um novo terminal, execute docker-compose logs-f. Isso mostrará o fluxo de logs de ambos os contêineres em tempo real e de forma entrelaçada.
 3. Use o Postman ou a interface web para interagir com a aplicação. Observe como as requisições geram logs no serviço Flask, que por sua vez geram logs no serviço coordenador, tudo visível em um único fluxo. O sistema deve
 funcionar perfeitamente.
 • Critérios de avaliação:
 – Arquivos Dockerfile e docker-compose.yml funcionais.
 – Aaplicação é executável com docker-compose up.
 – docker-compose logs demonstra com sucesso a agregação dos logs dos dois microserviços, provando que a observabilidade do sistema distribuído está funcionando.
</projeto>

<instrucoes_projeto>
# Plano Detalhado para o Projeto SCTEC - Sistema de Controle de Telescópio Espacial Compartilhado

Vou detalhar todas as tarefas e passos necessários para realizar este projeto com excelência máxima.

---

## 📋 ÍNDICE GERAL

1. Preparação do Ambiente
2. Entrega 1: Blueprint da API
3. Entrega 2: Sistema Inicial
4. Entrega 3: Serviço Coordenador
5. Entrega 4: Sincronização de Tempo
6. Entrega 5: Containerização
7. Testes e Validação Final

---

## 🔧 FASE 0: PREPARAÇÃO DO AMBIENTE

### Tarefa 0.1: Instalação de Ferramentas Base
**Tempo estimado: 1-2 horas**

#### Subtarefas:
1. **Instalar Python 3.13+**
   - Download do site oficial (python.org)
   - Verificar instalação: `python --version`
   - Configurar PATH do sistema
   - Instalar pip: `python -m ensurepip --upgrade`

2. **Instalar Node.js 24+**
   - Download do site oficial (nodejs.org)
   - Verificar instalação: `node --version` e `npm --version`
   - Configurar npm registry (opcional)

3. **Instalar Docker Desktop**
   - Download do site oficial (docker.com)
   - Configurar WSL2 (Windows) ou equivalente
   - Verificar: `docker --version` e `docker-compose --version`
   - Testar: `docker run hello-world`

4. **Instalar Cliente de API**
   - Postman (postman.com) OU
   - Insomnia (insomnia.rest)
   - Criar conta e workspace (usar curl por enquanto)

5. **Configurar Editor de Código**
   - VS Code (recomendado) com extensões:
     - Python
     - ESLint
     - Docker
     - REST Client
     - GitLens

### Tarefa 0.2: Estrutura de Pastas
**Tempo estimado: 15 minutos**

```bash
# Criar estrutura completa
mkdir telescopio-espacial
cd telescopio-espacial

mkdir servico-agendamento
mkdir servico-coordenador
mkdir docs
mkdir tests

# Criar arquivos base
touch README.md
touch .gitignore
touch docker-compose.yml
```

**Conteúdo inicial do .gitignore:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
*.db
*.log

# Node
node_modules/
npm-debug.log*

# Docker
*.env

# IDEs
.vscode/
.idea/
```

---

## 📝 ENTREGA 1: BLUEPRINT DA API

**Objetivo:** Design completo da arquitetura antes de programar
**Tempo estimado: 8-12 horas**

### Tarefa 1.1: Modelagem de Dados (MODELOS.md)
**Tempo estimado: 3-4 horas**

#### Subtarefas:

1. **Definir Entidade Cientista**
   ```markdown
   ## Cientista
   
   Representa um pesquisador autorizado a usar o telescópio.
   
   ### Atributos:
   - id (INTEGER, PK, AUTO_INCREMENT)
   - nome (STRING, 200, NOT NULL)
   - email (STRING, 200, UNIQUE, NOT NULL)
   - instituicao (STRING, 300, NOT NULL)
   - pais (STRING, 100, NOT NULL)
   - especialidade (STRING, 200)
   - data_cadastro (DATETIME, NOT NULL, DEFAULT=NOW)
   - ativo (BOOLEAN, NOT NULL, DEFAULT=TRUE)
   
   ### Regras de Negócio:
   - Email deve ser único e válido
   - Nome deve ter no mínimo 3 caracteres
   - Cientista inativo não pode criar agendamentos
   
   ### Índices:
   - idx_email (email)
   - idx_ativo (ativo)
   ```

2. **Definir Entidade Agendamento**
   ```markdown
   ## Agendamento
   
   Representa uma reserva de tempo no telescópio.
   
   ### Atributos:
   - id (INTEGER, PK, AUTO_INCREMENT)
   - cientista_id (INTEGER, FK -> Cientista.id, NOT NULL)
   - horario_inicio_utc (DATETIME, NOT NULL)
   - horario_fim_utc (DATETIME, NOT NULL)
   - objeto_celeste (STRING, 300, NOT NULL)
   - observacoes (TEXT, NULLABLE)
   - status (ENUM: 'AGENDADO', 'CANCELADO', 'CONCLUIDO', DEFAULT='AGENDADO')
   - data_criacao (DATETIME, NOT NULL, DEFAULT=NOW)
   - data_cancelamento (DATETIME, NULLABLE)
   - motivo_cancelamento (TEXT, NULLABLE)
   
   ### Regras de Negócio:
   - horario_fim_utc > horario_inicio_utc
   - Duração mínima: 5 minutos
   - Duração máxima: 2 horas
   - Não pode haver sobreposição de horários
   - Slots devem ser múltiplos de 5 minutos
   - Não pode agendar no passado
   - Antecedência mínima: 24 horas
   - Cientista pode ter no máximo 3 agendamentos ativos
   
   ### Índices:
   - idx_horario_status (horario_inicio_utc, horario_fim_utc, status)
   - idx_cientista (cientista_id)
   - idx_status (status)
   
   ### Constraints:
   - UNIQUE(horario_inicio_utc, horario_fim_utc) WHERE status='AGENDADO'
   ```

3. **Definir Relacionamentos**
   - Cientista 1:N Agendamento
   - Diagrama ER (pode usar draw.io ou similar)

4. **Validações e Constraints SQL**
   - Documentar triggers necessários
   - Documentar stored procedures (se aplicável)

### Tarefa 1.2: Especificação da API (API.md)
**Tempo estimado: 4-5 horas**

#### Subtarefas:

1. **Endpoint: GET /api/v1/time**
   ```markdown
   ### GET /api/v1/time
   
   Retorna o timestamp oficial do servidor para sincronização.
   
   **Request:**
   - Método: GET
   - Headers: Nenhum requerido
   - Body: Nenhum
   - Query Params: Nenhum
   
   **Response Success (200 OK):**
   ```json
   {
     "timestamp_utc": "2025-11-09T15:30:45.123456Z",
     "timezone": "UTC",
     "epoch_ms": 1731166245123,
     "_links": {
       "self": { "href": "/api/v1/time" },
       "agendamentos": { "href": "/api/v1/agendamentos" }
     }
   }
   ```
   
   **Códigos de Status:**
   - 200: Sucesso
   - 500: Erro interno do servidor
   ```

2. **Endpoint: GET /api/v1/cientistas**
   ```markdown
   ### GET /api/v1/cientistas
   
   Lista todos os cientistas cadastrados.
   
   **Request:**
   - Método: GET
   - Headers: Nenhum (futuramente: Authorization)
   - Query Params:
     - page (int, default=1): Número da página
     - per_page (int, default=20, max=100): Itens por página
     - ativo (bool, optional): Filtrar por status
   
   **Response Success (200 OK):**
   ```json
   {
     "cientistas": [
       {
         "id": 1,
         "nome": "Marie Curie",
         "email": "marie@curie.edu",
         "instituicao": "Universidade de Paris",
         "pais": "França",
         "especialidade": "Radioastronomia",
         "ativo": true,
         "_links": {
           "self": { "href": "/api/v1/cientistas/1" },
           "agendamentos": { "href": "/api/v1/cientistas/1/agendamentos" },
           "criar_agendamento": { 
             "href": "/api/v1/agendamentos",
             "method": "POST"
           }
         }
       }
     ],
     "pagination": {
       "page": 1,
       "per_page": 20,
       "total_items": 45,
       "total_pages": 3
     },
     "_links": {
       "self": { "href": "/api/v1/cientistas?page=1" },
       "next": { "href": "/api/v1/cientistas?page=2" },
       "last": { "href": "/api/v1/cientistas?page=3" }
     }
   }
   ```
   ```

3. **Endpoint: POST /api/v1/cientistas**
   - Request body completo
   - Validações (400)
   - Conflitos (409) - email duplicado
   - Success (201)

4. **Endpoint: GET /api/v1/cientistas/{id}**
   - Path parameters
   - 404 quando não encontrado
   - HATEOAS com links para atualizar/deletar/agendamentos

5. **Endpoint: GET /api/v1/agendamentos**
   - Filtros: data_inicio, data_fim, cientista_id, status
   - Ordenação: data ASC/DESC
   - Paginação
   - HATEOAS

6. **Endpoint: POST /api/v1/agendamentos** (PRINCIPAL)
   ```markdown
   ### POST /api/v1/agendamentos
   
   Cria um novo agendamento (operação crítica).
   
   **Request:**
   ```json
   {
     "cientista_id": 7,
     "horario_inicio_utc": "2025-12-01T03:00:00Z",
     "horario_fim_utc": "2025-12-01T03:30:00Z",
     "objeto_celeste": "NGC 1300",
     "observacoes": "Estudo de estrutura espiral"
   }
   ```
   
   **Validações:**
   - cientista_id existe e está ativo
   - horários são válidos e futuros
   - duração entre 5min e 2h
   - múltiplos de 5 minutos
   - antecedência mínima de 24h
   - sem conflitos no horário
   
   **Response Success (201 Created):**
   ```json
   {
     "id": 123,
     "cientista_id": 7,
     "cientista_nome": "Marie Curie",
     "horario_inicio_utc": "2025-12-01T03:00:00Z",
     "horario_fim_utc": "2025-12-01T03:30:00Z",
     "objeto_celeste": "NGC 1300",
     "observacoes": "Estudo de estrutura espiral",
     "status": "AGENDADO",
     "data_criacao": "2025-11-09T15:30:45Z",
     "_links": {
       "self": { "href": "/api/v1/agendamentos/123" },
       "cientista": { "href": "/api/v1/cientistas/7" },
       "cancelar": {
         "href": "/api/v1/agendamentos/123",
         "method": "DELETE"
       }
     }
   }
   ```
   
   **Códigos de Erro:**
   - 400: Dados inválidos
   - 404: Cientista não encontrado
   - 409: Conflito de horário ou recurso travado
   - 422: Regra de negócio violada
   - 500: Erro interno
   ```

7. **Endpoint: DELETE /api/v1/agendamentos/{id}**
   - Validação de status (só pode cancelar AGENDADO)
   - Soft delete (muda status)
   - Registro de motivo

8. **Endpoint: GET /api/v1/agendamentos/{id}**
   - Detalhes completos
   - HATEOAS condicional (links baseados no status)

### Tarefa 1.3: Especificação de Logging (LOGGING.md)
**Tempo estimado: 2-3 horas**

#### Subtarefas:

1. **Definir Estrutura de Log de Auditoria**
   ```markdown
   # Sistema de Logging - SCTEC
   
   ## Logs de Auditoria (JSON)
   
   ### Estrutura Base
   ```json
   {
     "timestamp_utc": "ISO8601",
     "level": "AUDIT",
     "event_type": "TIPO_EVENTO",
     "service": "nome-do-servico",
     "correlation_id": "uuid",
     "details": {}
   }
   ```
   
   ### Eventos de Auditoria
   
   #### CIENTISTA_CRIADO
   ```json
   {
     "timestamp_utc": "2025-11-09T15:30:45.123Z",
     "level": "AUDIT",
     "event_type": "CIENTISTA_CRIADO",
     "service": "servico-agendamento",
     "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
     "details": {
       "cientista_id": 7,
       "nome": "Marie Curie",
       "email": "marie@curie.edu",
       "instituicao": "Universidade de Paris"
     }
   }
   ```
   
   #### AGENDAMENTO_CRIADO
   ```json
   {
     "timestamp_utc": "2025-11-09T15:30:45.123Z",
     "level": "AUDIT",
     "event_type": "AGENDAMENTO_CRIADO",
     "service": "servico-agendamento",
     "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
     "details": {
       "agendamento_id": 123,
       "cientista_id": 7,
       "cientista_nome": "Marie Curie",
       "horario_inicio_utc": "2025-12-01T03:00:00Z",
       "horario_fim_utc": "2025-12-01T03:30:00Z",
       "objeto_celeste": "NGC 1300"
     }
   }
   ```
   
   #### AGENDAMENTO_CANCELADO
   #### AGENDAMENTO_CONFLITO
   (continuar para todos os eventos...)
   ```

2. **Definir Estrutura de Log de Aplicação**
   ```markdown
   ## Logs de Aplicação (Texto)
   
   ### Formato
   ```
   [LEVEL] timestamp_utc service correlation_id: mensagem
   ```
   
   ### Níveis
   - DEBUG: Detalhes técnicos para desenvolvimento
   - INFO: Fluxo normal da aplicação
   - WARNING: Situações incomuns mas tratadas
   - ERROR: Erros que impedem operações
   - CRITICAL: Falhas que comprometem o sistema
   
   ### Exemplos
   ```
   [INFO] 2025-11-09T15:30:45.123Z servico-agendamento a1b2c3d4: Requisição POST /agendamentos recebida
   [INFO] 2025-11-09T15:30:45.125Z servico-agendamento a1b2c3d4: Validando dados do agendamento
   [INFO] 2025-11-09T15:30:45.127Z servico-agendamento a1b2c3d4: Tentando adquirir lock para recurso Hubble-Acad_2025-12-01T03:00:00Z
   [INFO] 2025-11-09T15:30:45.250Z servico-agendamento a1b2c3d4: Lock adquirido com sucesso
   [INFO] 2025-11-09T15:30:45.252Z servico-agendamento a1b2c3d4: Verificando conflitos no banco de dados
   [INFO] 2025-11-09T15:30:45.275Z servico-agendamento a1b2c3d4: Nenhum conflito encontrado
   [INFO] 2025-11-09T15:30:45.280Z servico-agendamento a1b2c3d4: Salvando agendamento no banco de dados
   [INFO] 2025-11-09T15:30:45.295Z servico-agendamento a1b2c3d4: Agendamento salvo com ID 123
   [INFO] 2025-11-09T15:30:45.300Z servico-agendamento a1b2c3d4: Liberando lock
   [INFO] 2025-11-09T15:30:45.305Z servico-agendamento a1b2c3d4: Resposta 201 enviada
   ```
   ```

3. **Definir Pontos de Log no Fluxo**
   - Mapear cada endpoint e seus logs
   - Definir correlation_id (UUID por requisição)
   - Estratégia de rotação de logs
   - Níveis por ambiente (dev/prod)

### Tarefa 1.4: Diagramas de Arquitetura
**Tempo estimado: 1-2 horas**

1. **Diagrama de Arquitetura Geral**
   - Cliente Web → Serviço Agendamento → BD
   - Cliente Web → Serviço Agendamento ↔ Serviço Coordenador
   - Ferramenta: Draw.io, Lucidchart

2. **Diagrama de Sequência - Agendamento com Sucesso**
   ```
   Cliente → Flask: POST /agendamentos
   Flask → Flask: Gerar correlation_id
   Flask → Flask: Log INFO "Requisição recebida"
   Flask → Flask: Validar dados
   Flask → Node: POST /lock (recurso)
   Node → Node: Verificar disponibilidade
   Node → Node: Travar recurso
   Node → Flask: 200 OK
   Flask → Flask: Log INFO "Lock adquirido"
   Flask → BD: Verificar conflitos
   BD → Flask: Nenhum conflito
   Flask → BD: INSERT agendamento
   Flask → Flask: Log AUDIT "AGENDAMENTO_CRIADO"
   Flask → Node: POST /unlock (recurso)
   Node → Node: Liberar recurso
   Flask → Cliente: 201 Created + HATEOAS
   ```

3. **Diagrama de Sequência - Condição de Corrida**
   - Duas requisições simultâneas
   - Uma consegue lock, outra recebe 409

### Tarefa 1.5: Revisão e Documentação Final
**Tempo estimado: 1 hora**

1. **Criar README.md do projeto**
2. **Revisar todos os documentos**
3. **Criar checklist de validação**
4. **Commit da Entrega 1**

---

## 💻 ENTREGA 2: SISTEMA INICIAL

**Objetivo:** Implementar API funcional e provar a condição de corrida
**Tempo estimado: 16-20 horas**

### Tarefa 2.1: Setup do Serviço de Agendamento
**Tempo estimado: 2 horas**

#### Subtarefas:

1. **Criar ambiente virtual Python**
   ```bash
   cd servico-agendamento
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Instalar dependências**
   ```bash
   pip install Flask==3.0.0
   pip install Flask-SQLAlchemy==3.1.1
   pip install Flask-CORS==4.0.0
   pip install python-dotenv==1.0.0
   pip freeze > requirements.txt
   ```

3. **Criar estrutura de pastas**
   ```bash
   mkdir app
   mkdir app/models
   mkdir app/routes
   mkdir app/utils
   mkdir tests
   mkdir logs
   
   touch app/__init__.py
   touch app/models/__init__.py
   touch app/routes/__init__.py
   touch app/utils/__init__.py
   touch config.py
   touch run.py
   touch .env
   ```

4. **Configurar .env**
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=chave-super-secreta-trocar-em-producao
   DATABASE_URI=sqlite:///telescopio.db
   LOG_LEVEL=INFO
   COORDENADOR_URL=http://localhost:3000
   ```

### Tarefa 2.2: Configuração Base do Flask
**Tempo estimado: 2 horas**

#### Arquivo: config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///telescopio.db')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    COORDENADOR_URL = os.getenv('COORDENADOR_URL', 'http://localhost:3000')
    
    # Regras de negócio
    DURACAO_MINIMA_MINUTOS = 5
    DURACAO_MAXIMA_MINUTOS = 120
    ANTECEDENCIA_MINIMA_HORAS = 24
    MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA = 3

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

#### Arquivo: app/__init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
import os
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    """Factory pattern para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    
    # Configurar logging
    setup_logging(app)
    
    # Registrar blueprints
    from app.routes import time_bp, cientistas_bp, agendamentos_bp
    app.register_blueprint(time_bp, url_prefix='/api/v1')
    app.register_blueprint(cientistas_bp, url_prefix='/api/v1')
    app.register_blueprint(agendamentos_bp, url_prefix='/api/v1')
    
    # Criar tabelas
    with app.app_context():
        db.create_all()
    
    return app

def setup_logging(app):
    """Configura o sistema de logging"""
    # Criar diretório de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configurar formato
    log_format = '[%(levelname)s] %(asctime)s %(name)s %(correlation_id)s: %(message)s'
    
    # Handler para arquivo
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Configurar logger da aplicação
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
```

### Tarefa 2.3: Implementar Modelos
**Tempo estimado: 3 horas**

#### Arquivo: app/models/cientista.py
```python
from app import db
from datetime import datetime
from sqlalchemy import Index

class Cientista(db.Model):
    """Modelo de Cientista"""
    __tablename__ = 'cientistas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    instituicao = db.Column(db.String(300), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(200))
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    
    # Relacionamento
    agendamentos = db.relationship('Agendamento', back_populates='cientista', lazy='dynamic')
    
    # Índices
    __table_args__ = (
        Index('idx_email', 'email'),
        Index('idx_ativo', 'ativo'),
    )
    
    def __repr__(self):
        return f'<Cientista {self.nome}>'
    
    def to_dict(self, include_links=True):
        """Serializa o objeto para dicionário"""
        data = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'instituicao': self.instituicao,
            'pais': self.pais,
            'especialidade': self.especialidade,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() + 'Z'
        }
        
        if include_links:
            data['_links'] = self.get_links()
        
        return data
    
    def get_links(self):
        """Retorna links HATEOAS"""
        from flask import url_for
        return {
            'self': {'href': url_for('cientistas.get_cientista', id=self.id, _external=True)},
            'agendamentos': {'href': url_for('cientistas.get_cientista_agendamentos', id=self.id, _external=True)},
            'criar_agendamento': {
                'href': url_for('agendamentos.create_agendamento', _external=True),
                'method': 'POST'
            }
        }
    
    @staticmethod
    def validate_data(data, is_update=False):
        """Valida os dados do cientista"""
        errors = []
        
        if not is_update or 'nome' in data:
            nome = data.get('nome', '').strip()
            if not nome:
                errors.append('Nome é obrigatório')
            elif len(nome) < 3:
                errors.append('Nome deve ter no mínimo 3 caracteres')
        
        if not is_update or 'email' in data:
            email = data.get('email', '').strip()
            if not email:
                errors.append('Email é obrigatório')
            elif '@' not in email or '.' not in email:
                errors.append('Email inválido')
        
        if not is_update or 'instituicao' in data:
            if not data.get('instituicao', '').strip():
                errors.append('Instituição é obrigatória')
        
        if not is_update or 'pais' in data:
            if not data.get('pais', '').strip():
                errors.append('País é obrigatório')
        
        return errors
```

#### Arquivo: app/models/agendamento.py
```python
from app import db
from datetime import datetime, timedelta
from sqlalchemy import Index, CheckConstraint

class Agendamento(db.Model):
    """Modelo de Agendamento"""
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    cientista_id = db.Column(db.Integer, db.ForeignKey('cientistas.id'), nullable=False)
    horario_inicio_utc = db.Column(db.DateTime, nullable=False)
    horario_fim_utc = db.Column(db.DateTime, nullable=False)
    objeto_celeste = db.Column(db.String(300), nullable=False)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='AGENDADO')
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_cancelamento = db.Column(db.DateTime)
    motivo_cancelamento = db.Column(db.Text)
    
    # Relacionamento
    cientista = db.relationship('Cientista', back_populates='agendamentos')
    
    # Índices
    __table_args__ = (
        Index('idx_horario_status', 'horario_inicio_utc', 'horario_fim_utc', 'status'),
        Index('idx_cientista', 'cientista_id'),
        Index('idx_status', 'status'),
        CheckConstraint('horario_fim_utc > horario_inicio_utc', name='check_horarios'),
        CheckConstraint("status IN ('AGENDADO', 'CANCELADO', 'CONCLUIDO')", name='check_status'),
    )
    
    def __repr__(self):
        return f'<Agendamento {self.id} - {self.objeto_celeste}>'
    
    def to_dict(self, include_links=True):
        """Serializa o objeto para dicionário"""
        data = {
            'id': self.id,
            'cientista_id': self.cientista_id,
            'cientista_nome': self.cientista.nome,
            'horario_inicio_utc': self.horario_inicio_utc.isoformat() + 'Z',
            'horario_fim_utc': self.horario_fim_utc.isoformat() + 'Z',
            'objeto_celeste': self.objeto_celeste,
            'observacoes': self.observacoes,
            'status': self.status,
            'data_criacao': self.data_criacao.isoformat() + 'Z'
        }
        
        if self.status == 'CANCELADO':
            data['data_cancelamento'] = self.data_cancelamento.isoformat() + 'Z' if self.data_cancelamento else None
            data['motivo_cancelamento'] = self.motivo_cancelamento
        
        if include_links:
            data['_links'] = self.get_links()
        
        return data
    
    def get_links(self):
        """Retorna links HATEOAS"""
        from flask import url_for
        links = {
            'self': {'href': url_for('agendamentos.get_agendamento', id=self.id, _external=True)},
            'cientista': {'href': url_for('cientistas.get_cientista', id=self.cientista_id, _external=True)}
        }
        
        # Link condicional baseado no status
        if self.status == 'AGENDADO':
            links['cancelar'] = {
                'href': url_for('agendamentos.cancel_agendamento', id=self.id, _external=True),
                'method': 'DELETE'
            }
        
        return links
    
    @staticmethod
    def validate_data(data, config):
        """Valida os dados do agendamento"""
        errors = []
        
        # Validações básicas
        if 'cientista_id' not in data:
            errors.append('cientista_id é obrigatório')
        
        if 'horario_inicio_utc' not in data:
            errors.append('horario_inicio_utc é obrigatório')
        
        if 'horario_fim_utc' not in data:
            errors.append('horario_fim_utc é obrigatório')
        
        if 'objeto_celeste' not in data:
            errors.append('objeto_celeste é obrigatório')
        
        if errors:
            return errors
        
        # Converter strings para datetime
        try:
            inicio = datetime.fromisoformat(data['horario_inicio_utc'].replace('Z', '+00:00'))
            fim = datetime.fromisoformat(data['horario_fim_utc'].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            errors.append('Formato de data/hora inválido. Use ISO8601 (ex: 2025-12-01T03:00:00Z)')
            return errors
        
        agora = datetime.utcnow()
        
        # Validar horários
        if fim <= inicio:
            errors.append('horario_fim_utc deve ser posterior a horario_inicio_utc')
        
        duracao_minutos = (fim - inicio).total_seconds() / 60
        
        if duracao_minutos < config['DURACAO_MINIMA_MINUTOS']:
            errors.append(f'Duração mínima: {config["DURACAO_MINIMA_MINUTOS"]} minutos')
        
        if duracao_minutos > config['DURACAO_MAXIMA_MINUTOS']:
            errors.append(f'Duração máxima: {config["DURACAO_MAXIMA_MINUTOS"]} minutos')
        
        # Verificar múltiplos de 5 minutos
        if inicio.minute % 5 != 0 or fim.minute % 5 != 0:
            errors.append('Horários devem ser múltiplos de 5 minutos')
        
        # Verificar se não é no passado
        if inicio <= agora:
            errors.append('Não é possível agendar no passado')
        
        # Verificar antecedência mínima
        antecedencia = inicio - agora
        if antecedencia < timedelta(hours=config['ANTECEDENCIA_MINIMA_HORAS']):
            errors.append(f'Antecedência mínima: {config["ANTECEDENCIA_MINIMA_HORAS"]} horas')
        
        return errors
    
    @staticmethod
    def check_conflicts(inicio, fim, cientista_id=None, agendamento_id=None):
        """Verifica conflitos de horário"""
        query = Agendamento.query.filter(
            Agendamento.status == 'AGENDADO',
            Agendamento.horario_inicio_utc < fim,
            Agendamento.horario_fim_utc > inicio
        )
        
        if agendamento_id:
            query = query.filter(Agendamento.id != agendamento_id)
        
        conflitos = query.all()
        return conflitos
```

### Tarefa 2.4: Implementar Sistema de Logging
**Tempo estimado: 2 horas**

#### Arquivo: app/utils/logger.py
```python
import logging
import json
from datetime import datetime
from flask import g, has_request_context
import uuid

class CorrelationIdFilter(logging.Filter):
    """Filtro para adicionar correlation_id aos logs"""
    def filter(self, record):
        if has_request_context():
            record.correlation_id = g.get('correlation_id', 'no-correlation-id')
        else:
            record.correlation_id = 'no-correlation-id'
        return True

def get_correlation_id():
    """Obtém ou cria um correlation_id para a requisição atual"""
    if has_request_context():
        if 'correlation_id' not in g:
            g.correlation_id = str(uuid.uuid4())
        return g.correlation_id
    return str(uuid.uuid4())

def log_audit(event_type, details, service='servico-agendamento'):
    """
    Registra um evento de auditoria em formato JSON
    
    Args:
        event_type: Tipo do evento (ex: AGENDAMENTO_CRIADO)
        details: Dicionário com detalhes do evento
        service: Nome do serviço
    """
    audit_log = {
        'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
        'level': 'AUDIT',
        'event_type': event_type,
        'service': service,
        'correlation_id': get_correlation_id(),
        'details': details
    }
    
    # Usar logging.warning para garantir que será registrado
    # (AUDIT não é um nível padrão do Python)
    logger = logging.getLogger('audit')
    logger.warning(json.dumps(audit_log, ensure_ascii=False))

def setup_audit_logger():
    """Configura o logger de auditoria"""
    audit_logger = logging.getLogger('audit')
    audit_logger.setLevel(logging.WARNING)
    
    # Handler específico para auditoria
    handler = logging.FileHandler('logs/audit.log')
    handler.setLevel(logging.WARNING)
    
    # Formato simples para auditoria (já é JSON)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    
    audit_logger.addHandler(handler)
    audit_logger.propagate = False  # Não propagar para o root logger
```

#### Arquivo: app/utils/middleware.py
```python
from flask import g, request
from app.utils.logger import get_correlation_id
import logging

def setup_request_middleware(app):
    """Configura middleware para requisições"""
    
    @app.before_request
    def before_request():
        """Executado antes de cada requisição"""
        # Gerar correlation_id
        correlation_id = get_correlation_id()
        g.correlation_id = correlation_id
        
        # Log de entrada
        app.logger.info(
            f"Requisição {request.method} {request.path} recebida",
            extra={'correlation_id': correlation_id}
        )
    
    @app.after_request
    def after_request(response):
        """Executado após cada requisição"""
        correlation_id = g.get('correlation_id', 'no-correlation-id')
        
        # Log de saída
        app.logger.info(
            f"Resposta {response.status_code} para {request.method} {request.path}",
            extra={'correlation_id': correlation_id}
        )
        
        # Adicionar correlation_id no header da resposta
        response.headers['X-Correlation-ID'] = correlation_id
        
        return response
```

### Tarefa 2.5: Implementar Rotas - Parte 1 (Time e Cientistas)
**Tempo estimado: 3 horas**

#### Arquivo: app/routes/__init__.py
```python
from flask import Blueprint

time_bp = Blueprint('time', __name__)
cientistas_bp = Blueprint('cientistas', __name__)
agendamentos_bp = Blueprint('agendamentos', __name__)

from app.routes import time_routes, cientista_routes, agendamento_routes
```

#### Arquivo: app/routes/time_routes.py
```python
from flask import jsonify, url_for
from datetime import datetime
from app.routes import time_bp
import logging

logger = logging.getLogger(__name__)

@time_bp.route('/time', methods=['GET'])
def get_time():
    """
    GET /api/v1/time
    Retorna o timestamp oficial do servidor para sincronização
    """
    logger.info("Endpoint /time acessado")
    
    agora = datetime.utcnow()
    
    response = {
        'timestamp_utc': agora.isoformat() + 'Z',
        'timezone': 'UTC',
        'epoch_ms': int(agora.timestamp() * 1000),
        '_links': {
            'self': {'href': url_for('time.get_time', _external=True)},
            'agendamentos': {'href': url_for('agendamentos.list_agendamentos', _external=True)},
            'cientistas': {'href': url_for('cientistas.list_cientistas', _external=True)}
        }
    }
    
    logger.info(f"Timestamp retornado: {response['timestamp_utc']}")
    
    return jsonify(response), 200
```

#### Arquivo: app/routes/cientista_routes.py
```python
from flask import jsonify, request, url_for
from app.routes import cientistas_bp
from app.models.cientista import Cientista
from app import db
from app.utils.logger import log_audit
import logging

logger = logging.getLogger(__name__)

@cientistas_bp.route('/cientistas', methods=['GET'])
def list_cientistas():
    """
    GET /api/v1/cientistas
    Lista todos os cientistas com paginação
    """
    logger.info("Listando cientistas")
    
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)  # Máximo 100 por página
    
    # Filtro opcional por status
    ativo = request.args.get('ativo', type=lambda v: v.lower() == 'true')
    
    # Query base
    query = Cientista.query
    
    if ativo is not None:
        query = query.filter_by(ativo=ativo)
    
    # Paginar
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    cientistas = [c.to_dict() for c in pagination.items]
    
    response = {
        'cientistas': cientistas,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages
        },
        '_links': {
            'self': {'href': url_for('cientistas.list_cientistas', page=page, per_page=per_page, _external=True)}
        }
    }
    
    # Links de navegação
    if pagination.has_prev:
        response['_links']['prev'] = {
            'href': url_for('cientistas.list_cientistas', page=page-1, per_page=per_page, _external=True)
        }
    
    if pagination.has_next:
        response['_links']['next'] = {
            'href': url_for('cientistas.list_cientistas', page=page+1, per_page=per_page, _external=True)
        }
    
    response['_links']['first'] = {
        'href': url_for('cientistas.list_cientistas', page=1, per_page=per_page, _external=True)
    }
    response['_links']['last'] = {
        'href': url_for('cientistas.list_cientistas', page=pagination.pages, per_page=per_page, _external=True)
    }
    
    logger.info(f"Retornando {len(cientistas)} cientistas (página {page}/{pagination.pages})")
    
    return jsonify(response), 200

@cientistas_bp.route('/cientistas', methods=['POST'])
def create_cientista():
    """
    POST /api/v1/cientistas
    Cria um novo cientista
    """
    logger.info("Criando novo cientista")
    
    data = request.get_json()
    
    # Validar dados
    errors = Cientista.validate_data(data)
    if errors:
        logger.warning(f"Dados inválidos: {errors}")
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Verificar email duplicado
    if Cientista.query.filter_by(email=data['email']).first():
        logger.warning(f"Email já cadastrado: {data['email']}")
        return jsonify({'error': 'Email já cadastrado'}), 409
    
    # Criar cientista
    cientista = Cientista(
        nome=data['nome'].strip(),
        email=data['email'].strip().lower(),
        instituicao=data['instituicao'].strip(),
        pais=data['pais'].strip(),
        especialidade=data.get('especialidade', '').strip() or None
    )
    
    db.session.add(cientista)
    db.session.commit()
    
    logger.info(f"Cientista criado com ID {cientista.id}")
    
    # Log de auditoria
    log_audit('CIENTISTA_CRIADO', {
        'cientista_id': cientista.id,
        'nome': cientista.nome,
        'email': cientista.email,
        'instituicao': cientista.instituicao
    })
    
    return jsonify(cientista.to_dict()), 201

@cientistas_bp.route('/cientistas/<int:id>', methods=['GET'])
def get_cientista(id):
    """
    GET /api/v1/cientistas/{id}
    Obtém detalhes de um cientista
    """
    logger.info(f"Buscando cientista ID {id}")
    
    cientista = Cientista.query.get(id)
    
    if not cientista:
        logger.warning(f"Cientista ID {id} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    return jsonify(cientista.to_dict()), 200

@cientistas_bp.route('/cientistas/<int:id>/agendamentos', methods=['GET'])
def get_cientista_agendamentos(id):
    """
    GET /api/v1/cientistas/{id}/agendamentos
    Lista agendamentos de um cientista
    """
    logger.info(f"Listando agendamentos do cientista ID {id}")
    
    cientista = Cientista.query.get(id)
    
    if not cientista:
        logger.warning(f"Cientista ID {id} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    # Filtro opcional por status
    status = request.args.get('status')
    
    query = cientista.agendamentos
    if status:
        query = query.filter_by(status=status)
    
    agendamentos = [a.to_dict() for a in query.all()]
    
    response = {
        'cientista_id': id,
        'cientista_nome': cientista.nome,
        'agendamentos': agendamentos,
        'total': len(agendamentos),
        '_links': {
            'self': {'href': url_for('cientistas.get_cientista_agendamentos', id=id, _external=True)},
            'cientista': {'href': url_for('cientistas.get_cientista', id=id, _external=True)}
        }
    }
    
    return jsonify(response), 200
```

### Tarefa 2.6: Implementar Rotas - Parte 2 (Agendamentos SEM lock)
**Tempo estimado: 4 horas**

#### Arquivo: app/routes/agendamento_routes.py
```python
from flask import jsonify, request, url_for, current_app
from app.routes import agendamentos_bp
from app.models.agendamento import Agendamento
from app.models.cientista import Cientista
from app import db
from app.utils.logger import log_audit
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@agendamentos_bp.route('/agendamentos', methods=['GET'])
def list_agendamentos():
    """
    GET /api/v1/agendamentos
    Lista agendamentos com filtros e paginação
    """
    logger.info("Listando agendamentos")
    
    # Parâmetros
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    per_page = min(per_page, 100)
    
    # Filtros
    cientista_id = request.args.get('cientista_id', type=int)
    status = request.args.get('status')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Query base
    query = Agendamento.query
    
    if cientista_id:
        query = query.filter_by(cientista_id=cientista_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if data_inicio:
        try:
            dt_inicio = datetime.fromisoformat(data_inicio.replace('Z', '+00:00'))
            query = query.filter(Agendamento.horario_inicio_utc >= dt_inicio)
        except ValueError:
            return jsonify({'error': 'data_inicio inválida'}), 400
    
    if data_fim:
        try:
            dt_fim = datetime.fromisoformat(data_fim.replace('Z', '+00:00'))
            query = query.filter(Agendamento.horario_fim_utc <= dt_fim)
        except ValueError:
            return jsonify({'error': 'data_fim inválida'}), 400
    
    # Ordenar por data
    query = query.order_by(Agendamento.horario_inicio_utc.asc())
    
    # Paginar
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    agendamentos = [a.to_dict() for a in pagination.items]
    
    response = {
        'agendamentos': agendamentos,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': pagination.total,
            'total_pages': pagination.pages
        },
        '_links': {
            'self': {'href': url_for('agendamentos.list_agendamentos', page=page, _external=True)}
        }
    }
    
    return jsonify(response), 200

@agendamentos_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    """
    POST /api/v1/agendamentos
    Cria um novo agendamento (SEM LOCK - Entrega 2)
    """
    logger.info("Criando novo agendamento")
    
    data = request.get_json()
    
    # Validar dados
    config = {
        'DURACAO_MINIMA_MINUTOS': current_app.config['DURACAO_MINIMA_MINUTOS'],
        'DURACAO_MAXIMA_MINUTOS': current_app.config['DURACAO_MAXIMA_MINUTOS'],
        'ANTECEDENCIA_MINIMA_HORAS': current_app.config['ANTECEDENCIA_MINIMA_HORAS']
    }
    
    errors = Agendamento.validate_data(data, config)
    if errors:
        logger.warning(f"Dados inválidos: {errors}")
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Verificar se cientista existe e está ativo
    cientista = Cientista.query.get(data['cientista_id'])
    if not cientista:
        logger.warning(f"Cientista ID {data['cientista_id']} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    if not cientista.ativo:
        logger.warning(f"Cientista ID {data['cientista_id']} está inativo")
        return jsonify({'error': 'Cientista inativo não pode agendar'}), 422
    
    # Converter datas
    inicio = datetime.fromisoformat(data['horario_inicio_utc'].replace('Z', '+00:00'))
    fim = datetime.fromisoformat(data['horario_fim_utc'].replace('Z', '+00:00'))
    
    # IMPORTANTE: Aqui NÃO há lock ainda (Entrega 2)
    # Apenas verificamos conflitos no banco
    logger.info("Iniciando verificação de conflito no BD")
    
    conflitos = Agendamento.check_conflicts(inicio, fim)
    
    if conflitos:
        logger.warning(f"Conflito de horário detectado com agendamento(s): {[c.id for c in conflitos]}")
        return jsonify({
            'error': 'Conflito de horário',
            'conflitos': [c.to_dict(include_links=False) for c in conflitos]
        }), 409
    
    # Verificar limite de agendamentos ativos do cientista
    agendamentos_ativos = Agendamento.query.filter_by(
        cientista_id=cientista.id,
        status='AGENDADO'
    ).count()
    
    if agendamentos_ativos >= current_app.config['MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA']:
        logger.warning(f"Cientista {cientista.id} atingiu limite de agendamentos ativos")
        return jsonify({
            'error': f'Limite de {current_app.config["MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA"]} agendamentos ativos atingido'
        }), 422
    
    # Criar agendamento
    logger.info("Salvando novo agendamento no BD")
    
    agendamento = Agendamento(
        cientista_id=cientista.id,
        horario_inicio_utc=inicio,
        horario_fim_utc=fim,
        objeto_celeste=data['objeto_celeste'].strip(),
        observacoes=data.get('observacoes', '').strip() or None
    )
    
    db.session.add(agendamento)
    db.session.commit()
    
    logger.info(f"Agendamento criado com ID {agendamento.id}")
    
    # Log de auditoria
    log_audit('AGENDAMENTO_CRIADO', {
        'agendamento_id': agendamento.id,
        'cientista_id': cientista.id,
        'cientista_nome': cientista.nome,
        'horario_inicio_utc': agendamento.horario_inicio_utc.isoformat() + 'Z',
        'horario_fim_utc': agendamento.horario_fim_utc.isoformat() + 'Z',
        'objeto_celeste': agendamento.objeto_celeste
    })
    
    return jsonify(agendamento.to_dict()), 201

@agendamentos_bp.route('/agendamentos/<int:id>', methods=['GET'])
def get_agendamento(id):
    """
    GET /api/v1/agendamentos/{id}
    Obtém detalhes de um agendamento
    """
    logger.info(f"Buscando agendamento ID {id}")
    
    agendamento = Agendamento.query.get(id)
    
    if not agendamento:
        logger.warning(f"Agendamento ID {id} não encontrado")
        return jsonify({'error': 'Agendamento não encontrado'}), 404
    
    return jsonify(agendamento.to_dict()), 200

@agendamentos_bp.route('/agendamentos/<int:id>', methods=['DELETE'])
def cancel_agendamento(id):
    """
    DELETE /api/v1/agendamentos/{id}
    Cancela um agendamento
    """
    logger.info(f"Cancelando agendamento ID {id}")
    
    agendamento = Agendamento.query.get(id)
    
    if not agendamento:
        logger.warning(f"Agendamento ID {id} não encontrado")
        return jsonify({'error': 'Agendamento não encontrado'}), 404
    
    if agendamento.status != 'AGENDADO':
        logger.warning(f"Agendamento ID {id} não pode ser cancelado (status: {agendamento.status})")
        return jsonify({'error': f'Agendamento com status {agendamento.status} não pode ser cancelado'}), 422
    
    # Obter motivo do cancelamento (opcional)
    data = request.get_json() or {}
    motivo = data.get('motivo', 'Cancelado pelo usuário')
    
    # Atualizar agendamento
    agendamento.status = 'CANCELADO'
    agendamento.data_cancelamento = datetime.utcnow()
    agendamento.motivo_cancelamento = motivo
    
    db.session.commit()
    
    logger.info(f"Agendamento ID {id} cancelado")
    
    # Log de auditoria
    log_audit('AGENDAMENTO_CANCELADO', {
        'agendamento_id': agendamento.id,
        'cientista_id': agendamento.cientista_id,
        'cientista_nome': agendamento.cientista.nome,
        'horario_inicio_utc': agendamento.horario_inicio_utc.isoformat() + 'Z',
        'motivo': motivo
    })
    
    return jsonify(agendamento.to_dict()), 200
```

### Tarefa 2.7: Arquivo Principal de Execução
**Tempo estimado: 30 minutos**

#### Arquivo: run.py
```python
from app import create_app, db
from app.utils.logger import setup_audit_logger
from app.utils.middleware import setup_request_middleware
import os

# Criar aplicação
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Configurar logger de auditoria
setup_audit_logger()

# Configurar middleware
setup_request_middleware(app)

# Adicionar filtro de correlation_id aos loggers
from app.utils.logger import CorrelationIdFilter
for handler in app.logger.handlers:
    handler.addFilter(CorrelationIdFilter())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Tarefa 2.8: Script de Teste de Estresse
**Tempo estimado: 2 horas**

#### Arquivo: tests/test_concorrencia.py
```python
"""
Script para testar condição de corrida
Dispara múltiplas requisições simultâneas para o mesmo horário
"""

import requests
import threading
from datetime import datetime, timedelta
import json

BASE_URL = 'http://localhost:5000/api/v1'

def criar_cientista_teste():
    """Cria um cientista para teste"""
    data = {
        'nome': 'Alan Turing',
        'email': f'alan.turing.teste.{datetime.now().timestamp()}@test.com',
        'instituicao': 'University of Manchester',
        'pais': 'Reino Unido',
        'especialidade': 'Computação Quântica'
    }
    
    response = requests.post(f'{BASE_URL}/cientistas', json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"Erro ao criar cientista: {response.text}")
        return None

def tentar_agendamento(cientista_id, horario_inicio, horario_fim, thread_id):
    """Tenta criar um agendamento"""
    data = {
        'cientista_id': cientista_id,
        'horario_inicio_utc': horario_inicio,
        'horario_fim_utc': horario_fim,
        'objeto_celeste': f'Teste Concorrência Thread {thread_id}',
        'observacoes': f'Requisição da thread {thread_id}'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/agendamentos', json=data)
        print(f"[Thread {thread_id:02d}] Status: {response.status_code} - {response.json().get('error', 'Sucesso')}")
        return response.status_code, response.json()
    except Exception as e:
        print(f"[Thread {thread_id:02d}] Erro: {str(e)}")
        return None, None

def teste_concorrencia(num_threads=10):
    """
    Executa teste de concorrência
    """
    print("="*80)
    print("TESTE DE CONDIÇÃO DE CORRIDA - ENTREGA 2 (SEM LOCK)")
    print("="*80)
    print(f"\nConfigurando teste com {num_threads} threads simultâneas...\n")
    
    # Criar cientista
    print("1. Criando cientista de teste...")
    cientista_id = criar_cientista_teste()
    if not cientista_id:
        print("Falha ao criar cientista. Abortando teste.")
        return
    print(f"   Cientista criado: ID {cientista_id}\n")
    
    # Definir horário no futuro (25 horas a partir de agora)
    agora = datetime.utcnow()
    inicio = agora + timedelta(hours=25)
    # Arredondar para múltiplo de 5 minutos
    inicio = inicio.replace(minute=(inicio.minute // 5) * 5, second=0, microsecond=0)
    fim = inicio + timedelta(minutes=30)
    
    horario_inicio_str = inicio.isoformat() + 'Z'
    horario_fim_str = fim.isoformat() + 'Z'
    
    print(f"2. Horário alvo: {horario_inicio_str} - {horario_fim_str}\n")
    print(f"3. Disparando {num_threads} requisições simultâneas...\n")
    
    # Criar threads
    threads = []
    resultados = []
    
    for i in range(num_threads):
        def wrapper(tid=i):
            status, response = tentar_agendamento(
                cientista_id, 
                horario_inicio_str, 
                horario_fim_str, 
                tid
            )
            resultados.append((tid, status, response))
        
        thread = threading.Thread(target=wrapper)
        threads.append(thread)
    
    # Disparar todas ao mesmo tempo
    for thread in threads:
        thread.start()
    
    # Aguardar conclusão
    for thread in threads:
        thread.join()
    
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80 + "\n")
    
    # Analisar resultados
    sucessos = [r for r in resultados if r[1] == 201]
    conflitos = [r for r in resultados if r[1] == 409]
    erros = [r for r in resultados if r[1] not in [201, 409]]
    
    print(f"✓ Sucessos (201):  {len(sucessos)}")
    print(f"✗ Conflitos (409): {len(conflitos)}")
    print(f"⚠ Outros erros:    {len(erros)}")
    
    if len(sucessos) > 1:
        print(f"\n🚨 CONDIÇÃO DE CORRIDA DETECTADA! {len(sucessos)} agendamentos criados para o mesmo horário!")
        print("\nIDs dos agendamentos duplicados:")
        for tid, status, response in sucessos:
            if response and 'id' in response:
                print(f"   - Thread {tid:02d}: Agendamento ID {response['id']}")
    elif len(sucessos) == 1:
        print("\n✓ Apenas 1 agendamento criado (comportamento esperado COM lock)")
    else:
        print("\n⚠ Nenhum agendamento criado (investigar)")
    
    print("\n" + "="*80)
    print("VERIFICAÇÃO NO BANCO DE DADOS")
    print("="*80 + "\n")
    
    # Consultar agendamentos criados
    response = requests.get(
        f'{BASE_URL}/agendamentos',
        params={
            'cientista_id': cientista_id,
            'status': 'AGENDADO'
        }
    )
    
    if response.status_code == 200:
        agendamentos = response.json()['agendamentos']
        print(f"Agendamentos encontrados no banco: {len(agendamentos)}")
        
        # Agrupar por horário
        horarios = {}
        for ag in agendamentos:
            key = (ag['horario_inicio_utc'], ag['horario_fim_utc'])
            if key not in horarios:
                horarios[key] = []
            horarios[key].append(ag['id'])
        
        print("\nAgendamentos por horário:")
        for (inicio, fim), ids in horarios.items():
            print(f"   {inicio} - {fim}: {len(ids)} agendamento(s) - IDs: {ids}")
            if len(ids) > 1:
                print(f"      🚨 CONFLITO DETECTADO!")
    
    print("\n" + "="*80)
    print("ANÁLISE DOS LOGS")
    print("="*80)
    print("\nPara analisar os logs:")
    print("   1. Examine 'logs/app.log' para ver os logs entrelaçados")
    print("   2. Examine 'logs/audit.log' para ver os eventos de auditoria")
    print("   3. Procure por múltiplos eventos 'AGENDAMENTO_CRIADO' para o mesmo horário")
    print("\nComandos úteis:")
    print("   cat logs/app.log | grep 'Iniciando verificação de conflito'")
    print("   cat logs/audit.log | jq '.event_type'")
    print("="*80 + "\n")

if __name__ == '__main__':
    import sys
    
    num_threads = 10
    if len(sys.argv) > 1:
        try:
            num_threads = int(sys.argv[1])
        except ValueError:
            print("Uso: python test_concorrencia.py [num_threads]")
            sys.exit(1)
    
    teste_concorrencia(num_threads)
```

### Tarefa 2.9: Validação da Entrega 2
**Tempo estimado: 2 horas**

#### Checklist de validação:

1. **Testar servidor**
   ```bash
   cd servico-agendamento
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   python run.py
   ```
   - Verificar se inicia sem erros
   - Acesse http://localhost:5000/api/v1/time
   - Deve retornar timestamp

2. **Testar criação de cientista via Postman**
   - POST http://localhost:5000/api/v1/cientistas
   - Body JSON com dados válidos
   - Verificar retorno 201
   - Verificar links HATEOAS

3. **Testar agendamento individual**
   - POST http://localhost:5000/api/v1/agendamentos
   - Verificar retorno 201
   - Verificar log em logs/app.log
   - Verificar log de auditoria em logs/audit.log

4. **Executar teste de concorrência**
   ```bash
   python tests/test_concorrencia.py 10
   ```
   - Deve mostrar múltiplos sucessos (PROBLEMA!)
   - Verificar logs entrelaçados
   - Consultar banco: `sqlite3 instance/telescopio.db "SELECT * FROM agendamentos;"`

5. **Documentar resultados**
   - Capturar screenshots dos logs
   - Capturar saída do teste
   - Documentar quantos agendamentos duplicados foram criados
   - Criar arquivo ENTREGA2_RESULTADOS.md

6. **Commit**
   ```bash
   git add .
   git commit -m "Entrega 2: API funcional com condição de corrida demonstrada"
   git tag entrega-2
   ```

---

## 🔐 ENTREGA 3: SERVIÇO COORDENADOR

**Objetivo:** Implementar exclusão mútua com serviço de lock
**Tempo estimado: 12-16 horas**

### Tarefa 3.1: Setup do Serviço Coordenador
**Tempo estimado: 1 hora**

```bash
cd servico-coordenador
npm init -y
npm install express
npm install --save-dev nodemon
```

#### Arquivo: package.json (atualizar)
```json
{
  "name": "servico-coordenador",
  "version": "1.0.0",
  "description": "Serviço de coordenação e lock para o SCTEC",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "keywords": ["lock", "coordination", "distributed-systems"],
  "author": "Seu Nome",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.1"
  }
}
```

### Tarefa 3.2: Implementar Serviço de Lock
**Tempo estimado: 4-5 horas**

#### Arquivo: server.js
```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Armazenamento em memória dos locks
// Estrutura: { 'nome-do-recurso': { locked: true, timestamp: Date, holder: 'correlation-id' } }
const locks = new Map();

// Timeout para auto-liberação de locks (prevenção de deadlock)
const LOCK_TIMEOUT_MS = 30000; // 30 segundos

// Middleware de logging
app.use((req, res, next) => {
    const timestamp = new Date().toISOString();
    console.log(`[INFO] ${timestamp} ${req.method} ${req.path}`);
    next();
});

/**
 * POST /lock
 * Tenta adquirir um lock para um recurso
 */
app.post('/lock', (req, res) => {
    const { recurso, correlation_id } = req.body;
    
    if (!recurso) {
        console.log(`[WARNING] Requisição de lock sem recurso especificado`);
        return res.status(400).json({ 
            error: 'Campo "recurso" é obrigatório' 
        });
    }
    
    console.log(`[INFO] Recebido pedido de lock para recurso: ${recurso}`);
    
    // Verificar se o recurso já está travado
    if (locks.has(recurso)) {
        const lockInfo = locks.get(recurso);
        
        // Verificar timeout (auto-liberação)
        const agora = Date.now();
        const tempoDecorrido = agora - lockInfo.timestamp;
        
        if (tempoDecorrido > LOCK_TIMEOUT_MS) {
            console.log(`[WARNING] Lock para recurso ${recurso} expirou (timeout). Liberando automaticamente.`);
            locks.delete(recurso);
        } else {
            console.log(`[INFO] Recurso ${recurso} já está em uso (holder: ${lockInfo.holder}). Negando lock.`);
            return res.status(409).json({ 
                error: 'Recurso já está travado',
                recurso: recurso,
                locked_by: lockInfo.holder,
                locked_at: new Date(lockInfo.timestamp).toISOString()
            });
        }
    }
    
    // Travar o recurso
    locks.set(recurso, {
        locked: true,
        timestamp: Date.now(),
        holder: correlation_id || 'unknown'
    });
    
    console.log(`[INFO] Lock concedido para recurso: ${recurso} (holder: ${correlation_id || 'unknown'})`);
    
    res.status(200).json({
        message: 'Lock adquirido com sucesso',
        recurso: recurso,
        timestamp: new Date().toISOString()
    });
});

/**
 * POST /unlock
 * Libera um lock de um recurso
 */
app.post('/unlock', (req, res) => {
    const { recurso, correlation_id } = req.body;
    
    if (!recurso) {
        console.log(`[WARNING] Requisição de unlock sem recurso especificado`);
        return res.status(400).json({ 
            error: 'Campo "recurso" é obrigatório' 
        });
    }
    
    console.log(`[INFO] Recebido pedido de unlock para recurso: ${recurso}`);
    
    // Verificar se o recurso está travado
    if (!locks.has(recurso)) {
        console.log(`[WARNING] Tentativa de unlock de recurso não travado: ${recurso}`);
        return res.status(404).json({ 
            error: 'Recurso não está travado',
            recurso: recurso
        });
    }
    
    // Opcional: verificar se quem está liberando é quem travou
    const lockInfo = locks.get(recurso);
    if (correlation_id && lockInfo.holder !== correlation_id) {
        console.log(`[WARNING] Tentativa de unlock por holder diferente. Original: ${lockInfo.holder}, Requisição: ${correlation_id}`);
        // Pode escolher liberar mesmo assim ou negar
    }
    
    // Liberar o lock
    locks.delete(recurso);
    
    console.log(`[INFO] Lock liberado para recurso: ${recurso}`);
    
    res.status(200).json({
        message: 'Lock liberado com sucesso',
        recurso: recurso,
        timestamp: new Date().toISOString()
    });
});

/**
 * GET /locks
 * Lista todos os locks ativos (útil para debugging)
 */
app.get('/locks', (req, res) => {
    console.log(`[INFO] Consultando locks ativos`);
    
    const locksAtivos = [];
    const agora = Date.now();
    
    for (const [recurso, lockInfo] of locks.entries()) {
        const tempoDecorrido = agora - lockInfo.timestamp;
        
        locksAtivos.push({
            recurso: recurso,
            holder: lockInfo.holder,
            locked_at: new Date(lockInfo.timestamp).toISOString(),
            tempo_decorrido_ms: tempoDecorrido,
            expira_em_ms: Math.max(0, LOCK_TIMEOUT_MS - tempoDecorrido)
        });
    }
    
    res.status(200).json({
        total_locks: locksAtivos.length,
        locks: locksAtivos,
        timestamp: new Date().toISOString()
    });
});

/**
 * GET /health
 * Health check
 */
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        service: 'servico-coordenador',
        timestamp: new Date().toISOString(),
        locks_ativos: locks.size
    });
});

// Rota não encontrada
app.use((req, res) => {
    res.status(404).json({ error: 'Rota não encontrada' });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(`[ERROR] ${err.stack}`);
    res.status(500).json({ error: 'Erro interno do servidor' });
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`==================================================`);
    console.log(`   Serviço Coordenador - SCTEC`);
    console.log(`   Porta: ${PORT}`);
    console.log(`   Ambiente: ${process.env.NODE_ENV || 'development'}`);
    console.log(`   Lock Timeout: ${LOCK_TIMEOUT_MS}ms`);
    console.log(`==================================================`);
});

// Limpeza periódica de locks expirados
setInterval(() => {
    const agora = Date.now();
    let removidos = 0;
    
    for (const [recurso, lockInfo] of locks.entries()) {
        const tempoDecorrido = agora - lockInfo.timestamp;
        
        if (tempoDecorrido > LOCK_TIMEOUT_MS) {
            console.log(`[CLEANUP] Removendo lock expirado: ${recurso}`);
            locks.delete(recurso);
            removidos++;
        }
    }
    
    if (removidos > 0) {
        console.log(`[CLEANUP] ${removidos} lock(s) expirado(s) removido(s)`);
    }
}, 60000); // A cada 1 minuto
```

### Tarefa 3.3: Modificar Serviço de Agendamento para Usar Lock
**Tempo estimado: 3-4 horas**

#### Arquivo: app/utils/coordenador_client.py
```python
"""
Cliente para comunicação com o Serviço Coordenador
"""

import requests
from flask import current_app
import logging
from app.utils.logger import get_correlation_id

logger = logging.getLogger(__name__)

class CoordenadorClient:
    """Cliente para o serviço de coordenação"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or current_app.config.get('COORDENADOR_URL', 'http://localhost:3000')
        self.timeout = 5  # segundos
    
    def acquire_lock(self, recurso):
        """
        Tenta adquirir um lock para um recurso
        
        Args:
            recurso: Identificador único do recurso
            
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        correlation_id = get_correlation_id()
        
        logger.info(f"Tentando adquirir lock para o recurso: {recurso}")
        
        try:
            response = requests.post(
                f'{self.base_url}/lock',
                json={
                    'recurso': recurso,
                    'correlation_id': correlation_id
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Lock adquirido com sucesso para o recurso: {recurso}")
                return True, "Lock adquirido"
            elif response.status_code == 409:
                logger.info(f"Falha ao adquirir lock para o recurso: {recurso} (recurso ocupado)")
                data = response.json()
                return False, data.get('error', 'Recurso já está travado')
            else:
                logger.error(f"Erro inesperado ao tentar adquirir lock: {response.status_code}")
                return False, f"Erro ao adquirir lock: {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao tentar adquirir lock para o recurso: {recurso}")
            return False, "Timeout ao comunicar com serviço de coordenação"
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao tentar adquirir lock: {str(e)}")
            return False, f"Erro de comunicação: {str(e)}"
    
    def release_lock(self, recurso):
        """
        Libera um lock de um recurso
        
        Args:
            recurso: Identificador único do recurso
            
        Returns:
            tuple: (sucesso: bool, mensagem: str)
        """
        correlation_id = get_correlation_id()
        
        logger.info(f"Liberando lock para o recurso: {recurso}")
        
        try:
            response = requests.post(
                f'{self.base_url}/unlock',
                json={
                    'recurso': recurso,
                    'correlation_id': correlation_id
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                logger.info(f"Lock liberado com sucesso para o recurso: {recurso}")
                return True, "Lock liberado"
            elif response.status_code == 404:
                logger.warning(f"Tentativa de liberar lock não existente: {recurso}")
                return False, "Recurso não estava travado"
            else:
                logger.error(f"Erro inesperado ao tentar liberar lock: {response.status_code}")
                return False, f"Erro ao liberar lock: {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao tentar liberar lock para o recurso: {recurso}")
            return False, "Timeout ao comunicar com serviço de coordenação"
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de rede ao tentar liberar lock: {str(e)}")
            return False, f"Erro de comunicação: {str(e)}"
    
    def check_health(self):
        """
        Verifica se o serviço coordenador está disponível
        
        Returns:
            bool: True se o serviço está saudável
        """
        try:
            response = requests.get(f'{self.base_url}/health', timeout=2)
            return response.status_code == 200
        except:
            return False

def gerar_nome_recurso_agendamento(horario_inicio, horario_fim):
    """
    Gera um nome único para o recurso de agendamento
    
    Args:
        horario_inicio: datetime
        horario_fim: datetime
        
    Returns:
        str: Nome do recurso (ex: "Hubble-Acad_2025-12-01T03:00:00Z")
    """
    # Usar apenas o início para identificar o slot
    # Formato: "Hubble-Acad_YYYY-MM-DDTHH:MM:SSZ"
    nome_telescopio = current_app.config.get('NOME_TELESCOPIO', 'Hubble-Acad')
    timestamp = horario_inicio.strftime('%Y-%m-%dT%H:%M:%SZ')
    return f"{nome_telescopio}_{timestamp}"
```

#### Modificar: app/routes/agendamento_routes.py (apenas a função create_agendamento)
```python
# ... (imports existentes)
from app.utils.coordenador_client import CoordenadorClient, gerar_nome_recurso_agendamento

@agendamentos_bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    """
    POST /api/v1/agendamentos
    Cria um novo agendamento COM LOCK (Entrega 3)
    """
    logger.info("Criando novo agendamento")
    
    data = request.get_json()
    
    # Validar dados
    config = {
        'DURACAO_MINIMA_MINUTOS': current_app.config['DURACAO_MINIMA_MINUTOS'],
        'DURACAO_MAXIMA_MINUTOS': current_app.config['DURACAO_MAXIMA_MINUTOS'],
        'ANTECEDENCIA_MINIMA_HORAS': current_app.config['ANTECEDENCIA_MINIMA_HORAS']
    }
    
    errors = Agendamento.validate_data(data, config)
    if errors:
        logger.warning(f"Dados inválidos: {errors}")
        return jsonify({'error': 'Dados inválidos', 'details': errors}), 400
    
    # Verificar se cientista existe e está ativo
    cientista = Cientista.query.get(data['cientista_id'])
    if not cientista:
        logger.warning(f"Cientista ID {data['cientista_id']} não encontrado")
        return jsonify({'error': 'Cientista não encontrado'}), 404
    
    if not cientista.ativo:
        logger.warning(f"Cientista ID {data['cientista_id']} está inativo")
        return jsonify({'error': 'Cientista inativo não pode agendar'}), 422
    
    # Converter datas
    inicio = datetime.fromisoformat(data['horario_inicio_utc'].replace('Z', '+00:00'))
    fim = datetime.fromisoformat(data['horario_fim_utc'].replace('Z', '+00:00'))
    
    # NOVO: Gerar nome do recurso e adquirir lock
    nome_recurso = gerar_nome_recurso_agendamento(inicio, fim)
    logger.info(f"Tentando adquirir lock para o recurso: {nome_recurso}")
    
    coordenador = CoordenadorClient()
    lock_adquirido, mensagem = coordenador.acquire_lock(nome_recurso)
    
    if not lock_adquirido:
        logger.warning(f"Falha ao adquirir lock: {mensagem}")
        log_audit('AGENDAMENTO_CONFLITO', {
            'cientista_id': cientista.id,
            'horario_inicio_utc': inicio.isoformat() + 'Z',
            'motivo': 'Lock não disponível'
        })
        return jsonify({
            'error': 'Recurso temporariamente indisponível',
            'detalhes': mensagem
        }), 409
    
    logger.info(f"Lock adquirido com sucesso para o recurso: {nome_recurso}")
    
    # IMPORTANTE: Usar try-finally para garantir que o lock seja liberado
    try:
        # Verificar conflitos no banco
        logger.info("Iniciando verificação de conflito no BD")
        
        conflitos = Agendamento.check_conflicts(inicio, fim)
        
        if conflitos:
            logger.warning(f"Conflito de horário detectado com agendamento(s): {[c.id for c in conflitos]}")
            log_audit('AGENDAMENTO_CONFLITO', {
                'cientista_id': cientista.id,
                'horario_inicio_utc': inicio.isoformat() + 'Z',
                'conflitos_com': [c.id for c in conflitos]
            })
            return jsonify({
                'error': 'Conflito de horário',
                'conflitos': [c.to_dict(include_links=False) for c in conflitos]
            }), 409
        
        # Verificar limite de agendamentos ativos do cientista
        agendamentos_ativos = Agendamento.query.filter_by(
            cientista_id=cientista.id,
            status='AGENDADO'
        ).count()
        
        if agendamentos_ativos >= current_app.config['MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA']:
            logger.warning(f"Cientista {cientista.id} atingiu limite de agendamentos ativos")
            return jsonify({
                'error': f'Limite de {current_app.config["MAX_AGENDAMENTOS_ATIVOS_POR_CIENTISTA"]} agendamentos ativos atingido'
            }), 422
        
        # Criar agendamento
        logger.info("Salvando novo agendamento no BD")
        
        agendamento = Agendamento(
            cientista_id=cientista.id,
            horario_inicio_utc=inicio,
            horario_fim_utc=fim,
            objeto_celeste=data['objeto_celeste'].strip(),
            observacoes=data.get('observacoes', '').strip() or None
        )
        
        db.session.add(agendamento)
        db.session.commit()
        
        logger.info(f"Agendamento criado com ID {agendamento.id}")
        
        # Log de auditoria
        log_audit('AGENDAMENTO_CRIADO', {
            'agendamento_id': agendamento.id,
            'cientista_id': cientista.id,
            'cientista_nome': cientista.nome,
            'horario_inicio_utc': agendamento.horario_inicio_utc.isoformat() + 'Z',
            'horario_fim_utc': agendamento.horario_fim_utc.isoformat() + 'Z',
            'objeto_celeste': agendamento.objeto_celeste
        })
        
        return jsonify(agendamento.to_dict()), 201
        
    finally:
        # SEMPRE liberar o lock, sucesso ou erro
        logger.info(f"Liberando lock para o recurso: {nome_recurso}")
        coordenador.release_lock(nome_recurso)
```

#### Adicionar no config.py
```python
class Config:
    # ... (configurações existentes)
    NOME_TELESCOPIO = 'Hubble-Acad'
```

### Tarefa 3.4: Testar Integração
**Tempo estimado: 2 horas**

#### Arquivo: tests/test_com_lock.py
```python
"""
Script para testar o sistema COM lock
Deve demonstrar que apenas 1 agendamento é criado
"""

import requests
import threading
from datetime import datetime, timedelta
import json
import time

BASE_URL = 'http://localhost:5000/api/v1'
COORDENADOR_URL = 'http://localhost:3000'

def verificar_servicos():
    """Verifica se ambos os serviços estão rodando"""
    print("Verificando serviços...")
    
    try:
        resp1 = requests.get(f'{BASE_URL}/time', timeout=2)
        print("✓ Serviço de Agendamento: OK")
    except:
        print("✗ Serviço de Agendamento: OFFLINE")
        return False
    
    try:
        resp2 = requests.get(f'{COORDENADOR_URL}/health', timeout=2)
        print("✓ Serviço Coordenador: OK")
    except:
        print("✗ Serviço Coordenador: OFFLINE")
        return False
    
    return True

def criar_cientista_teste():
    """Cria um cientista para teste"""
    data = {
        'nome': 'Grace Hopper',
        'email': f'grace.hopper.teste.{datetime.now().timestamp()}@test.com',
        'instituicao': 'Yale University',
        'pais': 'Estados Unidos',
        'especialidade': 'Astrofísica Computacional'
    }
    
    response = requests.post(f'{BASE_URL}/cientistas', json=data)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print(f"Erro ao criar cientista: {response.text}")
        return None

def tentar_agendamento(cientista_id, horario_inicio, horario_fim, thread_id):
    """Tenta criar um agendamento"""
    data = {
        'cientista_id': cientista_id,
        'horario_inicio_utc': horario_inicio,
        'horario_fim_utc': horario_fim,
        'objeto_celeste': f'Teste Lock Thread {thread_id}',
        'observacoes': f'Requisição da thread {thread_id}'
    }
    
    try:
        inicio = time.time()
        response = requests.post(f'{BASE_URL}/agendamentos', json=data)
        duracao = time.time() - inicio
        
        status_emoji = "✓" if response.status_code == 201 else "✗"
        print(f"{status_emoji} [Thread {thread_id:02d}] Status: {response.status_code} - Tempo: {duracao:.3f}s")
        
        if response.status_code != 201:
            erro = response.json().get('error', 'Desconhecido')
            print(f"   └─ Motivo: {erro}")
        
        return response.status_code, response.json(), duracao
    except Exception as e:
        print(f"✗ [Thread {thread_id:02d}] Erro: {str(e)}")
        return None, None, 0

def teste_com_lock(num_threads=10):
    """
    Executa teste de concorrência COM LOCK
    """
    print("="*80)
    print("TESTE COM LOCK - ENTREGA 3")
    print("="*80)
    print()
    
    # Verificar serviços
    if not verificar_servicos():
        print("\n⚠ Um ou mais serviços estão offline. Abortando teste.")
        print("\nCertifique-se de que estão rodando:")
        print("   Terminal 1: cd servico-agendamento && python run.py")
        print("   Terminal 2: cd servico-coordenador && npm run dev")
        return
    
    print(f"\nConfigurando teste com {num_threads} threads simultâneas...\n")
    
    # Criar cientista
    print("1. Criando cientista de teste...")
    cientista_id = criar_cientista_teste()
    if not cientista_id:
        print("Falha ao criar cientista. Abortando teste.")
        return
    print(f"   Cientista criado: ID {cientista_id}\n")
    
    # Definir horário
    agora = datetime.utcnow()
    inicio = agora + timedelta(hours=25)
    inicio = inicio.replace(minute=(inicio.minute // 5) * 5, second=0, microsecond=0)
    fim = inicio + timedelta(minutes=30)
    
    horario_inicio_str = inicio.isoformat() + 'Z'
    horario_fim_str = fim.isoformat() + 'Z'
    
    print(f"2. Horário alvo: {horario_inicio_str} - {horario_fim_str}\n")
    print(f"3. Disparando {num_threads} requisições simultâneas...\n")
    print("-" * 80)
    
    # Criar threads
    threads = []
    resultados = []
    
    for i in range(num_threads):
        def wrapper(tid=i):
            status, response, duracao = tentar_agendamento(
                cientista_id, 
                horario_inicio_str, 
                horario_fim_str, 
                tid
            )
            resultados.append((tid, status, response, duracao))
        
        thread = threading.Thread(target=wrapper)
        threads.append(thread)
    
    # Disparar todas ao mesmo tempo
    inicio_teste = time.time()
    for thread in threads:
        thread.start()
    
    # Aguardar conclusão
    for thread in threads:
        thread.join()
    
    duracao_total = time.time() - inicio_teste
    
    print("-" * 80)
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80 + "\n")
    
    # Analisar resultados
    sucessos = [r for r in resultados if r[1] == 201]
    conflitos_409 = [r for r in resultados if r[1] == 409]
    outros_erros = [r for r in resultados if r[1] not in [201, 409] and r[1] is not None]
    falhas_rede = [r for r in resultados if r[1] is None]
    
    print(f"✓ Sucessos (201):         {len(sucessos)}")
    print(f"✗ Recursos ocupados (409): {len(conflitos_409)}")
    print(f"⚠ Outros erros:           {len(outros_erros)}")
    print(f"⚠ Falhas de rede:         {len(falhas_rede)}")
    print(f"\n⏱ Tempo total: {duracao_total:.3f}s")
    
    if resultados:
        tempos = [r[3] for r in resultados if r[3] > 0]
        if tempos:
            print(f"⏱ Tempo médio por requisição: {sum(tempos)/len(tempos):.3f}s")
            print(f"⏱ Tempo mínimo: {min(tempos):.3f}s")
            print(f"⏱ Tempo máximo: {max(tempos):.3f}s")
    
    print("\n" + "-"*80)
    
    if len(sucessos) == 1:
        print("\n🎉 SUCESSO! Apenas 1 agendamento criado (exclusão mútua funcionando!)")
        tid, status, response, duracao = sucessos[0]
        print(f"\nAgendamento vencedor:")
        print(f"   Thread: {tid}")
        print(f"   ID: {response['id']}")
        print(f"   Tempo: {duracao:.3f}s")
    elif len(sucessos) > 1:
        print(f"\n🚨 FALHA! {len(sucessos)} agendamentos criados (lock não está funcionando!)")
        print("\nAgendamentos duplicados:")
        for tid, status, response, duracao in sucessos:
            print(f"   - Thread {tid}: Agendamento ID {response['id']}")
    else:
        print("\n⚠ PROBLEMA! Nenhum agendamento criado")
    
    print("\n" + "="*80)
    print("VERIFICAÇÃO NO BANCO DE DADOS")
    print("="*80 + "\n")
    
    # Aguardar um pouco para garantir consistência
    time.sleep(0.5)
    
    # Consultar agendamentos
    response = requests.get(
        f'{BASE_URL}/agendamentos',
        params={
            'cientista_id': cientista_id,
            'status': 'AGENDADO'
        }
    )
    
    if response.status_code == 200:
        agendamentos = response.json()['agendamentos']
        print(f"Agendamentos no banco: {len(agendamentos)}")
        
        if len(agendamentos) == 1:
            print("\n✓ Banco de dados consistente (1 agendamento)")
        elif len(agendamentos) > 1:
            print(f"\n🚨 Inconsistência no banco ({len(agendamentos)} agendamentos)!")
            print("\nAgendamentos encontrados:")
            for ag in agendamentos:
                print(f"   - ID {ag['id']}: {ag['horario_inicio_utc']}")
    
    print("\n" + "="*80)
    print("ANÁLISE DOS LOGS")
    print("="*80)
    print("\nPara analisar os logs:")
    print("\n1. Serviço de Agendamento (Python):")
    print("   cat servico-agendamento/logs/app.log | grep -E '(Tentando adquirir lock|Lock adquirido|Falha ao adquirir)'")
    print("\n2. Serviço Coordenador (Node.js):")
    print("   (Ver saída do console onde está rodando)")
    print("\n3. Logs de Auditoria:")
    print("   cat servico-agendamento/logs/audit.log | jq '.event_type'")
    print("\n4. Docker Logs (se usando containers):")
    print("   docker-compose logs -f")
    print("="*80 + "\n")

if __name__ == '__main__':
    import sys
    
    num_threads = 10
    if len(sys.argv) > 1:
        try:
            num_threads = int(sys.argv[1])
        except ValueError:
            print("Uso: python test_com_lock.py [num_threads]")
            sys.exit(1)
    
    teste_com_lock(num_threads)
```

### Tarefa 3.5: Validação da Entrega 3
**Tempo estimado: 2 horas**

#### Checklist:

1. **Iniciar ambos os serviços em terminais separados**
   ```bash
   # Terminal 1
   cd servico-agendamento
   source venv/bin/activate
   python run.py
   
   # Terminal 2
   cd servico-coordenador
   npm run dev
   ```

2. **Testar endpoints do coordenador**
   - GET http://localhost:3000/health
   - GET http://localhost:3000/locks (deve estar vazio)

3. **Testar lock manualmente via Postman**
   - POST http://localhost:3000/lock
   - Body: `{"recurso": "teste", "correlation_id": "123"}`
   - Verificar 200 OK
   - Tentar novamente (deve dar 409)
   - POST http://localhost:3000/unlock
   - Verificar locks liberados

4. **Executar teste automatizado**
   ```bash
   python tests/test_com_lock.py 10
   ```
   - Deve mostrar apenas 1 sucesso
   - 9 conflitos (409)
   - 1 agendamento no banco

5. **Observar logs**
   - Terminal do Node.js: deve mostrar lock concedido e 9 negados
   - app.log: deve mostrar tentativas de lock
   - audit.log: deve ter apenas 1 AGENDAMENTO_CRIADO

6. **Documentar**
   - Criar ENTREGA3_RESULTADOS.md
   - Screenshots dos logs
   - Comparação com Entrega 2

7. **Commit**
   ```bash
   git add .
   git commit -m "Entrega 3: Exclusão mútua com serviço coordenador"
   git tag entrega-3
   ```

---

## ⏰ ENTREGA 4: SINCRONIZAÇÃO DE TEMPO

**Objetivo:** Implementar sincronização cliente-servidor e HATEOAS completo
**Tempo estimado: 10-12 horas**

### Tarefa 4.1: Interface Web do Cliente
**Tempo estimado: 4-5 horas**

#### Criar estrutura
```bash
cd servico-agendamento
mkdir static
mkdir templates
```

#### Arquivo: templates/index.html
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCTEC - Sistema de Agendamento</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .sync-status {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        
        .sync-status h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .time-display {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .time-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .time-box label {
            display: block;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .time-box .value {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            font-family: 'Courier New', monospace;
        }
        
        .sync-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-radius: 8px;
            margin-top: 15px;
        }
        
        .sync-indicator.synced {
            background: #d4edda;
            color: #155724;
        }
        
        .sync-indicator.syncing {
            background: #fff3cd;
            color: #856404;
        }
        
        .sync-indicator.error {
            background: #f8d7da;
            color: #721c24;
        }
        
        .sync-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .sync-indicator.synced .sync-dot {
            background: #28a745;
        }
        
        .sync-indicator.syncing .sync-dot {
            background: #ffc107;
        }
        
        .sync-indicator.error .sync-dot {
            background: #dc3545;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }
        
        .card h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            color: #333;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .agendamento-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        
        .agendamento-item.cancelado {
            border-left-color: #dc3545;
            opacity: 0.7;
        }
        
        .agendamento-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }
        
        .agendamento-title {
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        .agendamento-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .agendamento-status.agendado {
            background: #d4edda;
            color: #155724;
        }
        
        .agendamento-status.cancelado {
            background: #f8d7da;
            color: #721c24;
        }
        
        .agendamento-details {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        
        .agendamento-details div {
            margin-bottom: 5px;
        }
        
        .agendamento-actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .btn-small {
            padding: 6px 15px;
            font-size: 0.9em;
        }
        
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .alert.show {
            display: block;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-danger {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .alert-warning {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }
        
        .empty-state svg {
            width: 80px;
            height: 80px;
            margin-bottom: 15px;
            opacity: 0.3;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔭 SCTEC</h1>
            <p>Sistema de Controle de Telescópio Espacial Compartilhado</p>
        </div>
        
        <!-- Sync Status -->
        <div class="sync-status">
            <h2>⏰ Sincronização de Tempo</h2>
            <div class="time-display">
                <div class="time-box">
                    <label>Hora Local do Navegador</label>
                    <div class="value" id="local-time">--:--:--</div>
                </div>
                <div class="time-box">
                    <label>Hora do Servidor (UTC)</label>
                    <div class="value" id="server-time">--:--:--</div>
                </div>
                <div class="time-box">
                    <label>Diferença (ms)</label>
                    <div class="value" id="time-diff">--</div>
                </div>
                <div class="time-box">
                    <label>Latência de Rede (ms)</label>
                    <div class="value" id="network-latency">--</div>
                </div>
            </div>
            <div class="sync-indicator" id="sync-indicator">
                <div class="sync-dot"></div>
                <span id="sync-message">Sincronizando...</span>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <!-- Formulário de Agendamento -->
            <div class="card">
                <h2>📅 Novo Agendamento</h2>
                
                <div class="alert alert-success" id="success-alert"></div>
                <div class="alert alert-danger" id="error-alert"></div>
                
                <form id="agendamento-form">
                    <div class="form-group">
                        <label for="cientista">Cientista *</label>
                        <select id="cientista" required>
                            <option value="">Carregando...</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="horario_inicio">Horário de Início (UTC) *</label>
                        <input type="datetime-local" id="horario_inicio" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="duracao">Duração (minutos) *</label>
                        <select id="duracao" required>
                            <option value="5">5 minutos</option>
                            <option value="10">10 minutos</option>
                            <option value="15">15 minutos</option>
                            <option value="30" selected>30 minutos</option>
                            <option value="45">45 minutos</option>
                            <option value="60">60 minutos</option>
                            <option value="90">90 minutos</option>
                            <option value="120">120 minutos</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="objeto_celeste">Objeto Celeste *</label>
                        <input type="text" id="objeto_celeste" placeholder="Ex: NGC 1300" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="observacoes">Observações</label>
                        <textarea id="observacoes" placeholder="Descreva o objetivo da observação..."></textarea>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" id="submit-btn">
                        Agendar Observação
                    </button>
                </form>
            </div>
            
            <!-- Lista de Agendamentos -->
            <div class="card">
                <h2>📋 Meus Agendamentos</h2>
                
                <div class="alert alert-warning" id="cancel-alert"></div>
                
                <div id="agendamentos-container">
                    <div class="loading">Carregando agendamentos...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Configuração da API
        const API_BASE = '/api/v1';
        
        // Estado da aplicação
        let cientistas = [];
        let agendamentos = [];
        let cientistaAtualId = null;
        let offsetTempo = 0;  // Diferença entre servidor e cliente em ms
        let latenciaRede = 0;
        
        // ===== SINCRONIZAÇÃO DE TEMPO (Algoritmo de Cristian) =====
        
        async function sincronizarTempo() {
            try {
                const t0 = Date.now();
                
                const response = await fetch(`${API_BASE}/time`);
                const t1 = Date.now();
                
                if (!response.ok) {
                    throw new Error('Falha ao sincronizar tempo');
                }
                
                const data = await response.json();
                const tempoServidor = new Date(data.timestamp_utc).getTime();
                
                // Calcular latência de ida e volta (RTT)
                const rtt = t1 - t0;
                latenciaRede = rtt;
                
                // Calcular offset considerando latência
                // Assumimos que a latência é simétrica (ida = volta)
                const latenciaEstimada = rtt / 2;
                const tempoServidorAjustado = tempoServidor + latenciaEstimada;
                
                offsetTempo = tempoServidorAjustado - t1;
                
                atualizarIndicadorSync('synced', `Sincronizado (offset: ${offsetTempo}ms)`);
                
            } catch (error) {
                console.error('Erro na sincronização:', error);
                atualizarIndicadorSync('error', 'Erro na sincronização de tempo');
            }
        }
        
        function getTempoSincronizado() {
            // Retorna o tempo atual ajustado pelo offset
            return new Date(Date.now() + offsetTempo);
        }
        
        function formatarDataParaAPI(date) {
            // Formato ISO8601 UTC
            return date.toISOString();
        }
        
        function atualizarIndicadorSync(status, mensagem) {
            const indicator = document.getElementById('sync-indicator');
            const message = document.getElementById('sync-message');
            
            indicator.className = `sync-indicator ${status}`;
            message.textContent = mensagem;
        }
        
        // Atualizar displays de tempo em tempo real
        function atualizarDisplaysTempo() {
            const agoraLocal = new Date();
            const agoraSincronizado = getTempoSincronizado();
            
            document.getElementById('local-time').textContent = 
                agoraLocal.toLocaleTimeString('pt-BR');
            
            document.getElementById('server-time').textContent = 
                agoraSincronizado.toISOString().substr(11, 8);
            
            document.getElementById('time-diff').textContent = 
                `${offsetTempo >= 0 ? '+' : ''}${offsetTempo}`;
            
            document.getElementById('network-latency').textContent = 
                Math.round(latenciaRede);
        }
        
        // ===== OPERAÇÕES DA API =====
        
        async function carregarCientistas() {
            try {
                const response = await fetch(`${API_BASE}/cientistas`);
                const data = await response.json();
                
                cientistas = data.cientistas;
                
                const select = document.getElementById('cientista');
                select.innerHTML = '<option value="">Selecione um cientista</option>';
                
                cientistas.forEach(c => {
                    const option = document.createElement('option');
                    option.value = c.id;
                    option.textContent = `${c.nome} - ${c.instituicao}`;
                    select.appendChild(option);
                });
                
                // Selecionar o primeiro automaticamente
                if (cientistas.length > 0) {
                    cientistaAtualId = cientistas[0].id;
                    select.value = cientistaAtualId;
                    carregarAgendamentos(cientistaAtualId);
                }
                
            } catch (error) {
                console.error('Erro ao carregar cientistas:', error);
                mostrarAlerta('error', 'Erro ao carregar lista de cientistas');
            }
        }
        
        async function carregarAgendamentos(cientistaId) {
            try {
                const container = document.getElementById('agendamentos-container');
                container.innerHTML = '<div class="loading">Carregando agendamentos...</div>';
                
                const response = await fetch(`${API_BASE}/cientistas/${cientistaId}/agendamentos`);
                const data = await response.json();
                
                agendamentos = data.agendamentos;
                renderizarAgendamentos();
                
            } catch (error) {
                console.error('Erro ao carregar agendamentos:', error);
                document.getElementById('agendamentos-container').innerHTML = 
                    '<div class="empty-state">Erro ao carregar agendamentos</div>';
            }
        }
        
        function renderizarAgendamentos() {
            const container = document.getElementById('agendamentos-container');
            
            if (agendamentos.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <p>Nenhum agendamento encontrado</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = agendamentos
                .sort((a, b) => new Date(a.horario_inicio_utc) - new Date(b.horario_inicio_utc))
                .map(ag => criarCardAgendamento(ag))
                .join('');
        }
        
        function criarCardAgendamento(ag) {
            const inicio = new Date(ag.horario_inicio_utc);
            const fim = new Date(ag.horario_fim_utc);
            const duracao = Math.round((fim - inicio) / 60000);
            
            const podeCancelar = ag.status === 'AGENDADO' && ag._links.cancelar;
            
            return `
                <div class="agendamento-item ${ag.status.toLowerCase()}">
                    <div class="agendamento-header">
                        <div class="agendamento-title">${ag.objeto_celeste}</div>
                        <div class="agendamento-status ${ag.status.toLowerCase()}">${ag.status}</div>
                    </div>
                    <div class="agendamento-details">
                        <div>📅 ${inicio.toLocaleString('pt-BR')} UTC</div>
                        <div>⏱ Duração: ${duracao} minutos</div>
                        ${ag.observacoes ? `<div>📝 ${ag.observacoes}</div>` : ''}
                        ${ag.motivo_cancelamento ? `<div>❌ Motivo: ${ag.motivo_cancelamento}</div>` : ''}
                    </div>
                    ${podeCancelar ? `
                        <div class="agendamento-actions">
                            <button class="btn btn-danger btn-small" onclick="cancelarAgendamento(${ag.id})">
                                Cancelar Agendamento
                            </button>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        async function cancelarAgendamento(id) {
            if (!confirm('Tem certeza que deseja cancelar este agendamento?')) {
                return;
            }
            
            const motivo = prompt('Motivo do cancelamento (opcional):');
            
            try {
                const response = await fetch(`${API_BASE}/agendamentos/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        motivo: motivo || 'Cancelado pelo usuário'
                    })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erro ao cancelar');
                }
                
                mostrarAlertaTemporario('cancel', 'Agendamento cancelado com sucesso', 'warning');
                carregarAgendamentos(cientistaAtualId);
                
            } catch (error) {
                console.error('Erro ao cancelar:', error);
                mostrarAlertaTemporario('cancel', `Erro: ${error.message}`, 'danger');
            }
        }
        
        // ===== FORMULÁRIO DE AGENDAMENTO =====
        
        document.getElementById('agendamento-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submit-btn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Agendando...';
            
            try {
                // Obter valores do formulário
                const cientistaId = parseInt(document.getElementById('cientista').value);
                const horarioInicio = document.getElementById('horario_inicio').value;
                const duracao = parseInt(document.getElementById('duracao').value);
                const objetoCeleste = document.getElementById('objeto_celeste').value;
                const observacoes = document.getElementById('observacoes').value;
                
                // Converter horário para UTC sincronizado
                const dataInicio = new Date(horarioInicio);
                const dataFim = new Date(dataInicio.getTime() + duracao * 60000);
                
                // Usar tempo sincronizado
                const tempoSincronizado = getTempoSincronizado();
                
                // Preparar dados
                const dados = {
                    cientista_id: cientistaId,
                    horario_inicio_utc: formatarDataParaAPI(dataInicio),
                    horario_fim_utc: formatarDataParaAPI(dataFim),
                    objeto_celeste: objetoCeleste,
                    observacoes: observacoes || null
                };
                
                // Enviar requisição
                const response = await fetch(`${API_BASE}/agendamentos`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(dados)
                });
                
                const resultado = await response.json();
                
                if (!response.ok) {
                    throw new Error(resultado.error || 'Erro ao criar agendamento');
                }
                
                // Sucesso!
                mostrarAlerta('success', 'Agendamento criado com sucesso!');
                document.getElementById('agendamento-form').reset();
                carregarAgendamentos(cientistaId);
                
            } catch (error) {
                console.error('Erro ao agendar:', error);
                mostrarAlerta('error', `Erro: ${error.message}`);
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Agendar Observação';
            }
        });
        
        function mostrarAlerta(tipo, mensagem) {
            const alertaId = tipo === 'success' ? 'success-alert' : 'error-alert';
            const alerta = document.getElementById(alertaId);
            
            alerta.textContent = mensagem;
            alerta.classList.add('show');
            
            setTimeout(() => {
                alerta.classList.remove('show');
            }, 5000);
        }
        
        function mostrarAlertaTemporario(id, mensagem, tipo) {
            const alerta = document.getElementById(`${id}-alert`);
            alerta.className = `alert alert-${tipo} show`;
            alerta.textContent = mensagem;
            
            setTimeout(() => {
                alerta.classList.remove('show');
            }, 5000);
        }
        
        // ===== INICIALIZAÇÃO =====
        
        // Quando o cientista muda, recarregar agendamentos
        document.getElementById('cientista').addEventListener('change', (e) => {
            cientistaAtualId = parseInt(e.target.value);
            if (cientistaAtualId) {
                carregarAgendamentos(cientistaAtualId);
            }
        });
        
        // Inicializar quando a página carregar
        window.addEventListener('load', async () => {
            // Sincronizar tempo primeiro
            await sincronizarTempo();
            
            // Atualizar displays a cada segundo
            setInterval(atualizarDisplaysTempo, 1000);
            atualizarDisplaysTempo();
            
            // Ressincronizar a cada 30 segundos
            setInterval(sincronizarTempo, 30000);
            
            // Carregar dados
            await carregarCientistas();
        });
    </script>
</body>
</html>
```

### Tarefa 4.2: Servir a Interface no Flask
**Tempo estimado: 1 hora**

#### Modificar: app/__init__.py (adicionar rota para interface)
```python
from flask import render_template

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    # ... resto da configuração existente ...
    
    # Rota para a interface web
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
```

### Tarefa 4.3: Melhorias no Algoritmo de Sincronização
**Tempo estimado: 2 horas**

#### Opção de melhorias no JavaScript do cliente:

1. **Múltiplas medições (média)**
   - Fazer 5 requisições de sincronização
   - Calcular média do offset
   - Reduz impacto de variações de latência

2. **NTP-like (Network Time Protocol)**
   - Implementar versão simplificada do NTP
   - Mais preciso que Cristian

3. **Monitoramento de drift**
   - Detectar se o relógio local está desviando
   - Ressincronizar automaticamente

### Tarefa 4.4: Validação da Entrega 4
**Tempo estimado: 2 horas**

#### Checklist:

1. **Acessar interface web**
   - http://localhost:5000
   - Verificar se carrega corretamente

2. **Testar sincronização**
   - Observar os displays de tempo
   - Verificar se offset é calculado
   - Verificar latência de rede

3. **Criar agendamento pela interface**
   - Selecionar cientista
   - Escolher horário futuro
   - Preencher formulário
   - Submeter
   - Verificar se aparece na lista

4. **Testar HATEOAS**
   - Verificar se botão "Cancelar" aparece apenas em agendamentos AGENDADOS
   - Clicar em cancelar
   - Verificar se status muda

5. **Testar em múltiplas abas**
   - Abrir 3 abas simultâneas
   - Tentar agendar mesmo horário
   - Apenas 1 deve ter sucesso

6. **Documentar**
   - Screenshots da interface
   - Criar ENTREGA4_MANUAL_USUARIO.md
   - Documentar algoritmo de sincronização

7. **Commit**
   ```bash
   git add .
   git commit -m "Entrega 4: Interface web com sincronização de tempo"
   git tag entrega-4
   ```

---

## 🐳 ENTREGA 5: CONTAINERIZAÇÃO

**Objetivo:** Orquestrar com Docker Compose
**Tempo estimado: 8-10 horas**

### Tarefa 5.1: Dockerfile do Serviço de Agendamento
**Tempo estimado: 2 horas**

#### Arquivo: servico-agendamento/Dockerfile
```dockerfile
# Usar imagem oficial do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para logs
RUN mkdir -p logs

# Criar diretório para banco de dados
RUN mkdir -p instance

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para iniciar
CMD ["python", "run.py"]
```

#### Arquivo: servico-agendamento/.dockerignore
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
*.db
*.log
.git/
.gitignore
.vscode/
.idea/
*.md
tests/
```

### Tarefa 5.2: Dockerfile do Serviço Coordenador
**Tempo estimado: 1 hora**

#### Arquivo: servico-coordenador/Dockerfile
```dockerfile
# Usar imagem oficial do Node.js
FROM node:18-alpine

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 3000

# Variáveis de ambiente
ENV NODE_ENV=production
ENV PORT=3000

# Comando para iniciar
CMD ["node", "server.js"]
```

#### Arquivo: servico-coordenador/.dockerignore
```
node_modules/
npm-debug.log
.git/
.gitignore
.vscode/
.idea/
*.md
```

### Tarefa 5.3: Docker Compose
**Tempo estimado: 3 horas**

#### Arquivo: docker-compose.yml (na raiz do projeto)
```yaml
version: '3.8'

services:
  # Serviço Coordenador (Node.js)
  coordenador:
    build:
      context: ./servico-coordenador
      dockerfile: Dockerfile
    container_name: sctec-coordenador
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    networks:
      - sctec-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Serviço de Agendamento (Flask)
  agendamento:
    build:
      context: ./servico-agendamento
      dockerfile: Dockerfile
    container_name: sctec-agendamento
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=chave-super-secreta-trocar-em-producao
      - DATABASE_URI=sqlite:///instance/telescopio.db
      - LOG_LEVEL=INFO
      - COORDENADOR_URL=http://coordenador:3000
      - NOME_TELESCOPIO=Hubble-Acad
    volumes:
      # Persistir banco de dados
      - agendamento-db:/app/instance
      # Persistir logs
      - agendamento-logs:/app/logs
    networks:
      - sctec-network
    depends_on:
      coordenador:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:5000/api/v1/time"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  sctec-network:
    driver: bridge
    name: sctec-network

volumes:
  agendamento-db:
    name: sctec-agendamento-db
  agendamento-logs:
    name: sctec-agendamento-logs
```

### Tarefa 5.4: Scripts de Gerenciamento
**Tempo estimado: 1 hora**

#### Arquivo: start.sh (Linux/Mac)
```bash
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
echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

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
echo "   Parar: docker-compose stop"
echo "   Remover: docker-compose down"
echo ""
```

#### Arquivo: start.bat (Windows)
```batch
@echo off
echo ======================================
echo    SCTEC - Iniciando Sistema
echo ======================================
echo.

REM Verificar Docker
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo X Docker nao esta rodando. Inicie o Docker Desktop e tente novamente.
    exit /b 1
)

echo OK Docker esta rodando
echo.

echo Construindo e iniciando containers...
docker-compose up --build -d

echo.
echo Aguardando servicos ficarem prontos...
timeout /t 10 /nobreak >nul

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
echo    Parar: docker-compose stop
echo    Remover: docker-compose down
echo.
pause
```

#### Arquivo: stop.sh
```bash
#!/bin/bash

echo "Parando sistema SCTEC..."
docker-compose stop
echo "Sistema parado."
```

#### Arquivo: clean.sh
```bash
#!/bin/bash

echo "⚠️  ATENÇÃO: Isso irá remover todos os containers, volumes e dados!"
read -p "Tem certeza? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]
then
    echo "Removendo sistema SCTEC..."
    docker-compose down -v
    echo "Sistema removido."
fi
```

### Tarefa 5.5: Documentação Docker
**Tempo estimado: 1 hora**

#### Arquivo: DOCKER.md
```markdown
# Guia Docker - SCTEC

## Pré-requisitos

- Docker Desktop instalado
- Docker Compose (incluído no Docker Desktop)
- 2GB de RAM disponível
- Portas 5000 e 3000 livres

## Iniciar Sistema

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

### Windows:
```
start.bat
```

### Manualmente:
```bash
docker-compose up --build -d
```

## Parar Sistema

```bash
docker-compose stop
```

## Ver Logs

### Todos os serviços:
```bash
docker-compose logs -f
```

### Serviço específico:
```bash
docker-compose logs -f agendamento
docker-compose logs -f coordenador
```

### Últimas 100 linhas:
```bash
docker-compose logs --tail=100
```

## Reiniciar Serviço

```bash
docker-compose restart agendamento
docker-compose restart coordenador
```

## Acessar Shell do Container

```bash
docker exec -it sctec-agendamento /bin/bash
docker exec -it sctec-coordenador /bin/sh
```

## Verificar Status

```bash
docker-compose ps
```

## Verificar Uso de Recursos

```bash
docker stats
```

## Remover Tudo

⚠️ **CUIDADO: Remove dados!**

```bash
docker-compose down -v
```

## Troubleshooting

### Porta em uso
Se receber erro "port already allocated":
```bash
# Ver o que está usando a porta
lsof -i :5000
lsof -i :3000

# Ou parar todos os containers
docker-compose down
```

### Rebuild completo
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Limpar cache do Docker
```bash
docker system prune -a
```

### Ver logs de build
```bash
docker-compose build --progress=plain
```

## Volumes

### Listar volumes:
```bash
docker volume ls
```

### Inspecionar volume:
```bash
docker volume inspect sctec-agendamento-db
```

### Backup do banco de dados:
```bash
docker run --rm -v sctec-agendamento-db:/data -v $(pwd):/backup ubuntu tar czf /backup/backup.tar.gz -C /data .
```

### Restaurar backup:
```bash
docker run --rm -v sctec-agendamento-db:/data -v $(pwd):/backup ubuntu tar xzf /backup/backup.tar.gz -C /data
```

## Rede

### Inspecionar rede:
```bash
docker network inspect sctec-network
```

### Testar conectividade entre containers:
```bash
docker exec sctec-agendamento ping coordenador
```

## Monitoramento

### Healthchecks:
```bash
docker inspect --format='{{.State.Health.Status}}' sctec-agendamento
docker inspect --format='{{.State.Health.Status}}' sctec-coordenador
```

### Logs estruturados:
```bash
docker-compose logs --no-color agendamento | jq .
```
```

### Tarefa 5.6: Ajustes para Produção
**Tempo estimado: 1 hora**

#### Modificar: servico-agendamento/run.py
```python
import os
from app import create_app, db
from app.utils.logger import setup_audit_logger
from app.utils.middleware import setup_request_middleware

# Determinar ambiente
env = os.getenv('FLASK_ENV', 'development')

# Criar aplicação
app = create_app(env)

# Configurar logger de auditoria
setup_audit_logger()

# Configurar middleware
setup_request_middleware(app)

# Adicionar filtro de correlation_id aos loggers
from app.utils.logger import CorrelationIdFilter
for handler in app.logger.handlers:
    handler.addFilter(CorrelationIdFilter())

if __name__ == '__main__':
    # Desenvolvimento: Flask dev server
    if env == 'development':
        app.run(host='0.0.0.0', port=5000, debug=True)
    # Produção: usar gunicorn (adicionar no Dockerfile)
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)
```

### Tarefa 5.7: Validação da Entrega 5
**Tempo estimado: 2 horas**

#### Checklist:

1. **Build dos containers**
   ```bash
   docker-compose build
   ```
   - Verificar se build completa sem erros
   - Verificar tamanho das imagens

2. **Iniciar sistema**
   ```bash
   ./start.sh  # ou start.bat no Windows
   ```
   - Verificar se ambos os containers iniciam
   - Verificar healthchecks

3. **Testar aplicação**
   - Acessar http://localhost:5000
   - Criar agendamento
   - Verificar funcionamento completo

4. **Testar logs agregados**
   ```bash
   docker-compose logs -f
   ```
   - Fazer operações na interface
   - Observar logs entrelaçados de ambos os serviços
   - Verificar correlation_id

5. **Testar concorrência**
   - Executar teste de estresse
   - Observar comportamento

6. **Testar persistência**
   ```bash
   # Criar agendamento
   # Parar sistema
   docker-compose stop
   # Reiniciar
   docker-compose start
   # Verificar se dados persistiram
   ```

7. **Testar volumes**
   ```bash
   docker volume inspect sctec-agendamento-db
   docker volume inspect sctec-agendamento-logs
   ```

8. **Documentar**
   - Criar ENTREGA5_DOCKER.md
   - Screenshots do Docker Desktop
   - Comandos úteis

9. **Commit final**
   ```bash
   git add .
   git commit -m "Entrega 5: Containerização completa com Docker Compose"
   git tag entrega-5
   git tag v1.0.0
   ```

---

## ✅ VALIDAÇÃO FINAL E ENTREGA

**Tempo estimado: 4-6 horas**

### Tarefa Final 1: Documentação Completa
**Tempo estimado: 2-3 horas**

#### Arquivo: README.md (Atualizar)
```markdown
# SCTEC - Sistema de Controle de Telescópio Espacial Compartilhado

Sistema distribuído para agendamento de observações em telescópio espacial acadêmico, desenvolvido como projeto da disciplina de Computação Distribuída.

## 🎯 Objetivos do Projeto

- Implementar API RESTful com HATEOAS
- Resolver condição de corrida com exclusão mútua
- Sincronizar tempo entre cliente e servidor
- Implementar logging completo (aplicação + auditoria)
- Containerizar com Docker

## 🏗️ Arquitetura

### Microserviços

1. **Serviço de Agendamento** (Python/Flask)
   - API RESTful principal
   - Gerenciamento de cientistas e agendamentos
   - Persistência em SQLite
   - Logging estruturado

2. **Serviço Coordenador** (Node.js/Express)
   - Controle de locks (exclusão mútua)
   - Gerenciamento de recursos compartilhados
   - Alta performance para concorrência

### Comunicação

- HTTP/REST entre serviços
- JSON como formato de dados
- HATEOAS para descoberta de recursos

## 🚀 Início Rápido

### Pré-requisitos

- Docker Desktop
- Ou: Python 3.9+ e Node.js 18+

### Opção 1: Docker (Recomendado)

```bash
# Clonar repositório
git clone [url-do-repo]
cd telescopio-espacial

# Iniciar sistema
./start.sh  # Linux/Mac
start.bat   # Windows

# Acessar
http://localhost:5000
```

### Opção 2: Desenvolvimento Local

```bash
# Terminal 1 - Serviço de Agendamento
cd servico-agendamento
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# Terminal 2 - Serviço Coordenador
cd servico-coordenador
npm install
npm run dev
```

## 📚 Documentação

- [API Reference](docs/API.md)
- [Modelos de Dados](docs/MODELOS.md)
- [Sistema de Logging](docs/LOGGING.md)
- [Guia Docker](DOCKER.md)
- [Manual do Usuário](docs/MANUAL_USUARIO.md)

## 🧪 Testes

```bash
# Teste de concorrência (SEM lock - demonstra problema)
python tests/test_concorrencia.py

# Teste com lock (demonstra solução)
python tests/test_com_lock.py

# Teste com diferentes cargas
python tests/test_com_lock.py 50  # 50 threads simultâneas
```

## 📊 Entregas do Projeto

- ✅ **Entrega 1:** Blueprint da API
- ✅ **Entrega 2:** Sistema inicial (demonstração do problema)
- ✅ **Entrega 3:** Serviço coordenador (solução)
- ✅ **Entrega 4:** Sincronização de tempo e interface web
- ✅ **Entrega 5:** Containerização

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, Flask, SQLAlchemy
- **Coordenação:** Node.js 18, Express
- **Banco de Dados:** SQLite
- **Container:** Docker, Docker Compose
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)

## 👥 Autores

[Seus nomes aqui]

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos.
```

### Tarefa Final 2: Vídeo de Apresentação (Opcional)
**Tempo estimado: 1-2 horas**

1. **Roteiro (5-10 minutos)**:
   - Demonstração do problema (teste sem lock)
   - Arquitetura da solução
   - Demonstração funcionando (teste com lock)
   - Interface web
   - Logs e observabilidade
   - Docker Compose

### Tarefa Final 3: Checklist Final
**Tempo estimado: 1 hora**

```markdown
## Checklist de Entrega

### Código
- [ ] Todos os arquivos commitados
- [ ] Sem credenciais ou secrets no código
- [ ] .gitignore configurado
- [ ] Código comentado e limpo

### Documentação
- [ ] README.md completo
- [ ] API.md com todos endpoints
- [ ] MODELOS.md com entidades
- [ ] LOGGING.md com formato dos logs
- [ ] DOCKER.md com comandos

### Funcionalidades
- [ ] CRUD de cientistas
- [ ] CRUD de agendamentos
- [ ] Validações de regras de negócio
- [ ] Exclusão mútua funcionando
- [ ] Sincronização de tempo
- [ ] HATEOAS em todas as respostas
- [ ] Logs de aplicação
- [ ] Logs de auditoria
- [ ] Interface web funcional
- [ ] Cancelamento de agendamentos

### Docker
- [ ] Dockerfile do serviço de agendamento
- [ ] Dockerfile do serviço coordenador
- [ ] docker-compose.yml
- [ ] Volumes para persistência
- [ ] Healthchecks configurados
- [ ] Logs agregados funcionando

### Testes
- [ ] Script de teste sem lock
- [ ] Script de teste com lock
- [ ] Ambos executam corretamente
- [ ] Documentação dos resultados

### Extras (Opcional)
- [ ] Vídeo de apresentação
- [ ] Diagramas de arquitetura
- [ ] Análise de performance
- [ ] Testes unitários
- [ ] CI/CD configurado
```

---

## 📈 RESUMO DE HORAS

| Fase | Tempo Estimado |
|------|----------------|
| **Preparação do Ambiente** | 2-3h |
| **Entrega 1: Blueprint** | 8-12h |
| **Entrega 2: Sistema Inicial** | 16-20h |
| **Entrega 3: Coordenador** | 12-16h |
| **Entrega 4: Sincronização** | 10-12h |
| **Entrega 5: Docker** | 8-10h |
| **Validação Final** | 4-6h |
| **TOTAL** | **60-79h** |

---

## 💡 DICAS PARA EXCELÊNCIA

1. **Commits Frequentes**: Faça commits pequenos e frequentes com mensagens claras

2. **Testes Constantes**: Teste cada feature assim que implementar

3. **Documentação Contínua**: Documente conforme desenvolve, não deixe para o final

4. **Code Review**: Se possível, peça para colegas revisarem seu código

5. **Logging Detalhado**: Logs são seu melhor amigo para debugging distribuído

6. **Tratamento de Erros**: Sempre trate exceções adequadamente

7. **Validações**: Valide todos os inputs do usuário

8. **Performance**: Use índices no banco, otimize queries

9. **Segurança**: Não exponha informações sensíveis nos logs

10. **Observabilidade**: Mantenha correlation_id em todas as operações

---

## 🎯 CRITÉRIOS DE EXCELÊNCIA

Para atingir nota máxima:

✅ **Funcionalidade Completa**: Todos os requisitos implementados

✅ **Código Limpo**: Bem organizado, comentado e seguindo boas práticas

✅ **Documentação Completa**: README, API docs, comentários no código

✅ **Testes Robustos**: Scripts que provam o funcionamento

✅ **Logs Detalhados**: Rastreabilidade completa de todas operações

✅ **Docker Funcional**: Sistema sobe com um comando

✅ **HATEOAS**: Links dinâmicos em todas as respostas

✅ **Tratamento de Erros**: Respostas adequadas para todos os cenários

✅ **Performance**: Sistema suporta carga de 50+ requisições simultâneas

✅ **Extra Mile**: Interface web profissional, vídeo de apresentação

---
</instrucoes_projeto>