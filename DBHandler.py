import getpass
import datetime
import mysql.connector as mariadb
from smig_person import Person
from smig_event import Event

class DBHandler:

    NAME_MAX_CHAR = 20
    EMAIL_MAX_CHAR = 15
    ID_MAX_CHAR = 10
    EVENT_MAX_CHAR = 50

    def __init__(self):
        print("Welcome to the SMIG app v0.2")
        self.connect_db()
        self.create_tables()

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
        table_person = f"CREATE TABLE IF NOT EXISTS smig_person (first_name VARCHAR({self.NAME_MAX_CHAR}), last_name VARCHAR({self.NAME_MAX_CHAR}), email VARCHAR({self.EMAIL_MAX_CHAR}) PRIMARY KEY NOT NULL, `year` VARCHAR({self.NAME_MAX_CHAR}), course VARCHAR({self.EVENT_MAX_CHAR}))"
        table_membership = f"CREATE TABLE IF NOT EXISTS smig_membership (person_email VARCHAR({self.EMAIL_MAX_CHAR}) PRIMARY KEY NOT NULL, hasPaid BOOLEAN, CONSTRAINT FOREIGN KEY (person_email) REFERENCES smig_person (email) ON DELETE CASCADE)"
        table_ID = f"CREATE TABLE IF NOT EXISTS smig_ID (person_email VARCHAR({self.EMAIL_MAX_CHAR}) PRIMARY KEY NOT NULL, `type` BOOLEAN, `number` VARCHAR({self.ID_MAX_CHAR}), CONSTRAINT FOREIGN KEY (person_email) REFERENCES smig_person (email) ON DELETE CASCADE)"
        table_event = f"CREATE TABLE IF NOT EXISTS smig_event (id INT PRIMARY KEY AUTO_INCREMENT, `name` VARCHAR({self.EVENT_MAX_CHAR}), price_non_member DECIMAL(10,2), price_member DECIMAL(10,2), `date` DATE, `time` TIME, `location` VARCHAR({self.NAME_MAX_CHAR}))"
        table_event_attendee = f"CREATE TABLE IF NOT EXISTS smig_event_attendee (event_id INT, person_email VARCHAR({self.EMAIL_MAX_CHAR}), amount_paid DECIMAL(10,2), CONSTRAINT FOREIGN KEY (person_email) REFERENCES smig_person (email) ON DELETE CASCADE, CONSTRAINT FOREIGN KEY (event_id) REFERENCES smig_event (id) ON DELETE CASCADE)"
        table_event_guest = f"CREATE TABLE IF NOT EXISTS smig_event_guest (event_id INT, guest_name VARCHAR({self.NAME_MAX_CHAR}), amount_paid DECIMAL(10,2), CONSTRAINT FOREIGN KEY (event_id) REFERENCES smig_event (id) ON DELETE CASCADE)"
        self.query(table_person)
        self.query(table_membership)
        self.query(table_ID)
        self.query(table_event)
        self.query(table_event_attendee)
        self.query(table_event_guest)

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
            add_row = f"INSERT INTO smig_person(`first_name`, `last_name`, `email`, `year`, `course`) VALUES ('{person.first_name}', '{person.last_name}', '{person.email}', '{person.year}', '{person.course}')"
            self.query(add_row)
            self.log("add_person", "OK", person.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("add_person", "DUP", person.to_string())

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
            self.log("del_person", "OK", person.to_string())
            self.mariadb_connection.commit()
        else:
            self.log("del_person", "NEX", person.to_string())

    # checks if a person exists
    def exists_person(self, person):
        check_exists = f"SELECT COUNT(*) FROM smig_person WHERE email='{person.email}'"
        return self.exists_one(check_exists)

    # adds membership for person
    def add_membership(self, person, has_paid):
        # check if exists
        check_exists = f"SELECT COUNT(*) FROM smig_person WHERE email='{person.email}'"
        msg = f"{person.email}, {'paid' if has_paid else 'not paid'}"
        if self.exists_one(check_exists):
            add_member_row = f"INSERT INTO smig_membership(`person_email`, `hasPaid`) VALUES ('{person.email}', '{'1' if has_paid else '0'}')"
            print (add_member_row)
            self.query(add_member_row)
            self.log("add_membership", "OK", msg)
            self.mariadb_connection.commit()
        else:
            self.log("add_membership", "NEX", msg)

    # adds id number for person
    def add_ID(self, person, type, number):
        # check if exists
        check_exists = f"SELECT COUNT(*) FROM smig_membership WHERE person_email='{person.email}'"
        msg = f"{person.email}, {'Library' if type==1 else 'Student'}, {number}"
        if self.exists_one(check_exists):
            add_row = f"INSERT INTO smig_ID(`person_email`, `type`, `number`) VALUES ('{person.email}', '{type}', '{number}')"
            print (add_row)
            self.query(add_row)
            self.log("add_ID", "OK", msg)
            self.mariadb_connection.commit()
        else:
            self.log("add_ID", "NEX", msg)

    # Adds an event to the smig_event
    def add_event(self, event):
        check_exists = f"SELECT COUNT(*) FROM smig_event WHERE name='{event.name}'"
        msg = f"{event.name}, {event.price_non_member}, {event.price_member},{event.date}, {event.time}, {event.location}"
        if self.exists_one(check_exists):
            add_row = f"INSERT INTO smig_event(`name`, `price_non_member`, `price_member`, `date`, `time`, `location`) VALUES ('{event.name}', '{event.price_non_member}', '{event.price_member}','{event.date}', '{event.time}', '{event.location}')"
            print (add_row)
            self.query(add_row)
            self.log("add_event", "OK", msg)
            self.mariadb_connection.commit()
        else:
            self.log("add_event", "NEX", msg)

     # checks the number of persons in smig_person
    def no_of_events(self):
        get_count = "SELECT COUNT(*) FROM smig_event"
        self.query(get_count)
        return self.cursor.fetchone()[0]
    
    # removes a person object from smig_person
    def del_event(self, event):
        msg = f"{event.name}, {event.price_non_member}, {event.price_member},{event.date}, {event.time}, {event.location}"
        # checks if event exists
        if self.exists_event(event):
            del_row = f"DELETE FROM smig_event WHERE WHERE `name`='{event.name}' AND `date`='{event.date}' AND `location`='{event.location}'"
            self.query(del_row)
            self.log("del_event", "OK", msg)
            self.mariadb_connection.commit()
        else:
            self.log("del_event", "NEX", msg)

    # checks if an event exists
    def exists_event(self, event):
        check_exists = f"SELECT COUNT(*) FROM smig_event WHERE `name`='{event.name}' AND `date`='{event.date}' AND `location`='{event.location}'"
        return self.exists_one(check_exists)
    # convert to CSV

    # convert from CSV

    # get values from tables

    # create views

    def log(self, operation, status, string):
        f = open(f"log{datetime.date.today()}.txt","a+")
        f.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ({status}) {operation}: {string}\n")
        f.close()
    
# db = DBHandler()
# p1 = Person("Jane", "Smith", "js20", "1", "Computer Science")
# p2 = Person("John", "Sax", "js19", "2", "Physics")
# db.add_person(p1)
# db.add_membership(p2, True)
# db.add_ID(p1, 1, "8080808808")
# db.add_ID(p2, 0, "160009424")
# e1 = Event("Flavours of Malaysia", 10, 8, "2019-5-31", "14:30:00", "Holy Trinity Church Hall")
# db.add_event(e1)