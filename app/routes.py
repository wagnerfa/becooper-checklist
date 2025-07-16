import os, json
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from .models import db, Formulario, Foto, Sala, Equipamento
from .utilities import send_email

main = Blueprint('main', __name__)


def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
    )



@main.route('/', methods=['GET', 'POST'])
def cadastro_salas():
    if request.method == 'POST':
        nome = request.form.get('nome')
        capacidade = request.form.get('capacidade')


        if not nome or not capacidade:
            flash('Preencha todos os campos.', 'warning')
        else:
            try:

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
def cadastrar_formulario():
    if request.method == 'POST':
        nome = request.form.get('nome_locatario')
        email = request.form.get('email_locatario')
        telefone = request.form.get('telefone_locatario')
        sala = request.form.get('sala_locatario')
        equip_txt = ','.join(request.form.getlist('equipamentos'))

        # validações básicas...
        if not nome or not email or not sala:
            flash('Campos obrigatórios não preenchidos.', 'danger')
            return redirect(request.url)

        form = Formulario(
            nome_locatario=nome,
            email_locatario=email,
            telefone_locatario=telefone,
            sala=sala,
            equipamentos=equip_txt
        )
        db.session.add(form)
        db.session.commit()


        link = url_for('main.validar_formulario',
                       token=form.validation_token,
                       _external=True)
        corpo = f"Olá {form.nome_locatario},\n\n" \
                f"Para validar seu checklist, acesse:\n{link}"
        send_email(form.email_locatario, corpo)

        flash('Formulário cadastrado! Link de validação enviado ao locatário.', 'success')
        return redirect(url_for('main.cadastro_salas'))

    salas = Sala.query.all()
    equipamentos = Equipamento.query.all()
    return render_template(
        'formulario_cadastro.html',
        salas=salas,
        equipamentos=equipamentos
    )


@main.route('/validar/<token>', methods=['GET', 'POST'])
def validar_formulario(token):
    form = Formulario.query.filter_by(validation_token=token).first_or_404()
    original_equip = form.equipamentos.split(',')

    if request.method == 'POST':
        selecionados = request.form.getlist('equipamentos')
        obs = request.form.get('observacao_locatario', '').strip()
        faltantes = set(original_equip) - set(selecionados)

        if faltantes and not obs:
            flash(
              'Você deixou itens sem check. '
              'Por favor, informe observações sobre eles.',
              'danger'
            )
            return redirect(request.url)


        form.equipamentos_validados = json.dumps({
            eq: (eq in selecionados) for eq in original_equip
        })
        form.observacao_locatario = obs
        form.data_validacao_locatario = datetime.utcnow()


        for arquivo in request.files.getlist('fotos'):
            if arquivo and allowed_file(arquivo.filename):
                nome = secure_filename(arquivo.filename)
                caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], nome)
                arquivo.save(caminho)
                foto = Foto(id_formulario=form.id, caminho_foto=nome)
                db.session.add(foto)

        db.session.commit()

        flash('Validação enviada com sucesso!', 'success')
        return redirect(url_for('main.agradecimento'))

    return render_template(
        'formulario_validacao.html',
        formulario=form,
        equipamentos=original_equip
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


@main.route('/agradecimento')
def agradecimento():

    return 'Obrigado'