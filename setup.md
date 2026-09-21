# Setup

## 1. Inicialização do ambiente virtual
Crie e acesse o ambiente virtual
```
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instale as dependencias
Execute o pip nas dependencias listadas em `requirements.txt`
```
pip install -r requirements.txt
```

# 3. Configure as variaveis locais
Crie um arquivo `.env` na raiz do projeto. segue aqui uma recomendação de variaveis a serem usadas:
```.env
DATABASE_URL=sqlite:///./data/joao_ramos_consultas_database.db
IS_DEV=True
ADMIN_USERNAME=SEU_USUARIO
ADMIN_PASSWORD=SUA_SENHA
```
> **Lembre-se de substituir `ADMIN_USERNAME` e `ADMIN_PASSWORD` pelos valores desejados.**


## 4. (opcional) Configure um usuario admin
O banco de dados contendo um usuario asmin é automaticamente criado quando o projeto é executado, contudo, caso seja nescessario criar um novo usuario admin execute o seguinte comando:
``` python
python3 create_admin
```
