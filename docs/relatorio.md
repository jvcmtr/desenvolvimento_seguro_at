# Assessment - **Desenvolvimento Seguro de Aplicações Web**
![[static/InfnetLogo.png]]

Por João Victor Cícero de M. T. Ramos

*Instituto Infnet - Setembro de 2026*

---

# Apresentação do trabalho
A defesa em video deste assessment pode ser encontrada no seguinte link do google drive: 

---

# Repositório
O repositório referente a este AT pode ser encontrado atraves do seguinte link do **Github** :

---


### Exercício 1
- Ambiente python configurado, para reproduzir a configuração siga o passo a passo disponivel ![Aqui](/setup.md) (`setup.md`)
- Endpoints REST implementados para todas as entidades. Routers separados por controllers.
- Arquivo de teste do endpoint de **usuario** implementado ![Aqui](`tests/test_users_controller.py`)


### Exercício 2
- Response models pydantic implementados utilizando DTOs e mapeamento na propria classe.
- Controle de campos feito utilizando *ViewModels*
- Paginas Jinja2 implementadas usando herança de templates. Template base pode ser encontrado ![Aqui](app/views/base.html) (`app/views/base.html`).
- Evidencia da proteção contra XSS pode ser econtrada ![Aqui](/docs/evidencias/evidencia_ex2.png) (`/docs/evidencias/evidencia_ex2.png`)

**Evidencia de proteção contra XSS:**
![[/docs/evidencias/evidencia_ex2.png]]
