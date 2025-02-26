import turtle
import math
import random

# Create a new turtle screen and set its background color
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(1200, 800)

# Create a new turtle object for the sun
sun = turtle.Turtle()
sun.shape("circle")
sun.color("yellow")
sun.shapesize(5)
sun.penup()
sun.goto(0, 0)

# Create a new turtle object for the planets
planets = [
    {
        "name": "Mercury",
        "color": "gray",
        "distance": 57.9,
        "size": 0.5,
        "moons": [],
        "diameter": 4879,
        "mass": 3.3022e23,
        "orbital_period": 87.97,
        "rotation_period": 58.65,
    },
    {
        "name": "Venus",
        "color": "orange",
        "distance": 108.2,
        "size": 1.2,
        "moons": [],
        "diameter": 12104,
        "mass": 4.8695e24,
        "orbital_period": 224.7,
        "rotation_period": 243.0,
    },
    {
        "name": "Earth",
        "color": "blue",
        "distance": 149.6,
        "size": 1.5,
        "moons": [
            {"name": "Moon", "distance": 384400, "size": 0.2}
        ],
        "diameter": 12742,
        "mass": 5.9723e24,
        "orbital_period": 365.25,
        "rotation_period": 23.93,
    },
    {
        "name": "Mars",
        "color": "red",
        "distance": 227.9,
        "size": 1,
        "moons": [
            {"name": "Phobos", "distance": 6000, "size": 0.1},
            {"name": "Deimos", "distance": 20000, "size": 0.1},
        ],
        "diameter": 6792,
        "mass": 6.4185e23,
        "orbital_period": 687.0,
        "rotation_period": 24.62,
    },
    {
        "name": "Jupiter",
        "color": "brown",
        "distance": 778.3,
        "size": 4,
        "moons": [
            {"name": "Io", "distance": 426000, "size": 0.3},
            {"name": "Europa", "distance": 671000, "size": 0.3},
            {"name": "Ganymede", "distance": 1070000, "size": 0.4},
            {"name": "Callisto", "distance": 1880000, "size": 0.4},
        ],
        "diameter": 142984,
        "mass": 1.8986e27,
        "orbital_period": 4332.6,
        "rotation_period": 9.93,
    },
    {
        "name": "Saturn",
        "color": "yellow",
        "distance": 1427,
        "size": 3.5,
        "moons": [
            {"name": "Titan", "distance": 1222000, "size": 0.5},
            {"name": "Enceladus", "distance": 238000, "size": 0.2},
        ],
        "diameter": 116460,
        "mass": 5.6846e26,
        "orbital_period": 10759.2,
        "rotation_period": 10.66,
    },
    {
        "name": "Uranus",
        "color": "green",
        "distance": 2870,
        "size": 2.5,
        "moons": [
            {"name": "Titania", "distance": 435000, "size": 0.3},
            {"name": "Oberon", "distance": 583000, "size": 0.3},
        ],
        "diameter": 50724,
        "mass": 8.6810e25,
        "orbital_period": 30687.1,
        "rotation_period": 17.92,
    },
    {
        "name": "Neptune",
        "color": "blue",
        "distance": 4497,
        "size": 2.5,
        "moons": [
            {"name": "Triton", "distance": 354000, "size": 0.3},
        ],
        "diameter": 49528,
        "mass": 1.0243e26,
        "orbital_period": 60190.0,
        "rotation_period": 18.11,
    },
]

# Function to draw a planet
def draw_planet(planet):
    planet_turtle = turtle.Turtle()
    planet_turtle.shape("circle")
    planet_turtle.color(planet["color"])
    planet_turtle.shapesize(planet["size"])
    planet_turtle.penup()
    planet_turtle.goto(planet["distance"], 0)
    planet_turtle.pendown()
    planet_turtle.write(planet["name"], align="center", font=("Arial", 12, "bold"))

    # Draw moons
    for moon in planet["moons"]:
        moon_turtle = turtle.Turtle()
        moon_turtle.shape("circle")
        moon_turtle.color("gray")
        moon_turtle.shapesize(moon["size"])
        moon_turtle.penup()
        moon_turtle.goto(planet["distance"] + moon["distance"], 0)
        moon_turtle.pendown()
        moon_turtle.write(moon["name"], align="center", font=("Arial", 10, "bold"))

# Draw each planet
for planet in planets:
    draw_planet(planet)

# Create a new turtle object for the planet information
info_turtle = turtle.Turtle()
info_turtle.hideturtle()
info_turtle.penup()

# Function to display planet information
def display_info(planet):
    info_turtle.clear()
    info_turtle.goto(-600, 200)
    info_turtle.write(f"Name: {planet['name']}", font=("Arial", 14, "bold"))
    info_turtle.goto(-600, 150)
    info_turtle.write(f"Diameter: {planet['diameter']} km", font=("Arial", 14, "bold"))
    info_turtle.goto(-600, 100)
    info_turtle.write(f"Mass: {planet['mass']} kg", font=("Arial", 14, "bold"))
    info_turtle.goto(-600, 50)
    info_turtle.write(f"Orbital Period: {planet['orbital_period']} days", font=("Arial", 14, "bold"))
    info_turtle.goto(-600, 0)
    info_turtle.write(f"Rotation Period: {planet['rotation_period']} hours", font=("Arial", 14, "bold"))

# Display planet information on click
def on_click(x, y):
    for planet in planets:
        if math.hypot(x - planet["distance"], y) < 20:
            display_info(planet)

# Listen for mouse clicks
screen.onscreenclick(on_click)

# Animate the planets
def animate():
    for planet in planets:
        planet_turtle = turtle.Turtle()
        planet_turtle.shape("circle")
        planet_turtle.color(planet["color"])
        planet_turtle.shapesize(planet["size"])
        planet_turtle.penup()
        planet_turtle.goto(planet["distance"], 0)
        planet_turtle.pendown()
        planet_turtle.circle(planet["distance"])
    screen.ontimer(animate, 100)

animate()

# Keep the window open
turtle.done()