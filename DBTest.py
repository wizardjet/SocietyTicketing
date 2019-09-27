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
    
    def testAddPersons(self):
        for person in self.persons:
            self.db.add_person(person)
        assert(self.db.no_of_persons() == self.no_of_persons)

    def testDelPersons(self):
        for person in self.persons:
            self.db.del_person(person)
        assert(self.db.no_of_persons() == 0)

    # Create persons

    # Create events

    # Test add event

    # Test add 1 person

    # Test add duplicate person

    # Test add member

    # Test add ID


if __name__ == '__main__':
    unittest.main()