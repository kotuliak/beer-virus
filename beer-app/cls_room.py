import random
from state import State
from game_state import GameState
from location import Location

class Room:
    def __init__(self):
        self.id = random.randrange(0, 10000)
        self.users = []
        self.game_state = GameState.NOT_STARTED
        self.nbPlayersWhoMoved = []
        self.nbPlayersWhoVoted = []
        self.round = 0
        self.selectioncheck = False
        self.infected = 0
        self.newcases = 0

    ### ROOM LOGIC

    def add_user(self, user):
        for existing_user in self.users:
            if user.name == existing_user.name:
                raise NameError("User with name " + user.name + " already exists. Please pick a new name.")

        if len(self.users) == 0:
            user.admin=True

        self.users.append(user)
        print("added user " + user.name + " to the room")
        return user

    def add_users(self, users):
        for user in users:
            self.add_user(user)

    def get_user(self, name):
        for user in self.users:
            if name == user.name:
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
        self.game_state = GameState.PLAYING
        self.round = 1
        self.infected = 1
        self.newcases = 1
        self.nbPlayersWhoMoved = []
        self.nbPlayersWhoVoted = []
        self.selectioncheck = False
        self.reset_locations_and_votes()
        for user in self.users:
            user.heal()
            user.quarantineVisits = 0
            user.patient0 = False
            user.stayhome = False

        patient0 = random.choice(self.users)
        patient0.patient0 = True
        patient0.infect()

    def next_round(self):
        self.update_quarantine()
        self.update_users_state()
        self.heal_quarantined()
        self.count_infected()
        self.reset_round()
        return self.update_game_status()

    def reset_round(self):
        self.round += 1
        self.nbPlayersWhoMoved = []
        self.nbPlayersWhoVoted = []
        self.selectioncheck = False
        self.reset_locations_and_votes()

    def reset_locations_and_votes(self):
        for user in self.users:
            user.vote = None
            user.location = Location.HOME


    ### HANDLE USER INPUTS

    def move_user_location(self, name, location):
        user = self.get_user(name)
        user.move_location(Location[location])
        if user not in self.nbPlayersWhoMoved:
            self.nbPlayersWhoMoved.append(user)
        self.selection_check()
        print(str(self.nbPlayersWhoMoved) + "number of players who moved")

    def register_user_vote(self, name, vote):
        user = self.get_user(name)
        user.register_vote(self.get_user(vote))
        if user not in self.nbPlayersWhoVoted:
            self.nbPlayersWhoVoted.append(user)
        self.selection_check()
        print(str(self.nbPlayersWhoVoted) + "number of players who voted")

    ### GAME LOGIC

    def update_users_state(self):
        for location, users_in_location in self.get_locations_dict(self.users).items():
            if location == Location.HOME:
                for user in users_in_location:
                    user.stayhome = False
            elif self.contains_infected(users_in_location):
                for user in users_in_location:
                    user.infect()
            if location == Location.SUPERMARKET:
                for user in users_in_location:
                    user.stayhome = True

    def update_quarantine(self):
        for nomination, users_who_voted in self.get_votes_dict(self.users).items():
            if len(users_who_voted)/len(self.users) > 0.501:
                nomination.quarantine()

    def update_game_status(self):
        if self.check_all_same_state(self.users, State.HEALTHY):
            self.game_state = GameState.GOOD_GUYS_WON
        elif self.check_all_same_state(self.users, State.INFECTED):
            self.game_state = GameState.BAD_GUYS_WON
        else:
            self.game_state = GameState.PLAYING

    def heal_quarantined(self):
        for user in self.users:
            if user.patient0 == True:
                user.state = State.INFECTED
                if user.quarantineVisits == 2:
                    user.state = State.HEALTHY
            elif user.state == State.QUARANTINED:
                    user.state = State.HEALTHY

    def count_infected(self):
        before = self.infected
        count = 0
        for user in self.users:
            if user.state == State.INFECTED:
                count += 1
        self.infected = count
        self.newcases = max(count - before, 0)

    def selection_check(self):
        if len(self.nbPlayersWhoMoved) == len(self.users) and len(self.nbPlayersWhoVoted) == len(self.users):
            self.selectioncheck = True

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
            if user.state == State.QUARANTINED:
                continue
            if user.location in locations_dict:
                locations_dict[user.location].append(user)
            else:
                locations_dict[user.location] = [user]
        return locations_dict

    @staticmethod
    def get_votes_dict(users):
        votes_dict = dict()
        for user in users:
            if user.vote in votes_dict:
                votes_dict[user.vote].append(user)
            else:
                votes_dict[user.vote] = [user]
        return votes_dict

    @staticmethod
    def contains_infected(users_in_location):
        contains_infected = False
        for user in users_in_location:
            contains_infected = contains_infected or user.state == State.INFECTED
        return contains_infected
