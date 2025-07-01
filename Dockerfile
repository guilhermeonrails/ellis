FROM python:3.13.4-alpine3.22

# Define variáveis de ambiente para um comportamento otimizado do Python em contêineres
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Atualiza o pip e instala as dependências de forma otimizada
# Copiar o requirements.txt primeiro aproveita o cache de camadas do Docker.
# Se este arquivo não mudar, o Docker não reinstalará as dependências em builds futuros.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copia o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta 8000, que o uvicorn usará para rodar a API
EXPOSE 8000

# Comando para iniciar a aplicação FastAPI com Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
