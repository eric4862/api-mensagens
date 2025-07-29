from flask import Flask
from database import db
from routes import mensagens_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(mensagens_bp)

if __name__ == '__main__':
    app.run(debug=True)
