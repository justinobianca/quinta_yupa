from flask import Blueprint, request, render_template, redirect, url_for, session
from conexao import criar_conexao, fechar_conexao
from hashlib import sha256


usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/novousuario', methods=['GET', 'POST'])
def criar_usuarios():
    if request.method == 'POST':
        NOME = request.form['NOME']
        NOME_USUARIO = request.form['NOME_USUARIO']
        SENHA = request.form['SENHA']
        EMAIL = request.form['EMAIL']
        CPF = request.form['CPF']
        TIPO = request.form['TIPO']
        
        print(NOME, NOME_USUARIO, SENHA, EMAIL, CPF, TIPO)
        # Criptografa a senha
        senhaCripto = sha256(SENHA.encode('utf-8')).hexdigest()

        conn = criar_conexao()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO usuarios(nome, nome_usuario, senha, email, cpf, tipo) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (NOME, NOME_USUARIO, senhaCripto, EMAIL, CPF, TIPO))
        
        conn.commit()
        cursor.close()
        fechar_conexao(conn)
        return render_template('login.html', mensagem='Usuário criado com sucesso')

    return render_template('cadastrar_usuario.html')

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == "POST":
        NOME_USUARIO = request.form['NOME_USUARIO']
        SENHA = request.form['SENHA']
        TIPO = request.form['tipo']

        conn = criar_conexao()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT SENHA, NOME_USUARIO, ID_USUARIO, TIPO FROM USUARIOS WHERE NOME_USUARIO = %s and TIPO = %s", (NOME_USUARIO, TIPO, ))
        senhaBanco = cursor.fetchone()
        cursor.close()
        fechar_conexao(conn)

        if senhaBanco and checar_senha(senhaBanco['SENHA'], SENHA):
            session['usuario'] = {
                'id_usuario': senhaBanco['ID_USUARIO'],
                'tipo': senhaBanco['TIPO']
            }

            # Redireciona para a página de reservas, independentemente do tipo
            return redirect(url_for('reservas.nova_reserva'))  

        else:
            return render_template('login.html', mensagem='Login Incorreto')
    
    return render_template('login.html')

def checar_senha(senhaBanco, senha):
    senha_convertida = sha256(senha.encode('utf-8')).hexdigest()
    return senha_convertida == senhaBanco

@usuarios_bp.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove o usuário da sessão
    return redirect(url_for('home'))
