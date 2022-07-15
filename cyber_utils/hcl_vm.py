class VM:
  def __init__(self, name, params):
    self.name = name
    self.params = params
  def clone(self, clone):
    self.name = clone.name
    self.params = clone.params
  def __str__(self):
    print(self.name)
    for i in self.params:
      print(i)
    return ''