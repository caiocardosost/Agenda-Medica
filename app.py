"""
Biblioteca Flask - modulos:
    - flask - Classe principal (cria o servidor); 
    - render_template - abrir arquivos html
    - request - gerenciar as requisições no Flask
    - redirect - redireciona o usuário de uma URL para outra
Database - script criado que criar/conecta com a base de dados
 """
from flask import Flask, render_template, request, redirect 
from database import get_connection
import requests

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
- Quando o formulário, construido no html é preenchi, ele é enviado como requisição POST, com isso
obtém-se o usuário e a senha informados. A pagina é recarregada como requisão POST.
- Em seguida, conecta ao banco de dados e verifica se existe um registro
  com as credenciais fornecidas.
- Caso não encontre o usuário, recarrega a página de login exibindo uma mensagem de erro.
- Caso encontre, realiza uma requisição HTTP através da biblioteca request
com a rota da API (/agendamentos), que por sua vez retorna um json contendo a lista de agendamentos.
"""

@app.route("/", methods=["GET", "POST"]) #especificando que a rota aceita get e post
def login(): # se for acessado por get, mostra a tela de login; se post, realiza as validações

    if request.method == "POST":

        usuario = request.form["usuario"] # 'form' recupera dados do formulario html (geralmente credenciais POST)

        senha = request.form["senha"]

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM usuarios

        WHERE usuario = ?

        AND senha = ?

        """, (usuario, senha)) #Busca as credenciais no banco de dados

        resultado = cursor.fetchone() #recupera a próxima linha do resultado de uma consulta SQL (None, se não houver)

        conn.close() #encerra a conexão com o banco de dados

        if resultado:
            return redirect("/agenda") # Se o usuario for validado, redireciona para a rota 'agenda'

        else:

            return render_template(
                "login.html",
                erro="Usuário ou senha inválidos."
            )

    return render_template("login.html")


# Rota agenda:
"""
Após um login bem-sucedido, esta rota é acessada para carregar
a agenda médica. Inicialmente a busca não existe, logo seu parametro é vazio "". Com isso, api, quando
consultada com parametro vazio (""), retorna toda a tabela de agendamedo. Com ela então renderiza
a pagina html "agenda".
Quando o formulario disponivel para busca no html é preenchido, então uma nova requisição get é realizada
em /agenda com o parametro informado, (ex.: /agenda?busca=joao). Esse parâmetro da busca é então enviado para a API de
agendamentos, que retorna apenas os registros correspondentes.
Os dados recebidos em formato JSON são convertidos para objetos Python e enviados ao 
template "agenda.html", responsável por exibir a tabela ao usuário"""

@app.route("/agenda")
def agenda():

    busca = request.args.get("busca","") # 'args' recupera informação da URL - Geralmente em buscas 'GET'

    resposta = requests.get(
        "http://localhost:5001/agendamentos",
        params={"busca":busca}
    ) # aqui o request monta algo como /agendamentos?busca={valor da variavel busca} - Api então interpreta esse valor

    agendamentos = resposta.json()

    return render_template(

        "agenda.html",

        agendamentos=agendamentos,

        busca=busca

    )


if __name__ == "__main__":
    app.run(debug=True)