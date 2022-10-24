import copy
import sys

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

WHITE = "White"
BLACK = "Black"
ROWS = 7
COLUMNS = 7
DEPTH = 4
PIECE_VALUES = {
    "Pawn": 1,
    "Ferz": 2,
    "Knight": 3,
    "Bishop": 4,
    "Rook": 5,
    "Princess": 6,
    "Empress": 7,
    "Queen": 8,
     "King": 100,
}

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
def is_still_in_board(grid, grid_pos):
    return grid_pos[0] < len(grid) and grid_pos[1] < len(grid[0]) and grid_pos[0] >= 0 and grid_pos[1] >= 0 

def get_moves(grid, step_x, step_y, curr_pos, is_limited_range, is_white):
    moves = []
    # need to check if its out of the board
    while(is_still_in_board(grid, curr_pos)):
        next_pos = (curr_pos[0] + step_x, curr_pos[1] + step_y)
        if (not is_still_in_board(grid, next_pos)):
            break

        # only blocked by own piece, 
        # and break right after taking another piece
        if (is_capturing_next_pos(next_pos, grid, is_white)):
            moves.append(next_pos)
            break
        # not capturing and still in board
        else:
            if (grid[next_pos[0]][next_pos[1]] is None):
                moves.append(next_pos)
                curr_pos = next_pos
                if (is_limited_range):            
                    break
            else:
                break
    return moves 

def get_knight_moves(grid, from_pos, is_white):
    possible_moves = []
    # curr_pos_chess_coord = to_chess_coord(from_pos)
    possible_moves.append(from_pos)
    moves1 = get_moves(grid, -2, 1, from_pos, True, is_white)
    moves2 = get_moves(grid, -2, -1, from_pos, True, is_white)
    moves3 = get_moves(grid, 2, -1, from_pos, True, is_white)
    moves4 = get_moves(grid, 2, 1, from_pos, True, is_white)
    moves5 = get_moves(grid, 1, 2, from_pos, True, is_white)
    moves6 = get_moves(grid, 1, -2, from_pos, True, is_white)
    moves7 = get_moves(grid, -1, 2, from_pos, True, is_white)
    moves8 = get_moves(grid, -1, -2, from_pos, True, is_white)
    possible_moves.append(moves1)
    possible_moves.append(moves2)
    possible_moves.append(moves3)
    possible_moves.append(moves4)
    possible_moves.append(moves5)
    possible_moves.append(moves6)
    possible_moves.append(moves7)
    possible_moves.append(moves8)
    return list(filter(lambda x: x, possible_moves))

def is_capturing_next_pos(next_pos, grid, is_white):
    if (is_still_in_board(grid, next_pos)):
        if (grid[next_pos[0]][next_pos[1]] is not None):
            piece = grid[next_pos[0]][next_pos[1]]
            return piece.is_white != is_white
    return False

def get_pawn_moves(grid, curr_pos, is_white):
    moves = []
    dir = 1 if is_white else -1
    next_pos_straight = (curr_pos[0], curr_pos[1] + dir)
    next_pos_diagonal_right = (curr_pos[0] + dir, curr_pos[1] + dir)
    next_pos_diagonal_left = (curr_pos[0] - dir, curr_pos[1] + dir)
    
    # straight move only execute if no piece in front
    if (is_still_in_board(grid, next_pos_straight) 
    and grid[next_pos_straight[0]][next_pos_straight[1]] is None):
        moves.append(next_pos_straight)

    if (is_capturing_next_pos(next_pos_diagonal_right)):
        moves.append(next_pos_diagonal_right)
    
    if (is_capturing_next_pos(next_pos_diagonal_left)):
        moves.append(next_pos_diagonal_left)
    return moves

def get_straight_moves(grid, curr_pos, is_limited_range, is_white):
    possible_moves = []
    # curr_pos_chess_coord = to_chess_coord(curr_pos)
    possible_moves.append(curr_pos)
    moves_left = get_moves(grid, -1, 0, curr_pos, is_limited_range, is_white)
    moves_right = get_moves(grid, 1, 0, curr_pos, is_limited_range, is_white)
    moves_up = get_moves(grid, 0, -1, curr_pos, is_limited_range, is_white)
    moves_down = get_moves(grid, 0, 1, curr_pos, is_limited_range, is_white)
    possible_moves.append(moves_left)
    possible_moves.append(moves_right)
    possible_moves.append(moves_up)
    possible_moves.append(moves_down)
    return list(filter(lambda x: x, possible_moves))

def get_diagonal_moves(grid, from_pos, is_limited_range, is_white):
    possible_moves = []
    # curr_pos_chess_coord = to_chess_coord(from_pos)
    possible_moves.append(from_pos)
    moves1 = get_moves(grid, 1, 1, from_pos, is_limited_range, is_white)
    moves2 = get_moves(grid, 1, -1, from_pos, is_limited_range, is_white)
    moves3 = get_moves(grid, -1, -1, from_pos, is_limited_range, is_white)
    moves4 = get_moves(grid, -1, 1, from_pos, is_limited_range, is_white)
    possible_moves.append(moves1)
    possible_moves.append(moves2)
    possible_moves.append(moves3)
    possible_moves.append(moves4)
    return list(filter(lambda x: x, possible_moves))

class Piece:
    def __init__(self, name, from_pos, is_white):
        # standard initialisation of piece
        self.name = name
        self.from_pos = from_pos
        self.is_white = is_white
    
    def update_from_pos(self, from_pos):
        self.from_pos = from_pos
        
    def get_valid_moves(self, grid):
        if (self.name == "Rook"):
            return flatten(get_straight_moves(grid, self.from_pos, False, self.is_white))
        elif (self.name == "Pawn"):
            return flatten(get_straight_moves(grid, self.pos, ))
        elif (self.name == "Knight"):
            return flatten(get_knight_moves(grid, self.from_pos, self.is_white))
        elif (self.name == "Bishop"):
            return flatten(get_diagonal_moves(grid, self.from_pos, False, self.is_white))
        elif (self.name == "Queen"):
            moves_straight = get_straight_moves(grid, self.from_pos, False, self.is_white)
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, False, self.is_white)
            moves_straight.append(moves_diagonal)
            return flatten(moves_straight)
        elif (self.name == "King"):
            moves_straight = get_straight_moves(grid, self.from_pos, True, self.is_white)
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, True, self.is_white)
            moves_straight.append(moves_diagonal)
            return flatten(moves_straight)
        elif (self.name == "Ferz"):
            return flatten(get_diagonal_moves(grid, self.from_pos, True, self.is_white))
        elif (self.name == "Princess"):
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, False, self.is_white)
            moves_knight = get_knight_moves(grid, self.from_pos, self.is_white)
            moves_diagonal.append(moves_knight)
            return flatten(moves_diagonal)
        elif (self.name == "Empress"):
            moves_straight = get_straight_moves(grid, self.from_pos, False, self.is_white)
            moves_knight = get_knight_moves(grid, self.from_pos, self.is_white)
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

# should only change when a move is made
class Board:
    def __init__(self, grid): 
        self.grid = grid

# is dynamic
class State:
    def __init__(self, grid): 
        self.grid = grid
    
    # white tries to maximise this, black tries to minimise
    def get_objective_value_of_state(self):
        white_value = 0
        black_value = 0
        for j in range(COLUMNS):
            for i in range(ROWS):
                if (self.grid[i][j] is not None):
                    piece = self.grid[i][j]
                    if (piece.is_white):
                        white_value += PIECE_VALUES[piece.name]
                    else:
                        black_value += PIECE_VALUES[piece.name]
        return white_value - black_value

def get_next_states(curr_state: State, is_white_turn: bool) -> list[State]:
    result = []
    for j in range(COLUMNS):
        for i in range(ROWS):
            if curr_state.grid[i][j] is not None:
                # only move the piece of the current turn 
                piece = curr_state.grid[i][j]
                if (piece.is_white == is_white_turn):
                    moves = piece.get_valid_moves()
                    for move in moves:
                        new_grid = copy.deepcopy(curr_state.grid)
                        # move the piece from its curr pos
                        new_grid[i][j] = None
                        # put the pieace in new move
                        new_grid[move[0]][move[1]] = piece
                        new_state = State(new_grid)
                        result.append(new_state)
    return result
#Implement your minimax with alpha-beta pruning algorithm here.
def ab(board):
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
    return rows, cols, gameboard

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
    grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
    for pos, piece in gameboard.items():
        piece_obj = Piece(piece[0], pos, piece[1] == WHITE)
        grid[pos[0]][pos[1]] = piece_obj
    
    board = Board(grid)
    move = ab(gameboard)
    return move #Format to be returned (('a', 0), ('b', 3))

def main():
    board = setUpBoard()[2]
    print(studentAgent(board))


if __name__ == "__main__":
    main()