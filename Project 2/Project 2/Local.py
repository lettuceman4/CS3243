import sys

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
    def __init__(self, rows_no, columns_no, grid, pieces): 
        self.board = [] * rows_no
        for i in range(columns_no):
            self.board.append([None] * columns_no)
        
        self.grid = grid

        pieces_obj = []

        # pieces is a dict of <(r, c): name>
        for (pos, name) in pieces.items():
            pieces_obj.append(Piece(name, pos))

        self.pieces_obj = pieces_obj

class State:
    # a state is a config of the board -> a dict of <chess position: piece>
    # initial state: receives a dictionary of pieces of form [(r,c), piece]
    # goal state: k pieces, none threatening each other

    def __init__(self, dict, board):
        self.board = board
        self.dict = dict

     # run through the dict, check for each piece possible moves, if dict[possible_move] != null then that piece is threatening another pieace -> heuristic++

    # get the total heuristic of the state - number of pairs threatening each other
    def get_heuristic_of_state(self):
        heuristic = 0
        for (piece) in self.dict.values():
            valid_moves = piece.get_valid_moves(self.board.grid)
            for move in valid_moves:
                if move in self.dict.keys():
                    heuristic += 1

        return heuristic / 2


#############################################################################
######## Implement Search Algorithm
#############################################################################

def generate_next_states(currState: State):
    # remove 1 piece from the original state to create the next state, generate n next states 
    return_state_list = []
    for key, value in currState.dict.items():
        dict_copy = currState.dict.copy()
        del dict_copy[key]
    
        # 1 dict finish populating, generate state
        state = State(dict_copy, currState.board)
        return_state_list.append(state)
    return return_state_list

# def print_state(state: State):
#     dict = {}
#     for (pos, piece) in state.dict.items():
#         (x, y) = to_chess_coord(pos)
#         name = piece.name
#         dict[(x, y)] = name
#         print(name, (x, y), "\n")
    
# get the next state with the lowest heuristic
def get_next_best_state(currState: State):
    next_states = generate_next_states(currState)
    min_H = currState.get_heuristic_of_state()
    min_state = currState

    for state in next_states:
        curr_H = state.get_heuristic_of_state()
        if (curr_H <= min_H):
            min_H = curr_H
            min_state = state
    return min_state, min_H

def create_return_state_list(state: State):
    dict = {}
    for (pos, piece) in state.dict.items():
        (x, y) = to_chess_coord(pos)
        name = piece.name
        dict[(x, y)] = name
    return dict

def search(rows, cols, grid, pieces, k):
    board = Board(rows, cols, grid, pieces) #pieces in board are piece object
    n = len(pieces)

    #populate initial dict 
    dict = {}
    for piece in board.pieces_obj:
        dict[piece.from_pos] = piece
    
    initial_state = State(dict, board)
    curr_state = initial_state
    num_removed = n - int(k)
    while (num_removed > 0):
        curr_state, min_H = get_next_best_state(curr_state)
        
        # there is no pair threatening each other left
        if (min_H == 0):
            return create_return_state_list(curr_state)
        num_removed -= 1
        # random restart when no solution is found
    return create_return_state_list(curr_state)


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
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    k = handle.readline().split(":")[1].strip() # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece    

    return rows, cols, grid, pieces, k

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
def run_local():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    print(goalstate)
    return goalstate #Format to be returned

def main():
    run_local()

if __name__ == "__main__":
    main()