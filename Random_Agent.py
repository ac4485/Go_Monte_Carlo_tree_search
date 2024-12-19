from Agent import Agent
import numpy as np
import os
import random
from Go import Go
class Random_Agent(Agent):
  def __init__(self):
    pass
  def move(self,g:Go)->tuple:
    '''Return the selected move'''
    possible_moves = g.possible_moves()
    if len(possible_moves) > 0:
      return possible_moves[Random_Agent.pick(possible_moves)]
    else:
      return []
  def pick(pm:list)->int:
    return int((len(pm) - 1) * int.from_bytes(os.urandom(2),byteorder='big') / 65536)