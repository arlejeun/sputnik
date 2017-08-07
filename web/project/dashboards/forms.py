from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from project import upload_images_dashboards, upload_exported_dashboards


class AddDashboardForm(FlaskForm):
    dashboard_title = StringField('Dashboard Title', validators=[DataRequired()])
    dashboard_short_desc = StringField('Dashboard Description', validators=[DataRequired()])
    dashboard_image = FileField('Dashboard screenshot', validators=[FileRequired(), FileAllowed(upload_images_dashboards, 'Images only!')])
    dashboard_tags = FieldList(StringField(), min_entries=3, max_entries=8)
    dashboard_export = FileField('Dashboard definition', validators=[FileRequired(), FileAllowed(upload_exported_dashboards, 'JSON only!')])
    dashboard_overview = TextAreaField()
    dashboard_features = TextAreaField()
    dashboard_prerequisites = TextAreaField()
