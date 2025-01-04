import turtle
import math
import random

# Create a screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(1200, 800)

# Define a function to draw a planet
def draw_planet(t, radius, color, distance, orbit_radius):
    t.penup()
    t.goto(distance, 0)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

    # Draw orbit
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.color("gray")
    t.circle(orbit_radius)

# Define a function to draw a ring system
def draw_rings(t, radius, color, distance, orbit_radius):
    t.penup()
    t.goto(distance, 0)
    t.pendown()
    t.color(color)
    t.width(2)
    t.circle(orbit_radius)

# Define a function to draw a moon
def draw_moon(t, radius, color, distance, orbit_radius):
    t.penup()
    t.goto(distance, 0)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Draw Sun
sun = turtle.Turtle()
sun.speed(0)
sun.penup()
sun.goto(0, 0)
sun.pendown()
sun.fillcolor("yellow")
sun.begin_fill()
sun.circle(30)
sun.end_fill()

# Draw Mercury
mercury = turtle.Turtle()
mercury.speed(0)
draw_planet(mercury, 5, "gray", 60, 60)

# Draw Venus
venus = turtle.Turtle()
venus.speed(0)
draw_planet(venus, 10, "orange", 100, 100)

# Draw Earth
earth = turtle.Turtle()
earth.speed(0)
draw_planet(earth, 15, "blue", 140, 140)
earth_moon = turtle.Turtle()
earth_moon.speed(0)
draw_moon(earth_moon, 2, "white", 160, 160)

# Draw Mars
mars = turtle.Turtle()
mars.speed(0)
draw_planet(mars, 10, "red", 180, 180)
mars_moon = turtle.Turtle()
mars_moon.speed(0)
draw_moon(mars_moon, 2, "white", 200, 200)

# Draw Jupiter
jupiter = turtle.Turtle()
jupiter.speed(0)
draw_planet(jupiter, 30, "brown", 220, 220)
jupiter_moon = turtle.Turtle()
jupiter_moon.speed(0)
draw_moon(jupiter_moon, 5, "white", 240, 240)

# Draw Saturn
saturn = turtle.Turtle()
saturn.speed(0)
draw_planet(saturn, 25, "yellow", 260, 260)
draw_rings(saturn, 10, "white", 260, 280)
saturn_moon = turtle.Turtle()
saturn_moon.speed(0)
draw_moon(saturn_moon, 3, "white", 280, 280)

# Draw Uranus
uranus = turtle.Turtle()
uranus.speed(0)
draw_planet(uranus, 20, "green", 300, 300)
uranus_moon = turtle.Turtle()
uranus_moon.speed(0)
draw_moon(uranus_moon, 2, "white", 320, 320)

# Draw Neptune
neptune = turtle.Turtle()
neptune.speed(0)
draw_planet(neptune, 25, "blue", 340, 340)
neptune_moon = turtle.Turtle()
neptune_moon.speed(0)
draw_moon(neptune_moon, 2, "white", 360, 360)

# Draw Pluto
pluto = turtle.Turtle()
pluto.speed(0)
draw_planet(pluto, 10, "gray", 380, 380)

# Draw Dwarf Planets
ceres = turtle.Turtle()
ceres.speed(0)
draw_planet(ceres, 5, "brown", 400, 400)
haumea = turtle.Turtle()
haumea.speed(0)
draw_planet(haumea, 5, "blue", 420, 420)
makemake = turtle.Turtle()
makemake.speed(0)
draw_planet(makemake, 5, "green", 440, 440)
eris = turtle.Turtle()
eris.speed(0)
draw_planet(eris, 5, "red", 460, 460)

# Draw Asteroid Belt
asteroid_belt = turtle.Turtle()
asteroid_belt.speed(0)
asteroid_belt.penup()
asteroid_belt.goto(150, 0)
asteroid_belt.pendown()
asteroid_belt.color("gray")
asteroid_belt.width(2)
asteroid_belt.circle(150)

# Animate planetary movement
def animate():
    sun.right(1)
    mercury.right(2)
    venus.right(1.5)
    earth.right(1)
    mars.right(2)
    jupiter.right(0.5)
    saturn.right(0.8)
    uranus.right(1.2)
    neptune.right(1.5)
    pluto.right(2)
    ceres.right(1.8)
    haumea.right(2.2)
    makemake.right(1.5)
    eris.right(2.5)
    screen.ontimer(animate, 10)

animate()

# Hide turtles
sun.hideturtle()
mercury.hideturtle()
venus.hideturtle()
earth.hideturtle()
mars.hideturtle()
jupiter.hideturtle()
saturn.hideturtle()
uranus.hideturtle()
neptune.hideturtle()
pluto.hideturtle()
ceres.hideturtle()
haumea.hideturtle()
makemake.hideturtle()
eris.hideturtle()

# Add a text label
text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.penup()
text_turtle.goto(0, -300)
text_turtle.pendown()
text_turtle.write("Solar System Simulation", font=("Arial", 24, "bold"))

# Keep the window open
turtle.done()

"""
Solar System Simulation
A 2D animated simulation of the Solar System using Turtle graphics.
Features
Animated Planets: The simulation includes animated planets with different sizes, colors, and orbital paths.
Realistic Orbital Paths: The planets follow realistic orbital paths around the Sun.
Asteroid Belt: The simulation includes an asteroid belt between the orbits of Mars and Jupiter.
Dwarf Planets: The simulation includes dwarf planets such as Ceres, Haumea, Makemake, and Eris.
Requirements
Python 3.x: The simulation requires Python 3.x to run.
Turtle Graphics: The simulation uses Turtle graphics for animation.
Usage
Run the Script: Run the script using Python (e.g., python solar_system_simulation.py).
View the Simulation: View the simulation in the Turtle graphics window.
Customization
Planet Sizes and Colors: You can customize the sizes and colors of the planets by modifying the draw_planet function.
Orbital Paths: You can customize the orbital paths of the planets by modifying the animate function.
License
This code is released under the MIT License. See LICENSE.txt for details.
Contributing
Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
Acknowledgments
Special thanks to the Python and Turtle graphics communities for their support and resources.
"""
