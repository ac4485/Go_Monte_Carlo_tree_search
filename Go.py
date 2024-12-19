import numpy as np
from copy import copy

class Go:
  
  # true - player1 - 1, false - player2 - 2
  turn = True
  proc_num = 4 
  
  move_count= 0
  def __init__(self,siz:int=19,proc_num=4):
    '''Config use multiprocessor'''
    self.player1_last_move:tuple = None
    self.player2_last_move:tuple = None
    self.turn = True
    self.player1_trunks:list[set] = []
    self.player2_trunks:list[set] = []
    self.siz = siz
    self.board = np.zeros((siz,siz))
    self.proc_num = proc_num # Use 4 processor
    self.move_count = 0
    self.pass_count = 0
  def make_a_move(self,i,j):
    '''Make a move to the board.'''
    if i == None or j == None:
      self.pass_count+= 1
    else:
      if self.turn:
        self.board[i,j] = 1
        self.player1_last_move = (i,j)
        Go.track_trunks_player(self.board,i,j,1,self.player1_trunks,self.siz)
        # Kill a stone require at least 3 moves
        if self.move_count > 0:
          ddd = Go.remove_dead(self.board,self.player2_trunks)
          self.player2_trunks = ddd

      else:
        self.board[i,j] = 2
        self.player2_last_move = (i,j)
        Go.track_trunks_player(self.board,i,j,2,self.player2_trunks,self.siz)
        # Kill a stone require at least 3 moves

        if self.move_count > 0:
          ddd = Go.remove_dead(self.board,self.player1_trunks)
          # print(ddd)
          self.player1_trunks = ddd
    self.move_count+=1
    self.turn = not self.turn
    
  def contains_dead(board,trunks:list[set])->bool:
    ''' Check if the trunk of stone is dead. '''
    for ind in range(len(trunks)):
      if Go.trunk_dead(board,trunks[ind]):
        return True
    return False
      
  # def player1_handle_dead(self):
    
  # def player2_handle_dead(self):
  def remove_dead(board,trunks:list[set]):
    ''' Remove the list of trunk that has no space.
    Return the updated trunks'''
    # Get the dead list.
    
    trunks_remove = [x for x in trunks if Go.trunk_dead(board,x)]
    if len(trunks_remove) > 0:
      for tm in trunks_remove:
        for a,b in tm:
          board[a,b] = 0
      # Track the trunks
    return [x for x in trunks if not Go.trunk_dead(board,x)]
      
    
  def trunk_dead(board,s:set)->bool:
      spa = set()
      for p in s:
        sc:list[tuple] = Go._single_stone_space_check_2(board,p[0],p[1],board.shape[0])
        spa.update(sc)
      return len(spa) == 0

  def track_trunks_player(board,i:int,j:int,pn:int,trunks:list[set],siz:int):
    '''Track the trunks on the board for each player, avoid calculate everything every round.
    pn: 1 means player 1, 2 means player 2.'''
    assc1 = Go._around_single_stone_same_check_2(board,i,j,siz,pn)
    
    if len(assc1) > 0:
      for x in assc1:
        for tr in trunks:
          if x in tr:
            tr.add((i,j))
      if len(assc1) > 1:
        # 1,2,3,4
        a = 0
        b = 0
        while a < len(trunks) - 1:
          if (i,j) in trunks[a]:
            b = a + 1
            while b < len(trunks):
              if (i,j) in trunks[b]:
                trunks[a].update(trunks[b])
                trunks.remove(trunks[b])
              b += 1
            break
          a += 1
            
    else:
      s = set()
      s.add((i,j))
      if s not in trunks:
        trunks.append(s)

  def possible_moves(self):
    '''Return all the possible moves that satisfied the rule'''
    b00,b01 = np.where(self.board==0)
    if self.turn:
      empty_p = [v for v in zip(b00,b01) if v != self.player1_last_move]
      
      empty_p = [v for v in empty_p if Go.move_validate(self.board,v[0],v[1],1,self.player1_trunks,self.player2_trunks,self.siz)]
      
    else:
      empty_p = [v for v in zip(b00,b01) if v != self.player2_last_move]
      empty_p = [v for v in empty_p if Go.move_validate(self.board,v[0],v[1],2,self.player1_trunks,self.player2_trunks,self.siz)]
    empty_p.append((None,None))
    return empty_p

  def move_validate(board,i:int,j:int,pn:int,trunksp1,trunksp2,siz:int)->bool:
    ass1 = Go._around_single_stone_same_check_2(board,i,j,siz,pn)
    ass2 = Go._single_stone_space_check_2(board,i,j,siz)
    if len(ass2) == 0:
      if len(ass1) > 0:
        bb = np.copy(board)
        trunks1 = copy(trunksp1)
        trunks2 = copy(trunksp2)
        if pn == 1:
          bb[i,j] = 1
          Go.track_trunks_player(bb,i,j,1,trunks1,siz)
          Go.remove_dead(bb,trunks2)
          return not Go.contains_dead(bb,trunks1)
          
        elif pn == 2:
          bb[i,j] = 2
          Go.track_trunks_player(bb,i,j,2,trunks1,siz)
          Go.remove_dead(bb,trunks1)
          return not Go.contains_dead(bb,trunks2)
          
      else:
        return False
    else:
      return True
    
  def _around_single_stone_same_check_2(board,i:int,j:int,siz:int, pn)->list:
    '''Check the surround stones and return coordinate of the one that has the same color if exist. 
    If pn is not 1 or 2, return None'''
    if pn != 1 and pn != 2:
      return None
    rr = []
    # up
    if i > 0 and board[i - 1,j] == pn:
      rr.append((i-1,j))
    # down
    if i < siz - 1 and board[i + 1,j] == pn:
      rr.append((i+1,j))
    # left
    if j > 0 and board[i,j - 1] == pn:
      rr.append((i,j - 1))
    # right
    if j < siz - 1 and board[i,j + 1] == pn:
      rr.append((i,j + 1))
    return rr
  
  def _single_stone_space_check_2(board,i:int,j:int,siz:int)->list:
    '''Check the surround stones and return coordinate of the space if exist. 
    If None, return []'''
    rr = []
    # up
    if i > 0 and board[i - 1,j] == 0:
        rr.append((i-1,j))
    # down
    if i < siz - 1 and board[i + 1,j] == 0:
        rr.append((i+1,j))
    # left
    if j > 0 and board[i,j - 1] == 0:
        rr.append((i,j - 1))
    # right
    if j < siz - 1 and board[i,j + 1] == 0:
        rr.append((i,j + 1))
    return rr

    
  def print_board(self):
    print(self.board)
  def get_move_count(self)->int:
    return self.move_count
  def game_over(self)->bool:
    return len(self.possible_moves()) < 5 or self.move_count > 370 or self.pass_count > 1
### Warning Stablized methods ###

  def count_territory(self)->bool:
    '''True: player1 win, False: player2 win, player 1 need to win 4 more space to win.'''
    p1,p2 = self.tromp_taylor_rules()
    return p1 - 4 > p2
  def tromp_taylor_rules(self):
    n0,n1 = np.where(self.board == 0)
    p1 = np.count_nonzero(self.board == 1)
    p2 = np.count_nonzero(self.board == 2)
    d = 0
    for a,b in zip(n0,n1):
      d+=1
      nn = Go.check_stones_belonging(self.board,a,b,self.siz)
      if nn == 1:
        p1 += 1
      elif nn == 2:
        p2 += 1
    return p1,p2
      
  def check_stones_belonging(board,i,j,siz)->int:
    '''Find the owner of the space'''
    
    i0 = i
    j0 = j
    cc = set()
    # check up
    while i0 > 0:
      if i0 > 0 and board[i0,j0] == 0:
        i0 -= 1
      else:
        cc.add(board[i0,j0])
        break
    i0 = i
    # check down
    while i0 < siz - 1:
      if i0 < siz - 1 and board[i0,j0] == 0:
        i0 += 1
      else:
        cc.add(board[i0,j0])
        break
    i0 = i
    # check left
    while j0 > 0:
      if j0 > 0 and board[i0,j0] == 0:
        j0 -= 1
      else:
        cc.add(board[i0,j0])
        break
    j0 = j

    # check right
    while j0 < siz - 1:
      if j0 < siz - 1 and board[i0,j0] == 0:
        j0 += 1
      else:
        cc.add(board[i0,j0])
        break
    cc = [x for x in cc if x != 0]
    if len(cc) == 1:
      return cc.pop()
    else:
      return 0