import random
from state import State
from game_state import GameState


class Room:
    def __init__(self):
        self.id = random.randrange(0, 10000)
        self.users = []
        self.game_state = GameState.NOT_STARTED
        self.round = -1
        self.nbPlayersWhoPlayedTheirTurn = -1
        self.nbPlayersWhoVoted = -1

    ### ROOM LOGIC

    def add_user(self, user):
        for existing_user in self.users:
            if user.name == existing_user.name:
                raise NameError("User with name " + user.name + " already exists. Please pick a new name.")

        self.users.append(user)
        print("added user " + user.name + " to the room")
        return user

    def add_users(self, users):
        for user in users:
            self.add_user(user)

    def get_user(self, name):
        print("trying to get user " + name)
        for user in self.users:
            if name == user.name:
                print("found user " + name)
                return user
        return None

    def get_healthy_users(self):
        return self.get_users_for_state(State.HEALTHY)

    def get_infected_users(self):
        return self.get_users_for_state(State.INFECTED)

    def get_users_for_state(self, state):
        if self.game_state == GameState.NOT_STARTED:
            return None
        else:
            infected_users = []
            for user in self.users:
                if user.state == state:
                    infected_users.append(user)
            return infected_users

    ### ROUND LOGIC

    def start(self):
        print("Starting game")
        self.game_state = GameState.PLAYING
        self.round = 1
        self.nbPlayersWhoPlayedTheirTurn = 0
        self.nbPlayersWhoVoted = 0

        for user in self.users:
            user.heal()

        infected_user = random.choice(self.users)
        infected_user.infect()
        print("patient zero is " + infected_user.name)

    def next_round(self):
        remaining_locations = len(self.users) - self.nbPlayersWhoPlayedTheirTurn
        if remaining_locations > 0:
            print("Still waiting on " + str(remaining_locations) + " players to choose location")
            raise Exception("Still waiting on " + str(remaining_locations) + " players to choose location")

        remaining_votes = len(self.users) - self.nbPlayersWhoVoted
        if remaining_votes > 0:
            print("Still waiting on " + str(remaining_votes) + " players to choose nomination for quarantine")
            raise Exception("Still waiting on " + str(remaining_votes) + " players to choose nomination for quarantine")

        self.update_users_state()
        self.reset_round()
        return self.update_game_status()

    def reset_round(self):
        self.round += 1
        self.nbPlayersWhoPlayedTheirTurn = 0
        self.nbPlayersWhoVoted = 0
        print("resetting round")

    ### HANDLE USER INPUTS

    def move_user_location(self, name, location):
        user = self.get_user(name)
        user.move_location(location)
        self.nbPlayersWhoPlayedTheirTurn += 1

    def register_user_vote(self, name, nomination):
        user = self.get_user(name)
        user.register_vote(nomination)
        self.nbPlayersWhoVoted += 1
        return None

    ### GAME LOGIC

    def update_users_state(self):
        for location, users_in_location in self.get_locations_dict(self.users).items():
            if self.contains_infected(users_in_location):
                for user in users_in_location:
                    user.infect()

    def update_game_status(self):
        if self.check_all_same_state(self.users, State.HEALTHY):
            self.game_state = GameState.GOOD_GUYS_WON
        elif self.check_all_same_state(self.users, State.INFECTED):
            self.game_state = GameState.BAD_GUYS_WON
        else:
            self.game_state = GameState.PLAYING

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
            if user.location in locations_dict:
                locations_dict[user.location].append(user)
            else:
                locations_dict[user.location] = [user]
        return locations_dict

    @staticmethod
    def contains_infected(users_in_location):
        contains_infected = False
        for user in users_in_location:
            contains_infected = contains_infected or user.state == State.INFECTED
        return contains_infected
