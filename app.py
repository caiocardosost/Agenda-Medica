"""
Biblioteca Flask - modulos:
    -flask - Classe principal (cria o servidor); render_template - abrir arquivos html
    -request 
Database - script criado que criar/conecta com a base de dados
 """
from flask import Flask, render_template, request 
from database import get_connection

# Cria a aplicação Flask
app = Flask(__name__) #instancia objeto flask (__name__) será substituido pelo nome do arquivo (app)

# Definindo uma rota para a página inicial
"""
Basicamente temos um decorator, que é uma função que embrulha outra função '@função'
O que acontece é o seguinte:
app.route chama o metodo route do objeto app com o parametro "/" e a função abaixo dele (def login)
Internamente, 'route' está implementado e em algum momento chama 'func', neste caso a função que o 
decorator passou (login) é executada neste momento
login retorna um html chamado "login.html" para a função route. A bibliotec render_template busca justamente
a pasta "template" no diretório, e em seguida o arquivo login. 
Em geral, 'route' mapeia uma requisição para uma função python

"""

"""
Rota principal da aplicação responsável pelo login.

- Quando a página é acessada por GET, exibe o formulário de login.
- Quando o formulário é enviado por POST, obtém o usuário e a senha informados.
- Em seguida, conecta ao banco de dados e verifica se existe um registro
  com as credenciais fornecidas.
- Se encontrar um usuário correspondente, retorna uma mensagem de sucesso.
- Caso contrário, recarrega a página de login exibindo uma mensagem de erro.
- Por fim, a aplicação é iniciada em modo de depuração (debug) quando este
  arquivo é executado diretamente.
"""

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]

        senha = request.form["senha"]

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM usuarios

        WHERE usuario = ?

        AND senha = ?

        """, (usuario, senha))

        resultado = cursor.fetchone()

        conn.close()

        if resultado:

            return "Login realizado!"

        else:

            return render_template(
                "login.html",
                erro="Usuário ou senha inválidos."
            )

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)