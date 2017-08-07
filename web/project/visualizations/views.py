# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, flash, render_template, redirect, url_for
from flask_security import auth_token_required, http_auth_required, login_required
from project.visualizations.forms import AddVisualizationForm
import os, fnmatch, json, glob
from uuid import uuid4


viz_bp = Blueprint('visualizations', __name__, url_prefix='/pulse/visualizations', static_folder='../frontend/static', template_folder='../frontend/templates')


@viz_bp.route('/', methods=['GET'])
@viz_bp.route('', methods=['GET'])
def get_visualization_list():
    #TODO:How to share back-end objects to front-end using static files?
    # Do I need to use templates and update front-end files
    return viz_bp.send_static_file('index.html')


@viz_bp.route('/<name>', methods=['GET'])
def get_visualization(name):
    return viz_bp.send_static_file('index.html')
