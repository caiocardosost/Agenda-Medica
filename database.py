"""Script responsavel pela conexão com a base de dados"""

import sqlite3

DATABASE = "database/agenda.db" #caminho do banco de dados

def get_connection():
    conn = sqlite3.connect(DATABASE) #abre o banco de dados (se não existir, cria)

    conn.row_factory = sqlite3.Row #configura o acesso das colunas pelo nome

    return conn


"""
Armazena os agendamentos recebidos da API no banco de dados local.

Antes da inserção, remove os registros existentes para manter a base
sincronizada com os dados retornados pela API.

Retorna True quando a operação é realizada com sucesso e False em caso de erro (neste caso, se não conseguiu conectar
com o banco de dados).
"""

def salvar_agendamentos(agendamentos):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        # limpa dados antigos
        cursor.execute("DELETE FROM agendamentos")


        for registro in agendamentos:

            cursor.execute("""
            INSERT INTO agendamentos
            (
                paciente,
                cpf,
                medico,
                especialidade,
                data,
                horario,
                convenio,
                status
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """,
            (
                registro["paciente"],
                registro["cpf"],
                registro["medico"],
                registro["especialidade"],
                registro["data"],
                registro["horario"],
                registro["convenio"],
                registro["status"]
            ))


        conn.commit()

        conn.close()

        return True


    except sqlite3.Error:

        return False


"""
Consulta um usuário no banco de dados a partir do usuário e senha informados.

Retorna uma tupla contendo:
- o usuário encontrado (ou None);
- um possível erro de acesso ao banco de dados (ou None).
"""
def buscar_usuario(usuario, senha):
    try:
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE usuario = ?
            AND senha = ?
        """,
        (
            usuario,
            senha
        ))

        resultado = cursor.fetchone()

        #convertendo para dicionário, caso o resultado não seja None.
        if resultado:
            resultado = dict(resultado)

        conn.close()

        return resultado, None
    
    except sqlite3.Error as erro:

        return None, erro
    

"""
Realiza a consulta dos agendamentos armazenados no banco de dados.

Caso um parâmetro de busca seja informado, filtra os registros pelos campos
paciente, CPF ou médico utilizando o operador LIKE. Caso contrário,
retorna todos os agendamentos cadastrados.

Retorna uma tupla contendo:
- resultado da consulta;
- erro (None quando a operação é executada com sucesso).
"""

def buscar_agendamentos(busca=""):

    try:

        conn = get_connection()

        cursor = conn.cursor()


        if busca:

            cursor.execute("""
                SELECT *
                FROM agendamentos
                WHERE paciente LIKE ?
                OR cpf LIKE ?
                OR medico LIKE ?
            """,
            (
                f"%{busca}%",
                f"%{busca}%",
                f"%{busca}%"
            ))

        else:

            cursor.execute("""
                SELECT *
                FROM agendamentos
            """)


        resultado = cursor.fetchall()

        agendamentos = [dict(registro) for registro in resultado] # converte os registros retornados em dicionários.

        conn.close()

        return agendamentos, None


    except sqlite3.Error as erro:

        return [], erro