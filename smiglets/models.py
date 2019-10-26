from datetime import datetime
from smiglets import db

NAME_MAX_CHAR = 20
EMAIL_MAX_CHAR = 15
ID_MAX_CHAR = 10
EVENT_MAX_CHAR = 50
# STATUS_OK = "OK"
# STATUS_NOT_EXIST = "NEX"
# STATUS_DUPLICATE = "DUP"

class Person(db.Model):
    first_name = db.Column(db.String(NAME_MAX_CHAR), unique=False, nullable=False) # don't need unique
    last_name = db.Column(db.String(NAME_MAX_CHAR), unique=False, nullable=True) # don't need last name
    email = db.Column(db.String(EMAIL_MAX_CHAR), unique=True, nullable=False, primary_key=True) # must have unique email
    membership = db.relationship('Membership', back_populates='user')
    year_of_study = db.Column(db.String(NAME_MAX_CHAR), unique=False, nullable=True) # don't need year of study
    course = db.Column(db.String(NAME_MAX_CHAR), unique=False, nullable=True) # don't need course
    malaysian = db.Column(db.Boolean, default=False)
    committee = db.Column(db.Boolean, default=False)
    events = db.relationship('Event_Attendee', backref='attendee', lazy=True)

    # amount owed, primary join?

    def __repr__(self):
        return f"Person('{self.first_name}', '{self.last_name}', '{self.email}', '{self.membership}' '{self.year_of_study}', '{self.course}', '{'Malaysian' if self.malaysian else 'Non-Malaysian'}', '{'Is Committee' if self.committee else 'Non-Committee'}', '')"

class Membership(db.Model):
    person_email = db.Column(db.String(EMAIL_MAX_CHAR), db.ForeignKey('person.email'), primary_key=True, nullable=False)
    is_member = db.Column(db.Boolean, default=False)
    has_paid = db.Column(db.Boolean, default=False)
    id_number = db.Column(db.String(ID_MAX_CHAR), unique=True, nullable=True) # only accept library ID number

    user = db.relationship('Person', back_populates='membership')

    def __repr__(self):
        return f"Membership('{self.person_email}', '{'Member' if self.is_member else 'Non-member'}', '{'Paid' if self.has_paid else 'Not Paid'})"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(EVENT_MAX_CHAR), unique=True, nullable=False) # not allowed to have multiple events with the same name
    price_member = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)
    price_non_member = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)
    date = db.Column(db.DATE, nullable=False)
    time = db.Column(db.TIME, nullable=False)
    location = db.Column(db.String(EVENT_MAX_CHAR), nullable=False)
    attendees = db.relationship('Event_Attendee', backref='event', lazy=True)
    guests = db.relationship('Event_Guest', backref='event', lazy=True)

    def __repr__(self):
        return f"Event('{self.id}', '{self.name}', '{self.price_member}', '{self.price_non_member}', '{self.date}', '{self.time}', '{self.location}')"

class Event_Attendee(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False, primary_key=True) #can't have attendee without event
    attendee_email = db.Column(db.String(EMAIL_MAX_CHAR), db.ForeignKey('person.email'), primary_key=True) #cant have attendee without..attendee
    amount_paid = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)

    def __repr__(self):
        return f"Event_Attendee('{self.event_id}', '{self.attendee_email}', '{self.amount_paid}')"

class Event_Guest(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False, primary_key=True) #can't have attendee without event
    name = db.Column(db.String(NAME_MAX_CHAR), nullable=False, primary_key=True) #guests need name
    amount_paid = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)

    def __repr__(self):
        return f"Event_Guest('{self.event_id}', '{self.name}', '{self.amount_paid}')"