from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Habilita configs da pasta instance/
    app = Flask(__name__, instance_relative_config=True)
    # Carrega Config padrão e depois instance/config.py (se existir)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    # Cria todas as tabelas definidas nos models (incluindo `salas`)
    with app.app_context():
        db.create_all()

    # Importa e registra as rotas
    from app import routes
    app.register_blueprint(routes.main)

    return app