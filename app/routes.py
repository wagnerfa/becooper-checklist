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

        equipamento = Equipamento(nome=nome, valor=valor, quantidade=quantidade)
        db.session.add(equipamento)
        db.session.commit()
        flash('Equipamento cadastrada com sucesso!', 'success')
        return redirect(url_for('main.cadastro_equipamentos'))


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


@main.route('/formulario/cadastro', methods=['GET', 'POST'])
def formulario_cadastro():
    if request.method == 'POST':
        # Validação de campos obrigatórios
        nome = request.form.get('nome_locatario')
        if not nome:
            flash('O nome do locatário é obrigatório.', 'danger')
            return redirect(url_for('main.formulario_cadastro'))

        sala_id = request.form.get('sala_locatario')
        if not sala_id:
            flash('Selecione uma sala.', 'danger')
            return redirect(url_for('main.formulario_cadastro'))
        # Converte sala_id para inteiro ao invés de atribuir objeto Sala
        sala_id = int(sala_id)

        # Campos opcionais
        email = request.form.get('email_locatario') or ''
        telefone = request.form.get('telefone_locatario') or ''
        observacao_responsavel = request.form.get('observacao_responsavel_coop') or ''

        # Equipamentos pode ser múltiplo
        equipamentos_list = request.form.getlist('equipamentos')
        equipamentos = ','.join(equipamentos_list)

        # Cria instância do formulário atribuindo a chave estrangeira diretamente
        formulario = Formulario(
            nome_locatario=nome,
            sala=sala_id,
            email_locatario=email,
            telefone_locatario=telefone,
            data_locacao=datetime.utcnow(),
            observacao_responsavel_coop=observacao_responsavel,
            equipamentos=equipamentos
        )

        try:
            db.session.add(formulario)
            db.session.commit()
            flash('Formulário salvo com sucesso!', 'success')
            return redirect(url_for('main.formulario_cadastro'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar formulário: {e}', 'danger')
            return redirect(url_for('main.formulario_cadastro'))

    # GET: exibe o formulário com listas de salas e equipamentos
    salas = Sala.query.order_by(Sala.nome).all()
    equipamentos = Equipamento.query.order_by(Equipamento.nome).all()
    return render_template(
        'formulario_cadastro.html',
        salas=salas,
        equipamentos=equipamentos
    )


@main.route('/formulario')
def formulario():

    tabela = Formulario.query.all()

    return render_template('formulario.html', tabela=tabela)


@main.route('/formulario/view/<id>')
def formulario_view(id):

    formulario = Formulario.query.filter_by(id=id).first()

    return render_template('formulario_view.html', formulario=formulario)


@main.route('/formulario/<int:sala_id>', methods=['GET', 'POST'])
def delete_formulario(sala_id):
    sala = Formulario.query.get_or_404(sala_id)
    try:
        db.session.delete(sala)
        db.session.commit()
        flash('Sala excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir sala: {e}', 'danger')
    return redirect(url_for('main.formulario'))
