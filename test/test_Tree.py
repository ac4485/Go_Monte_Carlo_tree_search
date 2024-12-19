import unittest, sys,os

sys.path.insert(1,'/home/dds/csc4631/finalP-proj')
from Tree import Tree

class test_Tree(unittest.TestCase):
  def test_Tree(self):
    rer = Tree()
    rer.set_current_data((2,2))
    print(rer.get_current_data())
    rer.add_child((3,4))
    rer.cursor_down((3,4))
    print(rer.get_current_data())
    print(rer.current_node.get_parent().get_data())
    rer.cursor_up()
    print(rer.get_current_data())
    rer.rm_child((3,4))
    assert(rer.get_leaf_num() == 2)