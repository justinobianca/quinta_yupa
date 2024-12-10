from flask import Blueprint, request, render_template, redirect, url_for, session
from conexao import criar_conexao, fechar_conexao

# Criação do Blueprint para os quartos
quartos_bp = Blueprint('quartos', __name__)

# Rota para exibir o formulário de criação de quarto
@quartos_bp.route('novaQuarto', methods=['GET', 'POST'])
def nova_quartos():
    return render_template('adicionar_quarto.html')

# Rota para criar um novo quarto
@quartos_bp.route('novaquartos', methods=['GET', 'POST'])
def criar_quartos():
    if 'usuario' not in session:
        return redirect(url_for('usuarios.login_usuario'))
    
    if request.method == 'POST':
        NOME = request.form['NOME']
        NUMERO = request.form['NUMERO']
        CAMA_DE_SOLTEIRO = request.form['CAMA_DE_SOLTEIRO']
        CAMA_DE_CASAL = request.form['CAMA_DE_CASAL']
        DESCRICAO = request.form['DESCRICAO']
        PRECO = request.form['PRECO']
        IMAGEM = request.form['IMAGEM']

        conn = criar_conexao()
        cursor = conn.cursor()

        try:
            cursor.execute(
                'INSERT INTO quartos(nome, numero, cama_solteiro, cama_casal, descricao, preco, imagem) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (NOME, NUMERO, CAMA_DE_SOLTEIRO, CAMA_DE_CASAL, DESCRICAO, PRECO, IMAGEM)
            )
            conn.commit()
        except Exception as e:
            print(f"Erro ao inserir quarto: {e}")
            return "Erro ao criar o quarto", 500
        finally:
            cursor.close()
            fechar_conexao(conn)

        return redirect(url_for('reservas.nova_reserva'))

    return render_template('adicionar_quarto.html')

# Rota para excluir um quarto
@quartos_bp.route('/excluir/<int:id>', methods=['GET'])
def excluir_quarto(id):
    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        # Excluir reservas associadas ao quarto
        cursor.execute("DELETE FROM reservas WHERE id_quarto = %s", (id,))
        conn.commit()

        # Excluir o quarto após excluir as reservas
        cursor.execute("DELETE FROM quartos WHERE id_quarto = %s", (id,))
        conn.commit()

    except Exception as e:
        print(f"Erro ao excluir quarto com ID {id}: {e}")
        return "Erro ao excluir o quarto", 500
    finally:
        cursor.close()
        fechar_conexao(conn)

    return redirect(url_for('reservas.nova_reserva'))

# Rota para alterar um quarto
@quartos_bp.route('/alterar/<int:id>', methods=['GET', 'POST'])
def alterar_quarto(id):
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        NOME = request.form['NOME']
        NUMERO = request.form['NUMERO']
        CAMA_SOLTEIRO = request.form['CAMA_SOLTEIRO']
        CAMA_CASAL = request.form['CAMA_CASAL']
        DESCRICAO = request.form['DESCRICAO']
        PRECO = request.form['PRECO']
        IMAGEM = request.form['IMAGEM']

        cursor.execute(
            """UPDATE QUARTOS 
            SET nome = %s, numero = %s, cama_solteiro = %s, cama_casal = %s, descricao = %s, preco = %s, imagem = %s
            WHERE id_quarto = %s""",
            (NOME, NUMERO, CAMA_SOLTEIRO, CAMA_CASAL, DESCRICAO, PRECO, IMAGEM, id)
        )
        conn.commit()

        cursor.close()
        fechar_conexao(conn)

        # Redirecionar para reservas após salvar
        return redirect(url_for('reservas.nova_reserva'))

    cursor.execute("SELECT * FROM QUARTOS WHERE id_quarto = %s", (id,))
    quarto = cursor.fetchone()

    cursor.close()
    fechar_conexao(conn)

    return render_template('alterar_quartos.html', quarto=quarto)


 

