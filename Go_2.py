import numpy as np

class Go_2:
  board = None
  # true - player1 - 1, false - player2 - 2
  turn = True
  proc_num = 4 # Use 4 processor
  player1_last_move = None
  player2_last_move = None
  player1_trunks = dict()
  player2_trunks = dict()
  move_count= 0
  def __init__(self,proc_num=4):
    '''Config use multiprocessor'''
    
    self.board = np.zeros((19,19))
  def make_a_move(self,i,j):
    '''Make a move to the board.'''
    # if self.move_validation(i,j):
      # player 1
    if self.turn:
      self.board[i,j] = 1
      self.player1_last_move = [i,j]
      Go_2.handle_dead_player2(self.board)
    else:
    # player 2
      self.board[i,j] = 2
      self.player2_last_move = [i,j]
      Go_2.handle_dead_player1(self.board)
    self.move_count += 1
    self.turn = not self.turn
  
  def reset_board(self):
    self.board = np.zeros((19,19))
    self.move_count = 0
    self.player1_last_move = None
    self.player2_last_move = None
    self.player1_trunks.clear()
    self.player2_trunks.clear()
    
  # Return the coordinates of all possible moves with a list.
  def possible_moves(self)->list[list[int,int]]:
    '''Return all the possible moves that satisfied the rule'''

    b00,b01 = np.where(self.board==0)

    if self.turn:
      if self.player1_last_move != None and self.board[self.player1_last_move[0],self.player1_last_move[1]] == 0:
        b00,b01 = Go_2._avoid_repeat_move(b00,b01,self.player1_last_move)
      return Go_2._possible_moves(self.board,1,b00,b01)  
    else:
      if self.player2_last_move != None and self.board[self.player2_last_move[0],self.player2_last_move[1]] == 0:
        b00,b01 = Go_2._avoid_repeat_move(b00,b01,self.player2_last_move)
      return Go_2._possible_moves(self.board,2,b00,b01)
    
  def _avoid_repeat_move(b00,b01,last_move):
    ''' Remove the coordinate of the last move if it's empty. '''
    # b01 = b01[np.where(b01 == self.player2_last_move[1])]
    
    b00 = b00[np.atleast_1d(b00 == last_move[0]).nonzero()]
    b01 = b01[np.atleast_1d(b01 == last_move[0]).nonzero()]
    return b00,b01
  def _possible_moves(board,pn,x0,x1)->list:
    '''Make sure the move isn't in somewhere without any space'''
    r1 = []
    for s,d in zip(x0,x1):
        bb = np.copy(board)
        bb[s,d] = pn
        Go_2.check_q_num_2(bb,pn)
        if not Go_2.contains_dead(bb,pn):
          r1.append([s,d])
    return r1

  def contains_dead(board,pn)->bool:
    '''Check if the board contains any dead trunk of stone. '''
    if pn != 1 and pn != 2:
      return None
    return 0 in Go_2.check_q_num_2(board,pn)
  
  ### Warning Stablized methods ###
  # Check and remove the dead stones of player1.
  def handle_dead_player1(board):
    tr = Go_2.trunk_checker_2(board,1)
    cq = Go_2.check_q_num_2(board,1)
    Go_2._remove_dead_2(board,tr,cq)
    # Check and remove the dead stones of player2.
  def handle_dead_player2(board):
    tr = Go_2.trunk_checker_2(board,2)
    cq = Go_2.check_q_num_2(board,2)
    if len(tr) > 1:
      Go_2._remove_dead_2(board,tr,cq)
  # Do the removal
  def _remove_dead_2(board,trunk,q_num):
    for b in range(len(trunk)):
        if q_num[b] == 0:
          for c in range(len(trunk[b])):
            board[trunk[b][c][0],trunk[b][c][1]] = 0
  ### Warning Stablized methods ###
  # Only return the number of the coordinate of the space of all trunk.
  def check_q_num_2(board,pn)->list:
    if pn != 1 and pn != 2:
      return None
    trunks = Go_2.trunk_checker_2(board,pn)
    spaces = Go_2.single_stone_space_2(board,pn)
    rr = []
    for tr1 in trunks:
      se = set(tr1)
      xd = set()
      for sto in se:
        xd.update(spaces[sto])
      rr.append(len(xd))
    return rr
  # Return the coodinate of all space for each trunk.
  def check_q_2(board,pn)->list[int]:
    if pn != 1 and pn != 2:
      return None
    trunks = Go_2.trunk_checker_2(board,pn)
    spaces = Go_2.single_stone_space_2(board,pn)
    rr = []
    for tr1 in trunks:
      se = set(tr1)
      xd = set()
      for sto in se:
        xd.update(spaces[sto])
      rr.append(xd)
    return rr
  def trunk_checker_2(board,pn:int)->list[list]:
    if pn != 1 and pn != 2:
      return None
    trunks = []
    assc1 = Go_2.around_stone_same_check_2(board,pn)
    while len(assc1) > 0:
      for a in list(assc1):
        vvs = assc1[a]
        if Go_2._count_allies_2(vvs,trunks,a):
          trunks.append([a])
        del assc1[a]
    return trunks

  def _count_allies_2(vvs:list,lst:list,aa)->bool:
    check_all = True
    if vvs != None:
          for indd in range(len(lst)):
            for indd1 in range(len(vvs)):
              if vvs[indd1] in lst[indd]:
                check_all=False
                lst[indd].append(aa)
    return check_all


  # Don't use self
  def single_stone_space_2(board,pn:int)->dict:
    # Must be 1, or 2
    if pn != 1 and pn != 2:
      return None
    ind0,ind1 = np.where(board == pn)
    air = np.empty(board.shape,dtype=object)
    air = dict()
    if len(ind0) > 1:
      for i in range(len(ind0)):
        air[(ind0[i],ind1[i])] = Go_2._single_stone_space_check_2(board,ind0[i],ind1[i])
    elif len(ind0) > 0:
      air[(ind0[0],ind1[0])] = Go_2._single_stone_space_check_2(board,ind0[0],ind1[0])
    return air
  
  def single_stone_space_2a(board,pn:int,i:int,j:int,r1:dict):
    # Must be 1, or 2
    if pn != 1 and pn != 2:
      return None
    r1[(i,j)] = Go_2._single_stone_space_check_2(board,i,j)

  # For each stone color, return the surrounding spaces. Use dict for all except the board.
  def around_stone_same_check_2(board, pn)->dict:
    '''For the stones belong to the player, get the coordinate of the surround stones which have the same color.'''
    # Must be 1, or 2
    if pn != 1 and pn != 2:
      return None
    ind0,ind1 = np.where(board == pn)
    neighbours = dict()
    if len(ind0) > 1:
      for i in range(len(ind0)):
        neighbours[(ind0[i],ind1[i])] = Go_2._around_single_stone_same_check_2(board,ind0[i],ind1[i],pn)
    elif len(ind0) > 0:
      neighbours[(ind0[0],ind1[0])] = Go_2._around_single_stone_same_check_2(board,ind0[0],ind1[0],pn)
    return neighbours
  


  def _around_single_stone_same_check_2(board,i:int,j:int, pn)->list:
    '''Check the surround stones and return coordinate of the one that has the same color if exist. '''
    if pn != 1 and pn != 2:
      return None
    rr = []
    if i > 0 and board[i - 1,j] == pn:
      rr.append((i-1,j))
    if i < 18 and board[i + 1,j] == pn:
      rr.append((i+1,j))
    if j > 0 and board[i,j - 1] == pn:
      rr.append((i,j - 1))
    if j < 18 and board[i,j + 1] == pn:
      rr.append((i,j + 1))
    return list(set(rr))
  
  
  
  def _single_stone_space_check_2(board,i:int,j:int)->list:
    '''Check the surround stones and return coordinate of the space if exist. '''
    if board[i,j] == 0:
      return None
    rr = []
    if i > 0 and board[i - 1,j] == 0:
        rr.append((i-1,j))
    if i < 18 and board[i + 1,j] == 0:
        rr.append((i+1,j))
    if j > 0 and board[i,j - 1] == 0:
        rr.append((i,j - 1))
    if j < 18 and board[i,j + 1] == 0:
        rr.append((i,j + 1))
    return rr

  def print_board(self):
    print(self.board)
  def get_move_count(self)->int:
    return self.move_count
  def game_over(self)->bool:
    return len(self.possible_moves()) < 1
### Warning Stablized methods ###

  def count_territory(self)->bool:
    '''False: player1 win, True: player2 win'''
    return not np.count_nonzero(self.board == 1) - np.count_nonzero(self.board == 2) >10
    
  