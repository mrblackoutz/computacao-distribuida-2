# Entrega 4 - Interface Web e Sincronização de Tempo

## 🎯 Objetivo

Criar uma interface web profissional para o sistema SCTEC que implementa o **Algoritmo de Cristian** para sincronização de tempo entre cliente e servidor, garantindo que os timestamps enviados nas requisições sejam precisos.

## 📋 O que foi implementado

### 1. Interface Web Completa

**Arquivo:** `servico-agendamento/templates/index.html`

**Tecnologias:**
- HTML5 semântico
- CSS3 com gradientes e animações
- JavaScript vanilla (sem frameworks)
- Design responsivo

**Características:**
- ✨ Interface moderna com gradientes e efeitos visuais
- 📱 Totalmente responsiva (desktop, tablet, mobile)
- ⚡ Animações suaves e feedback visual
- 🎨 Sistema de cores consistente
- ♿ Acessibilidade considerada

### 2. Algoritmo de Cristian para Sincronização de Tempo

**Conceito:**
O Algoritmo de Cristian sincroniza relógios em sistemas distribuídos através de trocas de mensagens com um servidor de tempo confiável.

**Implementação JavaScript:**

```javascript
async function sincronizarTempo() {
    // t0: tempo antes da requisição
    const t0 = Date.now();
    
    const response = await fetch('/api/v1/time');
    
    // t1: tempo após receber resposta
    const t1 = Date.now();
    
    const data = await response.json();
    const tempoServidor = new Date(data.timestamp_utc).getTime();
    
    // RTT (Round-Trip Time)
    const rtt = t1 - t0;
    
    // Assumir latência simétrica: ida = volta = RTT/2
    const latenciaEstimada = rtt / 2;
    
    // Ajustar tempo do servidor pela latência
    const tempoServidorAjustado = tempoServidor + latenciaEstimada;
    
    // Calcular offset (diferença)
    offsetTempo = tempoServidorAjustado - t1;
}
```

**Fórmula:**
```
Offset = (TempoServidor + RTT/2) - TempoCliente
```

**Explicação:**
1. Cliente registra t0 e envia requisição
2. Servidor responde com seu timestamp
3. Cliente registra t1 ao receber
4. RTT = t1 - t0 (tempo total ida + volta)
5. Estimamos que metade do RTT foi na ida
6. Ajustamos o tempo do servidor somando RTT/2
7. Calculamos a diferença (offset)

### 3. Funcionalidades da Interface

#### Painel de Sincronização
- **Hora Local:** Relógio do navegador
- **Hora do Servidor (UTC):** Tempo sincronizado
- **Offset:** Diferença em ms (+ ou -)
- **RTT:** Latência de rede em ms
- **Indicador Visual:** Status da sincronização (synced/syncing/error)

#### Formulário de Agendamento
- Seleção de cientista (dropdown)
- Horário de início (datetime-local)
- Duração (select com opções de 5min a 2h)
- Objeto celeste (texto)
- Observações (textarea opcional)
- Validação em tempo real
- Timestamps ajustados automaticamente para UTC

#### Lista de Agendamentos
- Cards visuais para cada agendamento
- Cores diferentes por status (AGENDADO/CANCELADO/CONCLUIDO)
- Estatísticas (total, agendados, concluídos)
- Botão de cancelamento (apenas para AGENDADO)
- HATEOAS: botões aparecem/desaparecem baseados nos links da API
- Ordenação por data (mais recentes primeiro)

#### Sistema de Alertas
- Alertas de sucesso (verde)
- Alertas de erro (vermelho)
- Alertas de aviso (amarelo)
- Auto-dismiss após 5 segundos
- Animações de entrada

### 4. Navegação via HATEOAS

**Conceito:**
Hypermedia As The Engine Of Application State - o cliente descobre ações disponíveis através dos links fornecidos pela API.

**Implementação:**

```javascript
function criarCardAgendamento(ag) {
    // Verifica se o link 'cancelar' existe na resposta
    const podeCancelar = ag.status === 'AGENDADO' && ag._links && ag._links.cancelar;
    
    return `
        ${podeCancelar ? `
            <button onclick="cancelarAgendamento(${ag.id})">
                Cancelar Agendamento
            </button>
        ` : ''}
    `;
}
```

**Benefícios:**
- Cliente não precisa conhecer todas as regras de negócio
- Servidor controla quais ações estão disponíveis
- Interface se adapta dinamicamente ao estado do recurso

### 5. Fluxo Completo de Sincronização

```
1. Página carrega
   └─> Dispara sincronização inicial

2. sincronizarTempo()
   ├─> GET /api/v1/time
   ├─> Calcula RTT e offset
   └─> Atualiza indicador visual

3. Atualização contínua
   ├─> setInterval: atualiza displays (1s)
   └─> setInterval: ressincroniza (30s)

4. Ao criar agendamento
   ├─> Obtém horário do formulário
   ├─> Converte para UTC
   └─> Envia timestamp sincronizado
```

## 🚀 Como Usar

### Passo 1: Garantir que os serviços estão rodando

**Terminal 1 - Coordenador:**
```powershell
cd servico-coordenador
npm start
```

**Terminal 2 - Agendamento:**
```powershell
cd servico-agendamento
.\venv\Scripts\Activate.ps1
python run.py
```

### Passo 2: Acessar a interface

Abra o navegador em:
```
http://localhost:5000
```

### Passo 3: Usar o sistema

1. **Observar sincronização**
   - Os 4 displays de tempo se atualizam em tempo real
   - O indicador mostra status "Sincronizado"
   - Offset e RTT são exibidos

2. **Criar agendamento**
   - Selecionar cientista
   - Escolher data/hora (mínimo 24h no futuro)
   - Definir duração
   - Especificar objeto celeste
   - Adicionar observações (opcional)
   - Clicar em "Agendar Observação"

3. **Visualizar agendamentos**
   - Cards aparecem automaticamente
   - Estatísticas são atualizadas
   - Botão "Cancelar" visível apenas se aplicável

4. **Cancelar agendamento**
   - Clicar em "Cancelar Agendamento"
   - Confirmar ação
   - Opcionalmente fornecer motivo
   - Status muda para CANCELADO

## 📊 Validação da Sincronização

### Teste 1: Verificar offset inicial

1. Abrir DevTools do navegador (F12)
2. Ir para Console
3. Procurar por `[SYNC] Sincronização concluída:`
4. Observar valores de offset e RTT

**Resultado esperado:**
```
[SYNC] Sincronização concluída: {
  offset: -12,
  rtt: 24,
  latenciaEstimada: 12
}
```

### Teste 2: Simular relógio desajustado

1. Abrir DevTools → Console
2. Executar:
```javascript
// Adicionar 5 segundos de offset artificial
offsetTempo += 5000;
```
3. Observar que "Offset de Tempo" muda para ~+5000ms
4. Criar um agendamento
5. Verificar que o timestamp enviado foi ajustado

### Teste 3: Testar ressincronização automática

1. Aguardar 30 segundos
2. Observar mensagem no console: `[SYNC] Sincronização concluída:`
3. Confirmar que offset foi recalculado

### Teste 4: Latência de rede

**Simular latência alta:**
1. DevTools → Network → No throttling → Slow 3G
2. Aguardar ressincronização (30s)
3. Observar RTT aumentar para ~1000ms+
4. Confirmar que sistema continua funcionando

## 🎨 Recursos Visuais

### Cores por Status

```css
AGENDADO: Verde (#28a745)
  └─> Background: #d4edda
  └─> Border: verde sólido

CANCELADO: Vermelho (#dc3545)
  └─> Background: #f8d7da
  └─> Border: vermelho sólido
  └─> Opacidade: 0.8

CONCLUIDO: Azul (#0c5460)
  └─> Background: #d1ecf1
  └─> Border: azul sólido
```

### Animações

```css
pulse (sync-dot): 
  - Pulsa a cada 2s
  - Scale: 1.0 → 0.9 → 1.0

slideIn (alertas):
  - Desliza de cima para baixo
  - Duração: 0.3s

hover (cards):
  - Transform: translateX(5px)
  - Box-shadow aumenta
```

### Responsividade

```css
Desktop (> 1024px):
  └─> 2 colunas (formulário | lista)

Tablet/Mobile (≤ 1024px):
  └─> 1 coluna (formulário acima, lista abaixo)

Time displays:
  └─> Grid auto-fit: mínimo 250px
```

## 🔍 Logs e Debugging

### Console do Navegador

```javascript
[INIT] Iniciando aplicação...
[SYNC] Sincronização concluída: {offset: -12, rtt: 24}
[API] Erro ao carregar cientistas: TypeError...
[FORM] Enviando agendamento: {cientista_id: 1, ...}
```

### Network Tab

**Verificar requisições:**
- GET /api/v1/time (sincronização)
- GET /api/v1/cientistas (carregamento inicial)
- GET /api/v1/cientistas/{id}/agendamentos (lista)
- POST /api/v1/agendamentos (criação)
- DELETE /api/v1/agendamentos/{id} (cancelamento)

**Verificar headers:**
- X-Correlation-ID: presente em todas as respostas
- Content-Type: application/json

## 📈 Comparação com Soluções Alternativas

### NTP (Network Time Protocol)

**Cristian:**
- ✅ Simples de implementar
- ✅ Suficiente para aplicações web
- ✅ Precisão de ~10-100ms
- ❌ Não trata deriva (drift) de relógio

**NTP:**
- ❌ Mais complexo
- ✅ Precisão sub-milissegundo
- ✅ Compensa deriva de relógio
- ❌ Overhead desnecessário para web

### Berkeley Algorithm

**Cristian:**
- ✅ Servidor = fonte autoritativa
- ✅ Adequado para cliente-servidor
- ❌ Single point of failure

**Berkeley:**
- ✅ Sem servidor autoritativo
- ✅ Consenso entre pares
- ❌ Complexo para ambiente web

**Escolha:** Cristian é ideal para nosso caso (web app com servidor confiável).

## 🧪 Testes Manuais

### Teste 1: Sincronização visual
- [ ] Displays de tempo atualizam a cada 1s
- [ ] Offset é calculado corretamente
- [ ] RTT está entre 5-100ms (localhost)
- [ ] Indicador mostra "Sincronizado" em verde

### Teste 2: Criação de agendamento
- [ ] Formulário valida campos obrigatórios
- [ ] Horário aceita apenas futuro (>24h)
- [ ] Duração entre 5-120 minutos
- [ ] Sucesso: alerta verde + agendamento aparece na lista
- [ ] Erro: alerta vermelho + mensagem clara

### Teste 3: Cancelamento via HATEOAS
- [ ] Botão "Cancelar" visível apenas em AGENDADO
- [ ] Botão invisível em CANCELADO/CONCLUIDO
- [ ] Confirmação solicitada antes de cancelar
- [ ] Status atualiza para CANCELADO
- [ ] Card muda de cor para vermelho

### Teste 4: Estatísticas
- [ ] Total = soma de todos
- [ ] Agendados conta apenas status AGENDADO
- [ ] Concluídos conta apenas status CONCLUIDO
- [ ] Estatísticas atualizam após criar/cancelar

### Teste 5: Responsividade
- [ ] Desktop: 2 colunas lado a lado
- [ ] Mobile: 1 coluna vertical
- [ ] Touch: botões têm área clicável adequada
- [ ] Scroll: apenas onde necessário

## ✅ Critérios de Validação

- [x] Interface HTML5 criada
- [x] CSS moderno com gradientes e animações
- [x] JavaScript vanilla (sem dependências externas)
- [x] Algoritmo de Cristian implementado corretamente
- [x] Sincronização automática (inicial + a cada 30s)
- [x] Displays de tempo em tempo real
- [x] Formulário de agendamento funcional
- [x] Lista de agendamentos com cards visuais
- [x] Navegação via HATEOAS (links da API)
- [x] Sistema de alertas com feedback visual
- [x] Cancelamento com confirmação
- [x] Estatísticas dinâmicas
- [x] Design responsivo
- [x] Tratamento de erros
- [x] Logs no console para debugging

## 🐛 Troubleshooting

### Interface não carrega

**Sintoma:** Página em branco ou erro 404

**Solução:**
```powershell
# Verificar se templates/ e static/ existem
ls servico-agendamento/templates
ls servico-agendamento/static

# Verificar app/__init__.py
# Deve ter: template_folder='../templates'
```

### Sincronização falha

**Sintoma:** Indicador vermelho "Erro na sincronização"

**Solução:**
```javascript
// Console do navegador
// Verificar erro exato
[SYNC] Erro na sincronização: TypeError...

// Verificar endpoint
fetch('/api/v1/time').then(r => r.json()).then(console.log)
```

### Cientistas não carregam

**Sintoma:** Dropdown mostra "Carregando..."

**Solução:**
```powershell
# Criar cientista via API diretamente
curl -X POST http://localhost:5000/api/v1/cientistas `
  -H "Content-Type: application/json" `
  -d '{
    "nome": "Marie Curie",
    "email": "marie@curie.edu",
    "instituicao": "Universidade de Paris",
    "pais": "França"
  }'
```

### CORS error

**Sintoma:** Console mostra erro de CORS

**Solução:**
```python
# Verificar em app/__init__.py
from flask_cors import CORS
CORS(app)  # Deve estar presente
```

## 📚 Próximos Passos

**Entrega 5:** Containerização com Docker Compose
- Dockerfile para cada serviço
- docker-compose.yml
- Volumes para persistência
- Networks para comunicação

---

**Data de conclusão:** 2025-11-10  
**Status:** ✅ Completo
