/**
 * Serviço Coordenador - SCTEC
 * Gerenciamento de locks distribuídos para exclusão mútua
 */

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
        // Pode escolher liberar mesmo assim ou negar - vamos liberar
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
