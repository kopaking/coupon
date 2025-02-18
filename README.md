# AUTO POSTING - Coupon Admitad Bot

## 📌 Sobre o Projeto
Este projeto automatiza a postagem de cupons da plataforma Admitad em canais do Telegram. Ele utiliza a biblioteca Pyrogram para interagir com o Telegram e um sistema de manipulação de cupons para facilitar a publicação automática.
Programado em Python. 

## 🚀 Funcionalidades
- Obtenção e processamento de cupons da Admitad
- Envio automático de mensagens para canais do Telegram
- Sistema assíncrono utilizando `asyncio` para eficiência
- Configuração flexível para diferentes canais e formatos de postagem


## 🛠️ Requisitos
Antes de rodar o projeto, certifique-se de ter os seguintes requisitos instalados:
- Python 3.11+
- Bibliotecas:
  - `pyrogram`
  - `asyncio`
  - `sqlite3`
  - `dotenv`

Instale as dependências executando:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

TELEGRAM:
```env
API_ID=checar my.telegram.org/
API_HASH=checar my.telegram.org/
BOT_TOKEN=checar @botfather
CHAT_ID=id do seu canal.
ALLOWED_USER_ID=seu id de conta do telegram.
PHONE_NUMBER=seu número de telefone (da conta do telegram)
```

ADMITAD:
```env
CLIENT_ID=informação de autenticação da sua conta admitad
CLIENT_SECRET=informação de autenticação da sua conta admitad
BASE64_HEADER=informação de autenticação da sua conta admitad
W_ID=informação de autenticação da sua conta admitad
```


## ▶️ Como Executar
Dentro da pasta base do programa, execute:
```bash
python -m coupon.main
```


## 🐛 Debug e Solução de Problemas
Caso encontre problemas com importações:
1. Certifique-se de que os arquivos `__init__.py` existem.
2. Verifique se está rodando o script corretamente a partir do diretório `AUTO POSTING`.
3. Adicione ao `main.py`:
```python
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
```

## 📄 Licença
Este projeto é de uso privado. Caso queira contribuir ou usar como referência, entre em contato com o desenvolvedor.

