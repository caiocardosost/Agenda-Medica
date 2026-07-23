"""
Biblioteca Flask - modulos:
    - flask - Classe principal (cria o servidor); 
    - render_template - abrir arquivos html
    - request - gerenciar as requisições no Flask
    - redirect - redireciona o usuário de uma URL para outra
Database - script criado que criar/conecta com a base de dados
 """
from flask import Flask, render_template, request, redirect 
from database import (buscar_usuario, salvar_agendamentos, buscar_agendamentos)
import requests
import os

# Cria a aplicação Flask
app = Flask(__name__) #instancia objeto flask (__name__) será substituido pelo nome do arquivo (app)

# Definindo uma rota para a página inicial
"""
Basicamente no bloco a seguir, começamos com um decorator, que é uma função que embrulha 
outra função '@função'. O que acontece é o seguinte:
- app.route chama o metodo route do objeto app com o parametro "/" e a função abaixo dele (def login)
Internamente, 'route' está implementado e em algum momento chama 'func', neste caso a função que o 
decorator passou (login) é executada neste momento
- login executa uma série de operações definidas. Em geral, 'route' mapeia uma requisição para uma função python

Em geral, o fluxo é o seguinte:

- Quando a página é acessada por GET, a aplicação retorna o template login.html, 
exibindo o formulário de login ao usuário.
- Quando o formulário, construido no html é preenchida, ele é enviado como requisição POST, com isso
obtém-se o usuário e a senha informados. A pagina é recarregada como requisão POST.
- Em seguida, consulta o banco de dados para verificar se existe um registro
  com as credenciais fornecidas.
- Caso não encontre o usuário, recarrega a página de login exibindo uma mensagem de erro.
- Caso encontre, redireciona o usuário para a rota "/agenda", responsável por
  obter os agendamentos da API e exibi-los ao usuário.
"""

@app.route("/", methods=["GET", "POST"]) #especificando que a rota aceita get e post
def login(): # se for acessado por get, mostra a tela de login; se post, realiza as validações

    if request.method == "POST":

        usuario = request.form["usuario"] # 'form' recupera dados do formulario html (geralmente credenciais POST)

        senha = request.form["senha"]

        #realiza a busca do usuário no banco de dados, retornando o resultado e um possível erro (tupla)

        resultado, erro = buscar_usuario(usuario, senha)

        #se retornou erro
        if erro:

            return render_template(
                "login.html",
                erro="Não foi possível conectar ao banco de dados."
            )

        #se encontrou o usuário, redireciona para a rota /agenda
        if resultado:

            return redirect("/agenda")

        #se não encontrou o usuário, recarrega a página de login exibindo uma mensagem de erro
        else:

            return render_template(
                "login.html",
                erro="Usuário ou senha inválidos."
            )

    return render_template("login.html")


# Rota agenda:
"""
Após um login bem-sucedido, esta rota é acessada para carregar a agenda médica.
Inicialmente é realizada uma requisição HTTP para a API de agendamentos, que retorna
os registros em formato JSON. Esses dados são validados e armazenados no banco de
dados SQLite da aplicação.
Em seguida, a consulta é realizada sobre os dados armazenados localmente,
permitindo aplicar filtros por paciente, CPF ou médico através do parâmetro
'busca' recebido na URL (ex.: /agenda?busca=joao).
Por fim, os registros encontrados são enviados ao template "agenda.html",
responsável por exibir a tabela utilizando a biblioteca Tabulator.
"""

@app.route("/agenda")
def agenda():

    busca = request.args.get("busca","") # 'args' recupera informação da URL - Geralmente em buscas 'GET'

    # --ALTERAçÃO PARA PÓS IMPLEMENTAÇÃO DO DOCKER - 
    # api_url Recupera a variável de ambiente definida no docker-compose ou usa localhost, caso não
    # esteja rodando em container.
    # API_URL é a variável de ambiente definida no docker-compose.yml, que aponta para o serviço da API.
    api_url = os.getenv("API_URL", "http://localhost:5001/agendamentos")

    # Realiza uma requisição HTTP para obter todos os agendamentos disponíveis na API.
    # Os dados recebidos serão posteriormente armazenados no banco de dados local
    try:
        resposta = requests.get(
            api_url,
            timeout=5
        ) 

        
    except requests.exceptions.ConnectionError:

        return render_template(
            "agenda.html",
            erro="Não foi possível conectar ao servidor de agendamentos.",
            agendamentos=[],
            busca=busca
        )

    #verifica se a resposta da API foi bem-sucedida (código de status 200)
    if resposta.status_code != 200:
        return render_template(
            "agenda.html",
            erro="Erro ao consultar a API.",
            agendamentos=[],
            busca=busca

        )
    # verifica a validade da resposta da API.
    try:
        agendamentos = resposta.json()
    except ValueError:
        return render_template(
        "agenda.html",
        erro="Resposta inválida recebida da API.",
        agendamentos=[],
        busca=busca
    )

    #trata falta de dados na resposta da API:
    
    campos = [
    "paciente",
    "cpf",
    "medico",
    "especialidade",
    "data",
    "horario",
    "convenio",
    "status"
    ]

    for registro in agendamentos:

        for campo in campos:

            if campo not in registro:

                registro[campo] = "Não informado"

    # Atualiza a base de dados local com os agendamentos recebidos da API.
    # Os registros antigos são removidos e substituídos pelos novos. 

    sucesso = salvar_agendamentos(agendamentos)

    if not sucesso:

        return render_template(
            "agenda.html",
            erro="Não foi possível salvar os agendamentos.",
            agendamentos=[],
            busca=busca
        )

    # Consulta os agendamentos armazenados no banco de dados local, aplicando o filtro informado pelo usuário, quando existir.
    agendamentos, erro = buscar_agendamentos(busca)

    if erro:

        return render_template(
            "agenda.html",
            erro="Não foi possível consultar os agendamentos.",
            agendamentos=[],
            busca=busca
        )

    return render_template(

        "agenda.html",

        agendamentos=agendamentos,

        busca=busca

    )


if __name__ == "__main__":
    app.run(host="0.0.0.0",
        port=5000,
        debug=True)
    # app.run serve para iniciar o servidor Flask.
    # parametro Host 0.0.0.0 permite escutar em todas as interfaces de rede.
    # Desta forma, permite que a aplicação Flask seja acessível de fora do contêiner Docker, 
    # permitindo que outros dispositivos na rede acessem a aplicação.