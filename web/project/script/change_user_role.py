# -*- coding: utf-8 -*-
"""
    project
    ~~~~~~~~
    Flask project application package
"""

from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, UserMixin, RoleMixin
from werkzeug.security import check_password_hash
import sys, getopt


def usage():
    print 'change_user_role.py -u < user_email > -r <user_role (admin|editor) > add|remove'


def specify(txt):
    print ("Please specify the correct action - {0}".format(txt))

def main(argv):

    email = ''
    role = ''
    action = ''

    try:
        opts, args = getopt.getopt(argv,"hu:r:",["email=","role="])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-u", "--email"):
            email = arg
        elif opt in ("-r", "--role"):
            role = arg

    if len(args) == 0:
        usage()
        sys.exit()

    action = args[0]

    if not email:
        usage()
        sys.exit(2)

    if not role:
        usage()
        sys.exit(2)

    db = MongoEngine()
    db.connect('project1', host='mongodb://localhost:27017/pulse')

    class Role(db.Document, RoleMixin):
        name = db.StringField(max_length=80, unique=True)
        description = db.StringField(max_length=255)

    class User(db.Document, UserMixin):
        email = db.StringField(required=True, max_length=255, unique=True)
        password = db.StringField(max_length=255)
        username = db.StringField(max_length=255)
        active = db.BooleanField(default=True)
        confirmed_at = db.DateTimeField()
        roles = db.ListField(db.ReferenceField(Role), default=[])

        @staticmethod
        def validate_login(password_hash, password):
            return check_password_hash(password_hash, password)

        def get_roles(self):
            return [r.name.encode("utf-8") for r in self.roles]

    # Setup Flask-Security
    user_datastore = MongoEngineUserDatastore(db, User, Role)

    # Add a role to a user
    def add_role(user,role):
        added_role = user_datastore.find_or_create_role(role)
        user_datastore.add_role_to_user(user, added_role)
        print ("Added {0} role to user {1}".format(role, email))

    # Remove a role from a user
    def remove_role(user, role):
        added_role = user_datastore.find_or_create_role(role)
        user_datastore.remove_role_from_user(user, added_role)
        print ("Removed {0} role from user {1}".format(role, email))

    func, params = {
        'add': (add_role, (email, role)),
        'remove': (remove_role, (email, role))
    }.get(action, (specify, ('Action is not properly. Please select add or remove',)))

    func(*params)


if __name__ == '__main__':
    main(sys.argv[1:])

