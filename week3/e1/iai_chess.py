# play a game of chess
#

# example usage:
# from iai_chess import play_game
# play_game(depth=3) # to run a quick game
# play_game()        # default depth=4, which may take up to 20 minutes
# from our_heuristic import our_heuristic
# play_game(black_heuristic=our_heuristic) # an even game between two good bots
# 
# arguments to play_game:
# board = starting board position given as a chess.Board object
#         default is the usual starting position
# depth = game tree depth to explore, default = 4
# white_heuristic, black_heuristic = heuristic evaluation functions for
#    white and black player. see comments in your_heuristic.py
#    by default, white uses our "secret" evaluation function that you
#    should try to beat with your own your_heuristic function
# graphics: set to True to display svg graphics in a jupyter notebook
#           default = False, which prints ascii board positions


import sys
import numpy as np
from timeit import default_timer as timer
import chess
import chess.svg

version = (sys.version_info.major, sys.version_info.minor)
print(version)

if version == (3,7):
    from __pycache__.our_heuristic37 import our_heuristic
elif version == (3,8):
    from __pycache__.our_heuristic38 import our_heuristic
elif version == (3,9):
    from __pycache__.our_heuristic39 import our_heuristic
elif version == (3,10):
    from __pycache__.our_heuristic310 import our_heuristic
elif version == (3,11):
    from __pycache__.our_heuristic311 import our_heuristic
else:
    sys.exit("sorry. only python versions 3.6-3.11 supported")
    
from your_heuristic import your_heuristic


def max_value(board, alpha, beta, depth, heuristic):

    if board.is_game_over():
        if board.outcome().winner == chess.WHITE:
            return (1e10+depth, None)
        elif board.outcome().winner == chess.BLACK:
            return (-1e10-depth, None)
        else: return (0, None)  # draw

    if depth < 1:
        return (heuristic(board), None)

    v = -np.inf
    best_move = None

    legal_moves = board.legal_moves
    ranked_moves = {}
    for move in legal_moves:
        board.push(move)
        ranked_moves[move] = heuristic(board)
        board.pop()

    for move in sorted(ranked_moves, key=ranked_moves.get, reverse=True):
        board.push(move)
        (child_v, _) =  min_value(board, alpha, beta, depth-1, heuristic)
        board.pop()

        if child_v > v:
            v = child_v
            best_move = move
        alpha = max(alpha, child_v)
        if alpha >= beta: break

    return (v, best_move)

def min_value(board, alpha, beta, depth, heuristic):

    if board.is_game_over():
        if board.outcome().winner == chess.WHITE:
            return (1e10+depth, None)
        elif board.outcome().winner == chess.BLACK:
            return (-1e10-depth, None)
        else:
            return (0.0, None)  # draw

    if depth < 1:
        return (heuristic(board), None)

    v = np.inf
    best_move = None
    
    legal_moves = board.legal_moves
    ranked_moves = {}
    for move in legal_moves:
        board.push(move)
        ranked_moves[move] = heuristic(board)
        board.pop()

    for move in sorted(ranked_moves, key=ranked_moves.get, reverse=False):
        board.push(move)
        (child_v, _) =  max_value(board, alpha, beta, depth-1, heuristic)
        board.pop()

        if child_v < v:
            v = child_v
            best_move = move
        beta = min(beta, child_v)
        if alpha >= beta: break

    return (v, best_move)

def play_game(board=None, depth=4,
              white_heuristic=our_heuristic,
              black_heuristic=your_heuristic,
              graphics=False):

    if board == None:
        board = chess.Board() # normal starting position
    lastmove = None
        
    while not board.is_game_over():
        
        print(board)

    
        start = timer()
        if board.turn == chess.WHITE:
            print("white moves")
            (v, move) = max_value(board, -np.inf, +np.inf,
                                  depth, white_heuristic)
        else:
            print("black moves")
            (v, move) = min_value(board, -np.inf, +np.inf,
                                  depth, black_heuristic)
        lastmove = move
        end = timer()
        time_taken = end-start
        
        print(move)
        print(f"time taken {time_taken:.2f}")
        board.push(move)
        print("---")
        #input()

    print(board)

    print(f"game over because {board.outcome()}")
    if board.outcome().winner == chess.WHITE:
        print("white wins")
    elif board.outcome().winner == chess.BLACK:
        print("black wins")
    else:
        print("draw")

play_game(depth=3)
