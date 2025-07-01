from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
import os, json, base64

from config import db
from models import Sala, Pessoa, Locacao, EquipamentosLocacao, Devolucao
from itsdangerous import URLSafeSerializer, BadSignature

locacao_bp = Blueprint('locacao', __name__, template_folder='../templates')


def get_serializer():
    return URLSafeSerializer(current_app.config['SECRET_KEY'], salt='devolucao-salt')


@locacao_bp.route('/novo', methods=['GET', 'POST'])
def novo_locacao():
    if request.method == 'POST':
        sala_id = request.form.get('sala_id')
        pessoa_id = request.form.get('pessoa_id')
        equipamento_ids = request.form.getlist('equipamentos')

        locacao = Locacao(sala_id=sala_id, pessoa_id=pessoa_id)
        db.session.add(locacao)
        db.session.flush()

        for eq_id in equipamento_ids:
            assoc = EquipamentosLocacao(locacao_id=locacao.id, equipamento_id=eq_id)
            db.session.add(assoc)

        db.session.commit()

        token = get_serializer().dumps({'locacao_id': locacao.id})
        link = url_for('locacao.devolucao', token=token, _external=True)
        flash(f'Locação criada! Link de devolução: {link}', 'success')
        return redirect(url_for('locacao.novo_locacao'))

    salas = Sala.query.all()
    pessoas = Pessoa.query.all()
    return render_template('locacao_novo.html', salas=salas, pessoas=pessoas)


@locacao_bp.route('/<int:locacao_id>')
def ver_locacao(locacao_id):
    locacao = Locacao.query.get_or_404(locacao_id)
    token = get_serializer().dumps({'locacao_id': locacao.id})
    link = url_for('locacao.devolucao', token=token, _external=True)
    return render_template('locacao_ver.html', locacao=locacao, link=link)


@locacao_bp.route('/devolucao/<token>', methods=['GET', 'POST'])
def devolucao(token):
    try:
        data = get_serializer().loads(token)
        loc_id = data.get('locacao_id')
    except BadSignature:
        flash('Link de devolução inválido.', 'danger')
        return redirect(url_for('locacao.novo_locacao'))

    locacao = Locacao.query.get_or_404(loc_id)

    if request.method == 'POST':
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        target_dir = os.path.join(upload_folder, str(locacao.id))
        os.makedirs(target_dir, exist_ok=True)

        fotos = []
        for f in request.files.getlist('fotos'):
            filename = f.filename
            path = os.path.join(target_dir, filename)
            f.save(path)
            fotos.append(path)

        signature_data = request.form.get('assinatura')  # data:image/png;base64,...
        header, encoded = signature_data.split(',', 1)
        sig_path = os.path.join(target_dir, 'assinatura.png')
        with open(sig_path, 'wb') as img:
            img.write(base64.b64decode(encoded))

        devolucao = Devolucao(
            locacao_id=locacao.id,
            data_devolucao=datetime.utcnow(),
            fotos=json.dumps(fotos),
            assinatura=sig_path
        )
        locacao.data_fim = datetime.utcnow()
        db.session.add(devolucao)
        db.session.commit()

        return render_template('devolucao_sucesso.html', locacao=locacao)

    return render_template('devolucao_form.html', locacao=locacao)
