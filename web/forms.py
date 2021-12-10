from flask_wtf import FlaskForm
from models import Fcuser
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[
                             DataRequired(), EqualTo('re_password')])
    grafana_ip = StringField('grafana_ip', validators=[DataRequired()])

    re_password = PasswordField('re_password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            fcuser = Fcuser.query.filter_by(userid=userid).first()
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[
                             DataRequired(), UserPassword()])


class GrafanaForm(FlaskForm):
    # grafana form
    aws_ip = StringField('aws_ip', validators=[DataRequired()])
    azure_ip = StringField('azure', validators=[DataRequired()])
    gcp_ip = StringField('gcp_ip', validators=[DataRequired()])

    aws_api = StringField('aws_api', validators=[DataRequired()])
    azure_api = StringField('azure_api', validators=[DataRequired()])
    gcp_api = StringField('gcp_api', validators=[DataRequired()])

class UploadForm(FlaskForm):
    file = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['yaml', 'txt'])])
