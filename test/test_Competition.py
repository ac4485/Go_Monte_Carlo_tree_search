import unittest, sys,os

sys.path.insert(1,'/home/dds/csc4631/finalP-proj')
from Competition import Competition
from Random_Agent import Random_Agent

class TestCompetition(unittest.TestCase):
  def test_Competition(self):
    comp = Competition(Random_Agent(),Random_Agent())
    # Play a game.
    comp.run_n_times(1)
    

