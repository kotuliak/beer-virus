from state import State
from location import Location

class User:
	def __init__(self, name):
		self.name = name
		self.state = State.HEALTHY
		self.location = Location.HOME
		self.vote = None

	def heal(self):
		print("User " + self.name + " is HEALTHY")
		self.state = State.HEALTHY

	def infect(self):
		print("User " + self.name + " is INFECTED")
		self.state = State.INFECTED

	def quarantine(self):
		print("User " + self.name + " is QUARANTINED")
		self.state = State.QUARANTINED

	def register_vote(self, new_vote):
		print("User " + self.name + " voted for " + str(new_vote))
		self.vote = new_vote

	def move_location(self, new_location):
		if self.location == new_location:
			raise Exception("User is already in that location")
		else:
			print("Moving user " + self.name + " to new location " + str(new_location))
			self.location = new_location