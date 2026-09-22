# Assessment - **Desenvolvimento Seguro de Aplicações Web**
*Repositorio utilizado para o cumprimento do assessment da disciplina de Desenvolvimento Seguro de Aplicações Web (2026.3T). Por João Ramos.*

## Documentação e relatório
O relatório referente ao desenvolvimento deste projeto, assim como diagramas e outros documentos relativos ao projeto podem ser encontrados em `/docs/`

## Executando o projeto
Para executar o projeto, siga o passo a passo disponível em `/setup.md` e execute o seguinte comando:
```
python3 run
```

Para executar a suite de testes do projeto execute:
```
python3 -m pytest -v
```


# **Estrutura da Aplicação** (`app/`)

Pasta principal do projeto contendo codigos python da aplicação. Contém o script de inicialização `main.py` e o arquivo de configuração `config.py` que inicializa as variaveis de ambiente. 

É subdividida nos seguintes modulos:
### `core/`
Scripts, configurações e ferramentas centrais para diversos outros modulos do sistema, como por exemplo Autenticação.

### `database/`
Arquivos para configuração e comunicação com o banco de dados.

### `models/`
Contém as principais classes do sistema, incluindo tanto classes do domínio de **Consultas** como classes para o funcionamento da aplicação (**Core**).

### `routes/`
Contem as rotas to sistema divididas em *controllers*. Controllers de entidades do sistema respeitam o padrão REST, enquanto `pages_controller` e `misc_controller` são usados para servir arquivos html e ter endpoints utilitarios respectivamente.

> Por fins de divisão de responsabilidade, os DTOs (*Data Transfer Objects*) também ficam guardados aqui, já que eles dizem respeito ao contrato dos endpoints e não à lógica de negocio do domínio de consultas.

### `views/`
Contém os templates *Jinja2* utilizados para a renderização de paginas html com base nos dados

### `tools/`
Arquivos contendo script utilitarios para serem usados pelo desenvolvedor. **Não confundir com o diretorio comumente enccontrado em projetos `utils/`**

# **Estrutura do Projeto**

### `data/`
Diretorio onde é armazenado dados da apicação, incluindo o arquivo do banco de dados e arquivos de log.

### `docs/`
Diretorio contendo a maior parte da documentação do projeto, incluindo respostas às questões do assessment e evidencias da execução dos exercícios. Pode ser acessado via API atravéz de `/documents/`

### `static/`
Contém arquivos estáticos utilizados pelos templates `Jinja2` como imagens e arquivos css

### `tests/`
Contem a camada de teste da aplicação

### Outros arquivos relevantes:
- **`setup.md`** : Guia para o setup local do projeto.
- **`requirements.txt`** : Lista as dependencias do projeto, incluindo versionamento.
- `run` e `create_admin` : scripts para rodar a aplicação e criar um usuario, respectivamente.

 