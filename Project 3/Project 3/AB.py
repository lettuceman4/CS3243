import copy
from mimetypes import init
import sys
from typing import Dict, Set, Tuple

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.
WHITE = "White"
BLACK = "Black"
ROWS = 7
COLUMNS = 7
DEPTH = 4

# encourages pawn to advance, discourage the engine from leaving central pawns unmoved https://www.chessprogramming.org/Simplified_Evaluation_Function#Piece-Square_Tables
PAWN_SQUARE_TABLE = {
    (0, 0): 0,
    (0, 1): 0,
    (0, 2): 0,
    (0, 3): 0,
    (0, 4): 0,
    (0, 5): 0,
    (0, 6): 0,
    (1, 0): 5,
    (1, 1): 10,
    (1, 2): -10,
    (1, 3): -20,
    (1, 4): -10,
    (1, 5): 10,
    (1, 6): 5,
    (2, 0): 5,
    (2, 1): -5,
    (2, 2): -10,
    (2, 3): 0,
    (2, 4): -10,
    (2, 5): -5,
    (2, 6): 5,
    (3, 0): 5,
    (3, 1): 5,
    (3, 2): 10,
    (3, 3): 25,
    (3, 4): 10,
    (3, 5): 5,
    (3, 6): 5,
    (4, 0): 10,
    (4, 1): 10,
    (4, 2): 20,
    (4, 3): 30,
    (4, 4): 20,
    (4, 5): 10,
    (4, 6): 10,
    (5, 0): 50,
    (5, 1): 50,
    (5, 2): 50,
    (5, 3): 50,
    (5, 4): 50,
    (5, 5): 50,
    (5, 6): 50,
    (6, 0): 0,
    (6, 1): 0,
    (6, 2): 0,
    (6, 3): 0,
    (6, 4): 0,
    (6, 5): 0,
    (6, 6): 0
}

KNIGHT_SQUARE_TABLE = {
    (0, 0): -50,
    (0, 1): -40,
    (0, 2): -30,
    (0, 3): -30,
    (0, 4): -30,
    (0, 5): -40,
    (0, 6): -50,
    (1, 0): -40,
    (1, 1): -20,
    (1, 2): 0,
    (1, 3): 5,
    (1, 4): 0,
    (1, 5): -20,
    (1, 6): -40,
    (2, 0): -30,
    (2, 1): 5,
    (2, 2): 10,
    (2, 3): 15,
    (2, 4): 10,
    (2, 5): 5,
    (2, 6): -30,
    (3, 0): -30,
    (3, 1): 0,
    (3, 2): 15,
    (3, 3): 20,
    (3, 4): 15,
    (3, 5): 0,
    (3, 6): -30,
    (4, 0): -30,
    (4, 1): 5,
    (4, 2): 10,
    (4, 3): 15,
    (4, 4): 10,
    (4, 5): 5,
    (4, 6): -30,
    (5, 0): -40,
    (5, 1): -20,
    (5, 2): 0,
    (5, 3): 5,
    (5, 4): 0,
    (5, 5): -20,
    (5, 6): -40,
    (6, 0): -50,
    (6, 1): -40,
    (6, 2): -30,
    (6, 3): -30,
    (6, 4): -30,
    (6, 5): -40,
    (6, 6): -50
}

# avoid edges and corners
BISHOP_SQUARE_TABLE = {
    (0, 0): -20,
    (0, 1): -20,
    (0, 2): -20,
    (0, 3): -20,
    (0, 4): -20,
    (0, 5): -20,
    (0, 6): -20,
    (1, 0): -10,
    (1, 1): 0,
    (1, 2): 0,
    (1, 3): 0,
    (1, 4): 0,
    (1, 5): 0,
    (1, 6): -10,
    (2, 0): -10,
    (2, 1): 0,
    (2, 2): 10,
    (2, 3): 15,
    (2, 4): 10,
    (2, 5): 0,
    (2, 6): -10,
    (3, 0): -10,
    (3, 1): 10,
    (3, 2): 10,
    (3, 3): 20,
    (3, 4): 10,
    (3, 5): 10,
    (3, 6): -10,
    (4, 0): -10,
    (4, 1): 5,
    (4, 2): 10,
    (4, 3): 15,
    (4, 4): 10,
    (4, 5): 5,
    (4, 6): -10,
    (5, 0): -10,
    (5, 1): 0,
    (5, 2): 0,
    (5, 3): 0,
    (5, 4): 0,
    (5, 5): 0,
    (5, 6): -10,
    (6, 0): -20,
    (6, 1): -20,
    (6, 2): -20,
    (6, 3): -20,
    (6, 4): -20,
    (6, 5): -20,
    (6, 6): -20
}

#centralise
ROOK_SQUARE_TABLE = {
    (0, 0): 0,
    (0, 1): 0,
    (0, 2): 5,
    (0, 3): 5,
    (0, 4): 5,
    (0, 5): 0,
    (0, 6): 0,
    (1, 0): -5,
    (1, 1): 0,
    (1, 2): 0,
    (1, 3): 0,
    (1, 4): 0,
    (1, 5): 0,
    (1, 6): -5,
    (2, 0): -5,
    (2, 1): 0,
    (2, 2): 0,
    (2, 3): 0,
    (2, 4): 0,
    (2, 5): 0,
    (2, 6): -5,
    (3, 0): -5,
    (3, 1): 0,
    (3, 2): 0,
    (3, 3): 0,
    (3, 4): 0,
    (3, 5): 0,
    (3, 6): -5,
    (4, 0): -5,
    (4, 1): 0,
    (4, 2): 0,
    (4, 3): 0,
    (4, 4): 0,
    (4, 5): 0,
    (4, 6): -5,
    (5, 0): 5,
    (5, 1): 10,
    (5, 2): 10,
    (5, 3): 10,
    (5, 4): 10,
    (5, 5): 10,
    (5, 6): 5,
    (6, 0): 0,
    (6, 1): 0,
    (6, 2): 0,
    (6, 3): 0,
    (6, 4): 0,
    (6, 5): 0,
    (6, 6): 0
}

QUEEN_SQUARE_TABLE = {
    (0, 0): -20,
    (0, 1): -10,
    (0, 2): -10,
    (0, 3): -5,
    (0, 4): -10,
    (0, 5): -10,
    (0, 6): -20,
    (1, 0): -10,
    (1, 1): 0,
    (1, 2): 5,
    (1, 3): 0,
    (1, 4): 0,
    (1, 5): 0,
    (1, 6): -10,
    (2, 0): -10,
    (2, 1): 5,
    (2, 2): 5,
    (2, 3): 5,
    (2, 4): 5,
    (2, 5): 5,
    (2, 6): -10,
    (3, 0): 0,
    (3, 1): 5,
    (3, 2): 5,
    (3, 3): 5,
    (3, 4): 5,
    (3, 5): 5,
    (3, 6): 0,
    (4, 0): -10,
    (4, 1): 0,
    (4, 2): 0,
    (4, 3): 5,
    (4, 4): 0,
    (4, 5): 0,
    (4, 6): -10,
    (5, 0): -10,
    (5, 1): 0,
    (5, 2): 0,
    (5, 3): 0,
    (5, 4): 0,
    (5, 5): 0,
    (5, 6): -10,
    (6, 0): -20,
    (6, 1): -10,
    (6, 2): -10,
    (6, 3): -5,
    (6, 4): -10,
    (6, 5): -10,
    (6, 6): -20
}

KING_SQUARE_TABLE = {
    (0, 0): 20,
    (0, 1): 30,
    (0, 2): 10,
    (0, 3): 0,
    (0, 4): 10,
    (0, 5): 30,
    (0, 6): 20,
    (1, 0): 20,
    (1, 1): 20,
    (1, 2): 0,
    (1, 3): 0,
    (1, 4): 0,
    (1, 5): 20,
    (1, 6): 20,
    (2, 0): -10,
    (2, 1): -20,
    (2, 2): -20,
    (2, 3): -20,
    (2, 4): -20,
    (2, 5): -20,
    (2, 6): -10,
    (3, 0): -20,
    (3, 1): -30,
    (3, 2): -30,
    (3, 3): -40,
    (3, 4): -30,
    (3, 5): -30,
    (3, 6): -20,
    (4, 0): -30,
    (4, 1): -40,
    (4, 2): -40,
    (4, 3): -50,
    (4, 4): -40,
    (4, 5): -40,
    (4, 6): -30,
    (5, 0): -30,
    (5, 1): -40,
    (5, 2): -40,
    (5, 3): -50,
    (5, 4): -40,
    (5, 5): -40,
    (5, 6): -30,
    (6, 0): -30,
    (6, 1): -40,
    (6, 2): -40,
    (6, 3): -50,
    (6, 4): -40,
    (6, 5): -40,
    (6, 6): -30
}

# https://www.chessprogramming.org/Point_Value#Basic_values
PIECE_MATERIALS = {
    "Pawn": 100,
    "Ferz": 150,
    "Knight": 350,
    "Bishop": 350,
    "Rook": 525,
    "Princess": 650,
    "Empress": 750,
    "Queen": 1000,
    "King": 1000000,
}

# multiply w the material
MOVE_UTILITY_COEFF = {
    "Checkmate": 1000,
    "Check": 80,
}
move_count = 0

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
def is_still_in_board(grid, grid_pos):
    return grid_pos[0] < len(grid) and grid_pos[1] < len(grid[0]) and grid_pos[0] >= 0 and grid_pos[1] >= 0 

def get_moves(grid, step_x, step_y, curr_pos, is_limited_range, is_white) -> set():
    moves = set()
    # need to check if its out of the board
    while(is_still_in_board(grid, curr_pos)):
        next_pos = (curr_pos[0] + step_x, curr_pos[1] + step_y)
        if (not is_still_in_board(grid, next_pos)):
            break

        # only blocked by own piece, 
        # and break right after taking another piece
        if (is_capturing_next_pos(next_pos, grid, is_white)):
            moves.add(next_pos)
            break
        # not capturing and still in board
        else:
            if (grid[next_pos[0]][next_pos[1]] is None):
                moves.add(next_pos)
                curr_pos = next_pos
                if (is_limited_range):            
                    break
            else:
                break
    return moves 

def get_knight_moves(grid, from_pos, is_white):
    possible_moves = set()
    # curr_pos_chess_coord = to_chess_coord(from_pos)
    moves1 = get_moves(grid, -2, 1, from_pos, True, is_white)
    moves2 = get_moves(grid, -2, -1, from_pos, True, is_white)
    moves3 = get_moves(grid, 2, -1, from_pos, True, is_white)
    moves4 = get_moves(grid, 2, 1, from_pos, True, is_white)
    moves5 = get_moves(grid, 1, 2, from_pos, True, is_white)
    moves6 = get_moves(grid, 1, -2, from_pos, True, is_white)
    moves7 = get_moves(grid, -1, 2, from_pos, True, is_white)
    moves8 = get_moves(grid, -1, -2, from_pos, True, is_white)
    possible_moves.update(moves1)
    possible_moves.update(moves2)
    possible_moves.update(moves3)
    possible_moves.update(moves4)
    possible_moves.update(moves5)
    possible_moves.update(moves6)
    possible_moves.update(moves7)
    possible_moves.update(moves8)
    return possible_moves

def is_capturing_next_pos(next_pos, grid, is_white):
    if (is_still_in_board(grid, next_pos)):
        if (grid[next_pos[0]][next_pos[1]] is not None):
            piece = grid[next_pos[0]][next_pos[1]]
            return piece.is_white != is_white
    return False

def get_pawn_moves(grid, curr_pos, is_white):
    moves = set()
    dir = 1 if is_white else -1
    next_pos_straight = (curr_pos[0] + dir, curr_pos[1])
    next_pos_diagonal_right = (curr_pos[0] + dir, curr_pos[1] + dir)
    next_pos_diagonal_left = (curr_pos[0] + dir, curr_pos[1] - dir)
    
    # straight move only execute if no piece in front
    if (is_still_in_board(grid, next_pos_straight) 
    and grid[next_pos_straight[0]][next_pos_straight[1]] is None):
        moves.add(next_pos_straight)

    if (is_capturing_next_pos(next_pos_diagonal_right, grid, is_white)):
        moves.add(next_pos_diagonal_right)
    
    if (is_capturing_next_pos(next_pos_diagonal_left, grid, is_white)):
        moves.add(next_pos_diagonal_left)
    for move in moves:
        from_pos = to_chess_coord(curr_pos)
        to_pos = to_chess_coord(move)
        # print(from_pos, to_pos)
    return moves

def get_straight_moves(grid, curr_pos, is_limited_range, is_white):
    possible_moves = set()
    # curr_pos_chess_coord = to_chess_coord(curr_pos)
    moves_left = get_moves(grid, -1, 0, curr_pos, is_limited_range, is_white)
    moves_right = get_moves(grid, 1, 0, curr_pos, is_limited_range, is_white)
    moves_up = get_moves(grid, 0, -1, curr_pos, is_limited_range, is_white)
    moves_down = get_moves(grid, 0, 1, curr_pos, is_limited_range, is_white)
    possible_moves.update(moves_left)
    possible_moves.update(moves_right)
    possible_moves.update(moves_up)
    possible_moves.update(moves_down)
    return possible_moves

def get_diagonal_moves(grid, from_pos, is_limited_range, is_white):
    possible_moves = set()
    # curr_pos_chess_coord = to_chess_coord(from_pos)
    moves1 = get_moves(grid, 1, 1, from_pos, is_limited_range, is_white)
    moves2 = get_moves(grid, 1, -1, from_pos, is_limited_range, is_white)
    moves3 = get_moves(grid, -1, -1, from_pos, is_limited_range, is_white)
    moves4 = get_moves(grid, -1, 1, from_pos, is_limited_range, is_white)
    
    possible_moves.update(moves1)
    possible_moves.update(moves2)
    possible_moves.update(moves3)
    possible_moves.update(moves4)
    
    return possible_moves

class Piece:
    def __init__(self, name, is_white):
        # standard initialisation of piece
        self.name = name
        self.is_white = is_white

    def get_valid_moves(self, grid, from_pos):
        if (self.name == "Rook"):
            return get_straight_moves(grid, from_pos, False, self.is_white)
        elif (self.name == "Pawn"):
            return get_pawn_moves(grid, from_pos, self.is_white)
        elif (self.name == "Knight"):
            return get_knight_moves(grid, from_pos, self.is_white)
        elif (self.name == "Bishop"):
            return get_diagonal_moves(grid, from_pos, False, self.is_white)
        elif (self.name == "Queen"):
            moves_straight = get_straight_moves(grid, from_pos, False, self.is_white)
            moves_diagonal = get_diagonal_moves(grid, from_pos, False, self.is_white)
            moves_straight.update(moves_diagonal)
            return moves_straight
        elif (self.name == "King"):
            moves_straight = get_straight_moves(grid, from_pos, True, self.is_white)
            moves_diagonal = get_diagonal_moves(grid, from_pos, True, self.is_white)
            moves_straight.update(moves_diagonal)
            return moves_straight
        elif (self.name == "Ferz"):
            return get_diagonal_moves(grid, from_pos, True, self.is_white)
        elif (self.name == "Princess"):
            moves_diagonal = get_diagonal_moves(grid, from_pos, False, self.is_white)
            moves_knight = get_knight_moves(grid, from_pos, self.is_white)
            moves_diagonal.update(moves_knight)
            return moves_diagonal
        elif (self.name == "Empress"):
            moves_straight = get_straight_moves(grid, from_pos, False, self.is_white)
            moves_knight = get_knight_moves(grid, from_pos, self.is_white)
            moves_straight.update(moves_knight)
            return moves_straight

#############################################################################
######## Board
#############################################################################
def to_chess_coord(grid_pos):
    return (chr(grid_pos[1] + 97), grid_pos[0])

def to_grid_coord(chess_pos):
    return (chess_pos[1], ord(chess_pos[0]) - 97)

def has_king(pieces) -> bool:
    for piece in set(pieces.values()):
        if piece.name == "King": 
            return True
    return False

# should only change when a move is made
class Board:
    def __init__(self, grid): 
        self.grid = grid

# is dynamic
class State:
    #state is in form of dict<pos: piece>
    def __init__(self, white_pieces, black_pieces, is_white_turn):  
        
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.is_white_turn = is_white_turn
        self.grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        for pos, piece in black_pieces.items():
            (i, j) = pos
            self.grid[i][j] = piece
        for pos, piece in white_pieces.items():
            (i, j) = pos
            self.grid[i][j] = piece
    
    @staticmethod
    def get_state_from_gameboard(gameboard, is_white_turn):
        white_pieces = {}
        black_pieces = {}
        for pos, piece in gameboard.items():
            pos = to_grid_coord(pos)
            piece_obj = Piece(piece[0], piece[1] == WHITE)
            if (piece[1] == WHITE):
                white_pieces[pos] = piece_obj
            else:
                black_pieces[pos] = piece_obj
        return State(white_pieces, black_pieces, is_white_turn)
    
    def get_piece_square_score_helper(self, is_white: bool) -> int:
        total_score = 0
        dict_to_get = self.white_pieces if is_white else self.black_pieces        
        for pos, piece in dict_to_get.items():
            if (piece.name == "Pawn"):
                total_score += PAWN_SQUARE_TABLE[pos]
            if (piece.name == "Bishop"):
                total_score += BISHOP_SQUARE_TABLE[pos]
            if (piece.name == "Knight"):
                total_score += KNIGHT_SQUARE_TABLE[pos]
            if (piece.name == "Queen"):
                total_score += QUEEN_SQUARE_TABLE[pos]
            if (piece.name == "King"):
                total_score += KING_SQUARE_TABLE[pos]
            if (piece.name == "Empress"):
                total_score += QUEEN_SQUARE_TABLE[pos]
            if (piece.name == "Princess"):
                total_score += QUEEN_SQUARE_TABLE[pos]
            if (piece.name == "Rook"):
                total_score += ROOK_SQUARE_TABLE[pos]
            if (piece.name == "Ferz"):
                total_score += PAWN_SQUARE_TABLE[pos]
        return total_score
    
    def get_piece_square_score(self) -> int:
        return self.get_piece_square_score_helper(True) - self.get_piece_square_score_helper(False) 

    def get_material_score(self):
        white_value = 0
        black_value = 0
        for white_piece in self.white_pieces.values():
            white_value += PIECE_MATERIALS[white_piece.name]
        for black_piece in self.black_pieces.values():
            black_value += PIECE_MATERIALS[black_piece.name]    
        return white_value - black_value

    def get_playing_turn_king_pos(self, is_white_turn):
        if (is_white_turn):
            for pos, piece in self.white_pieces.items():
                if (piece.name == "King"):
                    return pos
        else:
            for pos, piece in self.black_pieces.items():
                if (piece.name == "King"):
                    return pos
        return None

class Game:
    # This occurs when the opponent???s King is in check, and there is no legal way to get it out of check. Since it is illegal for a player to make a move that puts or leaves its own King in check, if it is not possible to get its King out of check, then the player cannot make any other moves and the King is considered checkmated (and the game is over).
    @staticmethod
    def is_standard_checkmate(curr_state: State, is_white_turn: bool) -> bool:
        if (is_white_turn):
            playing_pieces = curr_state.white_pieces
        else:
            playing_pieces = curr_state.black_pieces
        
        return not has_king(playing_pieces)

    @staticmethod
    def evaluate(curr_state: State) -> int:
        return curr_state.get_material_score() + curr_state.get_piece_square_score()
    
    @staticmethod
    def is_draw(curr_state: State) -> bool:
        black_count = len(curr_state.black_pieces)
        white_count = len(curr_state.white_pieces)
        is_black_king_alive = has_king(curr_state.black_pieces)
        is_white_king_alive = has_king(curr_state.white_pieces)
        return black_count == white_count and is_black_king_alive and is_white_king_alive
    
    @staticmethod
    # check if the current turn is checked by opponent   
    def is_checked_by_opponent(curr_state: State, is_white_turn) -> bool:
        if (is_white_turn):
            enemy_team_pieces = curr_state.black_pieces
        else:
            enemy_team_pieces = curr_state.white_pieces
        # any pieces in the current team is threatening the opponent king
        playing_king_pos = curr_state.get_playing_turn_king_pos(is_white_turn)
        
        assert playing_king_pos is not None

        # get all the enemy possible moves, if they contains king position -> checked
        enemy_possible_moves = set()
        for pos, piece in enemy_team_pieces.items():
            possible_moves = piece.get_valid_moves(curr_state.grid, pos)
            enemy_possible_moves.add((pos))
            for move in possible_moves:
                enemy_possible_moves.add((move))

        if (playing_king_pos in enemy_possible_moves):
            return True
        
        return False

    @staticmethod
    def is_endgame(curr_state: State, is_white_turn: bool) -> bool:
        return Game.is_standard_checkmate(curr_state, is_white_turn)

# get the all the moves that generate the next state, along with the next state
def get_next_states(curr_state: State, is_white_turn: bool):
    if (is_white_turn):
        curr_team_dict = curr_state.white_pieces
        enemy_team_dict = curr_state.black_pieces
    else:
        curr_team_dict = curr_state.black_pieces
        enemy_team_dict = curr_state.white_pieces
    result = {}
    for old_pos, piece in curr_team_dict.items():
        moves = piece.get_valid_moves(curr_state.grid, old_pos)
        for new_pos in moves:
            new_team_dict = copy.copy(curr_team_dict)
            new_team_dict.pop(old_pos)
            new_team_dict[new_pos] = piece

            # if moving turn is capturing enemy team
            new_enemy_team_dict = copy.copy(enemy_team_dict)
            if (new_pos in set(enemy_team_dict.keys())):
                new_enemy_team_dict.pop(new_pos)

            if (is_white_turn):
                new_state = State(new_team_dict, new_enemy_team_dict, False)
            else:
                new_state = State(new_enemy_team_dict, new_team_dict, True)

            # only allows move that is not checked
            # print(Game.evaluate(new_state))
            # if (not Game.is_checked_by_opponent(new_state, is_white_turn)):
            result[(old_pos, new_pos)] = new_state
            
            # allows 1 move that allows check if result is empty
            # if len(result) == 0:
            #     result[(old_pos, new_pos)] = new_state
    return result

#Implement your minimax with alpha-beta pruning algorithm here. Returns a state that maximise for white player and minimise for black player
def ab(curr_state: State, alpha: int, beta: int, depth: int, is_white_turn: bool):
    # print("ab")
    if (depth == 0 or Game.is_endgame(curr_state, is_white_turn)):
        return None, Game.evaluate(curr_state)
    if (is_white_turn):
        max_eval = float("-infinity")
        next_states = get_next_states(curr_state, True)
        # for state in next_states.values():
        #     print(Game.evaluate(state))
        best_move = None
        for move, state in next_states.items():
            eval = ab(state, alpha, beta, depth - 1, False)[1]
            # if (not has_king(state.black_pieces)):
            #     best_move = move
            #     break
            # if (move[1] == (2, 3)):
            #     print(to_chess_coord(move[0]), to_chess_coord(move[1]), eval)
            if (eval >= max_eval):
                best_move = move
            max_eval = get_max(eval, max_eval)
            alpha = get_max(alpha, max_eval)
            if (alpha >= beta):
                break
        return best_move, max_eval
    else:
        min_eval = float("infinity")
        next_states = get_next_states(curr_state, False)
        best_move = None
        
        # for state in next_states.values():
        #     print(Game.evaluate(state))
        for move, state in next_states.items():
            # if (not has_king(state.white_pieces)):
            #     best_move = move
            #     break
            eval = ab(state, alpha, beta, depth - 1, True)[1]
            if (eval <= min_eval):
                best_move = move
            min_eval = get_min(eval, min_eval)
            beta = get_min(beta, min_eval)
            if (beta <= alpha):
                best_move = move
                break
        return best_move, min_eval

def get_max(n1: int, n2: int) -> int:
    if (n1 >= n2):
        return n1
    else:
        return n2

def get_min(n1: int, n2: int) -> int:
    if (n1 >= n2):
        return n2
    else:
        return n1

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
    
    initial_state = State.get_state_from_gameboard(gameboard, True)
    move = ab(initial_state, float("-infinity"), float("infinity"), 2, True)[0]
    if (move is not None):
        pos1 = to_chess_coord(move[0])
        pos2 = to_chess_coord(move[1])
        return pos1, pos2 #Format to be returned (('a', 0), ('b', 3)
    return None

def main():
    startBoard = {
        ('d', 2): ('King', 'Black'),
        ('c', 6): ('Queen', 'Black'),
        ('b', 6): ('Bishop', 'Black'),
        ('a', 6): ('Knight', 'Black'),
        ('g', 6): ('Rook', 'Black'),
        ('e', 6): ('Princess', 'Black'),
        ('f', 6): ('Empress', 'Black'),
        ('b', 5): ('Pawn', 'Black'),
        ('c', 5): ('Pawn', 'Black'),
        ('d', 5): ('Pawn', 'Black'),
        ('e', 5): ('Pawn', 'Black'),
        ('f', 5): ('Pawn', 'Black'),
        ('a', 5): ('Ferz', 'Black'),
        ('g', 5): ('Ferz', 'Black'),        
        
        ('d', 0): ('King', 'White'),
        ('c', 0): ('Queen', 'White'),
        ('b', 0): ('Bishop', 'White'),
        ('a', 0): ('Knight', 'White'),
        ('g', 0): ('Rook', 'White'),
        ('e', 0): ('Princess', 'White'),
        ('f', 0): ('Empress', 'White'),
        ('b', 1): ('Pawn', 'White'),
        ('c', 1): ('Pawn', 'White'),
        ('d', 1): ('Pawn', 'White'),
        ('e', 1): ('Pawn', 'White'),
        ('f', 1): ('Pawn', 'White'),
        ('a', 1): ('Ferz', 'White'),
        ('f', 2): ('Ferz', 'White')}
    # print(studentAgent(startBoard))


if __name__ == "__main__":
    main()