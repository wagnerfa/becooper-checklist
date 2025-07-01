from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checklist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        # importa os modelos para criar as tabelas
        from models import Sala, Equipamento, Pessoa, Locacao, EquipamentosLocacao, Devolucao
        db.create_all()

    # registro de blueprints
    from routes.locacao import locacao_bp
    app.register_blueprint(locacao_bp, url_prefix='/locacao')

    return app
