import math
from random import random
import numpy as np
import chess

# your_heuristic function should return a heuristic value based on the
# board state. the value should be the higher the more likely white
# is to win the game.

# hint: the below example assigns value +1 to each white piece on the
# board irrespective of where on the board and what piece it is, and
# likewise, value -1 to each black piece. it is probably a good idea
# to assign higher values to more important pieces. also, you may want
# to let the score depend on where on the board the pieces are
# located: usually the central squares are considered more important
OUR_COLOR = chess.BLACK
THEIR_COLOR = chess.WHITE

PIECE_VALUES = [None, 1, 3, 3, 5, 9, 10]

RISK_TAKING = 0.9 # how much to consider the loss of piece when attacking a piece that is defended
AGGRESSION = 0.9 # how valuable destroying opponent pieces is
POSITION_FACTOR = 0.5 # how much to consider piece positioning
RANDOMNESS = 0.05 # how much randomness to add

def get_pos(square: chess.Square):
    return (chess.square_file(square),chess.square_rank(square))

def position_value(square: chess.Square):
    (x, y) = get_pos(square)
    x_score = 0.5 - math.fabs(x / 7 - 0.5) # 0.5 at center, 0 at edges
    y_score = 0.5 - math.fabs(y / 7 - 0.5) # 0.5 at center, 0 at edges
    return POSITION_FACTOR * (x_score + y_score) + 1

def color_val(piece):
    return 1 if piece.color == chess.WHITE else -1
    
def pawn_value(piece, square):
    return color_val(piece) * position_value(square) * PIECE_VALUES[1]

def knight_value(piece, square):
    return color_val(piece) * position_value(square) * PIECE_VALUES[2]

def bishop_value(piece, square):
    return color_val(piece) * position_value(square) * PIECE_VALUES[3]

def rook_value(piece, square):
    return color_val(piece) * position_value(square) * PIECE_VALUES[4]

def queen_value(piece, square):
    return color_val(piece) * position_value(square) * PIECE_VALUES[5]

def king_value(piece, square):
    return color_val(piece) * PIECE_VALUES[6]

piece_values = [None, pawn_value, knight_value, bishop_value, rook_value, queen_value, king_value]

def piece_value(piece, square):
    return piece_values[piece.piece_type](piece, square)

def attacks_value(attacks: chess.SquareSet, board: chess.Board, piece, opponent_color):
    value = 0
    for square in attacks:
        attacked_piece = board.piece_at(square)
        if attacked_piece is None or attacked_piece.color == piece.color:
            continue
        # we can eat them, but is someone defending?
        defending_factor = 1 if len(board.attackers(opponent_color, square)) > 0 else 0
        risk_value = PIECE_VALUES[piece.piece_type] * defending_factor * RISK_TAKING
        total_attack_value = piece_value(attacked_piece, square) - risk_value

        value = max(value, total_attack_value)

    return value * 0.3

def your_heuristic(board: chess.Board, verbose=False):

    score = 0
    pmap = board.piece_map() # a dictionary with all the pieces of the board
    for square, piece in pmap.items():
        opponent_color = chess.WHITE if piece.color == chess.BLACK else chess.BLACK

        attacks = board.attacks(square)

        av = attacks_value(attacks, board, piece, opponent_color)

        rand = RANDOMNESS * (random() * 2 - 1)

        piece_score = piece_value(piece, square) + av + rand

        # you can use this for debugging
        if verbose:
            print((square, chess.square_rank(square), piece, piece_score))

        score += piece_score
    return score

