from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from datetime import datetime
import os, json, base64

from config import db
from models import *
from itsdangerous import URLSafeSerializer, BadSignature

locacao_bp = Blueprint('locacao', __name__, template_folder='../templates')


def get_serializer():
    return URLSafeSerializer(current_app.config['SECRET_KEY'], salt='devolucao-salt')


@locacao_bp.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

