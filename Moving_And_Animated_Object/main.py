import turtle
import time
import random

# Create a screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(800, 600)
screen.title("Bouncing Ball Animation")

# Create a turtle object
obj = turtle.Turtle()
obj.shape("circle")
obj.color("white")
obj.speed(0)

# Initial position and velocity
x, y = 0, 0
vx, vy = 2, 2

# Object properties
radius = 20
color_list = ["red", "green", "blue", "yellow", "purple"]

# Animation loop
def animate():
    global x, y, vx, vy

    # Clear previous position
    obj.clear()

    # Update position
    x += vx
    y += vy

    # Bounce off edges
    if x > 350 or x < -350:
        vx *= -1
        obj.color(random.choice(color_list))
    if y > 250 or y < -250:
        vy *= -1
        obj.color(random.choice(color_list))

    # Draw object at new position
    obj.penup()
    obj.goto(x, y)
    obj.pendown()

    # Repeat animation
    screen.ontimer(animate, 16)  # 16 ms = 60 FPS

# Keyboard controls
def up():
    global vy
    vy += 1

def down():
    global vy
    vy -= 1

def left():
    global vx
    vx -= 1

def right():
    global vx
    vx += 1

def reset():
    global x, y, vx, vy
    x, y = 0, 0
    vx, vy = 2, 2
    obj.color("white")

def increase_speed():
    global vx, vy
    vx *= 1.1
    vy *= 1.1

def decrease_speed():
    global vx, vy
    vx /= 1.1
    vy /= 1.1

# Set up keyboard bindings
screen.listen()
screen.onkey(up, "Up")
screen.onkey(down, "Down")
screen.onkey(left, "Left")
screen.onkey(right, "Right")
screen.onkey(reset, "r")
screen.onkey(increase_speed, "i")
screen.onkey(decrease_speed, "d")

# Start animation
animate()

# Keep the window open
turtle.done()

"""
Bouncing Ball Animation Application
A simple bouncing ball animation application built using Python and the Turtle graphics library.
Features
A bouncing ball that changes color when it hits an edge
Keyboard controls to move the ball up, down, left, and right
Ability to reset the ball to its initial position and velocity
Ability to increase and decrease the speed of the ball
Requirements
Python 3.x
Turtle graphics library (included with Python)
Usage
Run the script using Python (e.g., python bouncing_ball.py)
Use the arrow keys to move the ball up, down, left, and right
Press the "r" key to reset the ball to its initial position and velocity
Press the "i" key to increase the speed of the ball
Press the "d" key to decrease the speed of the ball
Customization
You can customize the appearance of the ball and the background by modifying the obj.color() and screen.bgcolor() functions
You can also add more features, such as scoring or levels, by modifying the animate() function
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""