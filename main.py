#!/usr/bin/env python3.12

from Competition import Competition
from Random_Agent import Random_Agent
from MCTS_agent import MCTS_agent
import sys, getopt
import multiprocessing as mp
def main():
    
    options= ['run',]
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hmo:',options)
        for carg,_ in opts:
            if carg == '--run':
                
                is_p1 = bool(args[0]) # p1
                levels = int(args[1]) #level
                depth = int(args[2]) #depth
                proc1= int(args[3]) #proc
                turn_num = int(args[4])
                board_s = int(args[5])
                if args[6] == 'mcts':
                    a1 = MCTS_agent(levels,depth,proc1)
                else:
                    a1 = Random_Agent()
                a2 = Random_Agent()
                
                if is_p1:
                    c1 = Competition(a1,Random_Agent(),board_s,proc1)
                else:
                    c1 = Competition(Random_Agent(),a2,board_s,proc1)
                rr = c1.turns(turn_num)
                len([x for x in rr if rr == True])/len(rr)
                print(rr)
    except getopt.error as err1:
        print('is_p1 levels depth proc turn_num board_size agent[mcts]')
        sys.exit(2)
        
    

if __name__ == "__main__":
    main()