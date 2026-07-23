# Agenda Médica

Aplicação web desenvolvida em Python utilizando Flask como parte de um desafio técnico.

O sistema permite autenticação de usuários utilizando SQLite, integração com uma API HTTP simulada para obtenção dos agendamentos e armazenamento local desses dados para realização de consultas e filtros.

---

## Tecnologias utilizadas

- Python 3
- Flask
- SQLite
- Requests
- Tabulator (tabela HTML)
- Docker
- Docker Compose

---

## Funcionalidades

- Login de usuários utilizando banco SQLite;
- Validação de credenciais;
- Consumo de API REST para obtenção dos agendamentos;
- Exibição dos agendamentos em tabela utilizando Tabulator;
- Busca de agendamentos por paciente, CPF ou médico;
- Tratamento de falhas de conexão com banco de dados e API;
- Execução da aplicação utilizando Docker.

---

## Estrutura do projeto

```
AgendaMedica/
│
├── app.py                 # Aplicação principal
├── api.py                 # API simulada de agendamentos
├── database.py            # Conexão com SQLite
├── seed.py                # Criação do banco e usuário de teste
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── templates/
│   ├── login.html
│   └── agenda.html
│
└── database/
    └── agenda.db
```

---

## Usuário de teste

O script 'seed.py` é utilizado para inicializar o banco de dados, criando as tabelas e um usuário inicial de teste.

As credenciais são:

```
Usuário: admin
Senha: 123456
```


---

## Executando sem Docker

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Criar o banco de dados

```bash
python seed.py
```

### Executar a API

```bash
python api.py
```

### Executar a aplicação

Em outro terminal:

```bash
python app.py
```

A aplicação ficará disponível em:

```
http://localhost:5000
```

---

## Executando com Docker

Construir as imagens:

```bash
docker compose build
```

Iniciar os containers:

```bash
docker compose up
```

A aplicação estará disponível em:

```
http://localhost:5000
```

Para finalizar:

```bash
docker compose down
```

---

## Tratamento de falhas implementado

A aplicação realiza tratamento para os seguintes cenários:

- Login inválido;
- Erro de conexão com o banco de dados;
- Indisponibilidade da API;
- Resposta JSON inválida;
- Campos obrigatórios ausentes na resposta da API.

Quando possível, os registros continuam sendo exibidos, preenchendo campos ausentes com **"Não informado"**, evitando interrupções na utilização do sistema.

---

## Observações

A API de agendamentos foi implementada como um serviço separado dentro do projeto para simular a comunicação entre aplicações via requisições HTTP, conforme solicitado no desafio.

---

## Processo de desenvolvimento

O foco principal do desenvolvimento foi a implementação da lógica de backend, incluindo:
- estruturação da aplicação Flask;
- autenticação de usuários;
- comunicação HTTP entre serviços;
- integração com banco SQLite;
- tratamento de erros e cenários de falha;
- organização da arquitetura da aplicação.

Como este foi o primeiro contato do desenvolvedor com parte dos conceitos e ferramentas utilizados na aplicação, foram utilizadas ferramentas de Inteligência Artificial como apoio durante o processo de desenvolvimento. A IA atuou como copiloto de programação, auxiliando na estruturação de componentes, revisão de código, esclarecimento de conceitos e, principalmente, no desenvolvimento dos elementos de frontend, como HTML, CSS e JavaScript.

O meu objetivo com o projeto foi compreender o funcionamento de uma aplicação web integrada, explorando a comunicação entre frontend, backend, banco de dados e serviços externos. Minha idéia é o projeto servir como uma porta de entrada para o desenvolvimento web, permitindo adquirir conhecimentos que possibilitem a criação de aplicações futuras de forma mais produtiva e autônoma.
