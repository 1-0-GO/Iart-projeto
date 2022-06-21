# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 44:
# 99068 Francisco Martins
# 93740 Miguel Oliveira
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
        self.unass_vars = list(map(lambda x: UnassignedVariable(x, self.board.possible_values(x[0], x[1]), self.board.count_constraints(x[0], x[1])), self.board.get_empty_pos()))
        self.var = None
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def get_var(self):
        """Retorna a variável a alterar neste estado de acordo 
        com as heurísticas MRV e maior grau para desempate"""
        if self.var == None:
            self.var = min(self.unass_vars)
        return self.var    
    
    def count_poss_nums_in_all_empty_boxes(self):
        """Devolve o número de números possíveis em todas 
        as posições livres"""
        return sum(map(lambda x: len(x.domain), self.unass_vars))


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
        """Devolve os valores na vertical ou na horizontal, 
        dependendo do modo, que estão à volta da posição indicada"""
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
        """Devolve todas as posições livres no tabuleiro"""
        return np.argwhere(self.board==2).tolist()
    
    def get_bincount_of_row(self, row):
        """Devolve contagem de 0's, 1's e 2's na linha indicada"""
        return np.bincount(np.ravel(self.board[row, :]))  
    
    def get_bincount_of_col(self, col):
        """Devolve contagem de 0's, 1's e 2's na coluna indicada"""
        return np.bincount(np.ravel(self.board[:, col]))  
    
    def count_constraints(self, row, col):
        """Devolve número de restrições na posição indicada"""
        return sum(map(lambda x: x==2, self.general_adjacent_numbers('h', row, col, 2))) + sum(map(lambda x: x==2, self.general_adjacent_numbers('v', row, col, 2))) 
     
    def possible_values(self, row, col):
        """Devolve os valores possíveis para a posição indicada"""
        poss = [0, 1]
        n = self.size//2 + 1 if self.size%2 else self.size/2
        bins = self.get_bincount_of_col(col), self.get_bincount_of_row(row)
        # check equal number of 0's and 1's
        for b in bins:
            for i in range(2):
                if i in poss and b[i] == n:
                    poss.remove(i)           
        # check no more than two adjacent
        h = self.general_adjacent_numbers('h', row, col, 2)
        v = self.general_adjacent_numbers('v', row, col, 2)
        a = set()
        for i in range(3):
            if h[i] == h[i+1]:
                a.add(h[i])
            if v[i] == v[i+1]:
                a.add(v[i])
        poss2 = [elem for elem in poss if elem not in a] 
        a = []
        # check all rows and collumns are unique
        if bins[0][2] == 1 or bins[1][2] == 1: 
            old = self.board[row, col]
            for val in poss2:    
                self.board[row, col] = val
                mat = np.unique(np.unique(self.board, axis=1), axis=0)
                if mat.shape != self.board.shape:
                    a.append(val)
            self.board[row, col] = old
        return [elem for elem in poss2 if elem not in a]        
            
    
    def insert(self, row, col, num):
        self.board[row, col] = num                      

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


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        var = state.get_var()
        return [(var.pos[0], var.pos[1], num) for num in var.domain]

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = Board(state.board.board.copy(), state.board.size)
        new_board.insert(action[0], action[1], action[2])
        return TakuzuState(new_board)
        
    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return not bool(state.board.get_empty_pos())

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        try:
            return len(node.state.unass_vars)+.5*(node.parent.state.count_poss_nums_in_all_empty_boxes() - node.state.count_poss_nums_in_all_empty_boxes())
        except AttributeError:
            return 0


class UnassignedVariable:
    """Representação de uma posição vazia no tabuleiro"""
    
    def __init__(self, pos, poss_vals, num_constr):
        self.pos = pos
        self.domain = poss_vals
        self.num_constr = num_constr
        
    def __lt__(self, other):
        """Comparação entre duas variáveis pelas heurísticas 
        MRV e maior grau para desempate"""
        return len(self.domain) < len(other.domain) or (len(self.domain) == len(other.domain) and self.num_constr > other.num_constr)

    def __str__(self):
        return ' '.join(str(self.pos) + str(self.domain) + str(self.num_constr))


if __name__ == "__main__":
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    goal_node = greedy_search(problem)
    print(goal_node.state.board)
