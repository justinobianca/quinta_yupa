import mysql.connector

def criar_conexao():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password ="ADMIN",
        database = "quinta_do_ypua"
    )

def fechar_conexao(conexao):
    if conexao: 
        conexao.close()