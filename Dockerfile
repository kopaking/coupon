# Usar a imagem oficial do Python
FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY . .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Definir a variável de ambiente (opcional)
ENV PYTHONUNBUFFERED=1

# Comando para rodar o bot
CMD ["python", "-m", "coupon.main"]
