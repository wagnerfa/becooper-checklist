import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    # URL do banco; aqui usamos SQLite local, mas pode apontar para Postgres, MySQL etc.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.dirname(__file__), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
