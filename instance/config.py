import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    # Aponta para o checklist.db dentro de instance/
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'checklist.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False