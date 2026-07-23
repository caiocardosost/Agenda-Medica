# Usa a imagem base do Python como base para o contêiner:
FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner:
WORKDIR /app

# Copia o arquivo de requisitos do diretório atual para o diretório de trabalho:
COPY requirements.txt .

# Instala as dependências do projeto listadas no arquivo requirements.txt:
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do diretório atual para o diretório de trabalho dentro do contêiner:
COPY . .

# aqui entraria CMD ["python", "app.py"], mas como tenho 2 arquivos, vou deixar para o docker-compose definir qual rodar.