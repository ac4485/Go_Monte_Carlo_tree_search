# Test
import unittest, sys,os

sys.path.insert(1,'/home/dds/csc4631/finalP-proj')
from Go import Go
import numpy as np
from Random_Agent import Random_Agent

class test_Go(unittest.TestCase):
  
  def test_go(self):
    ee = Go()
    ee.make_a_move(3,3) # 1
    # print(len(ee.possible_moves()))
    assert(len(ee.possible_moves())==360)
    # Go.track_trunks_player(ee.board,3,3,1,ee.player1_trunks)
    assert(len(ee.player1_trunks) == 1)
    # Go.track_trunks_player(ee.board,3,3,2,ee.player2_trunks)
    assert(ee.player1_trunks == [{(3, 3)}])

    # # Go.track_trunks_player(ee.board,3,3,1,ee.player1_trunks)
    assert(Go._single_stone_space_check_2(ee.board,3,3) == [(2, 3), (4, 3), (3, 2), (3, 4)])
    ee.make_a_move(5,5) # 2
    assert(len(ee.player2_trunks) == 1)
    assert(len(ee.possible_moves())==359)
    ee.make_a_move(0,5) # 1
    assert(len(ee.player1_trunks) == 2)
    assert(len(ee.possible_moves())==358)
    # ee.player1_trunks

    ee.make_a_move(4,5) # 2
    assert(len(ee.player2_trunks) == 1)
    assert(len(ee.possible_moves())==357)
    ee.make_a_move(3,2) # 1
    assert(len(ee.possible_moves())==356)
    assert(len(ee.player1_trunks) == 2) # player1: 2
    assert(len(ee.player2_trunks) == 1) # player2: 1

      # player1 2 trucks 
      # player2 1 trucks
    assert(Go._single_stone_space_check_2(ee.board,5,5) == [(6, 5), (5, 4), (5, 6)])


    ee.make_a_move(7,7) # 2
    # assert(Go.trunk_checker_2(ee.board,1) == [[(np.int64(0), np.int64(5))],
    #                                  [(np.int64(3), np.int64(2)), (np.int64(3), np.int64(3))]])
    # assert(Go.trunk_checker_2(ee.board,2) == [[(np.int64(4), np.int64(5)), (np.int64(5), np.int64(5))],
    #                                  [(np.int64(7), np.int64(7))]])
    assert(Go._around_single_stone_same_check_2(ee.board,4,5, 2) == [(5,5)])

    # # For test remove dead stones. 
    ee.make_a_move(6,6) # 2
    ee.make_a_move(0,4) # 1
    ee.make_a_move(2,2) # 2
    ee.make_a_move(0,6) # 1
    ee.make_a_move(0,0) # 2
    assert({(0,4)} in ee.player2_trunks)
    assert({(0,6)} in ee.player2_trunks)
    assert({(4,5),(5,5)} in ee.player2_trunks)
    assert({(7,7)} in ee.player2_trunks)
    assert(len(ee.player2_trunks) == 4)

    assert({(np.int64(0), np.int64(0))} in ee.player1_trunks)
    assert({(np.int64(0), np.int64(5))} in ee.player1_trunks)
    assert({(np.int64(2), np.int64(2)),(np.int64(3), np.int64(2)),(np.int64(3), np.int64(3))} in ee.player1_trunks)
    assert({(np.int64(6), np.int64(6))} in ee.player1_trunks)
    assert(len(ee.player1_trunks) == 4)
    assert(len(ee.possible_moves())==350)
    ee.make_a_move(1,5) # 1
    assert(ee.move_count == 12)
    assert(ee.player1_trunks == [{(2, 2), (3, 2), (3, 3)}, {(6, 6)},{(0,0)}])
    assert(ee.player2_trunks == [{(4, 5), (5, 5)}, {(7, 7)}, {(0, 4)}, {(0, 6)}, {(1, 5)}])
    ee.print_board()
    
  def test_go_33(unittest.TestCase):
    g = Go(3)
    a1 = Random_Agent()

    while True:
      n0,n1 = a1.move(g.possible_moves())
      g.make_a_move(n0,n1)

      # dd.append(g.board)
      # ds.append(g.possible_moves())
      g.print_board()
      if g.game_over():
        break

  def test_different_board_size(unittest.TestCase):
    for a in range(3,20,2):
      g = Go(a)
      a1 = Random_Agent()

      while True:
        n0,n1 = a1.move(g.possible_moves())
        g.make_a_move(n0,n1)
        if g.game_over():
          print(g.get_move_count())
          break
      print(str(a) + ' finished')