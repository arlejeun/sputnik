# -*- coding: utf-8 -*-

from flask_principal import Permission, RoleNeed
from flask import json, jsonify, request, Blueprint, flash
from flask_security import auth_token_required, http_auth_required, login_required, current_user
from ..models import db, Visualizations
from mongoengine.queryset import Q


viz_api = Blueprint('visualization_api', __name__, url_prefix='/api/pulse/visualizations')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


#Improve the logic here
@viz_api.route('', methods=['GET'])
@viz_api.route('/', methods=['GET'])
def get_visualizations_api():
    if current_user.has_role('admin'):
        visualizations = Visualizations.objects.all().order_by('-pub_date')
    elif current_user.has_role('editor'):
        visualizations = Visualizations.objects(Q(status='public') | Q(contributor=current_user.email)).order_by(
            '-pub_date')
    else:
        visualizations = Visualizations.objects(Q(status='public')).order_by('-pub_date')
    return jsonify({'result': visualizations})


@viz_api.route('/<name>', methods=['GET'])
def get_visualization_api(name):
    visualization = Visualizations.objects.filter(name=name).first_or_404()
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
@http_auth_required
@admin_permission.require(http_exception=403)
def delete_visualization_api(name):
    visualization = Visualizations.objects.filter(name=name).first_or_404()
#    visualization = Visualizations.objects.get_or_404(name=name)
    visualization.delete()
    return jsonify({'result': 'OK', 'msg': 'visualization deleted', 'name':name})


@viz_api.route('/<string:viz>', methods=['PUT'])
@http_auth_required
@admin_permission.require(http_exception=403)
def put_visualization_api(viz):
    #visualization = Visualizations.objects.get_or_404(name=viz)
    visualization = Visualizations.objects.filter(name=viz).first_or_404()
    payload = request.json
    validfields = set(Visualizations._fields) & set(payload)
    subset = {k: payload[k] for k in validfields}
    visualization.update(**subset)
    visualization.save()
    return jsonify({'result': visualization})
