import heapq
from queue import PriorityQueue
from random import randint
import sys
from typing import Dict

def get_manhattan_dist(from_pos, to_pos):
    x = ord(to_pos[0] - from_pos[0])
    y = to_pos[1] - from_pos[1]
    return (x, y)

def get_knight_moves(grid, from_pos):
    possible_moves = []
    # curr_pos_chess_coord = to_chess_coord(from_pos)
    possible_moves.append(from_pos)
    moves1 = get_moves(grid, -2, 1, from_pos, True)
    moves2 = get_moves(grid, -2, -1, from_pos, True)
    moves3 = get_moves(grid, 2, -1, from_pos, True)
    moves4 = get_moves(grid, 2, 1, from_pos, True)
    moves5 = get_moves(grid, 1, 2, from_pos, True)
    moves6 = get_moves(grid, 1, -2, from_pos, True)
    moves7 = get_moves(grid, -1, 2, from_pos, True)
    moves8 = get_moves(grid, -1, -2, from_pos, True)
    possible_moves.append(moves1)
    possible_moves.append(moves2)
    possible_moves.append(moves3)
    possible_moves.append(moves4)
    possible_moves.append(moves5)
    possible_moves.append(moves6)
    possible_moves.append(moves7)
    possible_moves.append(moves8)
    return list(filter(lambda x: x, possible_moves))

def get_straight_moves(grid, curr_pos, is_limited_range):
    possible_moves = []
    # curr_pos_chess_coord = to_chess_coord(curr_pos)
    possible_moves.append(curr_pos)
    moves_left = get_moves(grid, -1, 0, curr_pos, is_limited_range)
    moves_right = get_moves(grid, 1, 0, curr_pos, is_limited_range)
    moves_up = get_moves(grid, 0, -1, curr_pos, is_limited_range)
    moves_down = get_moves(grid, 0, 1, curr_pos, is_limited_range)
    possible_moves.append(moves_left)
    possible_moves.append(moves_right)
    possible_moves.append(moves_up)
    possible_moves.append(moves_down)
    return list(filter(lambda x: x, possible_moves))

def get_diagonal_moves(grid, from_pos, is_limited_range):
    possible_moves = []
    # curr_pos_chess_coord = to_chess_coord(from_pos)
    possible_moves.append(from_pos)
    moves1 = get_moves(grid, 1, 1, from_pos, is_limited_range)
    moves2 = get_moves(grid, 1, -1, from_pos, is_limited_range)
    moves3 = get_moves(grid, -1, -1, from_pos, is_limited_range)
    moves4 = get_moves(grid, -1, 1, from_pos, is_limited_range)
    possible_moves.append(moves1)
    possible_moves.append(moves2)
    possible_moves.append(moves3)
    possible_moves.append(moves4)
    return list(filter(lambda x: x, possible_moves))

def is_still_in_board(grid, grid_pos):
    return grid_pos[0] < len(grid) and grid_pos[1] < len(grid[0]) and grid_pos[0] >= 0 and grid_pos[1] >= 0 

def get_moves(grid, step_x, step_y, curr_pos, is_limited_range):
    moves = []
    #need to check for threatened position
    # need to check if its out of the board
    while(is_still_in_board(grid, curr_pos)):
        next_pos = (curr_pos[0] + step_x, curr_pos[1] + step_y)
        if (not is_still_in_board(grid, next_pos)):
            break
        if grid[next_pos[0]][next_pos[1]] < 0:
            break
        else:
            # next_pos_chess_coord = to_chess_coord(next_pos)
            moves.append(next_pos)
            curr_pos = next_pos
            if (is_limited_range):            
                break
    return moves 

    
class Piece:
    def __init__(self, name, from_pos):
        # standard initialisation of piece
        self.name = name
        self.from_pos = from_pos
    
    def update_from_pos(self, from_pos: tuple[int, int]):
        self.from_pos = from_pos
        
    def get_valid_moves(self, grid):
        if (self.name == "Rook"):
            return flatten(get_straight_moves(grid, self.from_pos, False))
        elif (self.name == "Knight"):
            return flatten(get_knight_moves(grid, self.from_pos))
        elif (self.name == "Bishop"):
            return flatten(get_diagonal_moves(grid, self.from_pos, False))
        elif (self.name == "Queen"):
            moves_straight = get_straight_moves(grid, self.from_pos, False)
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, False)
            moves_straight.append(moves_diagonal)
            return flatten(moves_straight)
        elif (self.name == "King"):
            moves_straight = get_straight_moves(grid, self.from_pos, True)
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, True)
            moves_straight.append(moves_diagonal)
            return flatten(moves_straight)
        elif (self.name == "Ferz"):
            return flatten(get_diagonal_moves(grid, self.from_pos, True))
        elif (self.name == "Princess"):
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, False)
            moves_knight = get_knight_moves(grid, self.from_pos)
            moves_diagonal.append(moves_knight)
            return flatten(moves_diagonal)
        elif (self.name == "Empress"):
            moves_straight = get_straight_moves(grid, self.from_pos, False)
            moves_knight = get_knight_moves(grid, self.from_pos)
            moves_straight.append(moves_knight)
            return flatten(moves_straight)

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

#############################################################################
######## Board
#############################################################################
def to_chess_coord(grid_pos):
    return (chr(grid_pos[1] + 97), grid_pos[0])

def to_grid_coord(chess_pos):
    return (chess_pos[1], ord(chess_pos[0]) - 97)

class Board:
    def __init__(self, rows_no, columns_no, grid, given_pieces_num): 
        self.board = [] * rows_no
        for i in range(columns_no):
            self.board.append([None] * columns_no)
        
        self.grid = grid

        pieces_count_dict = {}
        # pieces is an array of count
        # change to dict of <Piece, count>
        for i in range(len(given_pieces_num)):
            piece = None
            if (i == 0):
                piece = Piece("King", None)
            elif (i == 1):
                piece = Piece("Queen", None)
            elif (i == 2):
                piece = Piece("Bishop", None)
            elif (i == 3):
                piece = Piece("Rook", None)
            elif (i == 4):
                piece = Piece("Knight", None)
            elif (i == 5):                
                piece = Piece("Ferz", None)
            elif (i == 6):    
                piece = Piece("Princess", None)
            else:                
                piece = Piece("Empress", None)
            pieces_count_dict[piece] = given_pieces_num[i]
        self.pieces_num_dict = pieces_count_dict

    def is_all_pieces_assigned(self) -> bool:
        for num_piece in self.pieces_num_dict.values():
            if num_piece != 0:
                return False
        return True

class State:
    # a state is a config of the board -> a dict of <chess position: piece>
    # initial state: receives a dictionary of pieces of form [(r,c), piece]
    # goal state: k pieces, none threatening each other

    def __init__(self, dict: dict, board: Board):
        self.board = board
        self.dict = dict

     # run through the dict, check for each piece possible moves, if dict[possible_move] != null then that piece is threatening another pieace -> heuristic++

    # get the total heuristic of the state - number of pairs threatening each other
    def get_heuristic_of_state(self):
        heuristic = 0
        for (pos, piece) in self.dict.items():
            valid_moves = piece.get_valid_moves(self.board.grid)
            for move in valid_moves:
                if move in self.dict.keys() and move != pos:
                    heuristic += 1
        return heuristic / 2

#############################################################################
######## Implement Search Algorithm
#############################################################################

# get assignable cells - empty AND non-threatened
def get_assignable_cells(board: Board, curr_state: State) -> dict:
    empty_cells = {}
    grid = board.grid
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                empty_cells[(i, j)] = 0
    assignable_cells = empty_cells.copy()
    for piece in curr_state.dict.values():
        valid_moves = piece.get_valid_moves(board.grid)
        for move in valid_moves:
            if move in empty_cells.keys():
                del assignable_cells[move]

    return assignable_cells

# Using MRV: choose the empty cell that has the least number of assignable pieces
def select_unassigned_variable(board: Board, curr_state: State) -> tuple[int, int]:
    # assignable = none other pieces are threatening it 
    # cell must be empty -> get from board.grid
    # board containing remaining of the given pieces
    assignable_cells = get_assignable_cells(board, curr_state)
    # a pqueue of <(pos x, pos y), int> to keep track of number of assignable pieces for each cell given a state, ordered by least num 
    for pos, count1 in assignable_cells.items():
        for piece, piece_num in board.pieces_num_dict.items():
            if (piece_num > 0):
                piece.update_from_pos(pos)
                valid_moves = piece.get_valid_moves()
                for move in valid_moves:
                    # if it doesnt threaten any existing piece (the possible move is not occupied)
                    if move not in curr_state.dict.keys():
                        count1 += piece_num
    min_count = 26 * 26
    return_pos = None
    for pos, count in assignable_cells.items():
        if count < min_count:
            min_count = count
            return_pos = pos
    return return_pos

#for each remaining pieces (already arranged in order of LCV - choose the piece that has the least number of possible moves)
def get_order_domain_values(board: Board, state: State, pos: tuple[int, int]) -> list:
    order_domain_values = PriorityQueue()
    for piece in board.pieces_num_dict.keys():
        piece.update_from_pos(pos)
        valid_moves = piece.get_valid_moves()
        for move in valid_moves:
            # check if its consistent with assignemetn
            if move in state.dict.keys():
                total_possible_moves_num -= 1
        order_domain_values.put(total_possible_moves_num, piece)

    # list of { num of possible moves, piece }
    result = []
    while (not order_domain_values.empty()):
        result.append(order_domain_values.get())

    return result

def create_return_state_list(state: State):
    dict = {}
    for (pos, piece) in state.dict.items():
        (x, y) = to_chess_coord(pos)
        name = piece.name
        dict[(x, y)] = name
    return dict

def search(rows, cols, grid, num_pieces):
    board  = Board(rows, cols, grid, num_pieces)
    initial_state = State({}, board)
    result = backtrack(initial_state, board)
    return create_return_state_list(result)

def forward_check(board: Board, pos: tuple[int, int], state: State):
    possible_values = get_order_domain_values(board, state, pos)
    if (len(possible_values) == 0):
        return None
    else:
        return possible_values

# function to do CSP backtracking, curr_state is empty at the start
def backtrack(curr_state: State, board: Board) -> State:
    # if assignment is complete (all the given pieces have been assigned its position) -> return the curr_state
    if (board.is_all_pieces_assigned()):
        return curr_state

    # next cell to have the piece = an empty cell, determined with variable order heuristic - MRV: choose the one that has the least possible number of assignable pieces
    next_cell = select_unassigned_variable(board, curr_state)

    # for each remaining pieces (already arranged in order of LCV - choose the piece that has the least number of possible moves)
    remaining_pieces = get_order_domain_values(board, next_cell)
    if len(remaining_pieces) > 0:
        for piece in remaining_pieces:
            piece.update_from_pos(next_cell)
            valid_moves = piece.get_valid_moves(board.grid)
            # if the piece does not threaten any other piece (consistent with assignment) - then add the piece into curr_state {var = value}
            for move in valid_moves:
                if move not in curr_state.dict.keys():
                    curr_state.dict[next_cell] = piece
                
            # inferences with forward checking for the current assigned cell
            inferences = forward_check(board, next_cell, curr_state)

            # if inferences not failure then
            if inferences is not None: 
                # add inferences to csp
                # add piece to board (update board grid)
                old_value = board.grid[next_cell[0]][next_cell[1]]
                board.grid[next_cell[0]][next_cell[1]] = -2
                board.pieces_num_dict[piece] -= 1

                # result = backtrack(curr_state) - continues recursively as long as the assignment is viable
                result = backtrack(curr_state, board)

                # if result is not failure then return result
                if result is not None:
                    return result
                
                # remove inferences from csp
                board.grid[next_cell[0]][next_cell[1]] = old_value
                board.pieces_num_dict[piece] += 1

            # remove { var = value }
            del curr_state.dict[next_cell]
        # return None if there is no possible assignment 
    return None

#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    piece_nums = get_par(handle.readline()).split()
    num_pieces = [int(x) for x in piece_nums] #List in the order of King, Queen, Bishop, Rook, Knight

    return rows, cols, grid, num_pieces

def add_piece( comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

#Returns row and col index in integers respectively
def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    return goalstate #Format to be returned

def main():
    run_CSP()

if __name__ == "__main__":
    main()