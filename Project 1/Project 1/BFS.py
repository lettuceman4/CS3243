from queue import Queue
import sys

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
def get_manhattan_dist(from_pos, to_pos):
    x = ord(to_pos[0] - from_pos[0])
    y = to_pos[1] - from_pos[1]
    return (x, y)

def get_knight_moves(grid, from_pos):
    possible_moves = []
    curr_pos_chess_coord = to_chess_coord(from_pos)
    possible_moves.append(curr_pos_chess_coord)
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
    curr_pos_chess_coord = to_chess_coord(curr_pos)
    possible_moves.append(curr_pos_chess_coord)
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
    curr_pos_chess_coord = to_chess_coord(from_pos)
    possible_moves.append(curr_pos_chess_coord)
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
            next_pos_chess_coord = to_chess_coord(next_pos)
            moves.append(next_pos_chess_coord)
            curr_pos = next_pos
            if (is_limited_range):            
                break
    # print ("step: ({}, {}): {}".format(step_x, step_y, moves))
    return moves 

    
class Piece:
    def __init__(self, name, from_pos):
        # standard initialisation of piece
        self.name = name
        self.from_pos = from_pos

    def get_valid_moves(self, grid):
        if (self.name == "Rook"):
            return get_straight_moves(grid, self.from_pos, False)
        elif (self.name == "Knight"):
            return get_knight_moves(grid, self.from_pos)
        elif (self.name == "Bishop"):
            return get_diagonal_moves(grid, self.from_pos, False)
        elif (self.name == "Queen"):
            moves_straight = get_straight_moves(grid, self.from_pos, False)
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, False)
            moves_straight.append(moves_diagonal)
            return moves_straight
        elif (self.name == "King"):
            moves_straight = get_straight_moves(grid, self.from_pos, True)
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, True)
            moves_straight.append(moves_diagonal)
            return moves_straight
        elif (self.name == "Ferz"):
            return get_diagonal_moves(grid, self.from_pos, True)
        elif (self.name == "Princess"):
            moves_diagonal = get_diagonal_moves(grid, self.from_pos, False)
            moves_knight = get_knight_moves(grid, self.from_pos)
            moves_diagonal.append(moves_knight)
            return moves_diagonal
        elif (self.name == "Empress"):
            moves_straight = get_straight_moves(grid, self.from_pos, False)
            moves_knight = get_knight_moves(grid, self.from_pos)
            moves_straight.append(moves_knight)
            return moves_straight

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
    def __init__(self, rows_no, columns_no, grid, enemy_pieces, own_pieces, goals): 
        self.board = [] * rows_no
        for i in range(columns_no):
            self.board.append([None] * columns_no)
        
        self.enemy_pieces = enemy_pieces
        self.grid = grid
        self.own_pieces = own_pieces
        self.goal = goals

        # add enemies possible move
        enemy_list = []
        
        for i in range(len(enemy_pieces)):
            enemy_list.append(Piece(enemy_pieces[i][0], enemy_pieces[i][1]))

        possible_enemy_moves = []
        for i in range(len(enemy_list)):
            new_list = enemy_list[i].get_valid_moves(self.grid)
            possible_enemy_moves.append(new_list)
    
        possible_enemy_moves = flatten(possible_enemy_moves)
        blocked_square = set()
        for i in range (len(possible_enemy_moves)):
            curr_square = possible_enemy_moves[i]
            blocked_square.add(curr_square)
            (r, c) = to_grid_coord(curr_square)
            grid[r][c] = -2

#############################################################################
######## State
#############################################################################
# class State:
#     def __init__(self, board):
#         self.board = board
        
#         # construct search space
        
    
#     def move(self):
#         pass
         

#############################################################################
######## Implement Search Algorithm
#############################################################################
def goal_test(goal_lst, curr_pos):
    for i in range(len(goal_lst)):
        if curr_pos == goal_lst[i]:
            return (True, goal_lst[i])
    return (False, None)

def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    board = Board(rows, cols, grid, enemy_pieces, own_pieces, goals)
    # state = State(board)
    # for each movement of the king, 
    # find possible move, then
    # add them all to the frontier. 
    # pop the stack. 
    # add to path 
    frontier = Queue()
    path = []
    path_found = False
    first_goal_found = None
    parent = dict()
    visited = set()

    # for i in range(len(own_pieces)):
    for i in range(len(own_pieces)):
        piece = Piece(own_pieces[i][0], own_pieces[i][1])
        frontier.put(piece.from_pos)
        parent[piece.from_pos] = None
        while not frontier.empty():
            curr_pos = frontier.get()
            visited.add(curr_pos)

            if goal_test(goals, curr_pos)[0]:
                path_found = True
                first_goal_found = goal_test(goals, curr_pos)[1]
                break

            piece = Piece(own_pieces[i][0], curr_pos)
            possible_moves = piece.get_valid_moves(board.grid)
            possible_moves = flatten(possible_moves)
            possible_moves = list(dict.fromkeys(possible_moves))
            
            # print (possible_moves)
            # add neighbour to frontier
            for j in range(len(possible_moves)):
                neighbour = to_grid_coord(possible_moves[j])
                if (neighbour != curr_pos and neighbour not in visited):
                    visited.add(neighbour)
                    parent[neighbour] = curr_pos
                    frontier.put(neighbour)
    # backtrack
    if path_found:
        # path.append(first_goal_found)
        while parent[first_goal_found] is not None:
            first_goal_found_chess_coord = to_chess_coord(first_goal_found)
            move_pair = [first_goal_found_chess_coord]
            next_step = parent[first_goal_found]
            next_step_chess_coord = to_chess_coord(next_step)
            move_pair.append(next_step_chess_coord)
            move_pair.reverse()
            path.append(move_pair)
            first_goal_found = parent[first_goal_found]
        path.reverse()
    return path
    
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