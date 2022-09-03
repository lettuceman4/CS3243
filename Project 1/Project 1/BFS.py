import sys

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
def get_manhattan_dist(from_pos, to_pos):
    x = ord(to_pos[0] - from_pos[0])
    y = to_pos[1] - from_pos[1]
    return (x, y)

def get_knight_moves(board, from_pos):
    possible_moves = []
    moves1 = get_moves(board, -2, 1, from_pos, True)
    moves2 = get_moves(board, -2, -1, from_pos, True)
    moves3 = get_moves(board, 2, -1, from_pos, True)
    moves4 = get_moves(board, 2, 1, from_pos, True)
    moves5 = get_moves(board, 1, 2, from_pos, True)
    moves6 = get_moves(board, 1, -2, from_pos, True)
    moves7 = get_moves(board, -1, 2, from_pos, True)
    moves8 = get_moves(board, -1, -2, from_pos, True)
    possible_moves.append(moves1)
    possible_moves.append(moves2)
    possible_moves.append(moves3)
    possible_moves.append(moves4)
    possible_moves.append(moves5)
    possible_moves.append(moves6)
    possible_moves.append(moves7)
    possible_moves.append(moves8)
    return possible_moves

def get_straight_moves(board, curr_pos, is_limited_range):
    possible_moves = []
    moves_left = get_moves(board, -1, 0, curr_pos, is_limited_range)
    moves_right = get_moves(board, 1, 0, curr_pos, is_limited_range)
    moves_up = get_moves(board, 0, -1, curr_pos, is_limited_range)
    moves_down = get_moves(board, 0, 1, curr_pos, is_limited_range)
    possible_moves.append(moves_left)
    possible_moves.append(moves_right)
    possible_moves.append(moves_up)
    possible_moves.append(moves_down)
    return possible_moves

def get_diagonal_moves(board, from_pos, is_limited_range):
    possible_moves = []
    moves1 = get_moves(board, 1, 1, from_pos, is_limited_range)
    moves2 = get_moves(board, 1, -1, from_pos, is_limited_range)
    moves3 = get_moves(board, -1, -1, from_pos, is_limited_range)
    moves4 = get_moves(board, -1, 1, from_pos, is_limited_range)
    possible_moves.append(moves1)
    possible_moves.append(moves2)
    possible_moves.append(moves3)
    possible_moves.append(moves4)
    return possible_moves

def get_moves(board, step_x, step_y, curr_pos, is_limited_range):
    moves = []
    #need to check for threatened position
    while(curr_pos[0] <= board.columns_no & curr_pos[1] <= board.rows_no):
        next_pos = (curr_pos[0] + step_x, curr_pos[1] + step_y)
        if board.grid[next_pos[0]][next_pos[1]] == -1:
            break
        else:
            move_pair = [curr_pos]
            move_pair.append(next_pos)
            moves.append(move_pair)
            curr_pos = next_pos
            if (is_limited_range):
                break
    return moves 

    
class Piece:
    def __init__(self, name, from_pos):
        # standard initialisation of piece
        self.name = name
        self.from_pos = from_pos

    def get_valid_moves(self, board):
        if (self.name == "Rook"):
            return get_straight_moves(board, self.from_pos, False)
        elif (self.name == "Knight"):
            return get_knight_moves(board, self.from_pos)
        elif (self.name == "Bishop"):
            return get_diagonal_moves(board, self.from_pos, False)
        elif (self.name == "Queen"):
            moves_straight = get_straight_moves(board, self.from_pos, False)
            moves_diagonal = get_diagonal_moves(board, self.from_pos, False)
            return moves_straight.append(moves_diagonal)
        elif (self.name == "King"):
            moves_straight = get_straight_moves(board, self.from_pos, True)
            moves_diagonal = get_diagonal_moves(board, self.from_pos, True)
            return moves_straight.append(moves_diagonal)
        elif (self.name == "Ferz"):
            return get_diagonal_moves(board, self.from_pos, True)
        elif (self.name == "Princess"):
            moves_diagonal = get_diagonal_moves(board, self.from_pos, False)
            moves_knight = get_knight_moves(board, self.from_pos)
            return moves_diagonal.append(moves_knight)
        elif (self.name == "Empress"):
            moves_straight = get_straight_moves(board, self.from_pos, False)
            moves_knight = get_knight_moves(board, self.from_pos)
            return moves_straight.append(moves_knight)

#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self, rows_no, columns_no, grid, enemy_pieces, own_pieces, goals, blocked_grid):
        self.board = [] * rows_no
        for i in range(columns_no):
            self.board.append([None] * columns_no)
        
        self.enemy_pieces = enemy_pieces
        self.grid = grid
        self.own_pieces = own_pieces
        self.goal = goals                    
        
        for c in range(columns_no):
            for r in range(rows_no):
                if (grid[r][c] == -1):
                    blocked_grid[r][c] == -1
        
        # add enemies possible move
        enemy_list = []
        for i in range(len(enemy_pieces)):
            enemy_list.append(Piece(enemy_pieces[i][0], enemy_pieces[i][1]))

        blocked_squares = []
        for i in range(len(enemy_list)):
            blocked_squares.append(enemy_list[i].get_valid_moves(self.board))
        
        for s in blocked_squares:
            (r, c) = s[0]
            blocked_grid[r][c] = -1
        
#############################################################################
######## State
#############################################################################
class State:
    def __init__(self):
        # replace `pass` with the desired attributes and add any
        # additional parameters to the function
        pass

    def move(self):
        pass

#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    board = Board(rows_no=rows, columns_no=cols)
    board.print_board()


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
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

#############################################################################
######## Main function to be called
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# To return: List of moves
# Return Format Example: [[('a', 0), ('a', 1)], [('a', 1), ('c', 3)], [('c', 3), ('d', 5)]]
def run_BFS():    
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    moves = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves

def main():
    run_BFS()
if __name__ == "__main__":
    main()