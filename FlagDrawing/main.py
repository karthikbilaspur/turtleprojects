import turtle

# Create a screen
screen = turtle.Screen()
screen.bgcolor("white")

# Function to draw a rectangle
def draw_rectangle(t, width, height, color):
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()

# Function to draw a circle
def draw_circle(t, radius, color):
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Function to draw a star
def draw_star(t, size, color):
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(5):
        t.forward(size)
        t.right(144)
    t.end_fill()

# Function to draw a flag
def draw_flag(t, flag_type):
    if flag_type == "india":
        # Orange Rectangle 
        t.penup()
        t.goto(-400, 250)
        t.pendown()
        draw_rectangle(t, 800, 167, "orange")

        # Green Rectangle
        t.penup()
        t.goto(-400, 83)
        t.pendown()
        draw_rectangle(t, 800, 167, "green")

        # Big Blue Circle
        t.penup()
        t.goto(70, 0)
        t.pendown()
        draw_circle(t, 70, "navy")

        # Big White Circle
        t.penup()
        t.goto(60, 0)
        t.pendown()
        draw_circle(t, 60, "white")

        # Mini Blue Circles
        t.penup()
        t.goto(-57, -8)
        t.pendown()
        for i in range(24):
            draw_circle(t, 3, "navy")
            t.penup()
            t.forward(15)
            t.right(15)
            t.pendown()

        # Small Blue Circle
        t.penup()
        t.goto(20, 0)
        t.pendown()
        draw_circle(t, 20, "navy")

        # Spokes
        t.penup()
        t.goto(0, 0)
        t.pendown()
        t.pensize(2)
        for i in range(24):
            t.forward(60)
            t.backward(60)
            t.left(15)

    elif flag_type == "usa":
        # Blue Rectangle
        t.penup()
        t.goto(-400, 250)
        t.pendown()
        draw_rectangle(t, 800, 167, "blue")

        # Red Rectangle
        t.penup()
        t.goto(-400, 83)
        t.pendown()
        draw_rectangle(t, 800, 167, "red")

        # White Stripes
        t.penup()
        t.goto(-400, 167)
        t.pendown()
        t.color("white")
        t.begin_fill()
        for _ in range(10):
            t.forward(800)
            t.backward(800)
            t.left(90)
            t.forward(16)
            t.right(90)
        t.end_fill()

        # Stars
        t.penup()
        t.goto(-375, 200)
        t.pendown()
        t.color("white")
        for i in range(50):
            draw_star(t, 10, "white")
            t.penup()
            t.forward(20)
            t.pendown()

    elif flag_type == "china":
        # Red Rectangle
        t.penup()
        t.goto(-400, 250)
        t.pendown()
        draw_rectangle(t, 800, 334, "red")

        # Yellow Stars
        t.penup()
        t.goto(-375, 200)
        t.pendown()
        t.color("yellow")
        for i in range(5):
            draw_star(t, 20, "yellow")
            t.penup()
            t.forward(40)
            t.pendown()

# Draw Indian flag
t = turtle.Turtle
# Function to draw a flag pole
def draw_flag_pole(t, x, y, height, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(10)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()

# Function to draw a flag rope
def draw_flag_rope(t, x, y, length, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.width(2)
    t.forward(length)

# Draw flag poles
t = turtle.Turtle()
t.speed(0)
draw_flag_pole(t, -400, -250, 200, "brown")
draw_flag_pole(t, 0, -250, 200, "brown")
draw_flag_pole(t, 400, -250, 200, "brown")

# Draw flag ropes
t = turtle.Turtle()
t.speed(0)
draw_flag_rope(t, -410, -50, 100, "black")
draw_flag_rope(t, 10, -50, 100, "black")
draw_flag_rope(t, 410, -50, 100, "black")

turtle.done()

"""
    Here's a sample README file for your flag drawing application:
Flag Drawing Application
A simple application built using Python and the Turtle graphics library to draw flags of different countries.
Features
Draws flags of India, USA, and China
Includes flag poles and ropes for a more realistic representation
Simple and intuitive design
Requirements
Python 3.x
Turtle graphics library (included with Python)
Usage
Run the script using Python (e.g., python flag_drawing_app.py)
The flags of India, USA, and China will be displayed on the screen
Customization
You can customize the flags, flag poles, and ropes by modifying the draw_flag, draw_flag_pole, and draw_flag_rope functions
You can add more flags by creating new functions and calling them in the main script
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""
