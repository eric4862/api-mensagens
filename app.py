from flask import Flask
from database import db
from routes import mensagens_bp
from user_routes import usuarios_bp
from comment_routes import comentarios_bp
from flask_jwt_extended import JWTManager
from auth_routes import auth_bp

app = Flask(__name__)   # TEM que vir primeiro

# Configurações
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # segurança simples
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 900
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 604800

# Inicializa
db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

# Registra rotas
app.register_blueprint(auth_bp)
app.register_blueprint(mensagens_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(comentarios_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
