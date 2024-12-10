from flask import Blueprint, render_template, session
import pymysql
from flask import current_app



from flask import current_app

def buscar_quarto_por_id(id):
    db = current_app.config['DB_CONNECTION']  # Isso deve ser acessado dentro de um contexto de app
    cursor = db.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM quartos WHERE id_quarto = %s"
    cursor.execute(query, (id,))
    return cursor.fetchone()


detalhes_quarto = Blueprint('detalhes_quarto', __name__)

def buscar_quarto_por_id(id):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    query = """
        SELECT id_quarto, nome, numero, cama_solteiro, cama_casal, preco, descricao, imagem
        FROM quartos
        WHERE id_quarto = %s
    """
    cursor.execute(query, (id,))
    return cursor.fetchone()

@detalhes_quarto.route('/quarto/<int:id>', methods=['GET'])
def detalhes(id):
    quarto = buscar_quarto_por_id(id)
    if not quarto:
        return "Quarto não encontrado!", 404
    return render_template('detalhes.html', quarto=quarto)
