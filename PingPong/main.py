import turtle
import random

# Create screen
sc = turtle.Screen()
sc.title("Pong Game")
sc.bgcolor("black")
sc.setup(width=1000, height=600)

# Left paddle
left_pad = turtle.Turtle()
left_pad.speed(0)
left_pad.shape("square")
left_pad.color("white")
left_pad.shapesize(stretch_wid=6, stretch_len=2)
left_pad.penup()
left_pad.goto(-400, 0)

# Right paddle
right_pad = turtle.Turtle()
right_pad.speed(0)
right_pad.shape("square")
right_pad.color("white")
right_pad.shapesize(stretch_wid=6, stretch_len=2)
right_pad.penup()
right_pad.goto(400, 0)

# Ball of circle shape
hit_ball = turtle.Turtle()
hit_ball.speed(40)
hit_ball.shape("circle")
hit_ball.color("blue")
hit_ball.penup()
hit_ball.goto(0, 0)
hit_ball.dx = random.choice([-5, 5])
hit_ball.dy = random.choice([-5, 5])

# Score
left_score = 0
right_score = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"Left: {left_score} Right: {right_score}", align="center", font=("Arial", 24, "bold"))

# Paddle movement
def paddle_up_left():
    y = left_pad.ycor()
    if y < 250:
        y += 20
        left_pad.sety(y)

def paddle_down_left():
    y = left_pad.ycor()
    if y > -250:
        y -= 20
        left_pad.sety(y)

def paddle_up_right():
    y = right_pad.ycor()
    if y < 250:
        y += 20
        right_pad.sety(y)

def paddle_down_right():
    y = right_pad.ycor()
    if y > -250:
        y -= 20
        right_pad.sety(y)

# Keyboard bindings
sc.listen()
sc.onkey(paddle_up_left, "w")
sc.onkey(paddle_down_left, "s")
sc.onkey(paddle_up_right, "Up")
sc.onkey(paddle_down_right, "Down")

# Ball movement
def move_ball():
    global left_score, right_score
    hit_ball.setx(hit_ball.xcor() + hit_ball.dx)
    hit_ball.sety(hit_ball.ycor() + hit_ball.dy)

    # Border checking
    if hit_ball.ycor() > 290:
        hit_ball.sety(290)
        hit_ball.dy *= -1
    if hit_ball.ycor() < -290:
        hit_ball.sety(-290)
        hit_ball.dy *= -1
    if hit_ball.xcor() > 490:
        hit_ball.goto(0, 0)
        left_score += 1
        score_display.clear()
        score_display.write(f"Left: {left_score} Right: {right_score}", align="center", font=("Arial", 24, "bold"))
        hit_ball.dx *= -1
    if hit_ball.xcor() < -490:
        hit_ball.goto(0, 0)
        right_score += 1
        score_display.clear()
        score_display.write(f"Left: {left_score} Right: {right_score}", align="center", font=("Arial", 24, "bold"))
        hit_ball.dx *= -1

    # Paddle collision
    if (hit_ball.xcor() > 390 and hit_ball.xcor() < 400) and (hit_ball.ycor() < right_pad.ycor() + 60 and hit_ball.ycor() > right_pad.ycor() - 60):
        hit_ball.setx(390)
        hit_ball.dx *= -1
    if (hit_ball.xcor() < -390 and hit_ball.xcor() > -400) and (hit_ball.ycor() < left_pad.ycor() + 60 and hit_ball.ycor() > left_pad.ycor() - 60):
        hit_ball.setx(-390)
        hit_ball.dx *= -1

    sc.ontimer(move_ball, 100)

move_ball()

# Keep the window open
turtle.done()

"""
Pong Game Application
A simple Pong game application built using Python and the Turtle graphics library.
Features
A classic Pong game with two paddles and a ball
Keyboard controls to move the paddles up and down
Scoring system to keep track of points
Simple and intuitive gameplay
Requirements
Python 3.x
Turtle graphics library (included with Python)
Usage
Run the script using Python (e.g., python pong_game.py)
Use the "w" and "s" keys to move the left paddle up and down
Use the "Up" and "Down" arrow keys to move the right paddle up and down
Play the game and try to score points!
Customization
You can customize the appearance of the game by modifying the sc.bgcolor(), left_pad.color(), right_pad.color(), and hit_ball.color() functions
You can also add more features, such as sound effects or smoother animations, by modifying the move_ball() function
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""
