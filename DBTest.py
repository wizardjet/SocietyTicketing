# mymodule
import unittest
import random
from DBHandler import DBHandler
from smig_factory import Factory

class MyModuleTest(unittest.TestCase):

    def setUp(self):
        self.db = DBHandler()
        self.factory = Factory()
        # Create 10 persons, store in array
        self.persons = []
        self.no_of_persons = 10
        for x in range(self.no_of_persons):
            self.persons.append(self.factory.random_person())
        # Create 2 events, store in array
        self.events = []
        self.no_of_events = 4
        for x in range(self.no_of_events):
            self.events.append(self.factory.random_event())

    def tearDown(self):
        self.db.query("DROP TABLE IF EXISTS smig_membership")
        self.db.query("DROP TABLE IF EXISTS smig_ID")
        self.db.query("DROP TABLE IF EXISTS smig_event_attendee")
        self.db.query("DROP TABLE IF EXISTS smig_event_guest")
        self.db.query("DROP TABLE IF EXISTS smig_event")
        self.db.query("DROP TABLE IF EXISTS smig_person")

    def testAddAllPersons(self):
        self.addPersons()
        self.delPersons()

    def testAddAllEvents(self):
        self.addEvents()
        self.delEvents()

    def testAddMembership(self):
        self.addPersons()
        self.addMems()
        self.delMem()
        self.delPersons()

    def testAddID(self):
        self.addPersons()
        self.addMems()
        self.addIDs()
        self.delMem()
        self.delPersons() 
    
    def testAddAttendee(self):
        self.addPersons()
        self.addMems()
        self.addIDs()
        self.addEvents()
        self.addAttendees()
        self.delAttendees()
        self.delMem()
        self.delPersons() 
        self.delEvents()
    
    def addPersons(self):
        for person in self.persons:
            self.db.add_person(person)
        assert(self.db.no_of_persons() == self.no_of_persons)

    def addEvents(self):
        for event in self.events:
            self.db.add_event(event)
        assert(self.db.no_of_events() == self.no_of_events)

    def addMems(self):
        for person in self.persons:
            self.db.add_mem(person, True)
        assert(self.db.no_of_mem() == self.no_of_persons)

    def addIDs(self):
        for person in self.persons:
            self.db.add_ID(person, 1, random.randint(800000000,899999999))
        assert(self.db.no_of_ID() == self.no_of_persons)

    def addAttendees(self):
        # for each person, attend random event
        for person in self.persons:
            self.db.add_attendee(random.choice(self.events), person, 3)
        attendee_count = 0
        for event in self.events:
            attendee_count += self.db.no_of_attendees(event)
        assert(attendee_count == len(self.persons))

    def delEvents(self):
        for event in self.events:
            self.db.del_event(event)
        assert(self.db.no_of_events() == 0)
    
    def delPersons(self):
        for person in self.persons:
            self.db.del_person(person)
        assert(self.db.no_of_persons() == 0)

    def delMem(self):
        for person in self.persons:
            self.db.del_mem(person)
        assert(self.db.no_of_mem() == 0)

    def delAttendees(self):
        for event in self.events:
            # get attendees
            attendees = self.db.get_attendees(event)
            if attendees != None:
                for attendee in attendees:
                    self.db.del_attendee(event, attendee)
        for event in self.events:
            assert(self.db.no_of_attendees(event) == 0)

    def printPersons(self):
        for person in self.persons:
            print(person.to_string())

    # test membership

    # test id

    # Create persons

    # Create events

    # Test add event

    # Test add 1 person

    # Test add duplicate person

    # Test add member

    # Test add ID


if __name__ == '__main__':
    unittest.main()