# mymodule
import unittest
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

    def testAddPersons(self):
        old_no = self.db.no_of_persons()
        for person in self.persons:
            self.db.add_person(person)
        assert(self.db.no_of_persons() == old_no + self.no_of_persons)
        self.delPersons()

    def testAddEvents(self):
        old_no = self.db.no_of_events()
        for event in self.events:
            self.db.add_event(event)
        assert(self.db.no_of_events() == old_no + self.no_of_events)
        self.delEvents()

    def delEvents(self):
        for event in self.events:
            self.db.del_event(event)
    
    def delPersons(self):
        for person in self.persons:
            self.db.del_person(person)
        assert(self.db.no_of_persons() == 0)

    def printPersons(self):
        for person in self.persons:
            print(person.to_string())
        

    # Create persons

    # Create events

    # Test add event

    # Test add 1 person

    # Test add duplicate person

    # Test add member

    # Test add ID


if __name__ == '__main__':
    unittest.main()