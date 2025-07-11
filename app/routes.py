from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.util import methods_equivalent

from .models import *
from .utilities import *

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def cadastro_salas():
    if request.method == 'POST':
        nome = request.form.get('nome')
        capacidade = request.form.get('capacidade')

        # validação simples
        if not nome or not capacidade:
            flash('Preencha todos os campos.', 'warning')
        else:
            try:
                # cria e salva a sala
                sala = Sala(nome=nome, capacidade=int(capacidade))
                db.session.add(sala)
                db.session.commit()
                flash('Sala cadastrada com sucesso!', 'success')
                return redirect(url_for('main.cadastro_salas'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao cadastrar sala: {e}', 'danger')

    # (Opcional) buscar todas as salas para exibir na página
    salas = Sala.query.all()
    return render_template('cadastro_salas.html', salas=salas)



@main.route('/delete_sala/<int:sala_id>', methods=['GET', 'POST'])
def delete_sala(sala_id):
    sala = Sala.query.get_or_404(sala_id)
    try:
        db.session.delete(sala)
        db.session.commit()
        flash('Sala excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir sala: {e}', 'danger')
    return redirect(url_for('main.cadastro_salas'))


@main.route('/cadastro_equipamentos', methods=['GET', 'POST'])
def cadastro_equipamentos():
    if request.method == 'POST':
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        valor = request.form.get('valor')
        # cria e salva a sala
        equipamento = Equipamento(nome=nome, valor=valor, quantidade=quantidade)
        db.session.add(equipamento)
        db.session.commit()
        flash('Equipamento cadastrada com sucesso!', 'success')
        return redirect(url_for('main.cadastro_equipamentos'))

    # (Opcional) buscar todos os Equipamentos para exibir na página
    tabela = Equipamento.query.all()
    return render_template('cadastro_equipamentos.html', Equipamentos=tabela)


@main.route('/delete_equipamento/<int:id>', methods=['POST', 'GET'])
def delete_equipamento(id):
    sala = Equipamento.query.get_or_404(id)
    try:
        db.session.delete(sala)
        db.session.commit()
        flash('Sala excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir sala: {e}', 'danger')
    return redirect(url_for('main.cadastro_equipamentos'))


@main.route('/formulario/cadastro', methods=['GET','POST'])
def formulario_cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome_locatario')
        email = request.form.get('email_locatario')
        telefone = request.form.get('telefone_locatario')
        data = request.form.get('data_locatario')
        sala = request.form.get('sala_locatario')
        observacao_responsavel = request.form.get('observacao_responsavel_coop')
        observacao = request.form.get('observacao_locatario')
        assinatura = request.form.get('assinatura_locatario')
        equipamentos = request.form.get('equipamentos')

        formulario = Formulario(nome_locatario=nome, sala=sala, email_locatario=email, telefone_locatario=telefone,
        data_locacao=data , observacao_responsavel_coop=observacao_responsavel, observacao_locatario=observacao,
        assinatura=assinatura, equipamentos=equipamentos, fotos=1.0)


        db.session.add(formulario)
        db.session.commit()

        return redirect(url_for('main.formulario_cadastro'))

    return render_template('formulario_cadastro.html')

@main.route('/formulario')
def formulario():

    tabela = Formulario.query.all()

    return render_template('formulario.html', tabela=tabela)



@main.route('/formulario/view/<id>')
def formulario_view(id):

    formulario = Formulario.query.filter_by(id=id).first()

    return render_template('formulario_view.html', formulario=formulario)


