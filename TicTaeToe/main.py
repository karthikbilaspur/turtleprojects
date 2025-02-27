import turtle

# Constants
MIN_LENGTH = 50
MIN_GAP = 10
MAX_LENGTH = 800
MAX_GAP = 100
DEFAULT_LENGTH = 200
DEFAULT_GAP = 20

# Create a screen instance
screen = turtle.Screen()
screen.bgcolor("white")  # Set background color
screen.setup(width=800, height=600)  # Set screen size
screen.title("Square Drawing Tool")  # Set screen title

# Create a turtle instance
my_turtle = turtle.Turtle()
my_turtle.color("green")  # Set turtle color
my_turtle.width(2)  # Set turtle width
my_turtle.speed(2)  # Set turtle speed

# Function to draw a square
def draw_square(length):
    """
    Draw a square with the given length.
    
    Args:
        length (int): The length of the square.
    """
    for _ in range(4):
        my_turtle.forward(length)
        my_turtle.left(90)

# Function to draw inner lines
def draw_inner_lines(length, gap):
    """
    Draw inner lines within the square with the given length and gap.
    
    Args:
        length (int): The length of the square.
        gap (int): The gap between inner lines.
    """
    for i in range(1, int(length / gap)):
        my_turtle.penup()
        my_turtle.goto(0, gap * i)
        my_turtle.pendown()
        my_turtle.forward(length)

        my_turtle.penup()
        my_turtle.goto(gap * i, 0)
        my_turtle.pendown()
        my_turtle.left(90)
        my_turtle.forward(length)
        my_turtle.right(90)

# Function to draw a border
def draw_border(length):
    """
    Draw a border around the square with the given length.
    
    Args:
        length (int): The length of the square.
    """
    my_turtle.penup()
    my_turtle.goto(-length/2, -length/2)
    my_turtle.pendown()
    draw_square(length)

# Function to draw a grid
def draw_grid(length, gap):
    """
    Draw a grid with a border and inner lines with the given length and gap.
    
    Args:
        length (int): The length of the square.
        gap (int): The gap between inner lines.
    """
    draw_border(length)
    draw_inner_lines(length, gap)

# Function to get user input
def get_user_input():
    while True:
        try:
            length = int(screen.textinput("Enter length", f"Enter the length of the square ({MIN_LENGTH}-{MAX_LENGTH}) or press Cancel to use default ({DEFAULT_LENGTH})"))
            if length is None:
                length = DEFAULT_LENGTH
                break
            elif MIN_LENGTH <= length <= MAX_LENGTH:
                break
            else:
                print("Please enter a value within the valid range.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            gap = int(screen.textinput("Enter gap", f"Enter the gap between inner lines ({MIN_GAP}-{MAX_GAP}) or press Cancel to use default ({DEFAULT_GAP})"))
            if gap is None:
                gap = DEFAULT_GAP
                break
            elif MIN_GAP <= gap <= MAX_GAP:
                break
            else:
                print("Please enter a value within the valid range.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    return length, gap

# Main function
def main():
    length, gap = get_user_input()
    draw_grid(length, gap)

    # Add text label
    text_turtle = turtle.Turtle()
    text_turtle.hideturtle()
    text_turtle.penup()
    text_turtle.goto(0, -150)
    text_turtle.pendown()
    text_turtle.write("Square Drawing Tool", font=("Arial", 24, "bold"))

    # Keep the window open
    turtle.done()

# Call the main function
if __name__ == "__main__":
    main()