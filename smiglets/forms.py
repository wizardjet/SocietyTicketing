from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateTimeField
from wtforms.validators import Required, DataRequired, Length, Email, EqualTo, Regexp, ValidationError, InputRequired
from smiglets.models import Smiglet, Event
from datetime import datetime

############################# smiglet creation form #############################
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', 
                            render_kw={'placeholder':'Mohammad Amir'},
                            validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', 
                            render_kw={'placeholder':'bin Shafiq'},
                            validators=[DataRequired(), Length(min=0, max=50)])
    email = StringField('Email',
                            render_kw={'placeholder':'mabs2'},
                            validators=[DataRequired(), Length(min=0, max=10), Regexp('^\w+$', message="Must be alphanumerical")])
    year_of_study = SelectField('Year of Study', 
                            choices=[("Foundation","Foundation"), ("1st Year", "1st Year"), ("2nd Year", "2nd Year"), ("3rd Year", "3rd Year"),  ("4th Year", "4th Year"), ("Masters", "Masters"), ("PhD", "PhD"), ("Alumni", "Alumni")])
    course = StringField('Course', 
                            render_kw={'placeholder':'Pathway to Medicine'},
                            validators=[DataRequired(), Length(min=0, max=50)])
    malaysian = BooleanField('Are you Malaysian?')
    membership = BooleanField('Membership?')

    editing = False
    # make sure smiglet does not exist in database
    def validate_email(self, email):
        smiglet = Smiglet.query.filter_by(email=email.data).first()
        if not editing and smiglet:
            raise ValidationError('You are already a member!')
        elif editing and not smiglet:
            raise ValidationError('SMIGlet does not exist')

    submit = SubmitField('Join')

############################# membership creation form #############################
class CheckoutForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(min=0, max=10)])
    library_id = StringField('Library ID', render_kw={'placeholder':'0845678912U'},
                            validators=[Regexp('^([0-9])+[UP]$|^$', message="Must contain only numbers and end in U or P")]) #allow empty strings
    submit = SubmitField('Done')

############################# event creation form #############################
class EventForm(FlaskForm):
    name = StringField('Event Name', 
                            render_kw={'placeholder': 'Christavali'},
                            validators=[DataRequired(), Length(min=1, max=50)])
    # TODO: SelectField for event location
    location = StringField('Location', 
                            render_kw={'placeholder': 'Forbes Bar'},
                            validators=[DataRequired(), Length(min=1, max=50)])
    price_member = IntegerField('Member Price',
                            default=0,
                            validators=[DataRequired()])
    price_non_member = IntegerField('Non-member Price',
                            default=0,
                            validators=[DataRequired()])
    date_and_time = DateTimeField('Date and Time',
                            validators=[InputRequired()],
                            format = "%m/%d/%Y %I:%M %p",default= datetime.utcnow())
    submit = SubmitField('Create')

class SearchAttendeeForm(FlaskForm):
    by_name_or_email = StringField('By name or email',
                            render_kw={'placeholder':'Jewel OR Cha OR jcsj'},
                            validators=[Length(min=0, max=10), Regexp('^\w+$', message="Must be alphanumerical and contain only one word")])
    by_library_id = StringField('By Library ID',
                            render_kw={'placeholder':'0841234567U'},
                            validators=[Length(min=0, max=10), Regexp('^([0-9])+[UP]?$|^$', message="e.g. Invalid characters detected")])
    submit = SubmitField('Search')

############################# add attendee form #############################
class AttendeeForm(FlaskForm):
    event_id = IntegerField('Event ID',
                            validators=[DataRequired()])
    smiglet_email = StringField('Smiglet Email',
                            render_kw={'placeholder':'mabs2'},
                            validators=[DataRequired(), Length(min=0, max=10), Regexp('^\w+$', message="Must be alphanumerical")])
    amount_paid = IntegerField('Amount Paid',default=0,
                            validators=[DataRequired()])
    submit = SubmitField('Add')
    
    # make sure event exists in database
    def validate_event_id(self, id):
        event = Event.query.filter_by(id=id.data).first()
        if event == None:
            raise ValidationError('Event does not exist')
    
    # make sure smiglet exists in database
    def validate_smiglet_email(self, email):
        smiglet = Smiglet.query.filter_by(email=email.data).first()
        if smiglet == None:
            raise ValidationError('Smiglet does not exist')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

