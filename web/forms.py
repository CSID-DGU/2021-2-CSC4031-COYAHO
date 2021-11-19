from flask_wtf import FlaskForm
from models import Fcuser
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    # username = StringField('username', validators=[DataRequired()])
    grafana_ip = StringField('grafana_ip', validators=[DataRequired()])
    password = PasswordField('password', validators=[
                             DataRequired(), EqualTo('re_password')])  # equalTo("필드네임")
    re_password = PasswordField('re_password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            fcuser = Fcuser.query.filter_by(userid=userid).first()
            if fcuser.password != password:
                # raise ValidationError(message % d)
                raise ValueError('Wrong password')
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[
                             DataRequired(), UserPassword()])


class UploadForm(FlaskForm):
    file = FileField('Upload Image', validators=[
                     FileRequired(), FileAllowed(['yaml', 'txt'])])
