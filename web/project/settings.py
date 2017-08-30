# -*- coding: utf-8 -*-
"""
    overholt.settings
    ~~~~~~~~~~~~~~~
    overholt settings module
"""
import os

DEBUG = True
SECRET_KEY = 'super-secret-key'

#MONGO_DATABASE_URI = 'mongodb://mongo:27017/pulse'
MONGO_DATABASE_URI = 'mongodb://localhost:27017/pulse'
MONGO_DB = True
MONGO_USERS_COLLECTION_NAME = 'users'

#MAIL_DEFAULT_SENDER = 'info@overholt.com'
#MAIL_SERVER = 'smtp.postmarkapp.com'
#MAIL_PORT = 25
#MAIL_USE_TLS = True
#MAIL_USERNAME = 'username'
#MAIL_PASSWORD = 'password'

WTF_CSRF_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_PASSWORD_HASH = 'plaintext'
SECURITY_PASSWORD_SALT = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'
SECURITY_REMEMBER_SALT = 'remember_salt'
SECURITY_RESET_SALT = 'reset_salt'
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_REGISTERABLE = True

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = False
SECURITY_CONFIRMABLE = False

# Uploads
UPLOADS_DEFAULT_DEST = os.path.realpath('.') + '/project/upload/assets/user/'
#UPLOADS_SCREENSHOTS_URL = 'http://127.0.0.1:5000/pulse/upload/assets/screenshots/'
UPLOADED_IMAGES_DEST = os.path.realpath('.') + '/project/upload/assets/user/'
#UPLOADED_PLUGINS_URL = 'http://127.0.0.1:5000/pulse/upload/assets/plugins/'

# Recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LfdtC4UAAAAAHjjL08N7pE5FqgsD2x5zLcCh32Z'
RECAPTCHA_PRIVATE_KEY = '6LfdtC4UAAAAANBcrLpuHfWYx2tsPJQtdgEbS7PG'
SECRET_KEY = 'devkey'

# Static content
STATIC_FOLDER = 'frontend/static'
# For production use:
#STATIC_FOLDER = 'frontend/static/build/es6-bundled'