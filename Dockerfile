FROM python:3.13.4-alpine3.22
WORKDIR /app

# Instala compiladores e dependências do sistema
RUN apk add --no-cache build-base

# Copia apenas o requirements.txt para aproveitar o cache de dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Expõe a porta padrão do FastAPI/Uvicorn
EXPOSE 8000

# Comando padrão para rodar a aplicação em modo desenvolvimento
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]