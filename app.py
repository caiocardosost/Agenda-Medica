from flask import Flask, render_template #'flask - Classe principal (cria o servidor); render_template - abrir arquivos html

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

"""
@app.route("/") # neste caso, a rota inicial é a raiz - Decorator - Embrulha a função "login" dentro de "route" (Route é um metodo de 'app')
def login():
    return render_template("login.html")

# Inicia o servidor:
if __name__ == "__main__":
    app.run(debug=True) #este metodo (run) faz com que o servidor http://localhost:5000 passe a existir 