from datetime import datetime
from smiglets import db, app
from smiglets.search import add_to_index, remove_from_index, query_index

NAME_MAX_CHAR = 20
EMAIL_MAX_CHAR = 15
ID_MAX_CHAR = 10
EVENT_MAX_CHAR = 50
# STATUS_OK = "OK"
# STATUS_NOT_EXIST = "NEX"
# STATUS_DUPLICATE = "DUP"

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        emails, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(email=0), 0
        when = []
        for i in range(len(emails)):
            when.append((emails[i], i))
        return cls.query.filter(cls.email.in_(emails)).order_by(
            db.case(when, value=cls.email)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

class Smiglet(SearchableMixin, db.Model):   
    __searchable__ = ['first_name', 'last_name', 'email']

    # id = db.Column(db.Integer, primary_key=True)
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

    def is_member(self):
        print (self.membership.is_member.data)
        return True if str(self.membership[0])=="Member" else False

    def __repr__(self):
        return f"Smiglet('{self.first_name}', '{self.last_name}', '{self.email}', '{self.membership}' '{self.year_of_study}', '{self.course}', '{'Malaysian' if self.malaysian else 'Non-Malaysian'}', '{'Is Committee' if self.committee else 'Non-Committee'}', '')"

class Membership(SearchableMixin, db.Model):
    __searchable__ = ['id_number']

    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(EMAIL_MAX_CHAR), db.ForeignKey('smiglet.email'), nullable=False, primary_key=True)
    is_member = db.Column(db.Boolean, default=False)
    has_paid = db.Column(db.Boolean, default=False)
    id_number = db.Column(db.String(ID_MAX_CHAR), unique=True, nullable=True) # only accept library ID number

    user = db.relationship('Smiglet', back_populates='membership')
    
    def __repr__(self):
        # return f"Membership('{self.smiglet_email}', '{'Member' if self.is_member else 'Non-member'}', '{'Paid' if self.has_paid else 'Not Paid'})"
        return f"{'Member' if self.is_member else 'Non-member'}"

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(EVENT_MAX_CHAR), unique=True, nullable=False) # not allowed to have multiple events with the same name
    price_member = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)
    price_non_member = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)
    datetime = db.Column(db.DATETIME, nullable=False)
    # time = db.Column(db.TIME, nullable=False)
    location = db.Column(db.String(EVENT_MAX_CHAR), nullable=False)
    attendees = db.relationship('Event_Attendee', backref='event', lazy=True)
    guests = db.relationship('Event_Guest', backref='event', lazy=True)

    def __repr__(self):
        return f"Event('{self.id}', '{self.name}', '{self.price_member}', '{self.price_non_member}', '{self.date}', '{self.time}', '{self.location}')"

class Event_Attendee(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False, primary_key=True) #can't have attendee without event
    attendee_email = db.Column(db.String(EMAIL_MAX_CHAR), db.ForeignKey('smiglet.email'), primary_key=True) #cant have attendee without..attendee
    amount_paid = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)

    def __repr__(self):
        return f"Event_Attendee('{self.event_id}', '{self.attendee_email}', '{self.amount_paid}')"

class Event_Guest(SearchableMixin, db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False, primary_key=True) #can't have attendee without event
    name = db.Column(db.String(NAME_MAX_CHAR), nullable=False, primary_key=True) #guests need name
    amount_paid = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False, default=0.00)

    def __repr__(self):
        return f"Event_Guest('{self.event_id}', '{self.name}', '{self.amount_paid}')"

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)