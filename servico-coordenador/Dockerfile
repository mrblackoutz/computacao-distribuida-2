# Usar imagem oficial do Node.js 18 (Alpine para menor tamanho)
FROM node:18-alpine

# Metadados
LABEL maintainer="SCTEC Project"
LABEL description="Serviço Coordenador - SCTEC"

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências (apenas produção)
RUN npm i --only=production && \
    npm cache clean --force

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 3000

# Variáveis de ambiente padrão
ENV NODE_ENV=production \
    PORT=3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

# Usuário não-root para segurança
USER node

# Comando para iniciar
CMD ["node", "server.js"]
