# -*- coding: utf-8 -*-
import datetime
from flask_mongoengine import MongoEngine, ValidationError
from flask_security import UserMixin, RoleMixin
from werkzeug.security import check_password_hash
from mongoengine.fields import ListField, EmbeddedDocumentField, GenericEmbeddedDocumentField, ReferenceField, GenericReferenceField, SortedListField


from . import settings


# Create database connection object and instantiation of mongodb
db = MongoEngine()
db.connect('project1', host=settings.MONGO_DATABASE_URI)


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


class Dashboards (db.Document, object):

    def __init__(self, *args, **kwargs):
        super(db.Document, self).__init__(*args, **kwargs)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    name = db.StringField(max_length=60, required=True)
    title = db.StringField(max_length=60, required=True)
    short_desc = db.StringField(max_length=255, required=True)
    rating = db.IntField()
    image_src = db.StringField(max_length=255, required=True)
    tags = db.ListField(required=True)
    overview = db.DictField()
    features = db.DictField()
    prerequisites = db.DictField()
    download_link = db.StringField()
    ss_options_file = db.StringField()
    pub_date = db.DateTimeField(default=datetime.datetime.now)
    templates = db.ListField()
    meta = {'strict': False}

    def clean(self):

        req_fields = [k for k, v in Dashboards._fields.iteritems() if v.required]
        """Ensures that only published essays have a `pub_date` and
        automatically sets the pub_date if published and not set"""
        for prop in req_fields:
            if self[prop] is None:
                msg = 'Dashboard document entries should have a ' + prop + '.'
                raise ValidationError(msg)


class Visualizations (db.Document, object):

    def __init__(self, *args, **kwargs):
        super(db.Document, self).__init__(*args, **kwargs)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    name = db.StringField(max_length=60, required=True)
    title = db.StringField(max_length=60, required=True)
    short_desc = db.StringField(max_length=255, required=True)
    desc = db.StringField()
    rating = db.IntField()
    image_src = db.StringField(required=True)
    image_edit = db.StringField(required=True)
    plugin_src = db.StringField(required=True)
    pub_date = db.DateTimeField(default=datetime.datetime.now)
    status = db.StringField()
    contributor = db.StringField(max_length=125, required=True)
    meta = {'strict': False}

    def clean(self):

        req_fields = [k for k, v in Visualizations._fields.iteritems() if v.required]
        """Ensures that only published essays have a `pub_date` and
        automatically sets the pub_date if published and not set"""
        for prop in req_fields:
            if self[prop] is None:
                msg = 'Dashboard document entries should have a ' + prop + '.'
                raise ValidationError(msg)


class Templates (db.Document, object):

    def __init__(self, *args, **kwargs):
        super(db.Document, self).__init__(*args, **kwargs)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    name = db.StringField(max_length=60, required=True)
    definition = db.DictField(required=True)
    desc = db.StringField()
    metadata = db.DictField(required=True)
    rating = db.IntField()
    pub_date = db.DateTimeField(default=datetime.datetime.now)
    contributor = db.StringField(max_length=125)
    meta = {'strict': False}

    def clean(self):

        req_fields = [k for k, v in Templates._fields.iteritems() if v.required]
        """Ensures that only published essays have a `pub_date` and
        automatically sets the pub_date if published and not set"""
        for prop in req_fields:
            if self[prop] is None:
                msg = 'Dashboard document entries should have a ' + prop + '.'
                raise ValidationError(msg)

