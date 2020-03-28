class Users:
  def __init__(self, name):
    self.name = name
    self.state = "placeholder_for_state"
    self.location = "Location 1"

  def check(self):
    print("You have user called " + self.name + " and you're " + self.state)

u1 = Users("Jakub")
u1.check()

