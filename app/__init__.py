from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # inicializa DB
    db.init_app(app)

    # cria as tabelas, se não existirem
    with app.app_context():
        from . import models
        db.create_all()

    # registra as rotas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
