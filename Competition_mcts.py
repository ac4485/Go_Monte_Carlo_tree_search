from Go import Go
import numpy as np
from Agent import Agent
from Random_Agent import Random_Agent
from MCTS_agent import MCTS_agent
from copy import copy
import multiprocessing as mp


class Competition:
  
  '''True: player1 win, False: player2 win'''
  
  move_count = []
  def __init__(self,proc_num = 4):
    '''Agent1 goes first
    '''
    # self.winner = []
    self.proc_num = proc_num

  def turns(self,n):
    '''Run n games'''
    a1 = Random_Agent()
    a2 = MCTS_agent()
    r = []
    with mp.Pool(self.proc_num) as pool:
      a = pool.starmap(Competition.turn,[(a1,a2) for _ in range(n)])
      r.append(a)
    return r
    
  
  def turn(a1,a2):
    fd = True
    g = Go()
    while not g.game_over():
      if fd:
        n0,n1 = a1.move(g.possible_moves())
        g.make_a_move(n0,n1)
      else:
        m1,m2 = a2.move(g.possible_moves(),copy(g))
        g.make_a_move(m1,m2)
        
      fd = not fd
    return g.count_territory()
        

  def get_winners(self):
    return self.winner
