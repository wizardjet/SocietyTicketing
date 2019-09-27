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

    # def testAddAllPersons(self):
    #     old_no = self.db.no_of_persons()
    #     self.addPersons()
    #     assert(self.db.no_of_persons() == old_no + self.no_of_persons)
    #     self.delPersons()

    # def testAddAllEvents(self):
    #     old_no = self.db.no_of_events()
    #     self.addEvents()
    #     assert(self.db.no_of_events() == old_no + self.no_of_events)
    #     self.delEvents()

    # def testAddMembership(self):
    #     self.addPersons()
    #     self.addMems()
    #     assert(self.db.no_of_mem() == self.no_of_persons)
    #     self.delMem()
    #     assert(self.db.no_of_mem() == 0)
    #     self.delPersons()

    def testAddID(self):
        self.addPersons()
        self.addMems()
        self.addIDs()
        assert(self.db.no_of_ID() == self.no_of_persons)
        # self.delMem()
        # self.delPersons() 

    def addPersons(self):
        for person in self.persons:
            self.db.add_person(person)

    def addEvents(self):
        for event in self.events:
            self.db.add_event(event)

    def addMems(self):
        for person in self.persons:
            self.db.add_mem(person, True)

    def addIDs(self):
        for person in self.persons:
            self.db.add_ID(person, 1, random.randint(800000000,899999999))

    def delEvents(self):
        old_no = self.db.no_of_events()
        for event in self.events:
            self.db.del_event(event)
        # assert(old_no - self.db.no_of_events() == self.no_of_events)
    
    def delPersons(self):
        for person in self.persons:
            self.db.del_person(person)
        assert(self.db.no_of_persons() == 0)

    def delMem(self):
        for person in self.persons:
            self.db.del_mem(person)

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