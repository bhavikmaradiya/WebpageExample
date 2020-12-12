from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

from models import User


class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    enrollment = StringField('Enrollment', validators=[DataRequired(), Length(min=12, max=12,
                                                                              message='Enrollment must be 12 characters long.'),
                                                       Regexp(regex=r'([\s\d]+)$',
                                                              message='Invalid enrollment number.')])
    submit = SubmitField('Update')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    enrollment = StringField('Enrollment', validators=[DataRequired(), Length(min=12, max=12,
                                                                              message='Enrollment must be 12 characters long.'),
                                                       Regexp(regex=r'([\s\d]+)$',
                                                              message='Invalid enrollment number.')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,
                                                                            message='Password should be 6 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             message='Password does not match')])
    submit = SubmitField('Register')

    def validate_enrollment(self, enrollment):
        user = User.query.filter_by(enrollment=enrollment.data).first()
        if user:
            raise ValidationError('That enrollment number is already registered.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email address is taken, Please choose different email address.')


class LoginForm(FlaskForm):
    enrollment = StringField('Enrollment', validators=[DataRequired(), Length(min=12, max=12,
                                                                              message='Enrollment must be 12 characters long.'),
                                                       Regexp(regex=r'([\s\d]+)$',
                                                              message='Invalid enrollment number.')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,
                                                                            message='Password should be 6 characters long.')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
