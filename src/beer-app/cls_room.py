from cls_users import Users

class Room:
    def __init__(self):
        self.users = list()

    def create_user(self, name):
        self.users.append(Users(name))

    def get_user(self, name):
        for user in self.users:
            if user.name == name:
                return user

r1 = Room()
r1.create_user('Michal')
r1.users[0].check()