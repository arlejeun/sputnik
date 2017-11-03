# -*- coding: utf-8 -*-

from flask_principal import Permission, RoleNeed
from flask import json, jsonify, request, Blueprint, flash
from flask_security import auth_token_required, http_auth_required, login_required, current_user
from ..models import db, Templates
from mongoengine.queryset import Q



temp_api = Blueprint('template_api', __name__, url_prefix='/api/pulse/templates')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


@temp_api.route('', methods=['GET'])
@temp_api.route('/', methods=['GET'])
def get_templates_api():
    if current_user.has_role('admin'):
        templates = Templates.objects.all().order_by('-pub_date')
    elif current_user.has_role('editor'):
        templates = Templates.objects(Q(status='public') | Q(contributor=current_user.email)).order_by(
            '-pub_date')
    else:
        templates = Templates.objects(Q(status='public')).order_by('-pub_date')
    return jsonify({'result': templates})


@temp_api.route('/<name>', methods=['GET'])
def get_template_api(name):
    #template = Templates.objects.get_or_404(definition__guid=name)
    template = Templates.objects.filter(definition__guid=name).first_or_404()
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
@http_auth_required
@admin_permission.require(http_exception=403)
def delete_template_api(name):
    template = Templates.objects.filter(definition__guid=name).first_or_404()
    #template = Templates.objects.get_or_404(definition__guid=name)
    template.delete()
    return jsonify({'result': 'OK', 'msg': 'template deleted', 'name':name})


@temp_api.route('/<string:tmp>', methods=['PUT'])
@http_auth_required
@admin_permission.require(http_exception=403)
def put_template_api(tmp):
    template = Templates.objects.filter(definition__guid=tmp).first_or_404()
    #template = Templates.objects.get_or_404(definition__guid=tmp)
    payload = request.json
    validfields = set(Templates._fields) & set(payload)
    subset = {k: payload[k] for k in validfields}
    template.update(**subset)
    template.save()
    return jsonify({'result': 'OK', 'msg': 'Template updated', 'name':tmp})