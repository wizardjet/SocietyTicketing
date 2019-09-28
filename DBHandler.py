import getpass
import datetime
import mysql.connector as mariadb
from smig_person import Person
from smig_person import ID
from smig_person import Membership
from smig_event import Event

class DBHandler:

    NAME_MAX_CHAR = 20
    EMAIL_MAX_CHAR = 15
    ID_MAX_CHAR = 10
    EVENT_MAX_CHAR = 50
    STATUS_OK = "OK"
    STATUS_NOT_EXIST = "NEX"
    STATUS_DUPLICATE = "DUP"

    def __init__(self):
        print("Welcome to the SMIG app v0.2")
        self.connect_db()
        self.create_tables()
        self.create_views()

    def connect_db(self):
        try:
            self.mariadb_connection = mariadb.connect(user='smig', password="jommakan_55", database='smig_1920')
            self.cursor = self.mariadb_connection.cursor()
            print("Connect success")
        except Exception as e:
            print(e)
            return None

    def get_password(self):
        try:
            p = getpass.getpass()
        except Exception as error: 
            print('ERROR', error) 
        return p

    def create_tables(self):
        # create the tables that matter
        table_person = f"CREATE TABLE IF NOT EXISTS smig_person (first_name VARCHAR({self.NAME_MAX_CHAR}), last_name VARCHAR({self.NAME_MAX_CHAR}), email VARCHAR({self.EMAIL_MAX_CHAR}) PRIMARY KEY NOT NULL, `year` VARCHAR({self.NAME_MAX_CHAR}), course VARCHAR({self.EVENT_MAX_CHAR}), malaysian BOOLEAN, committee BOOLEAN)"
        table_membership = f"CREATE TABLE IF NOT EXISTS smig_membership (person_email VARCHAR({self.EMAIL_MAX_CHAR}) PRIMARY KEY NOT NULL, status BOOLEAN default 1, has_paid BOOLEAN, CONSTRAINT FOREIGN KEY (person_email) REFERENCES smig_person (email) ON DELETE CASCADE)"
        table_ID = f"CREATE TABLE IF NOT EXISTS smig_ID (person_email VARCHAR({self.EMAIL_MAX_CHAR}) PRIMARY KEY NOT NULL, `type` BOOLEAN, `number` VARCHAR({self.ID_MAX_CHAR}), CONSTRAINT FOREIGN KEY (person_email) REFERENCES smig_person (email) ON DELETE CASCADE)"
        table_event = f"CREATE TABLE IF NOT EXISTS smig_event (id INT PRIMARY KEY AUTO_INCREMENT, `name` VARCHAR({self.EVENT_MAX_CHAR}), price_non_member DECIMAL(10,2), price_member DECIMAL(10,2), `date` DATE, `time` TIME, `location` VARCHAR({self.EVENT_MAX_CHAR}))"
        table_event_attendee = f"CREATE TABLE IF NOT EXISTS smig_event_attendee (event_id INT, person_email VARCHAR({self.EMAIL_MAX_CHAR}), amount_paid DECIMAL(10,2), CONSTRAINT FOREIGN KEY (person_email) REFERENCES smig_person (email) ON DELETE CASCADE, CONSTRAINT FOREIGN KEY (event_id) REFERENCES smig_event (id) ON DELETE CASCADE)"
        table_event_guest = f"CREATE TABLE IF NOT EXISTS smig_event_guest (event_id INT, guest_name VARCHAR({self.NAME_MAX_CHAR}), amount_paid DECIMAL(10,2), CONSTRAINT FOREIGN KEY (event_id) REFERENCES smig_event (id) ON DELETE CASCADE)"
        self.query(table_person)
        self.query(table_membership)
        self.query(table_ID)
        self.query(table_event)
        self.query(table_event_attendee)
        self.query(table_event_guest)

    def create_views(self):
        view_csv = "CREATE VIEW csv AS SELECT ROW_NUMBER() OVER(ORDER BY p.email ASC) AS '#', p.first_name AS 'First Name', p.last_name AS 'Last Name', p.email AS 'Email', m.status AS 'Membership?', m.has_paid AS 'Paid?', p.course AS 'Course', p.malaysian AS 'Malaysian?', p.committee AS 'Committee?', id.type AS 'ID Type', id.number AS 'ID Number' FROM smig_person AS p LEFT JOIN smig_membership AS m ON p.email=m.person_email LEFT JOIN smig_ID as id ON m.person_email=id.person_email"
        self.query(view_csv)

    def query(self, statement):
        try:
            self.cursor.execute(statement)
        except Exception as e:
            print(e)
            return None
        
    def exists_one(self, statement):
        try:
            self.query(statement)
            if (self.cursor.fetchone()[0] == 1):
                return True
        except Exception as e:
            print(e)
        return False

    # adds a person object to smig_person
    def add_person(self, person):
        # check if not exists
        if not self.exists_person(person):
            add_row = f"INSERT INTO smig_person(`first_name`, `last_name`, `email`, `year`, `course`, `malaysian`, `committee`) VALUES ('{person.first_name}', '{person.last_name}', '{person.email}', '{person.year}', '{person.course}', '{1 if person.malaysian else 0}', '{1 if person.committee else 0}')"
            self.query(add_row)
            self.log("add_person", self.STATUS_OK, person.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("add_person", self.STATUS_DUPLICATE, person.to_string())

    # checks the number of persons in smig_person
    def no_of_persons(self):
        get_count = "SELECT COUNT(*) FROM smig_person"
        self.query(get_count)
        return self.cursor.fetchone()[0]
    
    # removes a person object from smig_person
    def del_person(self, person):
        # checks if person exists
        if self.exists_person(person):
            del_row = f"DELETE FROM smig_person WHERE email='{person.email}'"
            self.query(del_row)
            self.log("del_person", self.STATUS_OK, person.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("del_person", self.STATUS_NOT_EXIST, person.to_string())

    # checks if a person exists
    def exists_person(self, person):
        check_exists = f"SELECT COUNT(*) FROM smig_person WHERE email='{person.email}'"
        return self.exists_one(check_exists)
    
    # def get_persons(self):
    #     # get_rows = 

    # adds membership for person
    def add_mem(self, person, has_paid):
        msg = f"{person.email}, {'paid' if has_paid else 'not paid'}"
        # checks if person exists first
        if self.exists_person(person):
            add_row = f"INSERT INTO smig_membership(`person_email`, `has_paid`) VALUES ('{person.email}', '{'1' if has_paid else '0'}')"
            # assigns membership
            mem = Membership(has_paid)
            person.membership = mem
            self.query(add_row)
            self.log("add_mem", self.STATUS_OK, msg)
            self.mariadb_connection.commit()
        else:
            self.log("add_mem", self.STATUS_NOT_EXIST, msg)
    
    # deletes membership for person
    def del_mem(self, person):
        # checks if person is member first
        if self.exists_mem(person):
            del_row = f"DELETE FROM smig_membership WHERE person_email='{person.email}'"
            # unassigns membership
            person.membership = None
            self.query(del_row)
            self.log("del_mem", self.STATUS_OK, person.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("del_mem", self.STATUS_NOT_EXIST, person.to_string())
    
    # checks if a person has paid membership
    def paid_mem(self, person):
        # checks if object is assigned membership
        if person.membership != None:
            return person.membership.has_paid
        # checks if a person is a paid member
        elif self.exists_mem(person):
            check_paid = f"SELECT has_paid FROM smig_membership WHERE person_email='{person.email}'"
            self.query(check_paid)
            has_paid = self.cursor.fetchone[0]
            # assigns membership
            mem = Membership(True if has_paid else False)
            person.membership = mem

    # checks if a member exists
    def exists_mem(self, person):
        check_exists = f"SELECT COUNT(*) FROM smig_membership WHERE person_email='{person.email}'"
        return self.exists_one(check_exists)

    # checks the number of persons in smig_membership
    def no_of_mem(self):
        get_count = "SELECT COUNT(*) FROM smig_membership"
        self.query(get_count)
        return self.cursor.fetchone()[0]

    # adds id number for person
    def add_ID(self, person, type, number):
        # check if exists
        msg = f"{person.email}, {'Library' if type==1 else 'Student'}, {number}"
        if self.exists_person(person):
            if not self.exists_ID(person):
                add_row = f"INSERT INTO smig_ID(`person_email`, `type`, `number`) VALUES ('{person.email}', '{type}', '{number}')"
                # assigns ID
                # TODO: data check
                id = ID(type, number)
                person.ID = id
                self.query(add_row)
                self.log("add_ID", self.STATUS_OK, msg)
                self.mariadb_connection.commit()
            else:
                self.log("add_ID", self.STATUS_DUPLICATE, msg)
        else:
            self.log("add_ID", self.STATUS_NOT_EXIST, msg)

    # deletes ID for person
    def del_ID(self, person):
        id = None
        if person.id != None:
            id = person.id
        elif self.exists_ID(person):
            id = self.get_ID(person)
            del_row = f"DELETE FROM smig_ID WHERE person_email='{person.email}'"
            msg = f"{person.email}, {'Library' if type==1 else 'Student'}, {id.number}"
            self.query(del_row)
            person.id = None
            self.log("del_ID", self.STATUS_OK, msg)
            self.mariadb_connection.commit()
        else:
            self.log("del_ID", self.STATUS_NOT_EXIST, msg)

    # retrieves ID object from data from database
    def get_ID(self, person):
        get_row = f"SELECT type, number FROM smig_ID WHERE person_email='{person.email}'"
        self.query(get_row)
        return ID(self.cursor.fetchone[0], self.cursor.fetchone[1])

    # checks if ID exists
    def exists_ID(self, person):
        check_exists = f"SELECT COUNT(*) FROM smig_ID WHERE person_email='{person.email}'"
        return self.exists_one(check_exists)

    # checks the number of IDs in smig_ID
    def no_of_ID(self):
        get_count = "SELECT COUNT(*) FROM smig_ID"
        self.query(get_count)
        return self.cursor.fetchone()[0]

    # Adds an event to the smig_event
    def add_event(self, event):
        if not self.exists_event(event):
            add_row = f"INSERT INTO smig_event(`name`, `price_non_member`, `price_member`, `date`, `time`, `location`) VALUES ('{event.name}', '{event.price_non_member}', '{event.price_member}','{event.date}', '{event.time}', '{event.location}')"
            self.query(add_row)
            self.log("add_event", self.STATUS_OK, event.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("add_event", self.STATUS_DUPLICATE, event.to_string())

     # checks the number of persons in smig_person
    def no_of_events(self):
        get_count = "SELECT COUNT(*) FROM smig_event"
        self.query(get_count)
        return self.cursor.fetchone()[0]
    
    # removes a person object from smig_person
    def del_event(self, event):
        # checks if event exists
        if self.exists_event(event):
            del_row = f"DELETE FROM smig_event WHERE (`name`='{event.name}' AND `date`='{event.date}' AND `location`='{event.location}')"
            self.query(del_row)
            self.log("del_event", self.STATUS_OK, event.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("del_event", self.STATUS_NOT_EXIST, event.to_string())

    # checks if an event exists
    def exists_event(self, event):
        check_exists = f"SELECT COUNT(*) FROM smig_event WHERE (`name`='{event.name}' AND `date`='{event.date}' AND `location`='{event.location}')"
        return self.exists_one(check_exists)
    
    def get_event_ID(self, event):
        if self.exists_event(event):
            get_id = f"SELECT `id` FROM smig_event WHERE (`name`='{event.name}' AND `date`='{event.date}' AND `location`='{event.location}')"
            self.query(get_id)
            self.log("get_event_ID", self.STATUS_OK, event.to_string())
            event.ID = self.cursor.fetchone()[0]
            return event.ID
        else:
            self.log("get_event_ID", self.STATUS_DUPLICATE, event.to_string())

    def add_attendee(self, event, person, amount_paid):
        if self.exists_event(event) and self.exists_person(person):
            if event.ID == None:
                self.get_event_ID(event)
            add_row = f"INSERT INTO smig_event_attendee (`event_id`, `person_email`, `amount_paid`) VALUES ('{event.ID}', '{person.email}', '{amount_paid}')"
            self.query(add_row)
            self.log("add_attendee", self.STATUS_OK, f"{event.ID}, {person.email}")
            self.mariadb_connection.commit()
        else:
            self.log("add_attendee", self.STATUS_NOT_EXIST, f"{event.ID}, {person.email}")
            
    def log(self, operation, status, string):
        f = open(f"log{datetime.date.today()}.txt","a+")
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ({status}) {operation}: {string}\n")
        f.close()

    # convert to CSV

    # convert from CSV

    # get values from tables

    # create views
