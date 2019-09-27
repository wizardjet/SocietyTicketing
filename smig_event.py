class Event:

    def __init__(self, name, price_non_member, price_member, date, time, location):
        self.name = name
        self.price_non_member = price_non_member
        self.price_member = price_member
        self.date = date
        self.time = time
        self.location = location
        self.attendees = []
        self.guests = []
    
    def add_attendees(self, attendees):
        for attendee in attendees:
            self.attendees.append(attendee)

    def add_guests(self, guests):
        for guest in guests:
            self.guests.append(guest)
