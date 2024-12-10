from flask import Blueprint, request, render_template, redirect, url_for, session
from conexao import criar_conexao, fechar_conexao

registros_bp = Blueprint('registros', __name__)

@registros_bp.route('/registrar/<int:id_quarto>', methods=['GET', 'POST'])
def registrar(id_quarto):
    if 'usuario' not in session:
        return redirect(url_for('usuarios.login_usuario'))

    if request.method == 'POST':
        # Recebe os dados do formulário
        id_usuario = session['usuario']['id_usuario']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        adult_count = request.form['adult_count']
        preco_total = request.form['preco_total']

        # Valida os dados (exemplo: verifica se o preço total é um número válido)
        try:
            preco_total = float(preco_total)
        except ValueError:
            return "Erro: Preço total inválido", 400
        
        if not checkin or not checkout or preco_total <= 0:
            return "Erro: Dados inválidos", 400

        # Inserir no banco de dados
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO RESERVAS (id_usuario, id_quarto, data_checkin, data_checkout, qtd_adultos, preco_total)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (id_usuario, id_quarto, checkin, checkout, adult_count, preco_total))
        conn.commit()

        # Obtém o ID da reserva recém-criada
        id_reserva = cursor.lastrowid
        cursor.execute('SELECT * FROM RESERVAS WHERE id_reserva = %s', (id_reserva,))
        reserva = cursor.fetchone()
        cursor.close()
        fechar_conexao(conn)

        return render_template('finalizacao.html', reserva=reserva)

    # Recupera os dados do quarto
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM QUARTOS WHERE id_quarto = %s', (id_quarto,))
    quarto = cursor.fetchone()
    cursor.close()
    fechar_conexao(conn)

    if not quarto:
        return "Quarto não encontrado", 404

    return render_template('detalhes.html', quarto=quarto)
