import turtle
import random

# Constants
BOARD_SIZE = 800
SQUARE_SIZE = BOARD_SIZE // 8
PIECE_SIZE = SQUARE_SIZE // 2

# Colors
WHITE = "white"
BLACK = "black"
GRAY = "gray"
GOLD = "gold"
SILVER = "silver"
BROWN = "brown"

# Piece types
KING = "king"
QUEEN = "queen"
ROOK = "rook"
BISHOP = "bishop"
KNIGHT = "knight"
PAWN = "pawn"

class Piece:
    def __init__(self, piece_type, color, x, y):
        self.piece_type = piece_type
        self.color = color
        self.x = x
        self.y = y

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_pieces()

    def initialize_pieces(self):
        for i in range(8):
            self.board[1][i] = Piece(PAWN, WHITE, i, 1)
            self.board[6][i] = Piece(PAWN, BLACK, i, 6)

        self.board[0][0] = Piece(ROOK, WHITE, 0, 0)
        self.board[0][1] = Piece(KNIGHT, WHITE, 1, 0)
        self.board[0][2] = Piece(BISHOP, WHITE, 2, 0)
        self.board[0][3] = Piece(QUEEN, WHITE, 3, 0)
        self.board[0][4] = Piece(KING, WHITE, 4, 0)
        self.board[0][5] = Piece(BISHOP, WHITE, 5, 0)
        self.board[0][6] = Piece(KNIGHT, WHITE, 6, 0)
        self.board[0][7] = Piece(ROOK, WHITE, 7, 0)

        self.board[7][0] = Piece(ROOK, BLACK, 0, 7)
        self.board[7][1] = Piece(KNIGHT, BLACK, 1, 7)
        self.board[7][2] = Piece(BISHOP, BLACK, 2, 7)
        self.board[7][3] = Piece(QUEEN, BLACK, 3, 7)
        self.board[7][4] = Piece(KING, BLACK, 4, 7)
        self.board[7][5] = Piece(BISHOP, BLACK, 5, 7)
        self.board[7][6] = Piece(KNIGHT, BLACK, 6, 7)
        self.board[7][7] = Piece(ROOK, BLACK, 7, 7)

    def draw_board(self):
        screen = turtle.Screen()
        screen.setup(BOARD_SIZE, BOARD_SIZE)
        screen.title("Chess Game")

        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    turtle.penup()
                    turtle.goto(j * SQUARE_SIZE, i * SQUARE_SIZE)
                    turtle.pendown()
                    turtle.fillcolor(WHITE)
                    turtle.begin_fill()
                    for _ in range(4):
                        turtle.forward(SQUARE_SIZE)
                        turtle.right(90)
                    turtle.end_fill()
                else:
                    turtle.penup()
                    turtle.goto(j * SQUARE_SIZE, i * SQUARE_SIZE)
                    turtle.pendown()
                    turtle.fillcolor(BLACK)
                    turtle.begin_fill()
                    for _ in range(4):
                        turtle.forward(SQUARE_SIZE)
                        turtle.right(90)
                    turtle.end_fill()

    def draw_pieces(self):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None:
                    turtle.penup()
                    turtle.goto(j * SQUARE_SIZE + SQUARE_SIZE // 2, i * SQUARE_SIZE + SQUARE_SIZE // 2)
                    turtle.pendown()
                    if piece.piece_type == KING:
                        turtle.fillcolor(GOLD if piece.color == WHITE else BROWN)
                        turtle.begin_fill()
                        turtle.circle(PIECE_SIZE // 2)
                        turtle.end_fill()
                    elif piece.piece_type == QUEEN:
                        turtle.fillcolor(SILVER if piece.color == WHITE else GRAY)
                        turtle.begin_fill()
                        turtle.circle(PIECE_SIZE // 2)
                        turtle.end_fill()
                    elif piece.piece_type == BISHOP:
                        turtle.fillcolor(WHITE if piece.color == WHITE else BLACK)
                        turtle.begin_fill()
                        for _ in range(4):
                            turtle.forward(PIECE_SIZE // 2)
                            turtle.right(90)
                        turtle.end_fill()
                    elif piece.piece_type == KNIGHT:
                        turtle.fillcolor(WHITE if piece.color == WHITE else BLACK)
                        turtle.begin_fill()
                        turtle.circle(PIECE_SIZE // 2)
                        turtle.end_fill()
                    elif piece.piece_type == PAWN:
                        turtle.fillcolor(WHITE if piece.color == WHITE else BLACK)
                        turtle.begin_fill()
                        turtle.circle(PIECE_SIZE // 2)
                        turtle.end_fill()

    def handle_move(self, x1, y1, x2, y2):
        piece = self.board[y1][x1]
        if piece is not None:
            self.board[y1][x1] = None
            self.board[y2][x2] = piece
            piece.x = x2
            piece.y = y2

    def check_for_check(self):
        # Check if king is in check
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece is not None and piece.piece_type == KING:
                    king_x, king_y = j, i
                    for x in range(8):
                        for y in range(8):
                            opponent_piece = self.board[y][x]
                            if opponent_piece is not None and opponent_piece.color != piece.color:
                                if self.is_under_attack(king_x, king_y, opponent_piece):
                                    return True
        return False

    def is_under_attack(self, x, y, piece):
        # Check if piece is under attack by opponent piece
        if piece.piece_type == KNIGHT:
            # Check knight moves
            for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                if x + dx >= 0 and x + dx < 8 and y + dy >= 0 and y + dy < 8:
                    if self.board[y + dy][x + dx] is not None and self.board[y + dy][x + dx].color == piece.color:
                        return True
        elif piece.piece_type == BISHOP:
            # Check bishop moves
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.board[ny][nx] is not None:
                        if self.board[ny][nx].color == piece.color:
                            return True
                        break
                    nx += dx
                    ny += dy
        elif piece.piece_type == ROOK:
            # Check rook moves
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.board[ny][nx] is not None:
                        if self.board[ny][nx].color == piece.color:
                            return True
                        break
                    nx += dx
                    ny += dy
        elif piece.piece_type == QUEEN:
            # Check queen moves
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nx, ny = x + dx, y + dy
                while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.board[ny][nx] is not None:
                        if self.board[ny][nx].color == piece.color:
                            return True
                        break
                    nx += dx
                    ny += dy
        return False

    def check_for_checkmate(self):
        # Check if king is in checkmate
        if self.check_for_check():
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece is not None and piece.piece_type == KING:
                        king_x, king_y = j, i
                        for x in range(8):
                            for y in range(8):
                                 opponent_piece = self.board[y][x]
                    if opponent_piece is not None and opponent_piece.color != piece.color:
                                    if self.is_under_attack(king_x, king_y, opponent_piece):
                                        # Check if king can move to safety
                                        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                                            nx, ny = king_x + dx, king_y + dy
                                            if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                                                if self.board[ny][nx] is None:
                                                    # Simulate king move
                                                    self.board[king_y][king_x] = None
                                                    self.board[ny][nx] = piece
                                                    piece.x = nx
                                                    piece.y = ny
                                                    # Check if king is still under attack
                                                    if not self.is_under_attack(nx, ny, opponent_piece):
                                                        # King can move to safety, not checkmate
                                                        return False
                                                    # Revert simulated king move
                                                    self.board[king_y][king_x] = piece
                                                    self.board[ny][nx] = None
                                        # King cannot move to safety, checkmate
                                        return True
        # King is not in check, not checkmate
        return False

def main():
    board = Board()
    board.draw_board()
    board.draw_pieces()

    # Handle user input
    def handle_input():
        user_input = turtle.Screen.textinput("Enter move", "Enter move (e.g., e2e4)")
        if user_input is not None:
            move = user_input.split("e")
            move = [int(x) for x in move]
            board.handle_move(move[0] % 8, move[0] // 8, move[1] % 8, move[1] // 8)
            board.draw_board()
            board.draw_pieces()
            if board.check_for_checkmate():
                print("Checkmate!")

    # Create button to handle user input
    button = turtle.Button(turtle.Screen, handle_input, "Make move")
    button.place(x=350, y=350)

    # Keep the window open
    turtle.done()

if __name__ == "__main__":
    main()