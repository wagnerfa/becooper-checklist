from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)


    db.init_app(app)

    # registra as rotas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)


    with app.app_context():
        from . import models
        db.create_all()

    return app
