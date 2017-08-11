# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, flash, render_template, redirect, url_for
from flask_security import auth_token_required, http_auth_required, login_required, current_user


temp_bp = Blueprint('templates', __name__, url_prefix='/pulse/templates', static_folder='../frontend/static', template_folder='../frontend/templates')


@temp_bp.route('/', methods=['GET'])
@temp_bp.route('', methods=['GET'])
def get_template_list():
    #return temp_bp.send_static_file('index.html')
    return render_template('index.html', user=current_user)


@temp_bp.route('/<name>', methods=['GET'])
def get_template(name):
    #return temp_bp.send_static_file('index.html')
    return render_template('index.html', user=current_user)
