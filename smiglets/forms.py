from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', render_kw={'placeholder':'Mohammad Amir'},
                           validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', render_kw={'placeholder':'bin Shafiq'},
                           validators=[DataRequired(), Length(min=0, max=50)])
    email = StringField('Email', render_kw={'placeholder':'mabs2'},
                        validators=[DataRequired(), Length(min=0, max=10)])
    year_of_study = SelectField('Year of Study', choices=[("Foundation","Foundation"), ("1st Year", "1st Year"), ("2nd Year", "2nd Year"), ("3rd Year", "3rd Year"),  ("4th Year", "4th Year"), ("Masters", "Masters"), ("PhD", "PhD"), ("Alumni", "Alumni")])
    course = StringField('Course', render_kw={'placeholder':'Pathway to Medicine'},
                           validators=[DataRequired(), Length(min=0, max=50)])
    malaysian = BooleanField('Are you Malaysian?')
    membership = BooleanField('Membership?')

    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',
    #                                  validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Join')

class CheckoutForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(min=0, max=10)])
    library_id = StringField('Library ID',
                            validators=[Regexp('([0-9])[UP]')])

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')