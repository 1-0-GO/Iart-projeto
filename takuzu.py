# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    
    def __init__(self, matrix, size):
        self.board = matrix
        self.size = size
        
    def __str__(self):
        return '\n'.join('\t'.join('%d' %x for x in y) for y in self.board.tolist())
    
    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return self.general_adjacent_numbers('v', row, col, 1)[::-1]

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return self.general_adjacent_numbers('h', row, col, 1)
    
    def general_adjacent_numbers(self, mode, row: int, col: int, radius: int):
        matrix = self.board
        if mode == 'v':
            matrix = self.board.T
            row, col = col, row
        adj = []
        bounds = range(0, self.size)
        for dx in range(0-radius, 1+radius):
            if dx == 0:
                continue
            elif (col + dx) in bounds:
                adj.append(matrix[row, col+dx])
            else:
                adj.append(None)
        return tuple(adj)      
    
    def get_empty_pos(self):
        return np.argwhere(self.board==2).tolist()
    
    def get_bincount_of_row(self, row):
        return np.bincount(np.ravel(self.board[row, :]))  
    
    def get_bincount_of_col(self, col):
        return np.bincount(np.ravel(self.board[:, col]))  
    
    def count_constraints(self, row, col):
        return sum(map(lambda x: x==2, self.general_adjacent_numbers('h', row, col, 2))) + sum(map(lambda x: x==2, self.general_adjacent_numbers('v', row, col, 2))) + bool(self.get_bincount_of_col(col)[2]) + bool(self.get_bincount_of_row(row)[2])
     
    def possible_values(self, row, col):
        poss = [0, 1]
        n = round(self.size/2)
        bins = self.get_bincount_of_col(col), self.get_bincount_of_row(row)
        for b in bins:
            for i in range(2):
                if i in poss and b[i] == n:
                    poss.remove(i)
        h = self.general_adjacent_numbers('h', row, col, 2)
        v = self.general_adjacent_numbers('v', row, col, 2)
        a = set()
        for i in range(3):
            if h[i] == h[i+1]:
                a.add(h[i])
            if v[i] == v[i+1]:
                a.add(v[i])
        return [elem for elem in poss if elem not in a]                        

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        size = int(sys.stdin.readline())
        parsed_input = sys.stdin.read().replace('\t', ' ').replace('\n', '; ')
        return Board(np.matrix(parsed_input[:-2]), size)
    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

class UnassignedVariable:
    
    def __init__(self, pos, poss_vals, num_constr):
        self.pos = pos
        self.poss = poss_vals
        self.num_constr = num_constr
        
    def __lt__(self, other):
        return len(self.poss_vals) < len(other.poss_vals) or (len(self.poss_vals) == len(other.poss_vals) and self.num_constr > other.num_constr)

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
