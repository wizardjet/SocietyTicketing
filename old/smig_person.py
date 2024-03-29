class Person:

    def __init__(self, first_name, last_name, email, year, course, malaysian, committee):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.year = year
        self.course = course
        self.id = None
        self.membership = None
        self.malaysian = malaysian
        self.committee = committee

    def to_string(self):
        return f"{self.first_name}, {self.last_name}, {self.email}, {self.year}, {self.course}, {self.malaysian}, {self.committee}"

class ID:

    def __init__(self, type, number):
        self.type = type
        self.number = number
        
class Membership:
    
    def __init__(self, has_paid):
        self.has_paid = has_paid