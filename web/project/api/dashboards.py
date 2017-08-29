# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, flash
from flask_security import auth_token_required, http_auth_required, login_required
from ..models import db, Dashboards
from flask_principal import Permission, RoleNeed


dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/pulse/dashboards')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


@dashboard_api.route('', methods=['GET'])
@dashboard_api.route('/', methods=['GET'])
def get_dashboards_api():
    dashboards = Dashboards.objects.all()
    return jsonify({'result': dashboards})


@dashboard_api.route('/<name>', methods=['GET'])
def get_dashboard_api(name):
    dashboard = Dashboards.objects(name=name)
    if dashboard.count() == 0:
        dashboard = "No such dashboard for the given name"
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
    dashboard = Dashboards.objects(name=name)
    if dashboard.count() == 0:
        msg = "No such dashboard for the given name"
        return jsonify({'result': 'KO', 'msg': msg})
    else:
        dashboard.delete()
        return jsonify({'result': 'OK', 'msg': 'Dashboard deleted'})
