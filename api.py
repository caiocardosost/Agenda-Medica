"""
Api de integração
Cria novo objeto Flask
Retorna um json através do modulo jsonify
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/agendamentos")
def agendamentos():

    dados = [

        {
            "paciente":"João Silva",
            "cpf":"11111111111",
            "medico":"Dr. Pedro",
            "especialidade":"Cardiologia",
            "data":"23/07/2026",
            "horario":"09:00",
            "convenio":"Unimed",
            "status":"Confirmado"
        },

        {
            "paciente":"Maria Oliveira",
            "cpf":"22222222222",
            "medico":"Dra. Ana",
            "especialidade":"Dermatologia",
            "data":"23/07/2026",
            "horario":"10:30",
            "convenio":"Bradesco",
            "status":"Agendado"
        }

    ]

    """"""
    return jsonify(dados) # Retorna os dados em formato JSON.


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False)