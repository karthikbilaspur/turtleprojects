import time
import datetime as dt
import turtle
import logging
import pytz
from babel.dates import format_date
from babel.numbers import format_decimal

# Define constants
WIDTH = 400
HEIGHT = 250
BOX_WIDTH = 200
BOX_HEIGHT = 70
DATE_BOX_WIDTH = 200
DATE_BOX_HEIGHT = 20
FONT = ("Arial Narrow", 35, "bold")
DATE_FONT = ("Arial Narrow", 18, "bold")
TIME_ZONE = "Asia/Kolkata"  # Default time zone
LANGUAGE = "en"  # Default language
COUNTRY = "US"  # Default country

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ClockApp:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=WIDTH, height=HEIGHT)  # Set screen size
        self.time_turtle = turtle.Turtle()
        self.time_turtle.hideturtle()
        self.box_turtle = turtle.Turtle()
        self.box_turtle.hideturtle()
        self.date_turtle = turtle.Turtle()
        self.date_turtle.hideturtle()
        self.alarm_turtle = turtle.Turtle()
        self.alarm_turtle.hideturtle()
        self.draw_box(BOX_WIDTH, BOX_HEIGHT)
        self.draw_date_box(DATE_BOX_WIDTH, DATE_BOX_HEIGHT)
        self.update_time()
        self.update_date()
        self.screen.title("Digital Clock")  # Set screen title
        logging.info("Clock application started")
        self.alarm_set = False

        # Create alarm button
        self.alarm_button = turtle.Turtle()
        self.alarm_button.hideturtle()
        self.alarm_button.penup()
        self.alarm_button.goto(-100, -150)
        self.alarm_button.pendown()
        self.alarm_button.write("Alarm", font=("Arial", 18, "bold"))
        self.alarm_button.penup()
        self.alarm_button.goto(-100, -180)
        self.alarm_button.pendown()
        self.alarm_button.write("Click to set alarm", font=("Arial", 12, "normal"))

        # Create customize button
        self.customize_button = turtle.Turtle()
        self.customize_button.hideturtle()
        self.customize_button.penup()
        self.customize_button.goto(50, -150)
        self.customize_button.pendown()
        self.customize_button.write("Customize", font=("Arial", 18, "bold"))
        self.customize_button.penup()
        self.customize_button.goto(50, -180)
        self.customize_button.pendown()
        self.customize_button.write("Click to customize clock", font=("Arial", 12, "normal"))

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
        try:
            current_time = dt.datetime.now(pytz.timezone(TIME_ZONE))
            self.time_turtle.clear()
            self.time_turtle.penup()
            self.time_turtle.goto(0, 50)
            self.time_turtle.pendown()
            self.time_turtle.write(current_time.strftime("%H:%M:%S"), font=FONT)
            self.screen.update()
            self.screen.ontimer(self.update_time, 1000)
        except Exception as e:
            logging.error(f"Error updating time: {e}")

    def update_date(self):
        try:
            current_date = dt.datetime.now(pytz.timezone(TIME_ZONE))
            self.date_turtle.clear()
            self.date_turtle.penup()
            self.date_turtle.goto(0, -80)
            self.date_turtle.pendown()
            formatted_date = format_date(current_date, locale=LANGUAGE)
            self.date_turtle.write(formatted_date, font=DATE_FONT)
            self.screen.update
                        self.screen.ontimer(self.update_date, 60000)
        except Exception as e:
            logging.error(f"Error updating date: {e}")

    def set_alarm(self):
        try:
            alarm_time = self.alarm_turtle.textinput("Alarm", "Enter alarm time (HH:MM:SS)")
            if alarm_time:
                self.alarm_set = True
                logging.info(f"Alarm set for {alarm_time}")
        except Exception as e:
            logging.error(f"Error setting alarm: {e}")

    def check_alarm(self):
        try:
            if self.alarm_set:
                current_time = dt.datetime.now(pytz.timezone(TIME_ZONE))
                alarm_time = dt.datetime.strptime(self.alarm_turtle.textinput("Alarm", "Enter alarm time (HH:MM:SS)"), "%H:%M:%S")
                if current_time.hour == alarm_time.hour and current_time.minute == alarm_time.minute and current_time.second == alarm_time.second:
                    logging.info("Wake up!")
                    self.alarm_set = False
        except Exception as e:
            logging.error(f"Error checking alarm: {e}")
        self.screen.ontimer(self.check_alarm, 1000)

    def customize_clock(self):
        try:
            self.customize_turtle = turtle.Turtle()
            self.customize_turtle.hideturtle()
            self.customize_turtle.penup()
            self.customize_turtle.goto(0, -200)
            self.customize_turtle.pendown()
            self.customize_turtle.write("Customize clock", font=("Arial", 18, "bold"))
            self.customize_turtle.penup()
            self.customize_turtle.goto(0, -220)
            self.customize_turtle.pendown()
            self.customize_turtle.write("Change time zone, language, or country", font=("Arial", 12, "normal"))
        except Exception as e:
            logging.error(f"Error customizing clock: {e}")

    def run(self):
        turtle.done()

def main():
    app = ClockApp()
    app.run()

if __name__ == "__main__":
    main()