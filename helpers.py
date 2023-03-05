mode_enum = lambda a: {"string": "S", "file": "F"}[a.strip().lower()]
class Objectify:
  def __init__(self, thing):
    for k in thing:
      if type(thing[k]) is dict:
        self.__setattr__(k, Objectify(thing[k]))
      else:
        self.__setattr__(k, thing[k])
from rich.console import Console
console = Console()