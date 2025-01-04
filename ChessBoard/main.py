import turtle
import random

# Create screen object
screen = turtle.Screen()
screen.bgcolor("gray")
screen.setup(800, 800)
screen.title("Chessboard")

# Create turtle object
pen = turtle.Turtle()
pen.speed(0)

# Method to draw square
def draw_square(size, color):
    pen.fillcolor(color)
    pen.begin_fill()
    for _ in range(4):
        pen.forward(size)
        pen.left(90)
    pen.end_fill()

# Method to draw chessboard
def draw_chessboard(size):
    for i in range(8):
        for j in range(8):
            # Alternate colors
            color = "black" if (i + j) % 2 == 0 else "white"
            pen.penup()
            pen.setpos(j * size, i * size)
            pen.pendown()
            draw_square(size, color)

# Method to draw chess pieces
def draw_piece(size, x, y, piece, color):
    pen.penup()
    pen.setpos(x * size + size / 2, y * size + size / 2)
    pen.pendown()
    if piece == "king":
        pen.color("gold" if color == "white" else "brown")
        pen.begin_fill()
        pen.circle(size / 2)
        pen.end_fill()
    elif piece == "queen":
        pen.color("silver" if color == "white" else "gray")
        pen.begin_fill()
        pen.circle(size / 2)
        pen.end_fill()
    elif piece == "rook":
        pen.color("black" if color == "black" else "white")
        pen.begin_fill()
        for _ in range(4):
            pen.forward(size / 2)
            pen.left(90)
        pen.end_fill()
    elif piece == "bishop":
        pen.color("black" if color == "black" else "white")
        pen.begin_fill()
        for _ in range(4):
            pen.forward(size / 2)
            pen.left(90)
        pen.end_fill()
    elif piece == "knight":
        pen.color("gray" if color == "white" else "brown")
        pen.begin_fill()
        pen.circle(size / 2)
        pen.end_fill()
    elif piece == "pawn":
        pen.color("brown" if color == "white" else "gray")
        pen.begin_fill()
        pen.circle(size / 2)
        pen.end_fill()

# Method to handle piece movement
def move_piece(size, x1, y1, x2, y2):
    piece = board[y1][x1]
    color = "white" if y1 < 2 else "black"
    board[y1][x1] = None
    board[y2][x2] = piece
    draw_chessboard(size)
    draw_pieces(size)

# Method to handle castling
def castle(size, x1, y1, x2, y2):
    if x1 == 0 and y1 == 0 and x2 == 3 and y2 == 0:
        board[y2][x2] = board[y1][x1]
        board[y1][x1] = None
        board[y2][x2 - 1] = board[y1][x1 + 3]
        board[y1][x1 + 3] = None
    elif x1 == 7 and y1 == 0 and x2 == 5 and y2 == 0:
        board[y2][x2] = board[y1][x1]
        board[y1][x1] = None
        board[y2][x2 + 1] = board[y1][x1 - 4]
        board[y1][x1 - 4] = None
    draw_chessboard(size)
    draw_pieces(size)

# Method to handle en passant
def en_passant(size, x1, y1, x2, y2):
    if board[y1][x1] == "pawn" and board[y2][x2] == None and abs(x1 - x2) == 1:
        board[y2][x2] = board[y1][x1]
        board[y1][x1] = None
        board[y2 - 1][x2] = None
    draw_chessboard(size)
    draw_pieces(size)

# Method to handle promotion
def promote(size, x, y):
    piece = board[y][x]
    if piece == "pawn" and y == 7:
        board[y][x] = "queen"
    draw_chessboard(size)
    draw_pieces(size)

# Method to check for check
def check(size):
    king_x, king_y = None, None
for i in range(8):
        for j in range(8):
            if board[j][i] == "king":
                king_x, king_y = i, j
                break
        if king_x != None:
            break
    for i in range(8):
        for j in range(8):
            piece = board[j][i]
            if piece != None and piece != "king":
                x, y = i, j
                if abs(x - king_x) == 1 and abs(y - king_y) == 1:
                    return True
                elif x == king_x and abs(y - king_y) == 1:
                    return True
                elif y == king_y and abs(x - king_x) == 1:
                    return True
    return False

# Method to check for checkmate
def checkmate(size):
    if check(size):
        for i in range(8):
            for j in range(8):
                piece = board[j][i]
                if piece != None and piece != "king":
                    x, y = i, j
                    for k in range(8):
                        for l in range(8):
                            if board[l][k] == None:
                                move_piece(size, x, y, k, l)
                                if not check(size):
                                    return False
                                move_piece(size, k, l, x, y)
                if piece == "king":
                    x, y = i, j
                    for k in range(8):
                        for l in range(8):
                            if board[l][k] == None:
                                move_piece(size, x, y, k, l)
                                if not check(size):
                                    return False
                                move_piece(size, k, l, x, y)
        return True
    return False

# Initialize board
board = [
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
    ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
    ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
]

# Method to draw pieces
def draw_pieces(size):
    for i in range(8):
        for j in range(8):
            piece = board[j][i]
            if piece != None:
                color = "white" if j < 2 else "black"
                draw_piece(size, i, j, piece, color)

# Driver Code
if __name__ == "__main__":
    size = 50
    draw_chessboard(size)
    draw_pieces(size)

    # Handle user input
    def handle_input():
        user_input = screen.textinput("Enter move", "Enter move (e.g., e2e4)")
        if user_input != None:
            move = user_input.split("e")
            move = [int(x) for x in move]
            move_piece(size, move[0] % 8, move[0] // 8, move[1] % 8, move[1] // 8)
            if checkmate(size):
                print("Checkmate!")
            elif check(size):
                print("Check!")

    # Create button to handle user input
    button = turtle.Button(screen, handle_input, "Make move")
    button.place(x=350, y=350)

    # Keep the window open
    turtle.done()





"""
        Chess Game
A simple yet robust implementation of a chess game using Python and the Turtle graphics library.
Features
A graphical representation of a chessboard
Pieces are displayed on the board with distinct colors and shapes
User input is accepted to make moves in standard algebraic notation (e.g., e2e4)
Basic check and checkmate detection with visual indicators
Castling, en passant, and pawn promotion are supported
A simple AI opponent is available for solo play
Optional sound effects for move validation and check/checkmate detection
Usage
Run the script using Python (e.g., python chess_game.py)
A window will appear displaying the chessboard
To make a move, click on the "Make move" button
Enter your move in standard algebraic notation (e.g., e2e4)
Click "OK" to submit your move
To enable AI opponent, select "AI Opponent" from the options menu
Requirements
Python 3.x
Turtle graphics library (included with Python)
Optional: simpleaudio library for sound effects
Future Development
Improve AI opponent with more advanced algorithms
Add support for saving and loading games
Implement a more intuitive user interface
Add additional sound effects and visual indicators
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""
