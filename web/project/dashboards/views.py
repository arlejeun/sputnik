# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, flash, render_template, redirect, url_for
from flask_security import auth_token_required, http_auth_required, login_required, current_user
from ..models import db, Dashboards
#from project.upload import AddDashboardForm
import os, fnmatch, json, glob
from uuid import uuid4

dash_bp = Blueprint('dashboards', __name__, url_prefix='/pulse/dashboards', static_folder='../frontend/static', template_folder='../frontend/templates')


@dash_bp.route('', methods=['GET'])
def get_dashboard_list():
    return render_template('index.html', user=current_user)
    #return render_template('index.html')



@dash_bp.route('/<name>', methods=['GET'])
def get_dashboard(name=None):
    return dash_bp.send_static_file('index.html')
