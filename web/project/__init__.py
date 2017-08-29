# -*- coding: utf-8 -*-
"""
    project
    ~~~~~~~~
    Flask project application package
"""
from flask import Flask
from flask_script import Manager
from flask_security import Security, MongoEngineUserDatastore
from flask_security.utils import hash_password
#from flask_principal import Permission, RoleNeed
from flask_bootstrap import Bootstrap

from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, configure_uploads, IMAGES, DATA
from project.utils.uploadsets import upload_jar_plugins, upload_images, \
    upload_exported_dashboards, upload_exported_templates, upload_exported_options
from project import upload, api, dashboards, visualizations, templates, settings


def register_uploadsets(app, upload_jar_plugins, upload_images, upload_exported_dashboards,
                        upload_exported_templates, upload_exported_options):
    configure_uploads(app, upload_images)
    configure_uploads(app, upload_exported_dashboards)
    configure_uploads(app, upload_exported_templates)
    configure_uploads(app, upload_exported_options)
    configure_uploads(app, upload_jar_plugins)

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(upload.views.blueprint)
    app.register_blueprint(dashboards.views.dash_bp)
    app.register_blueprint(visualizations.views.viz_bp)
    app.register_blueprint(templates.views.temp_bp)
    app.register_blueprint(api.dashboards.dashboard_api)
    app.register_blueprint(api.visualizations.viz_api)
    app.register_blueprint(api.templates.temp_api)
    return None


# Create app
app = Flask(__name__, static_url_path='/static', static_folder=settings.STATIC_FOLDER, template_folder='frontend/templates')

app.config.from_object('project.settings')
app.debug = True
app.logger.info("Config: %s" % app.config['MONGO_DATABASE_URI'])


# Add bootstrap
Bootstrap(app)

# Register blueprints
register_blueprints(app)

# Register flask-upload
register_uploadsets(app, upload_jar_plugins, upload_images,
                    upload_exported_dashboards, upload_exported_templates, upload_exported_options)

# Set up mongo DB and user roles
from models import db, User, Role
db.init_app(app)



# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)


import project.views
import project.dashboards.views
import project.visualizations.views
import project.templates.views
import project.api.dashboards
import project.api.visualizations
import project.api.templates


# Create a user to test applications
@app.before_first_request
def create_user():

    test_role = user_datastore.find_or_create_role('test')
    admin_role = user_datastore.find_or_create_role('admin')
    editor_role = user_datastore.find_or_create_role('editor')

    if user_datastore.get_user('a@example.com') is None:
        app.logger.info("Add fake users because no users available")
        #password = generate_password_hash('abc123', method='pbkdf2:sha256')

        hash_pwd = hash_password('abc123')
        app.logger.info('Encrypted password %s', hash_pwd)

        user_datastore.create_user(
            email='a@example.com', password='abc123', roles=[test_role], username='test'
        )
        user_datastore.create_user(
            email='b@example.com', password='abcd1234', roles=[admin_role], username='admin'
        )
        user_datastore.create_user(
            email='c@example.com', password='ab12', roles=[editor_role], username='editor'
        )
        user_datastore.create_user(
            email='alejeune@genesys.com', password='ale', roles=[admin_role], username='alejeune'
        )

