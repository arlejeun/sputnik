# -*- coding: utf-8 -*-

from flask import json, jsonify, request, Blueprint, g, flash
from flask_security import auth_token_required, http_auth_required, login_required, current_user
from ..models import db, Dashboards
from flask_principal import Permission, RoleNeed
from mongoengine.queryset import Q
from ..settings import PAGINATION_DASHBOARD_PAGE


dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/<dashboard_type>/dashboards')

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))

PER_PAGE = PAGINATION_DASHBOARD_PAGE


@dashboard_api.url_defaults
def add_dashboard_type(endpoint, values):
    values.setdefault('dashboard_type', g.dashboard_type)


@dashboard_api.url_value_preprocessor
def pull_dashboard_type(endpoint, values):
    g.dashboard_type = values.pop('dashboard_type')


@dashboard_api.route('', methods=['GET'])
@dashboard_api.route('/', methods=['GET'])
def get_dashboards_api():
    total = Dashboards.objects().count()
    page = 1
    product = getProduct(g.dashboard_type)

    if 'page' in request.args:
        page = int(request.args['page'])

    if current_user.has_role('admin'):
        if product == 'pureEngage':
            dashboards = Dashboards.objects.all().order_by('-pub_date').paginate(page=page, per_page=PER_PAGE).items
        else:
            dashboards = Dashboards.objects(Q(product=product)).order_by('-pub_date').paginate(
                page=page, per_page=PER_PAGE).items
            total = Dashboards.objects(Q(product=product)).count()

    elif current_user.has_role('editor'):
        if product == 'pureEngage':
            dashboards = Dashboards.objects(Q(status='public') | Q(contributor=current_user.email)).order_by('-pub_date').paginate(page=page, per_page=PER_PAGE).items

        else:
            dashboards = Dashboards.objects((Q(status='public') | Q(contributor=current_user.email)) & (Q(product=product))).order_by(
                '-pub_date').paginate(page=page, per_page=PER_PAGE).items
            total = Dashboards.objects((Q(status='public') | Q(contributor=current_user.email)) & (Q(product=product))).count()
    else:

        if product == 'pureEngage':
            dashboards = Dashboards.objects(Q(status='public')).order_by('-pub_date').paginate(page=page,per_page=PER_PAGE).items
            total = Dashboards.objects(Q(status='public')).count()
        else:
            dashboards = Dashboards.objects(Q(status='public') & Q(product=product)).order_by('-pub_date').paginate(page=page, per_page=PER_PAGE).items
            total = Dashboards.objects(Q(status='public') & Q(product=product)).count()

    return jsonify({'total': total, 'per_page': PER_PAGE, 'result': dashboards})


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


def getProduct(dash_type):
    switcher = {
        'pulse': 'pulse',
        'gcxi': 'gcxi'
    }
    return switcher.get(dash_type, "pureEngage")