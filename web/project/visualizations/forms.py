from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, FieldList, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from project import upload_images, upload_jar_plugins


class AddVisualizationForm(FlaskForm):
    vis_title = StringField('Title', validators=[DataRequired()])
    vis_short_desc = TextAreaField('Short Description', validators=[DataRequired()])
    vis_desc = TextAreaField('Description')
    vis_image = FileField('Screenshot widget', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    vis_options = FileField('Screenshot options', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    vis_manifest = FileField('Visualization plugin', validators=[FileRequired(), FileAllowed(upload_jar_plugins, 'jar only!')])
    vis_rating = IntegerField('Rating 1-5')
    recaptcha = RecaptchaField('')
    submit_button = SubmitField('Submit Visualization')


