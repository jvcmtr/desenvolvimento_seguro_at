# Setup

## 1. Inicialização do ambiente virtual
Crie e acesse o ambiente virtual
```
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instale as dependencias
Execute o pip nas dependencias listadas em `requirements.txt` para instalar as bibliotecas nescessarias para a execução da aplicação.
```
pip install -r requirements.txt
```
Caso queira executar **testes localmente**, instale também as dependencias de teste disponiveis em ``requirements.testes.txt``:
```
pip install -r requirements.test.txt
```

# 3. Configure as variaveis locais
Crie um arquivo `.env` na raiz do projeto e insira as valores adequados para a sua utilização. Caso nescessário, você pode encontrar um exemplo das variaveis da aplicação no arquivo `.env.exemple`, disponivel na raiz do projeto.

> **Lembre-se de incluir as informações de login em `ADMIN_USERNAME` e `ADMIN_PASSWORD`.**


## 4. (opcional) Configure um usuario admin
O banco de dados contendo um usuario admin é automaticamente criado quando o projeto é executado, contudo, caso seja nescessario criar um novo usuario admin execute o seguinte comando:
``` python
python3 create_admin
```
