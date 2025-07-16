from datetime import datetime
import uuid
from . import db


class Sala(db.Model):

    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)

class Equipamento(db.Model):

    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)

class Formulario(db.Model):
    __tablename__ = 'formularios'
    id = db.Column(db.Integer, primary_key=True)
    nome_locatario = db.Column(db.String(100), nullable=False)
    email_locatario = db.Column(db.String(120), nullable=False)
    telefone_locatario = db.Column(db.String(30), nullable=True)
    sala = db.Column(db.String(100), nullable=False)
    data_locacao = db.Column(db.DateTime, default=datetime.utcnow)


    observacao_responsavel_coop = db.Column(db.Text, nullable=True)
    observacao_locatario = db.Column(db.Text, nullable=True)
    equipamentos = db.Column(db.Text, nullable=True)


    validation_token = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    equipamentos_validados = db.Column(db.Text, nullable=True)
    data_validacao_locatario = db.Column(db.DateTime, nullable=True)

    fotos = db.relationship(
        'Foto',
        backref='formulario',
        lazy=True,
        cascade='all, delete-orphan'
    )

class Foto(db.Model):
    __tablename__ = 'fotos'
    id = db.Column(db.Integer, primary_key=True)
    id_formulario = db.Column(
        db.Integer,
        db.ForeignKey('formularios.id'),
        nullable=False
    )
    caminho_foto = db.Column(db.String(255), nullable=False)
