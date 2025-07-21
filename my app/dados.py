import mysql.connector


def create(nome=None, email=None, senha=None, idioma=None, palavra=None, cadastro = False):
    conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234567',
    database='usuarios',
    )
    cursor = conexao.cursor()

    if cadastro == False:
        comando = f'INSERT INTO dados (nome, email, senha) VALUES ("{nome}", "{email}", "{senha}")'
        cursor.execute(comando)
        conexao.commit()
        cursor.close()
        conexao.close()
    
    else:
        comando = f'INSERT INTO palavras (nome, idioma, palavra) VALUES ("{nome}", "{idioma}", "{palavra}")'
        cursor.execute(comando)
        conexao.commit()
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


def buscar_palavras_por_idioma(nome):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234567',
        database='usuarios',
    )
    cursor = conexao.cursor()

    comando = f'SELECT idioma, palavra FROM palavras WHERE nome = "{nome}"'
    cursor.execute(comando)
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    # Retorna um dicionário: { "Inglês": ["dog", "cat"], "Espanhol": ["hola"] }
    palavras_por_idioma = {}
    for idioma, palavra in resultado:
        if idioma not in palavras_por_idioma:
            palavras_por_idioma[idioma] = []
        palavras_por_idioma[idioma].append(palavra)
    return palavras_por_idioma
