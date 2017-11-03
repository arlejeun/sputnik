# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, flash
from flask_security import auth_token_required, http_auth_required, login_required, current_user
from ..models import db, Dashboards
from flask_principal import Permission, RoleNeed
from mongoengine.queryset import Q


dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/pulse/dashboards')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


@dashboard_api.route('', methods=['GET'])
@dashboard_api.route('/', methods=['GET'])
def get_dashboards_api():
    if current_user.has_role('admin'):
        dashboards = Dashboards.objects.all().order_by('-pub_date')
    elif current_user.has_role('editor'):
        dashboards = Dashboards.objects(Q(status='public') | Q(contributor=current_user.email)).order_by(
            '-pub_date')
    else:
        dashboards = Dashboards.objects(Q(status='public')).order_by('-pub_date')

    return jsonify({'result': dashboards})


@dashboard_api.route('/<name>', methods=['GET'])
def get_dashboard_api(name):
    dashboard = Dashboards.objects.filter(name=name).first_or_404()
    return jsonify({'result': dashboard})


@dashboard_api.route('', methods=['POST'])
@http_auth_required
@admin_permission.require(http_exception=403)
def post_dashboard_api():
    payload = request.json
    validfields = set(Dashboards._fields) & set(payload)
    subset = {k: payload[k] for k in validfields}
    dashboard = Dashboards(**subset)
    dashboard.save()
    return jsonify({'result': dashboard})


@dashboard_api.route('/<name>', methods=['DELETE'])
@http_auth_required
@admin_permission.require(http_exception=403)
def delete_dashboard_api(name):
    dashboard = Dashboards.objects.filter(name=name).first_or_404()
    dashboard.delete()
    return jsonify({'result': 'OK', 'msg': 'Dashboard deleted'})


@dashboard_api.route('/<string:dash>', methods=['PUT'])
@http_auth_required
@admin_permission.require(http_exception=403)
def put_dashboard_api(dash):
    dashboard = Dashboards.objects.filter(name=dash).first_or_404()
    payload = request.json
    validfields = set(Dashboards._fields) & set(payload)
    subset = {k: payload[k] for k in validfields}
    dashboard.update(**subset)
    dashboard.save()
    return jsonify({'result': 'OK', 'msg': 'visualization updated', 'name':dash})