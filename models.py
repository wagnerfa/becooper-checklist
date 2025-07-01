from datetime import datetime
from config import db

class Sala(db.Model):
    __tablename__ = 'salas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    equipamentos = db.relationship('Equipamento', backref='sala', lazy=True)

    def __repr__(self):
        return f"<Sala {self.nome}>"

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)

    def __repr__(self):
        return f"<Equipamento {self.nome} em Sala {self.sala_id}>"

class Pessoa(db.Model):
    __tablename__ = 'pessoas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    locacoes = db.relationship('Locacao', backref='responsavel', lazy=True)

    def __repr__(self):
        return f"<Pessoa {self.nome}>"

class Locacao(db.Model):
    __tablename__ = 'locacoes'
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=True)

    sala = db.relationship('Sala', backref='locacoes')
    equipamentos_associados = db.relationship('EquipamentosLocacao', back_populates='locacao', cascade='all, delete-orphan')
    devolucao = db.relationship('Devolucao', back_populates='locacao', uselist=False)

    def __repr__(self):
        return f"<Locacao Sala:{self.sala_id} Pessoa:{self.pessoa_id}>"

class EquipamentosLocacao(db.Model):
    __tablename__ = 'equipamentos_locacao'
    id = db.Column(db.Integer, primary_key=True)
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacoes.id'), nullable=False)
    equipamento_id = db.Column(db.Integer, db.ForeignKey('equipamentos.id'), nullable=False)

    locacao = db.relationship('Locacao', back_populates='equipamentos_associados')
    equipamento = db.relationship('Equipamento')

    def __repr__(self):
        return f"<EquipamentoLocacao Equip:{self.equipamento_id} Locacao:{self.locacao_id}>"

class Devolucao(db.Model):
    __tablename__ = 'devolucoes'
    id = db.Column(db.Integer, primary_key=True)
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacoes.id'), nullable=False)
    data_devolucao = db.Column(db.DateTime, default=datetime.utcnow)
    fotos = db.Column(db.Text, nullable=True)  # JSON array with URLs or filenames of uploaded photos
    assinatura = db.Column(db.String(200), nullable=False)  # path/filename of the signature image

    locacao = db.relationship('Locacao', back_populates='devolucao')

    def __repr__(self):
        return f"<Devolucao Locacao:{self.locacao_id} em {self.data_devolucao}>"
