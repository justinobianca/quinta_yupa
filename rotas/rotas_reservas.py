from flask import Blueprint, request, render_template, redirect, url_for,session
from conexao import criar_conexao,fechar_conexao


reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('novaReserva', methods=['GET', 'POST'])
def nova_reserva ():
    conn= criar_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM  QUARTOS')
    quartos = cursor.fetchall()
    
    return render_template('reservas.html',quartos=quartos)

@reservas_bp.route('novareservas', methods=['GET','POST'])
def criar_reservas():
    #validação se meu usuario esta na sessão
    if 'usuario' not in session:
        return redirect(url_for('usuarios.login_usuario'))
    
    if request.method == 'POST':
        TITULO = request.form['TITULO']
        RESERVA = request.form['RESERVA'] 
        IMAGEM = request.form['FOTO']

        DATA_CADASTRO = request.form['DATA_CADASTRO']
        ID_USUARIO = session.get('usuario')['id_usuario']

        conn = criar_conexao()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO RESERVAS(titulo, quarto, data_cadastro, imagem, id_usuario)'
                       "VALUES (%s, %s, %s, %s, %s)", (TITULO,RESERVA,DATA_CADASTRO, IMAGEM, ID_USUARIO))
        conn.commit()
        cursor.close()
        fechar_conexao(conn)
        return redirect(url_for('reservas.listar_reservas'))
    

      
    conn= criar_conexao()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM USUARIOS')
    editoras = cursor.fetchall()
    usuario_nome = session.get('nome_usuario')

    

    cursor.close()
    fechar_conexao(conn)
    return render_template('nova_reservas.html', editoras = editoras, usuario_nome = usuario_nome, livros = None)

@reservas_bp.route('/listar_reservas', methods=['GET'])
def listar_todas_reservas():
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    #Consulta para retornar todos os livros, ordenados pelos mais recentes
    cursor.execute("""
    SELECT * FROM reservas ORDER BY id_quarto DESC;
""")
    
    reservas = cursor.fetchall()
    cursor.close()
    fechar_conexao(conn)
    return render_template('index.html', reservas = reservas)

@reservas_bp.route('/listar', methods =['GET'])
def listar_reservas():
    if 'usuario' not in session or 'id_usuario' not in session['usuario']:
        return redirect(url_for('usuarios.login_usuario'))
    
    id_usuario_logado = session['usuario']['id_usuario']
    PESQUISAR = request.args.get('PESQUISAR')
    conn = criar_conexao()
    cursor = conn.cursor(dictionary=True)

    if PESQUISAR:
        cursor.execute("""
        SELECT r.id_reserva, r.titulo, r.reserva, r.imagem, u.nome AS nome_usuario
                       FROM reservas r
                       LEFT JOIN usuarios u  ON r.id_usuario = u.id_usuario
                       WHERE r.id_usuario = %s
                       AND (r.titulo LIKE %s OR r.reserva LIKE %s)    
        """,(id_usuario_logado, '%' + PESQUISAR + '%','%' + PESQUISAR + '%'))
    else:
        cursor.execute("""
                       SELECT r.id_reserva, r.titulo, r.reserva, r.data_cadastro,r.imagem, u.nome AS nome_usuario
                       FROM reservas r
                       LEFT JOIN usuarios u ON r.id_usuario = u.id_usuario
                       WHERE r.id_usuario = %s
        """, (id_usuario_logado,))

    reservas = cursor.fetchall()
    cursor.close()
    fechar_conexao(conn)
    return render_template('livros.html', reservas = reservas)  

