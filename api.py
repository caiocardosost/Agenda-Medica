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
    busca = request.args.get("busca","").lower()

    if busca == "":
        return jsonify(dados)

    resultado = []

    for registro in dados:

        if (

            busca in registro["paciente"].lower()

            or

            busca in registro["cpf"]

            or

            busca in registro["medico"].lower()

        ):

            resultado.append(registro)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False)