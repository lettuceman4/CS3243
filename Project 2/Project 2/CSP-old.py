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
    blocked_cells_unflatten = []
    for pos, piece_name in curr_state.dict.items():
        cells = Piece(piece_name, pos).get_valid_moves(board.grid)
        # print("{} at {} but actually at {} moves {}".format(piece_name.name, to_chess_coord(pos), to_chess_coord(piece_name.from_pos), print_moves(cells)))
        blocked_cells_unflatten.append(cells)
    
    blocked_cells = flatten(blocked_cells_unflatten)
    blocked_cells = list(dict.fromkeys(blocked_cells))
    # print("blocked:", print_moves(blocked_cells))
    empty_cells = {}
    grid = board.grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                empty_cells[(r, c)] = 0
    # print(grid[1][0])
    assignable_cells = empty_cells.copy()
    for pos in empty_cells:
        if (pos in blocked_cells):
            del assignable_cells[pos]
    # print("assignaable cells count: ", len(assignable_cells.keys()))
    print("assignaable cells: ", print_moves(assignable_cells.keys()))
    print("        ")
    return assignable_cells

# Using MRV: choose the empty cell that has the least number of assignable pieces-> tuple(int, int):
def select_unassigned_variable(board: Board, curr_state: State):
    # assignable = none other pieces are threatening it 
    # cell must be empty -> get from board.grid
    # board containing remaining of the given pieces
    assignable_cells = get_assignable_cells(board, curr_state)
    # a pqueue of <(pos x, pos y), int> to keep track of number of assignable pieces for each cell given a state, ordered by least num 
    for pos in assignable_cells.keys():
        assignable_piece_num = 0
        for piece, piece_num in board.pieces_num_dict.items():
            if (piece_num > 0):
                piece.update_from_pos(pos)
                # if (piece.name == "Empress"):
                #     print_moves(piece.get_valid_moves(board.grid))
                if (not is_piece_threatening_any_existing(piece, curr_state)):
                    assignable_piece_num += 1
        assignable_cells[pos] += assignable_piece_num
    min_count = 26 * 26
    return_pos = None
    for pos, count in assignable_cells.items():
        if count < min_count and count > 0:
            min_count = count
            return_pos = pos
    return return_pos

def print_moves(moves):
    result = ""
    for move in moves:
        result += str(to_chess_coord(move))
    return result

#for each remaining pieces (already arranged in order of LCV - choose the piece that has the least number of possible moves)

def get_order_domain_values(board: Board, state: State, pos) -> list:
    order_domain_values = []
    for piece, count in board.pieces_num_dict.items():
        if (pos is not None) and count > 0:
            piece.update_from_pos(pos)
            #get only add the value to domain (piece to list) whrn it is not threatening any other pieces
            valid_moves = piece.get_valid_moves(board.grid)
            if (not is_piece_threatening_any_existing(piece, state)):
                order_domain_values.append((len(valid_moves), piece))
    
    order_domain_values.sort(key=lambda a: a[0])
    print(order_domain_values)
    return order_domain_values
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
    result = backtrack(initial_state, board)
    return create_return_state_list(result)

def forward_check(board: Board, pos, state: State):
    possible_values = get_order_domain_values(board, state, pos)
    print("possible val:", possible_values)
    if (len(possible_values) == 0):
        return None
    else:
        return possible_values

def is_piece_threatening_any_existing(piece: Piece, curr_state: State) -> bool:
    valid_moves = piece.get_valid_moves(curr_state.board.grid)
    # print("STATE: ", curr_state.dict)
    # print("{} moves: {}".format(piece.name, print_moves(valid_moves)))
    # print(piece.name, print_moves(valid_moves))
    for move in valid_moves:
        # if curr_state.board.grid[move[0]][move[1]] == -2:
        if move in curr_state.dict and move != piece.from_pos:
            return True
    return False

# function to do CSP backtracking, curr_state is empty at the start
def backtrack(curr_state: State, board: Board) -> State:
    # if assignment is complete (all the given pieces have been assigned its position) -> return the curr_state
    if (board.is_all_pieces_assigned()):
        # print("all pieces assgined")
        return curr_state

    # next cell to have the piece = an empty cell, determined with variable order heuristic - MRV: choose the one that has the least possible number of assignable pieces
    next_cell = select_unassigned_variable(board, curr_state)
    if( next_cell is not None):
        print(to_chess_coord(next_cell))
    # for each remaining pieces (already arranged in order of LCV - choose the piece that has the least number of possible moves)
    remaining_pieces = get_order_domain_values(board, curr_state, next_cell)

    if (next_cell is not None):
        print(to_chess_coord(next_cell), get_tuple1(remaining_pieces))
    # print("remaining_length: ", len(remaining_pieces))
    # print("remaining_pieces: ", remaining_pieces)
    for (move_count, piece) in remaining_pieces:
        # if the piece does not threaten any other piece (consistent with assignment) - then add the piece into curr_state {var = value}
        if (not is_piece_threatening_any_existing(piece, curr_state)):                
            curr_state.dict[next_cell] = piece.name
            print("reture_state: ", create_return_state_list(curr_state))
            board.pieces_num_dict[piece] -= 1
            result = backtrack(curr_state, board)
                # print("state: ", curr_state)

                # if result is not failure then return result
            if result is not None:
                return result
            board.pieces_num_dict[piece] += 1
            
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
    print(goalstate)
    return goalstate #Format to be returned

def main():
    run_CSP()

if __name__ == "__main__":
    main()