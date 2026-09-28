# 1. Ativos principais
- **Dados de entidaes do sistema:** Informações armazenadas sobre os pacientes, proficionais e consultas.
- **Dados de Usuários:** Credenciais, informações pessoais e dados de sessão.
- **Credenciais e Segredos :** Tokens de autenticação (JWT), senhas e variaveis de ambiente.
- **Disponibilidade e Recursos do Servidor:** Memória, Disco, processamento (CPU) e largura de banda da maquina e rede onde a API é executada.

# 2. Superficies de ataque
### Endpoints REST:
Os controladores a seguir que possuem operações REST para manipulação das entidades do sistema: 
- `/users`
- `/pacientes`
- `/proficionais`
- `/consultas` 

### Paginas de visualização HTML:
O controllador `/html` fornesce informações das entidades do sistema via paginas html.

### Persistencia:
O banco de dados utiliza sqlite e armazena os dados em um arquivo.db

# 3. Ameaças identificadas (STRIDE)
![Clique aqui para ver o arquivo STRIDE.csv](/docs/STRIDE.csv)

| Identificador | Categoria STRIDE        | Componente      | Ameaça                                                                                                                                                                                                                    |
| ------------- | ----------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vuln 01       | Spoofing                | Persistencia    | Um usuario pode alterar seu nome, realizar uma alteração em uma entidade e retornar seu nome ou valor original. Isso fará com que a propriedade `updated_by` fique registrada como tendo sido alterada por outro usuario. |
| Vuln 02       | Tampering               | Contrato da API | Os endpoints de alteração (`PUT`) e deleção (`DELETE`) não requerem **autenticação** e não possuem mecanismo de **autorização**, Fazendo com que qualquer usuario possa alterar as entidades do sistema.                  |
| Vuln 03       | Repudiation             | Logica Interna  | O mecanismo de soft delete assim como a classe base de auditoria não são implementados corretamente. O ID do usuario que realiza a operação, é sempre salvo com o mesmo valor.                                            |
| Vuln 04       | Information Disclosure  | Contrato da API | Os endpoints de leitura e listagem (`GET`) não requerem **autenticação** e não possuem mecanismo de **autorização**, Fazendo com que qualquer usuario possa ler as informações das entidades do sistema.                  |
| Vunl 05       | Denial of Service (DoS) | Logica Interna  | A falta de mecanismos de *rate-limiting* permitem que um usuario mal intencionado se aproveitando da falta de paginação nos endpoints de listagem de entidades                                                            |
| vuln 06       | Elevation of Privilege  | Contrato da API | O endpoint de criação  (`POST`) e de alteração (`PUT`) de usuario não realizam nenhum controle o `role=ADMIN`.                                                                                                            |


# 4. Mitigações
- ### Mecanismo de Soft-Delete *(Implementado)*
    As rotas `DELETE` não deletam os dados do banco, garantindo a integridade de auditoria.

- ### Restrição na leitura e cadastro de dados *(Implementado)*
    DTOs pydandic são usados para definir as assinaturas dos endpoints, garantindo que os modelos brutos não sejam expostos. 

- ### Proteção contra injeção SQL *(Implementado)*
    São utilizadas as funções da biblioteca SQLAlchemy e injeção de dependencia para operações no banco, protegendo o sistema contra injeção de SQL para queries no banco.

- ### Proteção contra injeção XSS *(Implementado)*
    Os modelos pydantic, assim como os templates Jinja2 protegem os usuarios contra injeção de scripts maliciosos executaos no browzer do cliente.

- ### Classe base de auditoria *(Parcialmente implementado)*
    Uma classe base de auditoria é herdada pelos modelos garantindo que eles possuam campos de auditoria adequado. contudo, o preenchimento destes campos ainda não esta devidamente correto.

- ### Mecanismo de autenticação *(⚠NÃO IMPLEMENTADO)*
    O sistema não possui camada de autenticação, permitindo que usuarios não cadastrados realizem operações no sistema.

- ### Mecanismo de autorização *(⚠NÃO IMPLEMENTADO)*
    O sistema não possui mecanismo de autorização, permitindo que um usuario realize leitura e gravação em entidades de terceiros. 

- ### Mecanismo de rate-limiting *(⚠NÃO IMPLEMENTADO)*
    O sistema não possui mecanismo de *rate-limiting*, ficando vulneravel a ataques de negação de serviço.
