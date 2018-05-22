# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, flash, render_template, g, redirect, url_for
from flask_security import auth_token_required, http_auth_required, login_required, current_user


#dash_bp = Blueprint('dashboards', __name__, url_prefix='/pulse/dashboards', static_folder='../frontend/static', template_folder='../frontend/templates')
dash_bp = Blueprint('dashboards', __name__, url_prefix='/<dashboard_type>/dashboards', static_folder='../frontend/static', template_folder='../frontend/templates')


@dash_bp.url_defaults
def add_dashboard_type(endpoint, values):
    if 'dashboard_type' in values or not g.dashboard_type:
        return
    values.setdefault('dashboard_type', getDashboardType(g.dashboard_type))


@dash_bp.url_value_preprocessor
def pull_dashboard_type(endpoint, values):
    g.dashboard_type = values.pop('dashboard_type', None)


@dash_bp.route('', methods=['GET'])
def get_dashboard_list():
    #return render_template('index.html')
    return render_template('index.html', user=current_user)


@dash_bp.route('/<name>', methods=['GET'])
def get_dashboard(name=None):
    # return dash_bp.send_static_file('index.html')
    return render_template('index.html', user=current_user)


def getDashboardType(dash_type):
    switcher = {
        'pulse': 'pulse',
        'gcxi': 'gcxi'
    }
    return switcher.get(dash_type, "pureEngage")