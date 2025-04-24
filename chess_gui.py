import chess
import customtkinter as ctk
from tkinter import messagebox
from main import GameManager

class ChessGUI:
    def __init__(self):
        # Configure customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("Advanced Chess Variant with AI")
        self.window.geometry("1200x800")

        # Unicode chess pieces
        self.pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
            '.': ' '
        }

        # Create main containers
        self.create_layout()

        # Initialize game manager
        self.manager = GameManager()
        self.manager.start_new_game()

        # GUI state
        self.selected_square = None
        self.square_size = 64

        # Colors
        self.light_square = "#FFFFFF"
        self.dark_square = "#A9A9A9"
        self.selected_color = "#90EE90"

        # Create game elements
        self.create_info_panel()
        self.create_board()
        self.create_game_controls()
        self.create_move_history()
        self.moves_list = []

        self.update_board()

    def create_layout(self):
        # Create main frames
        self.left_panel = ctk.CTkFrame(self.window, width=310)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)

        self.center_panel = ctk.CTkFrame(self.window)
        self.center_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.right_panel = ctk.CTkFrame(self.window, width=300)
        self.right_panel.pack(side="right", fill="y", padx=10, pady=10)

    def create_info_panel(self):
        info_label = ctk.CTkLabel(
            self.left_panel,
            text="Advanced Chess Variant with AI",
            font=("Arial", 24, "bold")
        )
        info_label.pack(pady=10)

        # Enhanced explanation text
        explanation = """
        🎮 Special Variant Rules:
        • Pawns can make a double move from ANY rank
        • This special ability can be used once per pawn
        • Regular chess rules apply otherwise

        🤖 Advanced AI Features:
        • Minimax with Alpha-Beta Pruning (Depth 3)
        • Sophisticated Position Evaluation:
            - Material value
            - Piece positioning
            - Pawn structure analysis
            - King safety evaluation
            - Center control scoring
            - Mobility assessment

        🎯 Strategy Tips:
        • Use pawn double-moves strategically
        • Control the center early
        • Protect your king with pawns
        • Watch for tactical opportunities

        ⚡ Quick Guide:
        1. Click piece to select
        2. Click target square to move
        3. Invalid moves will be rejected
        4. Watch for special notifications
        """

        info_text = ctk.CTkTextbox(self.left_panel, width=280, height=400)
        info_text.pack(pady=10, padx=10)
        info_text.insert("1.0", explanation)
        info_text.configure(state="disabled")

        # Enhanced status display
        self.status_frame = ctk.CTkFrame(self.left_panel)
        self.status_frame.pack(pady=10, fill="x", padx=10)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Game Status: White to move",
            font=("Arial", 14, "bold")
        )
        self.status_label.pack(pady=5)

        self.check_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=("Arial", 12),
            text_color="red"
        )
        self.check_label.pack(pady=5)

    def create_board(self):
        self.board_frame = ctk.CTkFrame(self.center_panel)
        self.board_frame.pack(padx=20, pady=20)

        self.squares = {}
        # Create 8x8 grid of labels
        for row in range(8):
            for col in range(8):
                bg_color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                square = ctk.CTkLabel(
                    self.board_frame,
                    text="",
                    width=60,
                    height=60,
                    fg_color=bg_color,
                    text_color="black",
                    font=("Arial", 36),
                    corner_radius=0
                )
                square.grid(row=row, column=col, padx=1, pady=1)
                square.bind('<Button-1>', lambda e, pos=(row, col): self.handle_click(pos))
                self.squares[(row, col)] = square

    def create_game_controls(self):
        controls_frame = ctk.CTkFrame(self.left_panel)
        controls_frame.pack(pady=20, fill="x", padx=10)

        new_game_btn = ctk.CTkButton(
            controls_frame,
            text="New Game",
            command=self.new_game
        )
        new_game_btn.pack(pady=5)

        resign_btn = ctk.CTkButton(
            controls_frame,
            text="Resign",
            command=self.resign_game
        )
        resign_btn.pack(pady=5)

    def create_move_history(self):
        history_label = ctk.CTkLabel(
            self.right_panel,
            text="Move History",
            font=("Arial", 16, "bold")
        )
        history_label.pack(pady=10)

        self.history_text = ctk.CTkTextbox(
            self.right_panel,
            width=250,
            height=600
        )
        self.history_text.pack(pady=10, padx=10)

    def update_board(self):
        board = chess.Board(self.manager.get_board_state())
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7-row)
                piece = board.piece_at(square)
                piece_symbol = piece.symbol() if piece else '.'

                bg_color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                if square == self.selected_square:
                    bg_color = self.selected_color

                self.squares[(row, col)].configure(
                    text=self.pieces[piece_symbol],
                    fg_color=bg_color
                )

    def handle_click(self, pos):
        row, col = pos
        square = chess.square(col, 7-row)

        if self.selected_square is None:
            self.selected_square = square
            piece = self.manager.game.board.piece_at(square)
            if piece:
                self.status_label.configure(text=f"Selected: {piece.symbol()} at {chess.square_name(square)}")
        else:
            try:
                move_uci = chess.square_name(self.selected_square) + chess.square_name(square)
                result = self.manager.make_user_move(move_uci)

                # Enhanced move history
                from_square = chess.square_name(self.selected_square)
                to_square = chess.square_name(square)
                piece_symbol = self.manager.game.board.piece_type_at(square)
                move_text = f"White: {piece_symbol} {from_square}-{to_square}\n"
                move_text += f"Black: {result['ai_move']}\n"
                self.history_text.insert("end", move_text)
                self.history_text.see("end")

                # Update game status with detailed information
                board = self.manager.game.board
                if result['is_game_over']:
                    if board.is_checkmate():
                        winner = "Black" if board.turn else "White"
                        messagebox.showinfo("Checkmate!", f"Game Over - {winner} wins by checkmate!")
                    elif board.is_stalemate():
                        messagebox.showinfo("Stalemate!", "Game Over - Draw by stalemate")
                    elif board.is_insufficient_material():
                        messagebox.showinfo("Draw!", "Game Over - Draw by insufficient material")
                    elif board.is_fifty_moves():
                        messagebox.showinfo("Draw!", "Game Over - Draw by fifty-move rule")
                    elif board.is_repetition():
                        messagebox.showinfo("Draw!", "Game Over - Draw by repetition")
                    self.new_game()
                else:
                    # Update status for ongoing game
                    if board.is_check():
                        self.check_label.configure(text="⚠️ CHECK!")
                    else:
                        self.check_label.configure(text="")

                    self.status_label.configure(
                        text=f"Last move: {result['ai_move']}"
                    )

            except ValueError:
                messagebox.showerror("Invalid Move", "That move is not allowed!")
            except RuntimeError as e:
                messagebox.showerror("Error", str(e))

            self.selected_square = None

        self.update_board()

    def new_game(self):
        self.manager.start_new_game()
        self.selected_square = None
        self.history_text.delete("1.0", "end")
        self.status_label.configure(text="White to move")
        self.update_board()

    def resign_game(self):
        messagebox.showinfo("Game Over", "White resigns. Black wins!")
        self.new_game()

    # Add method to create move notation
    def get_piece_name(self, piece_type: int) -> str:
        names = {
            chess.PAWN: "Pawn",
            chess.KNIGHT: "Knight",
            chess.BISHOP: "Bishop",
            chess.ROOK: "Rook",
            chess.QUEEN: "Queen",
            chess.KING: "King"
        }
        return names.get(piece_type, "")

def main():
    app = ChessGUI()
    app.window.mainloop()

if __name__ == "__main__":
    main()