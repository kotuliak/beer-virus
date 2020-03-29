import unittest
from cls_user import User
from cls_room import Room

test_users = [User("Luca"), User("Martin"), User("Michal"), User("Matej"), User("Jakub")]


class RoomTest(unittest.TestCase):

    def test_simple(self):
        room = Room()
        room.add_users(test_users)

        assert len(room.users) == len(test_users)

