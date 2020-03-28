from cls_users import Users

class Room:
    def __init__(self):
        self.users = dict()
        self.user_locations = dict()

    def create_user(self, name):
        self.users[name] = Users(name)
        self.user_locations[name] = None
    
    def assign_location(self, name, location):
        self.user_locations[name] = location
        if not(None in self.user_locations.values()):
            self.check_infection()
    
    def check_infection(self):
        infected_locations = list()
        for user in self.user_locations:
            if self.users[user].get_state() == "Sick":
                infected_locations.append(self.user_locations[user])

        infected_locations = list(set(infected_locations))

        for user in self.user_locations:
            if self.user_locations[user] in infected_locations:
                self.users[user].infect()

    

r1 = Room()
r1.create_user('Michal')
r1.create_user('Matej')
print(r1.user_locations)
r1.assign_location('Michal', 'Bathroom')
print(r1.user_locations)
r1.users['Matej'].infect()
r1.assign_location('Matej', "Bathroom")
print(r1.user_locations)
print(r1.users['Michal'].get_state())