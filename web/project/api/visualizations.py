# -*- coding: utf-8 -*-

from flask_principal import Permission, RoleNeed
from flask import json, jsonify, request, Blueprint, flash
from flask_security import auth_token_required, http_auth_required, login_required
from ..models import db, Visualizations


viz_api = Blueprint('visualization_api', __name__, url_prefix='/api/pulse/visualizations')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


@viz_api.route('', methods=['GET'])
@viz_api.route('/', methods=['GET'])
def get_visualizations_api():
    visualizations = Visualizations.objects.all()
    return jsonify({'result': visualizations})


@viz_api.route('/<name>', methods=['GET'])
def get_visualization_api(name):
    visualization = Visualizations.objects(name=name)
    if visualization.count() == 0:
        visualization = "No such visualization for the given name"
    return jsonify({'result': visualization})


@viz_api.route('', methods=['POST'])
@http_auth_required
@admin_permission.require(http_exception=403)
def post_visualization_api():
    payload = request.json
    validfields = set(Visualizations._fields) & set(payload)
    subset = {k: payload[k] for k in validfields}
    viz = Visualizations(**subset)
    viz.save()
    return jsonify({'result': viz})


@viz_api.route('/<name>', methods=['DELETE'])
@login_required
#@auth_token_required
#@http_auth_required
@admin_permission.require(http_exception=403)
def delete_visualization_api(name):
    visualization = Visualizations.objects(name=name)
    if visualization.count() == 0:
        msg = "No such visualization for the given name"
        return jsonify({'result': 'KO', 'msg': msg})
    else:
        visualization.delete()
        return jsonify({'result': 'OK', 'msg': 'visualization deleted'})
