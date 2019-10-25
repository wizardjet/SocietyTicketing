import random
import names
from smig_person import Person
from smig_event import Event

class Factory:

    def __init__(self):
        # self.first_name_list = ["Jane", "Jack", "Jason", "Jacob", "Kristy", "Julianna", "Mohammed"]
        # self.last_name_list = ["Bowles", "Jackson", "Smith", "Keyes", "Min", "Lee", "Won"]
        self.year_list = ["1st Year", "2nd Year", "3rd Year", "4th Year", "PhD", "Masters", "Foundation"]
        self.course_list = ["Computer Science", "Medicine", "IR", "History", "Psychology", "Philosophy", "Pathway to Medicine"]
        self.event_list = ["Flavours of Malaysia", "Christavali", "Live Lounge", "Freshers Fayre", "Icebreaker", "Taste of Asia", "Capture the Flag"]
        self.location_list = ["Nisbet Room", "Forbes Bar", "Cockshaugh Park", "Sports Hall", "Holy Trinity Church Hall"]

    def random_person(self):
        # first_name = random.choice(self.first_name_list)
        # last_name = random.choice(self.last_name_list)
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = self.generate_email(first_name, last_name)
        year = random.choice(self.year_list)
        course = random.choice(self.course_list)
        malaysian = bool(random.getrandbits(1))
        committee = bool(random.getrandbits(1))
        return Person(first_name, last_name, email, year, course, malaysian, committee)

    def random_event(self):
        name = random.choice(self.event_list)
        price_non_mem = random.randint(4,10)
        price_mem = price_non_mem-2
        date = self.random_date()
        time = self.random_time()
        location = random.choice(self.location_list)
        return Event(name, price_non_mem, price_mem, date, time, location)

    def generate_email(self, first_name, last_name):
        return f"{first_name[0]}{last_name[0]}{random.randint(1,300)}"

    # generates random date YYYY-MM-DD    
    def random_date(self):
        return f"{random.randint(1970,2075)}-{random.randint(1,12)}-{random.randint(1,28)}"

    # generates random 24 time hh:mm:ss
    def random_time(self):
        return f"{random.randint(1,24)}:{random.randint(0,59)}:{random.randint(0,59)}"
