import chess
import random

# Piece-Square Tables: Positional evaluation charts for each piece type.
# These lists represent the relative value of each square on the board for a given piece type.
# Higher values indicate more favorable positions.
pawn_chart = [
    # Positional evaluation for pawns
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knight_chart = [
    # Positional evaluation for knights
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishops_chart = [
    # Positional evaluation for bishops
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rooks_chart = [
    # Positional evaluation for rooks
    -10, 0, 0, 5, 5, 0, 0, -10,
    5, 0, 0, 0, 0, 0, 0, 5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    -10, 0, 0, 0, 0, 0, 0, -10]

queens_chart = [
    # Positional evaluation for queens
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kings_chart = [
    # Positional evaluation for kings in early/middle game
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

class TranspositionTable:
    # A class to handle caching of board evaluations to optimize search
    def __init__(self):
        self.table = {}

    def lookup(self, key):
        # Retrieve a stored evaluation from the transposition table, if available
        return self.table.get(key)

    def store(self, key, value):
        # Store a board evaluation in the transposition table
        self.table[key] = value

class group1:
    # A class representing a simple chess engine, responsible for board evaluation and move selection
    def __init__(self, color):
        self.color = color
        self.transposition_table = TranspositionTable()

    def generate_board_key(self, board):
        # Generate a unique key for the current board state using the FEN notation
        return board.fen()

    def evaluate_board(self, board):
        # Evaluate the current board position using material and positional analysis
        # Special cases for checkmate, stalemate, and insufficient material
        if board.is_checkmate():
            return -9999 if board.turn else 9999  # Assign high negative/positive values for checkmate
        if board.is_stalemate() or board.is_insufficient_material():
            return 0  # Draw conditions

        # Check if evaluation for the current board state is cached
        board_key = self.generate_board_key(board)
        cached_value = self.transposition_table.lookup(board_key)
        if cached_value is not None:
            return cached_value
        else:
            # Material evaluation: Weigh the number of pieces for each side
            pw = len(board.pieces(chess.PAWN, chess.WHITE))
            pb = len(board.pieces(chess.PAWN, chess.BLACK))
            nw = len(board.pieces(chess.KNIGHT, chess.WHITE))
            nb = len(board.pieces(chess.KNIGHT, chess.BLACK))
            bw = len(board.pieces(chess.BISHOP, chess.WHITE))
            bb = len(board.pieces(chess.BISHOP, chess.BLACK))
            rw = len(board.pieces(chess.ROOK, chess.WHITE))
            rb = len(board.pieces(chess.ROOK, chess.BLACK))
            qw = len(board.pieces(chess.QUEEN, chess.WHITE))
            qb = len(board.pieces(chess.QUEEN, chess.BLACK))

            material = 100 * (pw - pb) + 320 * (nw - nb) + 330 * (bw - bb) + 500 * (rw - rb) + 900 * (qw - qb)

            # Positional evaluation using Piece-Square tables
            pawnsq = sum([pawn_chart[i] for i in board.pieces(chess.PAWN, chess.WHITE)]) + \
                     sum([-pawn_chart[chess.square_mirror(i)] for i in board.pieces(chess.PAWN, chess.BLACK)])
            knightsq = sum([knight_chart[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)]) + \
                       sum([-knight_chart[chess.square_mirror(i)] for i in board.pieces(chess.KNIGHT, chess.BLACK)])
            bishopsq = sum([bishops_chart[i] for i in board.pieces(chess.BISHOP, chess.WHITE)]) + \
                       sum([-bishops_chart[chess.square_mirror(i)] for i in board.pieces(chess.BISHOP, chess.BLACK)])
            rooksq = sum([rooks_chart[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) + \
                     sum([-rooks_chart[chess.square_mirror(i)] for i in board.pieces(chess.ROOK, chess.BLACK)])
            queensq = sum([queens_chart[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) + \
                      sum([-queens_chart[chess.square_mirror(i)] for i in board.pieces(chess.QUEEN, chess.BLACK)])
            kingsq = sum([kings_chart[i] for i in board.pieces(chess.KING, chess.WHITE)]) + \
                     sum([-kings_chart[chess.square_mirror(i)] for i in board.pieces(chess.KING, chess.BLACK)])

            evaluation = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

            # Store the computed evaluation in the transposition table
            self.transposition_table.store(board_key, evaluation)
            return evaluation

    def get_move(self, board):
        # Select a random move from available legal moves
        move = random.choice(list(board.legal_moves))
        return move
