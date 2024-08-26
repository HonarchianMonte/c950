import datetime
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status, notes):
        #Package details
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.notes = notes
        self.delivery_time = None
        self.departure_time = None

    def update_status(self, current_time):
        if self.ID == 9 and current_time >= datetime.timedelta(hours=10, minutes=20):
            self.address = "410 S State St"
            self.zipcode = "84111"
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time and current_time >= self.departure_time:
            self.status = "En Route"
        else:
            self.status = "At Hub"
