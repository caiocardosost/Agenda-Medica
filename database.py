"""Script responsavel pela conexão com a base de dados"""

import sqlite3

DATABASE = "database/agenda.db" #caminho do banco de dados

def get_connection():
    conn = sqlite3.connect(DATABASE) #abre o banco de dados (se não existir, cria)

    conn.row_factory = sqlite3.Row #configura o acesso das colunas pelo nome

    return conn