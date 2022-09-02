import sys

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
def check_if_dest_empty(board, to_pos):
    # can be obstacles or enemy pieces
    # if there is obstacle
    is_obstacle = board.grid[to_pos[0]][to_pos[1]] == -1
    for e in board.enemy_pieces:
        if (e == to_pos):
            return False
    return is_obstacle

def get_pos_diff(from_pos, to_pos):
    x = ord(to_pos[0] - from_pos[0])
    y = to_pos[1] - from_pos[1]
    return (x, y)

def check_knight(board, from_pos, to_pos):
    (x, y) = get_pos_diff(from_pos, to_pos)
    return abs(x * y == 2) & check_if_dest_empty(board, to_pos) 

def check_adj_straight(board, from_pos, to_pos):
    (x, y) = get_pos_diff(from_pos, to_pos)
    return x * y == 0 & (x == 1 | y == 1) & check_if_dest_empty(board, to_pos)

def check_straight(board, from_pos, to_pos):
    is_valid = True
    (x, y) = get_pos_diff(from_pos, to_pos)
    is_vertical = x == 0
    is_horizontal = y == 0 
    n = x - y
    step = n/(abs(n))

    # check for every step of the rook, in both directions
    if (is_vertical):
        for i in range(0, n, step):
            prev_coord = (from_pos[0], from_pos[1] + i)
            next_coord = (from_pos[0], from_pos[1] + i + step)
            if (not check_adj_straight(board, prev_coord, next_coord)):
                return False
    if (is_horizontal):
        for i in range(0, n. step):
            prev_coord = (from_pos[0] + i, from_pos[1])
            next_coord = (from_pos[0] + i + step, from_pos[1])
            if (not check_adj_straight(board, prev_coord, next_coord)):
                return False
    return is_valid

def check_diagonal(board, from_pos, to_pos):
    is_valid = True
    (x, y) = get_pos_diff(from_pos, to_pos)[0]
    n = abs(x)
    step = x/y 

    print("n: " + n)
    print("step: " + step)

    for i in range(0, n, step):
        prev_coord = (from_pos[0] + i, from_pos[1] + i)
        next_coord = (from_pos[0] + i + step, from_pos[1] + i + step)
        if (not check_adj_diagonal(board, prev_coord, next_coord)):
            return False
    return is_valid

def check_adj_diagonal(board, from_pos, to_pos):
    (x, y) = get_pos_diff(from_pos, to_pos)
    return abs(x * y == 1) & check_if_dest_empty(board, to_pos)

def is_straight_line(from_pos, to_pos):
    (x, y) = get_pos_diff(from_pos, to_pos)
    return x == 0 | y == 0

def is_diagonal_line(from_pos, to_pos):
    (x, y) = get_pos_diff(from_pos, to_pos)
    return abs(x) == abs(y)

    
class Piece:
    def __init__(self, is_enemy):
        # standard initialisation of piece
        self.is_enemy = is_enemy

    def is_valid_move(self, board, from_pos, to_pos):
        return False

    def __str__(self):
        return ''

class Rook(Piece):
    def __init__(self, is_enemy):
        super(Rook, self).__init__(is_enemy)

    def is_valid_move(self, board, from_pos, to_pos):
        if (is_straight_line(from_pos, to_pos)):
            return check_straight(board, from_pos, to_pos)
        return False

class Knight(Piece):
    def __init__(self):
        super().__init__()

    def is_valid_move(board, from_pos, to_pos):
        return check_knight(board, from_pos, to_pos)

class Bishop(Piece):
    def __init__(self):
        super().__init__()

    def is_valid_move(self, board, from_pos, to_pos):
        if (is_diagonal_line(from_pos, to_pos)):
            return check_diagonal(board, from_pos, to_pos)
        return False

class Queen(Piece):
    def __init__(self):
        super().__init__()

    def is_valid_move(self, board, from_pos, to_pos):
        if (is_diagonal_line(from_pos, to_pos)):
            return check_diagonal(board, from_pos, to_pos)
        if (is_straight_line(from_pos, to_pos)):
            return check_straight(board, from_pos, to_pos)
        return False

class King(Piece):
    def __init__(self):
        super().__init__()

    def is_valid_move(self, board, from_pos, to_pos):
        return check_adj_diagonal(board, from_pos, to_pos) | check_adj_straight(board, from_pos, to_pos)

#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self, rows_no, columns_no, grid, enemy_pieces, own_pieces, goals):
        self.board = [] * rows_no
        for i in range(columns_no):
            self.board.append([None] * columns_no)
        
        self.enemy_pieces = enemy_pieces
        self.grid = grid
        self.own_pieces = own_pieces
        self.goal = goals

    def print_board(self):
        rows = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        # for i in range(len(rows) - 1):
        #     print(" " + rows[i] + " ", end=" ")
        # print(" " + rows[len(rows) - 1] + "  ")

        # buffer = ""
        # for i in range(41):
        #     buffer += "*"
        # print(buffer)
        # for i in range(len(self.board)):
        #     tmp_str = "|"
        #     for j in self.board[i]:
        #         if j is None or j.name == 'GP':
        #             tmp_str += "   |"
        #         elif len(j.name) == 2:
        #             tmp_str += (" " + str(j) + "|")
        #         else:
        #             tmp_str += (" " + str(j) + " |")
        #     print(tmp_str)
        # buffer = ""
        # for i in range(41):
        #     buffer += "*"
        # print(buffer)
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