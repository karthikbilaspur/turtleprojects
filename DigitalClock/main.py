import time
import datetime as dt
import turtle

class ClockApp:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.bgcolor("green")
        self.screen.setup(width=400, height=250)  # Set screen size
        self.time_turtle = turtle.Turtle()
        self.time_turtle.hideturtle()
        self.box_turtle = turtle.Turtle()
        self.box_turtle.hideturtle()
        self.date_turtle = turtle.Turtle()
        self.date_turtle.hideturtle()
        self.draw_box(200, 70)
        self.draw_date_box(200, 20)
        self.update_time()
        self.update_date()
        self.screen.title("Digital Clock")  # Set screen title

    def draw_box(self, width, height):
        self.box_turtle.pensize(3)
        self.box_turtle.color('black')
        self.box_turtle.penup()
        self.box_turtle.goto(-width/2, height/2)
        self.box_turtle.pendown()
        for _ in range(2):
            self.box_turtle.forward(width)
            self.box_turtle.left(90)
            self.box_turtle.forward(height)
            self.box_turtle.left(90)

    def draw_date_box(self, width, height):
        self.date_turtle.pensize(3)
        self.date_turtle.color('black')
        self.date_turtle.penup()
        self.date_turtle.goto(-width/2, -height/2 - 80)
        self.date_turtle.pendown()
        for _ in range(2):
            self.date_turtle.forward(width)
            self.date_turtle.left(90)
            self.date_turtle.forward(height)
            self.date_turtle.left(90)

    def update_time(self):
        current_time = dt.datetime.now()
        self.time_turtle.clear()
        self.time_turtle.penup()
        self.time_turtle.goto(0, 50)
        self.time_turtle.pendown()
        self.time_turtle.write(current_time.strftime("%H:%M:%S"), font=("Arial Narrow", 35, "bold"))
        self.screen.update()
        self.screen.ontimer(self.update_time, 1000)

    def update_date(self):
        current_date = dt.datetime.now()
        self.date_turtle.clear()
        self.date_turtle.penup()
        self.date_turtle.goto(0, -80)
        self.date_turtle.pendown()
        self.date_turtle.write(current_date.strftime("%A, %B %d, %Y"), font=("Arial Narrow", 18, "bold"))
        self.screen.update()
        self.screen.ontimer(self.update_date, 60000)

    def run(self):
        turtle.done()

def main():
    app = ClockApp()
    app.run()

if __name__ == "__main__":
    main()
    
"""
Digital Clock Application
A simple digital clock application built using Python and the Turtle graphics library.
Features
Displays the current time in hours, minutes, and seconds
Displays the current date
Updates the time and date in real-time
Simple and intuitive user interface
Requirements
Python 3.x
Turtle graphics library (included with Python)
Usage
Run the script using Python (e.g., python digital_clock.py)
The digital clock application will appear on the screen
The time and date will update in real-time
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""
