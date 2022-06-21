# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:38:41 2022

@author: marti
"""
import os
import numpy as np
import sys
from takuzu import Board, TakuzuState, Takuzu
from search import (
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
    compare_searchers,
    compare_graph_searchers,
    InstrumentedProblem
)
from random import choices, seed

#print(sum(map(lambda x: x==2, [2,2,4,3])))
#new_str = "2\t1\t2\t0\n2\t2\t0\t2\n2\t0\t2\t2\n1\t1\t2\t0\n".replace('\t', ' ').replace('\n', '; ')[:-2]
#new_str = "1\t2\n3\t4\n".replace('\t', ' ').replace('\n', '; ')[:-2]
# num = int(sys.stdin.readline())
# new_str = sys.stdin.read().replace('\t', ' ').replace('\n', '; ')[:-2]
# print(str(num) + new_str)
#a = np.matrix(new_str)
#b = np.matrix('1 2; 3 4')
#print(a)
#print(b)

# board = Board.parse_instance_from_stdin() 
# print(board)
# print(sum(map(lambda x: x==2, board.board[0, :])))
#print(board.count_constraints(11, 9))
# print(board.general_adjacent_numbers('v', 1, 2, 2))
# print(board.get_number(3, 3))
# twos = np.argwhere(board.board==2)
# print(twos.tolist())
# ls = []
# def my_func(a):
#     ls.append((a[0], a[1]))
# np.apply_along_axis(my_func, 1, twos)
# print(ls)
# a = np.array([0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1])
# print(np.bincount(a))
# for i in range(3):    
#     print(np.bincount(np.ravel(board.board[i,:])))
# print(board.possible_values(0, 0))
# print(max(map(lambda x: x**2, [0,3,2,5,6])))
# initial_state = TakuzuState(board)
# problem = Takuzu(board)
# for action in problem.actions(initial_state):
#     print('\n', problem.result(initial_state, action).board)
# b = np.matrix('1 0 1; 1 0 1; 1 2 1')
# print(any(np.equal(b.T, [1, 2, 0]).all(1)))
# print(np.unique(b, axis = 0))
# print(not bool(np.argwhere(b==0).tolist())) 
# board = Board(b, 3) 
# print(board.possible_values(1, 1))
# print(sum(np.equal(b, b[1, :]).all(1))[0,0])

# stat = TakuzuState(Board.parse_instance_from_stdin())
# print(stat.board)
# print(stat.count_poss_nums_in_all_empty_boxes())

# problem = Takuzu(Board.parse_instance_from_stdin())
# goal_node = greedy_search(problem)
# print(goal_node.state.board, sep="")
# print(np.unique(goal_node.state.board.board, axis = 0).shape == goal_node.state.board.board.shape)

def make_emptier(mat):
    seed(13)
    for i in range(len(mat)):
        for j in range(len(mat)):
            if choices([0, 1], weights=[6, 1])[0] == 1:
                mat[i, j] = 2
    return mat            

boards = []
dire = "../testes-takuzu"

for name in os.listdir(dire):
    if name[0] == 'i':    
        with open(os.path.join(dire, name), 'r') as f:        
            size = int(f.readline())
            parsed_input = f.read().replace('\t', ' ').replace('\n', '; ')
            boards.append(Board(make_emptier(np.matrix(parsed_input[:-2])), size))
problems = [Takuzu(bo) for bo in boards[:-3]]
header = ['Searcher']
other_header = ['Problem' + str(i) for i in range(1, 1 + len(boards))]
header.extend(other_header)
searchers = [breadth_first_tree_search, depth_first_tree_search, greedy_search, astar_search]
compare_searchers(problems, header, searchers)


#print(len(Board.parse_instance_from_stdin().get_empty_pos()))
# compare_graph_searchers()

# bo = Board(make_emptier(np.matrix('2 1 1 0 1; 2 1 0 2 0; 2 0 1 0 2; 2 1 2 1 0; 2 1 1 0 2')), 4)
# print(bo)
# problem = InstrumentedProblem(Takuzu(bo))
# goal_node = greedy_search(problem)