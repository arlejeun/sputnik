from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, FieldList, TextAreaField, IntegerField, SubmitField, FileField, RadioField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired
from ..utils.uploadsets import upload_images, upload_plugins


class AddVisualizationForm(FlaskForm):
    vis_title = StringField('Title', validators=[DataRequired()])
    vis_short_desc = TextAreaField('Short Description', validators=[DataRequired()])
    vis_desc = TextAreaField('Description')
    vis_image = FileField('Screenshot widget', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    vis_options = FileField('Screenshot options', validators=[FileRequired(), FileAllowed(upload_images, 'Images only!')])
    vis_manifest = FileField('Visualization plugin', validators=[FileRequired(), FileAllowed(upload_plugins, 'jar or mstr only!')])
    vis_rating = IntegerField('Rating 1-5')
    vis_credit = TextAreaField('Additional information (external link, ...)')
    vis_type = RadioField('Label', choices=[('pulse', 'Pulse Visualization'), ('cx_insights', 'CX Insights Visualization')], default='pulse', validators=[DataRequired()])
    #recaptcha = RecaptchaField('')
    submit_button = SubmitField('Submit Visualization')


