from random import shuffle
from turtle import *

# Set the screen
screen = Screen()
screen.setup(800, 600)  # Increased window size

# Choose background color
screen.bgcolor("light blue")

# Define the function for creating a square section
def Square(x, y, color):
    up()
    goto(x, y)
    down()
    color('white', color)
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()

# Define function to keep a check of index number
def Numbering(x, y):
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)

# Define function
def Coordinates(count):
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200

# Define function to make it interactive (user click)
def click(x, y):
    spot = Numbering(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None
        check_win()

def check_win():
    if all(not hidden for hidden in hide):
        screen.bgcolor("green")
        write("Congratulations! You won!", font=('Arial', 30, 'bold'))

def draw():
    clear()
    goto(0, 0)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = Coordinates(count)
            Square(x, y, 'gray')  # Changed color
        else:
            x, y = Coordinates(count)
            up()
            goto(x + 2, y)
            color('black')
            write(tiles[count], font=('Arial', 30, 'normal'))

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = Coordinates(mark)
        up()
        goto(x + 2, y)
        color('red')  # Highlighted color
        write(tiles[mark], font=('Arial', 30, 'normal'))

    update()
    ontimer(draw, 10)

tiles = list(range(32)) * 2
state = {'mark': None}
hide = [True] * 64

# Shuffle numbers
shuffle(tiles)

tracer(False)
onscreenclick(click)
draw()
done()

"""
Memory Game Application
A simple memory game application built using Python and the Turtle graphics library.
Features
A 8x8 grid of tiles with hidden numbers
User can click on a tile to reveal the number
User can match two tiles with the same number
Game ends when all tiles are matched
Requirements
Python 3.x
Turtle graphics library (included with Python)
Usage
Run the script using Python (e.g., python memory_game.py)
Click on a tile to reveal the number
Click on another tile to reveal the number and try to match
Continue playing until all tiles are matched
Customization
You can customize the game by changing the size of the grid, the numbers on the tiles, and the colors used
You can also add more features, such as a timer or a score counter
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""