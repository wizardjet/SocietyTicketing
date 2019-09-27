import random
from smig_person import Person

class Factory:

    def __init__(self):
        self.first_name_list = ["Jane", "Jack", "Jason", "Jacob", "Kristy", "Julianna", "Mohammed"]
        self.last_name_list = ["Bowles", "Jackson", "Smith", "Keyes", "Min", "Lee", "Won"]
        self.year_list = ["1st Year", "2nd Year", "3rd Year", "4th Year", "PhD", "Masters", "Foundation"]
        self.course_list = ["Computer Science", "Medicine", "IR", "History", "Psychology", "Philosophy", "Pathway to Medicine"]

    def random_person(self):
        first_name = random.choice(self.first_name_list)
        last_name = random.choice(self.last_name_list)
        email = self.generate_email(first_name, last_name)
        year = random.choice(self.year_list)
        course = random.choice(self.course_list)
        return Person(first_name, last_name, email, year, course)

    def generate_email(self, first_name, last_name):
        return f"{first_name[0]}{last_name[0]}{random.randint(1,300)}"