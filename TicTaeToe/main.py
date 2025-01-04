import turtle

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
    for i in range(3):
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
    length = int(screen.textinput("Enter length", "Enter the length of the square"))
    gap = int(screen.textinput("Enter gap", "Enter the gap between inner lines"))
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
    
"""
Square Drawing Tool
A simple Turtle graphics project that draws a square grid with user-defined length and gap.
Features
User-Defined Length and Gap: The user can input the length and gap of the square grid.
Animated Drawing: The square grid is drawn animatedly using Turtle graphics.
Customizable: The user can customize the length and gap of the square grid.
Requirements
Python 3.x: The project requires Python 3.x to run.
Turtle Graphics: The project uses Turtle graphics for animation.
Usage
Run the Script: Run the script using Python (e.g., python square_drawing_tool.py).
Enter Length and Gap: Enter the length and gap of the square grid when prompted.
View the Animation: View the animated drawing of the square grid.
Customization
Length and Gap: You can customize the length and gap of the square grid by entering different values when prompted.
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""
