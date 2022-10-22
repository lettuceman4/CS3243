import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
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
        # if the position is blocked
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

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard):
    pass

#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    gameboard = {}
    
    enemy_piece_nums = get_par(handle.readline()).split()
    num_enemy_pieces = 0 # Read Enemy Pieces Positions
    for num in enemy_piece_nums:
        num_enemy_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_enemy_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "Black")    

    own_piece_nums = get_par(handle.readline()).split()
    num_own_pieces = 0 # Read Own Pieces Positions
    for num in own_piece_nums:
        num_own_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_own_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "White")    

    return rows, cols, gameboard

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

# You may call this function if you need to set up the board
def setUpBoard():
    config = sys.argv[1]
    rows, cols, gameboard = parse(config)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook, Princess, Empress, Ferz, Pawn (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new ending position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    move = ab(gameboard)
    return move #Format to be returned (('a', 0), ('b', 3))

