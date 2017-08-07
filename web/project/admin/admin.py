from flask import Blueprint, render_template, abort
from flask_security import login_required
from jinja2 import TemplateNotFound

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')


@admin.route('/', defaults={'page': 'index'})
@admin.route('/<page>')
@login_required
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)