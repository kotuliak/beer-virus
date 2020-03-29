import random
from cls_user import User
from state import State
from game_state import GameState


class Room:
    def __init__(self):
        self.id = random.randrange(0, 10000)
        self.users = []
        self.round = -1
        self.nbPlayersWhoPlayedTheirTurn = -1

    ### ROOM LOGIC

    def add_user(self, user):
        for existing_user in self.users:
            if user.name == existing_user.name:
                raise NameError("User with name " + user.name + " already exists. Please pick a new name.")

        self.users.append(user)
        print("added user " + user.name + " to the room")

    def add_users(self, users):
        for user in users:
            self.add_user(user)

    def get_user(self, name):
        print("trying to get user " + name)
        for user in self.users:
            if name == user.name:
                print("found user " + name)
                return user
        raise LookupError("User with name " + name + " isn't in the room.")

    ### ROUND LOGIC

    def start(self):
        print("Starting game")
        self.round = 1
        self.nbPlayersWhoPlayedTheirTurn = 0

        for user in self.users:
            user.heal()

        infected_user = random.choice(self.users)
        infected_user.infect()
        print("patient zero is " + infected_user.name)

    def next_round(self):
        remaining = len(self.users) - self.nbPlayersWhoPlayedTheirTurn
        if remaining > 0:
            print("Still waiting on " + str(remaining) + " players to play their turn.")
            raise Exception("Still waiting on " + str(remaining) + " players to play their turn.")

        self.update_users_state()
        self.reset_round()
        return self.check_game_status()

    def reset_round(self):
        self.round += 1
        self.nbPlayersWhoPlayedTheirTurn = 0
        print("resetting round")

    ### HANDLE USER INPUTS

    def move_user_location(self, name, location):
        user = self.get_user(name)
        user.move_location(location)
        self.nbPlayersWhoPlayedTheirTurn += 1

    def register_user_vote(self):
        # TODO
        return None

    ### GAME LOGIC

    def update_users_state(self):
        for location, users_in_location in self.get_locations_dict(self.users).items():
            if self.contains_infected(users_in_location):
                for user in users_in_location:
                    user.infect()

    def check_game_status(self):
        if self.check_all_same_state(self.users, State.HEALTHY):
            return GameState.GOOD_GUYS_WON
        elif self.check_all_same_state(self.users, State.INFECTED):
            return GameState.BAD_GUYS_WON
        else:
            return GameState.PLAYING

    @staticmethod
    def check_all_same_state(users, state):
        all_same = True
        for user in users:
            all_same = all_same and user.state == state
        return all_same

    @staticmethod
    def get_locations_dict(users):
        locations_dict = dict()
        for user in users:
            locations_dict[user.location] = user
        return locations_dict

    @staticmethod
    def contains_infected(users_in_location):
        contains_infected = False
        for user in users_in_location:
            contains_infected = contains_infected or user.state == State.INFECTED
        return contains_infected
