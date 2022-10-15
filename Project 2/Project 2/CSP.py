import heapq
from queue import PriorityQueue
from random import randint
import sys
from typing import Dict
from webbrowser import get
from xmlrpc.client import boolean

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
        if grid[next_pos[0]][next_pos[1]] == -1:
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
    
    def update_from_pos(self, from_pos):
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
    return (chr(grid_pos[1] + 97), grid_pos[0] + 1)

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
                piece = "King"
            elif (i == 1):
                piece = "Queen"
            elif (i == 2):
                piece = "Bishop"
            elif (i == 3):
                piece = "Rook"
            elif (i == 4):
                piece = "Knight"
            elif (i == 5):                
                piece = "Ferz"
            elif (i == 6):    
                piece = "Princess"
            else:                
                piece = "Empress"
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

def print_moves(moves):
    result = ""
    for move in moves:
        result += str(to_chess_coord(move))
    return result

#for each remaining pieces (already arranged in order of LCV - choose the piece that has the least number of possible moves)
def get_tuple1(list):
    result = []
    for item in list:
        result.append(item[1].name)
    return result
def create_return_state_list(state: State):
    dict = {}
    if (state is not None):
        for (pos, piece) in state.dict.items():
            (x, y) = to_chess_coord(pos)
            dict[(x, y)] = piece
    return dict

def search(rows, cols, grid, num_pieces):
    board  = Board(rows, cols, grid, num_pieces)
    initial_state = State({}, board)
    assignable_cells = get_assignable_cells(board, initial_state)
    result = backtrack(initial_state, board, assignable_cells)
    return create_return_state_list(result)

# def forward_check(board: Board, pos, state: State):
#     possible_values = get_order_domain_values(board, state, pos)
#     print("possible val:", possible_values)
#     if (len(possible_values) == 0):
#         return None
#     else:
#         return possible_values

def is_piece_threatening_any_existing(piece: Piece, curr_state: State) -> bool:
    valid_moves = piece.get_valid_moves(curr_state.board.grid)
    for move in valid_moves:
        if move in curr_state.dict and move != piece.from_pos:
            return True
    return False

PIECE_POWER = {
    "King": 7,
    "Ferz": 6,
    "Knight": 5,
    "Bishop": 4,
    "Rook": 3,
    "Princess": 2,
    "Empress": 1,
    "Queen": 0
}

def select_unassigned_piece(pieces: dict) -> str:
    result = PriorityQueue()
    for piece, count in pieces.items():
        if (count > 0):
            # print(piece)
            result.put((PIECE_POWER[piece], piece))
    return (result.get())[1]

def get_assignable_cells(board: Board, state: State):
    # if cell is empty (no obstacle or other piece)
    empty_cells = []
    grid = board.grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (grid[r][c] == 0):
                empty_cells.append((r, c))
    
    blocked_cells = []
    blocked_cells_unflatten = []
    for pos, piece_name in state.dict.items():
        cells = Piece(piece_name, pos).get_valid_moves(board.grid)
        blocked_cells_unflatten.append(cells)
    
    blocked_cells = flatten(blocked_cells_unflatten)
    blocked_cells = list(dict.fromkeys(blocked_cells))

    assignable_cells = empty_cells.copy()
    for pos in empty_cells:
        if (pos in blocked_cells):
            assignable_cells.remove(pos)
    return assignable_cells

# check if the assignment will lead to no other pieces can be assigned
def forward_check_inference(board: Board, state: State) -> bool:
    remaining_cells = get_assignable_cells(board, state)
    total_remaining = 0
    for count in board.pieces_num_dict.values():
        total_remaining += count
    return len(remaining_cells) > total_remaining - 1

def backtrack(curr_state: State, board: Board, assignable_cells: list):
    if (board.is_all_pieces_assigned()):
        return curr_state

    next_piece = select_unassigned_piece(board.pieces_num_dict)
    # print("next_piece: ", next_piece)
    # print("possible_cells: ", print_moves(assignable_cells))

    for cell in assignable_cells:
        curr_piece = Piece(next_piece, cell)
        # check if can put the piece here (not threatening any other pieces)
        if (not is_piece_threatening_any_existing(curr_piece, curr_state)):
            curr_state.dict[cell] = next_piece
            # print(create_return_state_list(curr_state))
            original_val = board.grid[cell[0]][cell[1]]
            board.grid[cell[0]][cell[1]] = -2
            board.pieces_num_dict[next_piece] -= 1 

            if (forward_check_inference(board, curr_state)):
                #update assignable cells
                blocked_cells = curr_piece.get_valid_moves(board.grid)
                for c in blocked_cells:
                    if c in assignable_cells:
                        assignable_cells.remove(c)
                
                result = backtrack(curr_state, board, assignable_cells)
                
                if result is not None:
                    return result

            board.grid[cell[0]][cell[1]] = original_val
            board.pieces_num_dict[next_piece] += 1 
            del curr_state.dict[cell]
            assignable_cells = get_assignable_cells(board, curr_state)

    return None


# function to do CSP backtracking, curr_state is empty at the start
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
    return (int(ch_coord[1:]) - 1, ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    # print(goalstate)
    return goalstate #Format to be returned

def main():
    run_CSP()

if __name__ == "__main__":
    main()