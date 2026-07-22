"""
Biblioteca Flask - modulos:
    - flask - Classe principal (cria o servidor); 
    - render_template - abrir arquivos html
    - request - gerenciar as requisições no Flask
Database - script criado que criar/conecta com a base de dados
 """
from flask import Flask, render_template, request 
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
- Quando o formulário é enviado por POST, obtém o usuário e a senha informados.
- Em seguida, conecta ao banco de dados e verifica se existe um registro
  com as credenciais fornecidas.
- Caso não encontre o usuário, recarrega a página de login exibindo uma mensagem de erro.
- Caso encontre, realiza uma requisição HTTP através da biblioteca request
com a rota da API (/agendamentos), que por sua vez retorna um json contendo a lista de agendamentos.
"""

@app.route("/", methods=["GET", "POST"]) #especificando que a rota aceita get e post
def login(): # se for acessado por get, mostra a tela de login; se post, realiza as validações

    if request.method == "POST":

        usuario = request.form["usuario"] #recupera o usuário (metodo request.form)

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
            resposta = requests.get(
            "http://localhost:5001/agendamentos"
            )

            agendamentos = resposta.json()

            return str(agendamentos)

        else:

            return render_template(
                "login.html",
                erro="Usuário ou senha inválidos."
            )

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)