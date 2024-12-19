from Node import Node
import numpy as np

class Tree:
  def __init__(self):

    '''The cursor will at the root node.'''
    self.root:Node = Node()
    
    self.current_node:Node = self.root
    
  # def add_current_child(self,data:tuple):    
  #   self.cursor.add_child(data)

  # def get_potential_win(self):
  #   return {x for x in self.cursor.get_children() if x.get_win() > 0}

  
  def get_cursor(self)->Node:
    return self.current_node

  def cursor_up(self):
    '''Move the cursor to the parent'''
    if self.current_node.parent != None:
      self.current_node = self.current_node.parent

  def cursor_down(self,data:tuple[int,int]):
    '''Move the cursor to the selected child. Create a new Node if it's a leaf node.
    Won't change if doesnt exist and not a leaf node. '''
    if not self.current_node.is_leaf():
      for a in self.current_node.child:
        if a.get_data() == data:
          self.current_node = a
    
  def cursor_reset(self):
    self.current_node:Node = self.root
  
  def get_current_data(self):
    return self.current_node.get_data()
    
  def set_current_data(self,data:tuple):
    self.current_node.set_data(data)
    
    
  def get_the_child(self,data:tuple)->Node:
    for a in self.current_node.child:
      if a.get_data() == data:
        return a
      
  def get_children(self)->set:
    return self.current_node.child
    
  def add_child(self,data:tuple):
    '''Add a child Node'''
    nn = Node(data)
    nn.parent = self.current_node
    self.current_node.child.append(nn)

  def add_empty(self):
    ''' Add a Node that has None.'''
    self.add_child(None)
  
  def rm_child(self,data:tuple):
    rms = {x for x in self.current_node.child if x.get_data() == data}
    
    self.current_node.child = {x for x in self.current_node.child if x.get_data() != data}
  
        
  def print_children_data(self):
    self.current_node.print_children_data()
  def get_root(self)->Node:
    return self.root
  def get_total_node_num(self)->int:
    ii = 1
    Tree._bfs_count_node(self.root,ii)
    return ii
  
  def _bfs_count_node(root:Node,ii:int):
    if len(root.child) > 0:
      
      for a in root.child:
        ii+=1
        print(ii)
        Tree._bfs_count_node(a,ii)

  
  def get_node_num(self)->int:
    return Tree._get_node_num(self.root)
    
  
  def _get_node_num(root:Node):
    if root.is_leaf():
      return 1
    else:
      ii:int = 1
      for a in root.child:
        ii = ii + Tree._get_node_num(a)
    return ii
  def get_leaf_num(self):
    ii = 0
    return Tree._get_leaf_num(self.root)
  
  def _get_leaf_num(root:Node):

    if root.is_leaf():
      return 1
    ii = 0
    for a in root.child:
      ii = ii + Tree._get_leaf_num(a)
    return ii
  
  def bfs(self):
    print(self.root.get_data(),'-',1)
    
    Tree._bfs(self.root,1)

  def _bfs(root:Node,ii:int):
    if len(root.child) > 0:
      ii+=1
      for a in root.child:
        a.print_node()
        print(a.get_data(),'-',ii)
        
        Tree._bfs(a,ii)
  def print_root(self):
    self.root.print_node()