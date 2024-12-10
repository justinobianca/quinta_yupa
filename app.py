from flask import Flask, render_template,session,redirect, url_for
from flask_cors import CORS
from rotas.rotas_usuarios import usuarios_bp
from rotas.rotas_reservas import reservas_bp, listar_todas_reservas
from rotas.rotas_quartos import quartos_bp
from rotas.rotas_detalhes import detalhes_bp
from rotas.rotas_registro import registros_bp


app = Flask(__name__)
CORS(app)
app.secret_key = "123456"

app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(quartos_bp, url_prefix='/quartos')
app.register_blueprint(detalhes_bp, url_prefix='/detalhes')
app.register_blueprint(registros_bp, url_prefix='/registros')

@app.route('/')
def home():
    #verificação se esta logado e redirecionamento da página
    if 'usuario' in session:
        # return listar_todas_resenhas()
        return render_template('index.html')
    else: 
        return render_template('index.html')
    
 
@app.route('/detalhes')
def detalhes():
  return render_template('detalhes.html')


if __name__ == "__main__":
    app.run(port=5001,host="localhost",debug=True)



