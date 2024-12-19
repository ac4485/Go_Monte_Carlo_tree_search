import random
from Tree import Tree
from Agent import Agent
from Random_Agent import Random_Agent
from Go import Go
import numpy as np
from copy import deepcopy
import multiprocessing as mp
from Node import Node
# Incomplete

class MCTS_agent(Agent):
  def __init__(self,level_num:int=4,depth:int=3,proc = 4):
    self.proc = proc
    self.tree = Tree()
    self.game = None
    self.level_num = level_num
    self.depth = depth
    self.c = 0.4
    
  # play the game
  def move(self,g:Go):
    gg = deepcopy(g)
    return self._move(gg)
    
  def _move(self,gg:Go):
    ds,sd,last_nodes = MCTS_agent._expansion(gg,self.level_num,self.depth)
    
    aa = MCTS_agent._simulations(sd,self.depth,self.proc)
    
    MCTS_agent._backpropagation(last_nodes,aa)
    ubcs = []
    for a in ds:
      wimlo1 = a.root.get_win() - a.root.get_loss_count()
      
      ubcs.append(MCTS_agent.ucb1(wimlo1, a.root.get_visited_count(),2.3,a.get_leaf_num() * self.level_num))
    return ds[ubcs.index(max(ubcs))].root.get_data()  
  def _expansion(gg:Go,level2:int=3,dep:int=2):
    ''' return list of Tree, list of Go 
    Every Node expand level2 children, Tree depth: dep.'''
    nlis = []
    node_list = []
    gls = []
    pm = gg.possible_moves()
    
    for _ in range(level2):
      se = random.choice(pm)
      ttt = Tree()
      nn = ttt.get_cursor()
      nn.set_data(se)
      gs1 = deepcopy(gg)
      gs1.make_a_move(se[0],se[1])
      MCTS_agent._expansion_3(nn,gs1,gls,node_list,dep,level2,dep)
      nlis.append(ttt)
    return nlis,gls,node_list
    
  def _expansion_3(tre:Node,gg:Go,gg_list:list[Go],node_list:list[Node],dep_ori:int,level2,dep:int):
    if dep > 0:
      pm = gg.possible_moves()
      dep -= 1
      for _ in range(level2):
        se = random.choice(pm)
        nn = Node(se)
        nn.parent = tre
        gs1 = deepcopy(gg)
        gs1.make_a_move(se[0],se[1])
        tre.child.append(nn)
        if dep == 0:
          gg_list.append(deepcopy(gs1))
          node_list.append(nn)
        MCTS_agent._expansion_3(nn,gs1,gg_list,node_list,dep_ori,level2,dep)

  def _simulation(g:Go, is_player1:bool):
    a1 = Random_Agent()
    turn = is_player1
    while not g.game_over():
      if turn:
        r0,r1 = random.choice(g.possible_moves())
        g.make_a_move(r0,r1)
      else:
        f1,f2 = a1.move(g=g)
        g.make_a_move(f1,f2)
      turn = not turn
    return is_player1 == g.count_territory()
    
  def _simulations(gms:list[Go],depth:int,proc:int)->list[bool]:
    is_player1 = depth % 2 == 0
    '''Return a list of result of each leaf node. '''
    with mp.Pool(8) as pool:
      a = pool.starmap(MCTS_agent._simulation,[(g,is_player1) for g in gms])      
    return a
      
  def _backpropagation(nos:list[Node],win_lst:list[Node]):
    for ind1 in range(len(nos)):
      MCTS_agent._backpropagation_one(nos[ind1],win_lst[ind1])
  

  def _backpropagation_one(nod:Node,won:bool):
    ''' nod: the selected leave. '''
    nod.visited()
    if won:
      nod.win()
    else:
      nod.loss()
    while True:
      nod = nod.parent
      nod.visited()
      if won:
        nod.win()
      else:
        nod.loss()
      if nod.parent == None:
        break
    
  
    

  def ucb1(w:int,n:int,c:float,N:int):
    '''
    w: number of wins, 
    n: the number time the node was visited, 
    N: the number time the parent node was visited, 
    c: factor to balanced betern exploration and exploitation.
    Use only when n, N > 0. 
    '''
    return w / n + c * np.sqrt(np.log(N)/n)