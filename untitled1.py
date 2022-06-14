# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:38:41 2022

@author: marti
"""
import numpy as np
import sys
from takuzu import Board


#print(sum(map(lambda x: x==2, [2,2,4,3])))
#new_str = "2\t1\t2\t0\n2\t2\t0\t2\n2\t0\t2\t2\n1\t1\t2\t0\n".replace('\t', ' ').replace('\n', '; ')[:-2]
#new_str = "1\t2\n3\t4\n".replace('\t', ' ').replace('\n', '; ')[:-2]
#new_str = sys.stdin.read().replace('\t', ' ').replace('\n', '; ')[2:-2]
#print(new_str)
#a = np.matrix(new_str)
#b = np.matrix('1 2; 3 4')
#print(a)
#print(b)

board = Board.parse_instance_from_stdin() 
print(board)
#print(board.board.tolist())
print(board.get_number(0, 2))
