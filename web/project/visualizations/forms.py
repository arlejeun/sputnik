from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from project import upload_images, upload_jar_plugins


class AddVisualizationForm(FlaskForm):
    vis_title = StringField('Visualization Title', validators=[DataRequired()])
    vis_short_desc = TextAreaField('Visualization Short Description', validators=[DataRequired()])
    vis_desc = TextAreaField('Visualization Description')
    vis_image = FileField('Visualization widget', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    vis_options = FileField('Visualization display options', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    vis_manifest = FileField('Visualization manifest', validators=[FileRequired(), FileAllowed(upload_jar_plugins, 'jar only!')])
    vis_rating = IntegerField('Rating 1-5')
