class Users:
  def __init__(self, name):
    self.name = name
    self.state = "placeholder_for_state"

  def get_state(self):
    return self.state
  
  def get_name(self):
    return self.name
  
  def change_name(self, name):
    self.name = name

  def heal(self):
    self.state = 'Healthy'

  def infect(self):
    self.state = 'Sick'

u1 = Users("Jakub")
u1.check()

