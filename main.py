from game import ChessGame
from ai import ChessAI
from typing import Dict, Optional

class GameManager:
    def __init__(self):
        self.game = None
        self.ai = None

    def start_new_game(self) -> None:
        self.game = ChessGame()
        self.ai = ChessAI(depth=2)

    def make_user_move(self, uci: str) -> Dict[str, str]:
        if not self.game:
            raise RuntimeError("Game not started")

        if not self.game.apply_user_move(uci):
            raise ValueError("Invalid move")

        # Get AI's response
        ai_move = self.ai.get_best_move(self.game.board)
        ai_move_uci = self.game.apply_ai_move(ai_move)

        return {
            "ai_move": ai_move_uci,
            "fen": self.game.get_board_fen(),
            "is_game_over": self.game.is_game_over(),
            "result": self.game.get_result()
        }

    def get_board_state(self) -> str:
        if not self.game:
            raise RuntimeError("Game not started")
        return self.game.get_board_fen()

    def get_last_ai_move(self) -> Optional[str]:
        if not self.game or not self.game.last_move:
            return None
        return self.game.last_move.uci()