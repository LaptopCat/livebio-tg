modes = {"string": "S", "file": "F"}
from rich.console import Console
console = Console()
def mode_enum(a):
  a = a.strip().lower()
  if a in modes:
    return modes[a]
  else:
    console.log("[CONFIG] telegram.auth.mode is invalid. Using default (file)")
    return "F"
class Objectify:
  def __init__(self, thing):
    for k in thing:
      if type(thing[k]) is dict:
        self.__setattr__(k, Objectify(thing[k]))
      else:
        self.__setattr__(k, thing[k])
