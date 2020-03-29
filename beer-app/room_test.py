import unittest
from cls_user import User
from cls_room import Room
from location import Location
from game_state import GameState

test_users = [User("Luca"), User("Martin"), User("Michal"), User("Matej"), User("Jakub")]


class RoomTest(unittest.TestCase):

    def test_simple(self):
        room = Room()
        room.add_users(test_users)

        assert len(room.users) == len(test_users)

    def test_complex(self):
        room = Room()
        room.add_users(test_users)

        room.start()

        infected_users = room.get_infected_users()
        assert len(infected_users) == 1

        room.move_user_location(infected_users[0].name, Location.PARK)

        for user in room.get_healthy_users():
            room.move_user_location(user.name, Location.PARK)

        room.next_round()

        assert len(room.get_infected_users()) == len(test_users)
        print(room.game_state)
        assert room.game_state == GameState.BAD_GUYS_WON


