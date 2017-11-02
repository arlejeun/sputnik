from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired
from project.utils.uploadsets import upload_images, upload_exported_templates


class AddDashboardForm(FlaskForm):
    dashboard_metadata = FileField('Dashboard CC Metadata definition', validators=[DataRequired(),FileAllowed(upload_exported_templates, 'JSON only!')])
    dashboard_image = FileField('Dashboard screenshot', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    dashboard_export = FileField('Dashboard export', validators=[FileRequired(), FileAllowed(upload_exported_templates, 'JSON only!')])
    dashboard_type = RadioField('Label', choices=[('pulse', 'Pulse Dashboard'), ('cx_insights', 'CX Insights Dashboard')], validators=[DataRequired()])

    submit_button = SubmitField('Submit Dashboard')