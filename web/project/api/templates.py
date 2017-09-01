# -*- coding: utf-8 -*-

from flask_principal import Permission, RoleNeed
from flask import json, jsonify, request, Blueprint, flash
from flask_security import auth_token_required, http_auth_required, login_required
from ..models import db, Templates


temp_api = Blueprint('template_api', __name__, url_prefix='/api/pulse/templates')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


@temp_api.route('', methods=['GET'])
@temp_api.route('/', methods=['GET'])
def get_templates_api():
    templates = Templates.objects.all()
    return jsonify({'result': templates})


@temp_api.route('/<name>', methods=['GET'])
def get_template_api(name):
    template = Templates.objects(name=name)
    if template.count() == 0:
        template = "No such template for the given name"
    return jsonify({'result': template})


@temp_api.route('', methods=['POST'])
@http_auth_required
@admin_permission.require(http_exception=403)
#@auth_token_required
def post_template_api():
    payload = request.json
    validfields = set(Templates._fields) & set(payload)
    subset = {k: payload[k] for k in validfields}
    temp = Templates(**subset)
    temp.save()
    return jsonify({'result': temp})


@temp_api.route('/<name>', methods=['DELETE'])
@login_required
@admin_permission.require(http_exception=403)
def delete_template_api(name):
    template = Templates.objects(name=name)
    if template.count() == 0:
        msg = "No such template for the given name"
        return jsonify({'result': 'KO', 'msg': msg})
    else:
        template.delete()
        return jsonify({'result': 'OK', 'msg': 'template deleted'})
