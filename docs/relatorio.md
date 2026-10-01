# Assessment - **Desenvolvimento Seguro de Aplicações Web**
**Por João Victor Cícero de M. T. Ramos**

![static/InfnetLogo.png](/static/InfnetLogo.png)

*Instituto Infnet - Setembro de 2026*


### Apresentação do trabalho
A defesa em video deste assessment pode ser encontrada no seguinte link do google drive: 


### Repositório
O repositório referente a este AT pode ser encontrado atraves do seguinte link do **Github** :
- https://github.com/jvcmtr/desenvolvimento_seguro_at/edit/main/docs/relatorio.md

---

# Execução dos exercícios e evidencias: 

## Exercício 1
- Ambiente python configurado, para reproduzir a configuração siga o passo a passo disponivel [Aqui](/setup.md) (`setup.md`)
- Endpoints REST implementados para todas as entidades. Routers separados por controllers.
- Arquivo de teste do endpoint de **usuario** implementado [Aqui](`tests/test_users_controller.py`) (`tests/test_users_controller.py`)


## Exercício 2
- Response models pydantic implementados utilizando DTOs e mapeamento na propria classe.
- Controle de campos feito utilizando *ViewModels*
- Paginas Jinja2 implementadas usando herança de templates. Template base pode ser encontrado [Aqui](app/views/base.html) (`app/views/base.html`).
- Evidencia da proteção contra XSS pode ser econtrada [Aqui](/docs/evidencias/evidencia_ex2.png) (`/docs/evidencias/evidencia_ex2.png`)

#### Evidencia de proteção contra XSS:
[Clique aqui para ver o aruivo evidencia_ex2.png](/docs/evidencias/evidencia_ex2.png)

![/docs/evidencias/evidencia_ex2.png](/docs/evidencias/evidencia_ex2.png)


## Exercício 3
### Avaliação CIA
#### Confidencialidade
O sistema apresenta vulnerabilidades no quesito **Confidencialidade** no sentido em que não apresenta camada de autenticação e permissionamento, fazendo com que informações pessoais possam ser lidas por qualquer usuario, autenticado ou não.

#### Integridade
O sistema é robusto em termos de **Integridade** boa integridade no sentido em que se utiliza de um banco de dados para operações atomicas, mecanismo de "*soft-delete*" e uma classe base de `AuditResource` que registra datas e usuarios responsáveis por criar, editar e apagar entidades do banco. 

#### Disponbilidade
O sistema apresenta algumas vulnerabilidades no quesito **Disponibilidade**. Apesar de se utilizar da assincronissidade do framework FastAPI para lidar melhor com requisições simultaneas, A falta de mecanismos de *rate-limiting*, e a falta de paginação nos endpoints de listagem (como `GET /pacientes`) pode deixar o sistema fragil a ataques de negação de serviço.


### Vulnerabilidades OWASP Top 10
OBS: *Consideram se aqui os padrões vulneraveis existentes somente neste momento do trabalho.*

#### A01:2025 Broken Access Control
> https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/

O sistema não apresenta camada de Autorização/Permissionamento, permitindo que qualquer usuario (cadastrado ou não) realize qualquer operação na API e tenha acesso a qualquer dado cadastrado (com exeção de dados de auditoria). 


#### A02:2025 Security Misconfiguration
> https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/

O Banco de dados utilizado pelo sistema não possui nenhuma configuração de segurança, o que permite que um usuario malicioso acesse diretamente o banco.

A API não esta devidamente configurada para o uso do protocolo HTTPS, tornando-a vulneravel a *sniffing* e outros ataques.

#### A04:2025 Cryptografic Failures
> https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures/

A senhas de usuarios cadastrados não são devidamente criptografadas quando gravadas no banco.

#### A06:2025 Insecure Design
> https://top10.owasp.org/2025/A06_2025-Insecure_Design/

Não existe documentação definindo os requisitos de segurança da aplicação, os níveis de permição de acesso ou *misuse cases* (até o momento)

#### A09:2025 Security Logging e Alerting Failures
> https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/

A aplicação não possui logs de auditoria ou de segurança, o que invisibiliza ataques aos endpoints.

### Tust Boundries

#### Diagrama contendo os Trust Boundries do sistema:
[CLique aqui para vizualizar o aquivo trust_boundries.png](/docs/diagrams/trust_boundries.png)

![/docs/diagrams/trust_boundries.png](/docs/diagrams/trust_boundries.png)


## Exercício 4
### Misuse cases (MU):

#### MU1 - Criação de usuario admin:
Um usuario malicioso enviar um payload ao endpoint `POST /users` contendo `role: "ADMIN"` para elevar seus privilegios.

#### MU2 - Alterações de consultas de terceiros
Um usuario malicioso pode utilizar os endpoints `PUT /consultas/` ou `DELETE /consultas` para alterar ou apagar consultas de outros usuarios.

#### MU3 - Leitura de dados de terceiros
Um usuario malicioso pode acessar os endpoints `GET users/{id}` e `GET /consultas/{id}` para ler informações de terceiros.

### Avaliação STRIDE
**Threat Model :** ![Clique aqui para ver o arquivo threat_model.md](/docs/threat_model.md)

**Avaliação STRIDE :** ![Clique aqui para ver o arquivo STRIDE.csv](/docs/STRIDE.csv)

| Identificador | Categoria STRIDE        | Componente      | Ameaça                                                                                                                                                                                                                    |
| ------------- | ----------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vuln 01       | Spoofing                | Persistencia    | Um usuario pode alterar seu nome, realizar uma alteração em uma entidade e retornar seu nome ou valor original. Isso fará com que a propriedade `updated_by` fique registrada como tendo sido alterada por outro usuario. |
| Vuln 02       | Tampering               | Contrato da API | Os endpoints de alteração (`PUT`) e deleção (`DELETE`) não requerem **autenticação** e não possuem mecanismo de **autorização**, Fazendo com que qualquer usuario possa alterar as entidades do sistema.                  |
| Vuln 03       | Repudiation             | Logica Interna  | O mecanismo de soft delete assim como a classe base de auditoria não são implementados corretamente. O ID do usuario que realiza a operação, é sempre salvo com o mesmo valor.                                            |
| Vuln 04       | Information Disclosure  | Contrato da API | Os endpoints de leitura e listagem (`GET`) não requerem **autenticação** e não possuem mecanismo de **autorização**, Fazendo com que qualquer usuario possa ler as informações das entidades do sistema.                  |
| Vunl 05       | Denial of Service (DoS) | Logica Interna  | A falta de mecanismos de *rate-limiting* permitem que um usuario mal intencionado se aproveitando da falta de paginação nos endpoints de listagem de entidades                                                            |
| vuln 06       | Elevation of Privilege  | Contrato da API | O endpoint de criação  (`POST`) e de alteração (`PUT`) de usuario não realizam nenhum controle o `role=ADMIN`.                                                                                                            |


## Exercício 5
### Componentes do sistema:
- #### Cliente externo
    Navegador do cliente que acessa a Interface Swagger, Paginas HTML, e documentação do sistema

- #### Roteadores e Controladores
    Controladores REST e responsaveis por renderizar paginas web.

- #### Modelagem e regras de negocio
    Modelos, DTOs e a regra de mapeamento entre eles.

- #### Camada de configuração
    Arquivos de configuração e variaveis de ambiente, incluindo chave, e url e outras configurações para comunicação com o banco SQLite.

- #### Banco de dados
    Banco de dados SQLite e camada de abstração usando a biblioteca SQLAlchemy para realizar operações e consultas no banco.

- #### Core *(Não implementado)*
     Classes, midlewares e outras ferramentas utilizadas por outros componentes. Incluindo autenticação, autorização, MFA, algorítimos de hash, logs, dentre outros.

### Fluxo de dados entre componentes do sistema:
[Clique Aqui para acessa o diagrama fluxo_de_dados_entre_componentes.png](/docs/diagrams/fluxo_de_dados_entre_componentes.drawio.png)

![/docs/diagrams/fluxo_de_dados_entre_componentes.drawio.png](/docs/diagrams/fluxo_de_dados_entre_componentes.drawio.png)

### Vetores de ataque:
#### Autenticação e Autorização
- As rotas da API não possuem mecanismo de autorização
- As rotas da API não possuem mecanismo de Autorização ou Logica de permissionamento.
- Não existe validação sobre o atributo `role` no momento de criação de usuario, permitindo que qualquer usuario seja `role=ADMIN`.

#### Integridade
- As informações de auditoria não estão sendo inicializadas adequadamente. A logica não é centralizada e utiliza valores default em vez de cadastrar informações de auditoria.
- Entidades deletadas (com *soft-delete*) não são filtradas no momento da leitura, fazendo com que a funcionalidade de deleção não funcione como o esperado.

#### Infraestrutura
- Os endpoints de listagem não apresentam mecanismo de paginação ou filtragem, permitindo grandes leituras que podem atrapalhar a disponibilidade do sistema.


## Exercício 6
- Login com MFA implementado
- Rotas protegidas
- Verificação de ownership adicionada. 
    > O modelo é uma mistura de RBAC e ABAC, onde usuarios não administradores só podem ler e alterar seus proprios recursos, enquanto administradores tem permissionamento total. 
- Informações de auditoria sendo carregadas corretamente
    > Olhar 'vuln 01', 'vuln 03' e 'vuln 04'
- Rota protegida `/adm-ping` adicionada
- Testes sobre a nova rota adicionados
    > Ambiente de teste adaptado para usar banco de dados temporario. Classe utilitaria criada


## Exercício 7
- Inclui `CLIENT_SECRET` e `CLIENT_ID` como variaveis de ambiente
- FLuxo OAuth 2.0 com *claims* e *scopes* implementado
- Rota exclusiva para integrações M2M `/m2m-ping` implementada


## Exercício 8
**Vulnerabilidades OWASP Top 10**

OBS: *Consideram se aqui os padrões vulneraveis existentes somente neste momento do trabalho.*

#### A01:2025 Broken Access Control
> https://top10.owasp.org/2025/A01_2025-Broken_Access_Control/

O modelo de permissionamento do sistema centraliza sua logica na entidade criadora do recurso, fazendo com que o paciente ou o proficional de saude não tenham acesso a entidade consulta já que somente um deles pode ter criado a entidade. 

#### A02:2025 Security Misconfiguration
> https://top10.owasp.org/2025/A02_2025-Security_Misconfiguration/

O Banco de dados utilizado pelo sistema não possui nenhuma configuração de segurança, o que permite que um usuario malicioso acesse diretamente o banco.

A API não esta devidamente configurada para o uso do protocolo HTTPS, tornando-a vulneravel a *sniffing* e outros ataques.

#### A07:2025 Authentication Failures
> https://top10.owasp.org/2025/A07_2025-Authentication_Failures/

A implementação atual de verificação de MFA usa somente um codigo de 4 digitos, não possui *rate-limiting* e não possui proteção contra sucessos duplicados, tornando o endpoint de verificação de MFA vulneravel à ataques de força bruta.

#### A09:2025 Security Logging e Alerting Failures
> https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures/

A aplicação não possui logs de auditoria ou de segurança, o que invisibiliza ataques aos endpoints.