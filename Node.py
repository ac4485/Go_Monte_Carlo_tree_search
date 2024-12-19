import numpy as np

class Node:
  def __init__(self,data:tuple=None):
    '''
    parent store the reference to the upper Node. 
    data store the coordinate of the move. 
    visited_count the time the node was visited. 
    child store the reference to the lower Node. 
    '''
    self.data:tuple = data
    self.parent:Node = None
    self.visited_count:int = 0
    self.win_count:int = 0
    self.lose_count:int = 0
    self.parent = None
    self.child:list[Node] = []


  def is_leaf(self)->bool:
    ''' Check whether contains child. '''
    return len(self.child) == 0

  def get_parent(self):
    ''' Return the parent '''
    return self.parent
  def set_children(self,st:list):
    self.child = st
  def get_children(self)->list:
    ''' Return the set of children '''
    return self.child
  
  def get_child(self,d:tuple)->tuple:
    ''' Return the child that contains the given data. '''
    for a in self.child:
      if d == a.get_data():
        return a
    return None
  def get_data(self)->tuple:
    ''' Return the coordinate'''
    return self.data
  
  def set_data(self,data:tuple):
    self.data = data

  def clear_chilren(self):
    self.child = self.child.clear()

  def print_children_data(self):
    for a in self.child:
      print(a.get_data())
  
  def get_tried_num(self)->int:
    ''' Return the number of the children that has been tried. '''
    return len(x for x in self.child if x.get_visited_count > 0)

  def get_untried_num(self)->int:
    '''Return the number of the children that its visited_count is 0'''
    return len(x for x in self.child if x.get_visited_count == 0)

  def get_untried_set(self)->set:
    '''Return the set that the visited_count is 0'''
    return {x for x in self.child if x.get_visited_count == 0}
  
  def get_no_win_num(self)->int:
    ''' Return the number of children that the win_count == 0 '''
    return len(x for x in self.child if x.get_win() == 0)

  def get_visited_count(self)->int:
    '''Get the visited count from the current Node'''
    return self.visited_count
  
  def get_potential_win_num(self):
    ''' Return a set that the children's win_count > 0 '''
    return len(x for x in self.get_children() if x.get_win() > 0)

  def get_potential_win_set(self):
    ''' Return a set that the children's win_count > 0 '''
    return {x for x in self.get_children() if x.get_win() > 0}

  def get_win(self)->int:
    ''' Return the win count at the current Node. '''
    return self.win_count
  
  def get_loss_count(self)->int:
    ''' Return the loss count at the current Node. '''
    return self.lose_count
  
  # def add_child(self,c:tuple):
  #   self.child.add(Node(c,self.))
  
  # def add_child_empty(self,upper):
  #   self.child.add(Node(upper=upper))
    
  def rm_child(self,data:tuple):
    '''Data: the coordinate'''
    self.child = [x for x in self.child if x.get_data() != data ]
    
  def visited(self):
    self.visited_count += 1
  
  def win(self):
    self.win_count += 1
  
  def loss(self):
    self.lose_count += 1
  def print_node(self):
    print('data ',self.data)
    print('win count ',self.win_count)
    print('lose count ',self.lose_count)
    print('visited count ',self.visited_count)
    print('child count ',len(self.child))
  
    