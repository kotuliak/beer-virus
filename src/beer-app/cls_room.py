from cls_users import Users

class Room:
    def __init__(self):
        self.users = list()

    def create_user(self, name):
        self.users.append(Users(name))

r1 = Room()
r1.create_user('Michal')
r1.users[0].check()