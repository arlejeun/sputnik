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

MAIL_DEFAULT_SENDER = 'dashboard.community.center@gmail.com'
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'dashboard.community.center@gmail.com'
MAIL_PASSWORD = 'blackmail32'

WTF_CSRF_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_PASSWORD_HASH = 'plaintext'
SECURITY_PASSWORD_SALT = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'
SECURITY_REMEMBER_SALT = 'remember_salt'
SECURITY_RESET_SALT = 'reset_salt'
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = False
SECURITY_CONFIRMABLE = True
SECURITY_CHANGEABLE = True

SECURITY_EMAIL_SENDER = 'dashboard.community.center@gmail.com'
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
SECURITY_SEND_PASSWORD_RESET_EMAIL = True
SECURITY_LOGIN_WITHOUT_CONFIRMATION = False

#Email
SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to the Genesys Dashboard Community Center'
SECURITY_EMAIL_SUBJECT_CONFIRM = 'Please confirm your email for the Genesys Dashboard Community Center'

# Uploads
UPLOADS_DEFAULT_DEST = os.path.realpath('.') + '/project/upload/assets/community/'
UPLOADED_IMAGES_DEST = os.path.realpath('.') + '/project/upload/assets/community/'

# Recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LfdtC4UAAAAAHjjL08N7pE5FqgsD2x5zLcCh32Z'
RECAPTCHA_PRIVATE_KEY = '6LfdtC4UAAAAANBcrLpuHfWYx2tsPJQtdgEbS7PG'
SECRET_KEY = 'devkey'

# Static content
STATIC_FOLDER = 'frontend/static'
# For production use:
#STATIC_FOLDER = 'frontend/static/build/es6-bundled'