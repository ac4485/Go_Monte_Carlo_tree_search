from Go import Go
import numpy as np
from Agent import Agent
from Random_Agent import Random_Agent
from MCTS_agent import MCTS_agent
import multiprocessing as mp
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
class Competition:
  
  '''True: player1 win, False: player2 win'''
  
  move_count = []
  def __init__(self,ag1:Agent,ag2:Agent,bs:int=9,proc_num:int=4):
    '''Agent1 goes first
    '''
    # self.winner = []
    self.a1 = ag1
    self.a2 = ag2
    self.proc_num = proc_num
    self.board_size = bs

  def turns(self,n):
    '''Run n games'''
    # a1 = Random_Agent()
    # a2 = Random_Agent()
    # a2 = MCTS_agent(5,2,self.proc_num)
    r = []
    
    # for _ in range(n):
      # r.append(Competition.turn(self.a1,self.a2))
    # with mp.Pool(self.proc_num) as pool:
    #   a = pool.starmap(Competition.turn,[(a1,a2) for _ in range(n)])
      # r.append(a)
      
    with concurrent.futures.ProcessPoolExecutor() as ppe1:
      # r= list(ppe1.map(Competition.turn,[((deepcopy(self.a1),deepcopy(self.a2)),self.board_size) for _ in range(n)]))
      r= list(ppe1.map(Competition.turn,[(deepcopy(self.a1),deepcopy(self.a2),self.board_size) for _ in range(n)]))


    return r
    
  
  def turn(ags:tuple[Agent,Agent,int]):
    a1 = ags[0]
    a2 = ags[1]
    bs = ags[2]
    fd = True
    g = Go(bs,proc_num=2)
    while not g.game_over():
      if fd:
        nns = a1.move(g)
        # if nns is not None:
        n0,n1 = nns
        g.make_a_move(n0,n1)
      else:
        mm = a2.move(g)
        # if mm is not None:
        m1,m2 = mm
        g.make_a_move(m1,m2)
      fd = not fd
    return g.count_territory()
        

  def get_winners(self):
    return self.winner
