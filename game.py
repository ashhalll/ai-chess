import chess
from typing import Optional, Dict, Set

class VariantBoard(chess.Board):
    def __init__(self):
        super().__init__()
        # Track pawns that have used their special double move
        self.double_moved_pawns: Set[int] = set()

    def is_legal_variant_move(self, move: chess.Move) -> bool:
        # Check if it's a pawn move
        if not self.piece_type_at(move.from_square) == chess.PAWN:
            return self.is_legal(move)

        # Check if it's a double move (two ranks)
        if abs(chess.square_rank(move.from_square) - chess.square_rank(move.to_square)) == 2:
            # Check if pawn hasn't used double move yet
            if move.from_square not in self.double_moved_pawns:
                return True
            return False

        return self.is_legal(move)

    def push(self, move: chess.Move) -> None:
        # Track double moves
        if self.piece_type_at(move.from_square) == chess.PAWN:
            if abs(chess.square_rank(move.from_square) - chess.square_rank(move.to_square)) == 2:
                self.double_moved_pawns.add(move.from_square)
        super().push(move)

class ChessGame:
    def __init__(self):
        self.board = VariantBoard()
        self.last_move = None

    def apply_user_move(self, move_uci: str) -> bool:
        try:
            move = chess.Move.from_uci(move_uci)
            if self.board.is_legal_variant_move(move):
                self.board.push(move)
                self.last_move = move
                return True
            return False
        except ValueError:
            return False

    def apply_ai_move(self, move: chess.Move) -> str:
        self.board.push(move)
        self.last_move = move
        return move.uci()

    def get_board_fen(self) -> str:
        return self.board.fen()

    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    def get_result(self) -> str:
        if not self.is_game_over():
            return "*"
        if self.board.is_checkmate():
            return "1-0" if self.board.turn else "0-1"
        return "1/2-1/2"