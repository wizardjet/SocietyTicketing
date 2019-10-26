from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=0, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Length(min=0, max=10)])
    year_of_study = SelectField('Year of Study', choices=[("Foundation","Foundation"), ("1st Year", "1st Year"), ("2nd Year", "2nd Year"), ("3rd Year", "3rd Year"),  ("4th Year", "4th Year"), ("Masters", "Masters"), ("PhD", "PhD"), ("Alumni", "Alumni")])
    course = StringField('Course',
                           validators=[DataRequired(), Length(min=0, max=50)])
    malaysian = BooleanField('Malaysian?')
    membership = BooleanField('Would you like a membership?')

    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',
    #                                  validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Join')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')