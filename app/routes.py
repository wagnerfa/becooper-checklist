from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/cadastro_salas')
def cadastro_salas():
    return render_template('cadastro_salas.html')


@main.route('/cadastro_equipamentos')
def cadastro_equipamentos():
    return render_template('cadastro_equipamentos.html')


@main.route('/formulario')
def formulario():
    return render_template('index.html')


@main.route('/formulario/cadastro')
def formulario_cadastro():
    return render_template('formulario_cadastro.html')

