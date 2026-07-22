"""
Responsável pela criação das tabelas e a inserção do usuário inicial
Basicamente temos 2 metodos importantes:
- get_connection inicia a conexão com o banco de dados, retornando o objeto 'conn'
- cursor é um objeto derivado de conn (conn.cursor), que é o responsavel por executar 
comandos SQL (como consultas e alterações) no servidor, percorrer os resultados 
obtidos e gerenciar transações. """

from database import get_connection

conn = get_connection() #abre o banco de dados

cursor = conn.cursor() # Cuida das consultas SQL.

#Criando tabela de usuários
""" 
Executa um comando SQL que cria a tabela "usuarios" caso ela ainda não exista.
A tabela possui um ID gerado automaticamente, um nome de usuário único e uma senha.
"""
cursor.execute("""

CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    usuario TEXT NOT NULL UNIQUE,

    senha TEXT NOT NULL

)

""")


#Criando a tabela de agendamento

cursor.execute("""
CREATE TABLE IF NOT EXISTS agendamentos(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    paciente TEXT NOT NULL,

    cpf TEXT NOT NULL,

    medico TEXT NOT NULL,

    especialidade TEXT NOT NULL,

    data TEXT NOT NULL,

    horario TEXT NOT NULL,

    convenio TEXT NOT NULL,

    status TEXT NOT NULL

)
""")

# Registrando o primeiro usuário

"""
Insere um usuário no banco de dados; se ele já existir, a operação é ignorada.

"""

cursor.execute("""

INSERT OR IGNORE INTO usuarios(usuario, senha)

VALUES (?, ?)

""", ("admin", "123456"))

conn.commit() # Salva as alterações realizadas no banco de dados.

conn.close() # Encerra a conexão com o banco de dados.

print("Banco criado com sucesso.")