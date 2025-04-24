import chess
from typing import Optional, Tuple, Dict
import random

class ChessAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        # Enhanced piece values with position-dependent scoring
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        # Piece-Square Tables for positional evaluation
        self.pawn_table = [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]

        self.knight_table = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]

        # Cache for transposition table
        self.transposition_table: Dict[str, Tuple[float, Optional[chess.Move]]] = {}

    def evaluate_position(self, board: chess.Board) -> float:
        if board.is_checkmate():
            return float('-inf') if board.turn else float('inf')

        if board.is_stalemate() or board.is_insufficient_material():
            return 0.0

        score = 0.0

        # Material and position evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                # Base material value
                value = self.piece_values[piece.piece_type]

                # Add positional bonus
                if piece.piece_type == chess.PAWN:
                    value += self.pawn_table[square if piece.color else 63 - square] * 0.1
                elif piece.piece_type == chess.KNIGHT:
                    value += self.knight_table[square if piece.color else 63 - square] * 0.1

                score += value if piece.color else -value

        # Mobility evaluation
        mobility_score = len(list(board.legal_moves)) * 10
        score += mobility_score if board.turn else -mobility_score

        # Center control (with expanded center)
        center_squares = {chess.E4, chess.E5, chess.D4, chess.D5,
                        chess.C3, chess.C4, chess.C5, chess.C6,
                        chess.D3, chess.D6, chess.E3, chess.E6,
                        chess.F3, chess.F4, chess.F5, chess.F6}
        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                bonus = 30 if square in {chess.E4, chess.E5, chess.D4, chess.D5} else 15
                score += bonus if piece.color else -bonus

        # Pawn structure evaluation
        score += self._evaluate_pawn_structure(board)

        # King safety
        score += self._evaluate_king_safety(board)

        return score if board.turn else -score

    def _evaluate_pawn_structure(self, board: chess.Board) -> float:
        score = 0.0

        # Evaluate doubled pawns (penalty)
        for file in range(8):
            white_pawns = 0
            black_pawns = 0
            for rank in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                if piece and piece.piece_type == chess.PAWN:
                    if piece.color:
                        white_pawns += 1
                    else:
                        black_pawns += 1
            if white_pawns > 1:
                score -= 20 * (white_pawns - 1)
            if black_pawns > 1:
                score += 20 * (black_pawns - 1)

        return score

    def _evaluate_king_safety(self, board: chess.Board) -> float:
        score = 0.0

        # King shield (pawns near king)
        for color in [True, False]:
            king_square = board.king(color)
            if king_square is None:
                continue

            king_file = chess.square_file(king_square)
            king_rank = chess.square_rank(king_square)

            # Check pawns in front of king
            for file_offset in [-1, 0, 1]:
                if 0 <= king_file + file_offset <= 7:
                    pawn_square = chess.square(king_file + file_offset,
                                            king_rank + (1 if color else -1))
                    if board.piece_at(pawn_square) and \
                       board.piece_at(pawn_square).piece_type == chess.PAWN and \
                       board.piece_at(pawn_square).color == color:
                        score += 30 if color else -30

        return score

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float) -> Tuple[float, Optional[chess.Move]]:
        # Check transposition table
        board_hash = board.fen()
        if depth > 1 and board_hash in self.transposition_table:
            return self.transposition_table[board_hash]

        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None
        if board.turn:  # Maximizing player
            max_eval = float('-inf')
            # Move ordering - evaluate captures first
            moves = list(board.legal_moves)
            moves.sort(key=lambda m: board.is_capture(m), reverse=True)

            for move in moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta)
                board.pop()

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            # Store in transposition table
            if depth > 1:
                self.transposition_table[board_hash] = (max_eval, best_move)
            return max_eval, best_move

        else:  # Minimizing player
            min_eval = float('inf')
            moves = list(board.legal_moves)
            moves.sort(key=lambda m: board.is_capture(m), reverse=True)

            for move in moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta)
                board.pop()

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            if depth > 1:
                self.transposition_table[board_hash] = (min_eval, best_move)
            return min_eval, best_move

    def get_best_move(self, board: chess.Board) -> chess.Move:
        # Clear transposition table periodically to prevent memory issues
        if len(self.transposition_table) > 1000000:
            self.transposition_table.clear()

        _, best_move = self.minimax(board, self.depth, float('-inf'), float('inf'))
        return best_move