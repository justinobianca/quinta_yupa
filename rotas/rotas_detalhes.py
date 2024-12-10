from flask import Blueprint, request, render_template, redirect, url_for,session
from conexao import criar_conexao,fechar_conexao

#cria rota, criar quarto.
detalhes_bp = Blueprint('detalhes', __name__)

@detalhes_bp.route('/detalhes/<int:id>', methods=['GET', 'POST'])
def detalhes_quarto(id):
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM QUARTOS WHERE id_quarto = %s", (id,))
    quarto = cursor.fetchone()

    cursor.close()
    fechar_conexao(conn)

    return render_template('detalhes.html', quarto = quarto)