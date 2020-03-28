import random
from cls_users import Users

class Room:
    def __init__(self):
        self.id = random.randrange(0, 1000)
        self.users = list()
        print("id is " + str(self.id))

    def create_user(self, name):
        self.users.append(Users(name))

    def get_user(self, name):
        for user in self.users:
            if user.name == name:
                return user