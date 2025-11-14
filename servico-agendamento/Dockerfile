# Usar imagem oficial do Python 3.13
FROM python:3.13-slim

# Metadados
LABEL maintainer="SCTEC Project"
LABEL description="Serviço de Agendamento - SCTEC"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p logs instance && chmod 777 logs instance

# Copiar e expor entrypoint (ajusta permissões em volumes montados antes de iniciar)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expor porta
EXPOSE 5000

# Variáveis de ambiente padrão
ENV FLASK_APP=run.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    COORDENADOR_URL=http://coordenador:3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/v1/time')"

# Usar entrypoint que ajusta permissões e depois executa o comando
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "run.py"]
