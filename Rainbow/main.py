import turtle
import random

# Create a turtle screen object
screen = turtle.Screen()

# Create a turtle object (pen)
pen = turtle.Turtle()

# Define a method to form a semicircle
# with a dynamic radius and color
def semi_circle(color, radius, position):
    pen.color(color)
    pen.circle(radius, -180)
    pen.up()
    pen.setpos(position, 0)
    pen.down()
    pen.right(180)

# Set the colors for drawing
colors = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']

# Setup the screen features
screen.setup(800, 600)
screen.bgcolor('black')
screen.title("Rainbow Semicircles")

# Setup the turtle features
pen.right(90)
pen.width(10)
pen.speed(7)

# Loop to draw 7 semicircles
for i in range(7):
    semi_circle(colors[i], 10 * (i + 8), -10 * (i + 1))

# Hide the turtle
pen.hideturtle()

# Add a text label
text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.penup()
text_turtle.goto(0, -200)
text_turtle.pendown()
text_turtle.write("Rainbow Semicircles", font=("Arial", 24, "bold"))

# Function to handle user input
def handle_input():
    user_input = screen.textinput("Enter color", "Enter color (e.g., red, blue, green)")
    if user_input != None:
        colors.append(user_input)
        semi_circle(user_input, 10 * (len(colors) + 7), -10 * (len(colors)))

# Create button to handle user input
button = turtle.Button(screen, handle_input, "Add color")

# Function to animate
def animate():
    pen.clear()
    for i in range(7):
        semi_circle(colors[i], 10 * (i + 8), -10 * (i + 1))
    screen.ontimer(animate, 1000)

# Create button to animate
animate_button = turtle.Button(screen, animate, "Animate")

# Function to undo
def undo():
    if len(colors) > 7:
        colors.pop()
        pen.clear()
        for i in range(7):
            semi_circle(colors[i], 10 * (i + 8), -10 * (i + 1))

# Create button to undo
undo_button = turtle.Button(screen, undo, "Undo")

# Function to redo
def redo():
    if len(colors) > 0:
        colors.append(colors[-1])
        semi_circle(colors[-1], 10 * (len(colors) + 7), -10 * (len(colors)))

# Create button to redo
redo_button = turtle.Button(screen, redo, "Redo")

# Function to reset
def reset():
    colors.clear()
    colors.extend(['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red'])
    pen.clear()
    for i in range(7):
        semi_circle(colors[i], 10 * (i + 8), -10 * (i + 1))

# Create button to reset
reset_button = turtle.Button(screen, reset, "Reset")

# Function to randomize colors
def randomize_colors():
    global colors
    colors = [random.choice(['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red']) for _ in range(7)]
    pen.clear()
    for i in range(7):
        semi_circle(colors[i], 10 * (i + 8), -10 * (i + 1))

# Create button to randomize colors
randomize_button = turtle.Button(screen, randomize_colors, "Randomize Colors")

# Keep the window open
turtle.done()

"""
A colorful and interactive Turtle graphics project that draws a series of semicircles in different colors.
Features
Draws a series of 7 semicircles in different colors
Allows users to add new colors to the semicircles
Includes buttons to animate, undo, redo, reset, and randomize colors
Uses Turtle graphics for a fun and interactive experience
Requirements
Python 3.x
Turtle graphics library (included with Python)
Usage
Run the script using Python (e.g., python rainbow_semicircles.py)
Use the buttons to interact with the semicircles
Add new colors to the semicircles using the "Add color" button
Animate the semicircles using the "Animate" button
Undo and redo changes using the "Undo" and "Redo" buttons
Reset the semicircles to their original state using the "Reset" button
Randomize the colors of the semicircles using the "Randomize Colors" button
Customization
You can customize the appearance of the semicircles by modifying the colors list and the semi_circle function
You can also add more features, such as sound effects or smoother animations, by modifying the animate function
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""