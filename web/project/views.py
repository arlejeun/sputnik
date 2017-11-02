from project import app
from flask import flash, render_template, session, request, redirect, url_for
from flask_security import login_user, login_required, LoginForm,http_auth_required, auth_token_required
#from flask_login import login_user, login_required
from models import User
from flask_principal import Permission, RoleNeed
from flask_security import current_user

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))


# Views
@app.route('/')
def home():
    return app.send_static_file('index.html')


# Views
@app.route('/pulse')
def pulse():
    return redirect(url_for('dashboards.get_dashboard_list'))
    #return render_template('index.html', user=current_user)


@app.route('/pulse/help')
def help():
    return render_template('index.html', user=current_user)


@app.route('/lost')
def lost():
    return 'lost'

@app.errorhandler(403)
def page_not_found(e):
    session['redirected_from'] = request.url
    return redirect(url_for('lost'))


''' Test routes

@app.route('/private')
@login_required
def private():
    return 'private'


@app.route('/todos')
def todos():
    Todo.objects().delete()  # Removes
    Todo(title="Simple todo A", text="12345678910").save()  # Insert
    Todo(title="Simple todo B", text="12345678910").save()  # Insert
    Todo.objects(title__contains="B").update(set__text="Hello world")  # Update
    todos = list(Todo.objects[:10])
    todos = Todo.objects.all()
    return render_template('todo.html', todos=todos)


@app.route('/pagination')
def pagination():
    Todo.objects().delete()
    for i in range(10):
        Todo(title='Simple todo {}'.format(i), text="12345678910").save()  # Insert
    page_num = int(request.args.get('page') or 1)
    todos_page = Todo.objects.paginate(page=page_num, per_page=3)
    return render_template('pagination.html', todos_page=todos_page)


@app.route('/protected')
@http_auth_required
@admin_permission.require(http_exception=403)
def protected():
    return 'protected'

@app.route('/protected1')
@auth_token_required
@admin_permission.require(http_exception=403)
def protected1():
    return 'protected 1'

@app.route('/edit')
@login_required
@editor_permission.require(http_exception=403)
def edit():
    return 'edit'
'''