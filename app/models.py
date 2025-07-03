from datetime import datetime
from . import db

class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sala {self.nome} ({self.capacidade} pessoas)>'

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Equipamento {self.nome} — {self.quantidade} unid.>'

class Formulario(db.Model):
    __tablename__ = 'formularios'
    id = db.Column(db.Integer, primary_key=True)
    nome_locatario = db.Column(db.String(100), nullable=False)
    email_locatario = db.Column(db.String(120), nullable=False)
    telefone_locatario = db.Column(db.String(30), nullable=True)
    data_locacao = db.Column(db.DateTime, default=datetime.utcnow)
    observacao_responsavel_coop = db.Column(db.Text, nullable=True)
    observacao_locatario = db.Column(db.Text, nullable=True)

    assinatura = db.Column(db.String(255), nullable=True)

    equipamentos = db.Column(db.Text, nullable=True)

    # relacionamento 1:N com fotos
    fotos = db.relationship('Foto',
                            backref='formulario',
                            lazy=True,
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Formulario {self.id} — {self.nome_locatario}>'

class Foto(db.Model):
    __tablename__ = 'fotos'
    id = db.Column(db.Integer, primary_key=True)
    id_formulario = db.Column(db.Integer,
                              db.ForeignKey('formularios.id'),
                              nullable=False)

    caminho_foto = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Foto {self.id} do Form {self.id_formulario}>'
