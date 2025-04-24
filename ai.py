import chess
from typing import Optional, Tuple

class ChessAI:
    def __init__(self, depth: int = 2):
        self.depth = depth
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

    def evaluate_position(self, board: chess.Board) -> float:
        if board.is_checkmate():
            return float('-inf') if board.turn else float('inf')

        score = 0.0
        # Material evaluation
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                value = self.piece_values[piece.piece_type]
                score += value if piece.color else -value

        # Center control bonus
        center_squares = {chess.E4, chess.E5, chess.D4, chess.D5}
        for square in center_squares:
            piece = board.piece_at(square)
            if piece is not None:
                bonus = 30
                score += bonus if piece.color else -bonus

        return score if board.turn else -score

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float) -> Tuple[float, Optional[chess.Move]]:
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None

        best_move = None
        if board.turn:  # Maximizing player
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta)
                board.pop()

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:  # Minimizing player
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta)
                board.pop()

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, board: chess.Board) -> chess.Move:
        _, best_move = self.minimax(board, self.depth, float('-inf'), float('inf'))
        return best_move