import mysql.connector


def create(nome, email, senha):
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567',
    database='usuarios',
    )
    cursor = conexao.cursor()

    comando = f'INSERT INTO dados (nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")'
    cursor.execute(comando)
    conexao.commit() # edita o banco de dados
    cursor.close()
    conexao.close()

def read():
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567',
    database='usuarios',
    )
    cursor = conexao.cursor()

    comando = 'select * from dados'
    cursor.execute(comando)
    resultado = cursor.fetchall() # ler o banco de dados
    cursor.close()
    conexao.close()
    return resultado

def update(nome, senha):
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567',
    database='usuarios',
    )
    cursor = conexao.cursor()

    comando = f'UPDATE dados SET senha = "{senha}" WHERE nome = "{nome}"'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()

def delete(nome):
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567',
    database='usuarios',
    )
    cursor = conexao.cursor()

    comando = f'DELETE FROM dados WHERE nome = "{nome}"'
    cursor.execute(comando)
    conexao.commit()
    cursor.close()
    conexao.close()


