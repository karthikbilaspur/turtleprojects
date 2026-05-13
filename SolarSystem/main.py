import turtle
import math
import random

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(1200, 800)
screen.title("Solar System Simulation")
screen.tracer(0)  # Turn off auto animation for manual updates

# Scale factors - real solar system doesn't fit on screen
DISTANCE_SCALE = 0.8  # AU to pixels
SIZE_SCALE = 0.3      # Real radius scaling, but exaggerated for visibility
TIME_SCALE = 1.0      # Global speed multiplier

# Planet data: name, radius, color, distance in AU, orbital period in Earth days
PLANETS = [
    ("Mercury", 0.38, "gray", 0.39, 88),
    ("Venus", 0.95, "orange", 0.72, 225),
    ("Earth", 1.0, "dodger blue", 1.0, 365),
    ("Mars", 0.53, "red", 1.52, 687),
    ("Jupiter", 11.2, "sandy brown", 5.2, 4333),
    ("Saturn", 9.45, "light goldenrod", 9.5, 10759),
    ("Uranus", 4.0, "light sea green", 19.2, 30687),
    ("Neptune", 3.88, "royal blue", 30.1, 60190),
]

class CelestialBody:
    def __init__(self, name, radius, color, distance_au, period_days):
        self.name = name
        self.radius = max(2, radius * SIZE_SCALE)  # Min size 2px for visibility
        self.color = color
        self.distance = distance_au * DISTANCE_SCALE * 50 + 60  # +60 to clear the sun
        self.period = period_days
        self.angle = random.uniform(0, 360)  # Random starting position
        self.orbit_radius = self.distance

        # Turtle for the planet
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.shapesize(stretch_wYour code draws the planets but they don't actually orbit — they just spin in place. Plus the scales and speeds are way off. 

Here's an enhanced **Solar System Simulation** with proper orbital mechanics, speed controls, and better scaling:

### **solar_system.py**
```python
import turtle
import math

# Screen setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(1200, 800)
screen.title("Solar System Simulation")
screen.tracer(0)  # Turn off auto-update for smooth animation

# Constants
SUN_RADIUS = 20
AU = 50  # 1 AU = 50 pixels, scaled down for screen
SPEED_MULTIPLIER = 1

# Planet data: name, radius, color, distance in AU, orbital period in Earth days
PLANETS = [
    {"name": "Mercury", "radius": 2, "color": "#8C7853", "distance": 0.39, "period": 88},
    {"name": "Venus", "radius": 4, "color": "#FFA500", "distance": 0.72, "period": 225},
    {"name": "Earth", "radius": 4, "color": "#1E90FF", "distance": 1.0, "period": 365},
    {"name": "Mars", "radius": 3, "color": "#FF4500", "distance": 1.52, "period": 687},
    {"name": "Jupiter", "radius": 11, "color": "#D2691E", "distance": 5.2, "period": 4333},
    {"name": "Saturn", "radius": 9, "color": "#F4A460", "distance": 9.5, "period": 10759, "rings": True},
    {"name": "Uranus", "radius": 7, "color": "#40E0D0", "distance": 19.2, "period": 30687},
    {"name": "Neptune", "radius": 7, "color": "#4169E1", "distance": 30.1, "period": 60190},
]

class Planet:
    def __init__(self, data):
        self.name = data["name"]
        self.radius = data["radius"]
        self.color = data["color"]
        self.orbit_radius = data["distance"] * AU
        self.period = data["period"]
        self.has_rings = data.get("rings", False)
        self.angle = random.uniform(0, 360)  # Random starting position

        # Turtle for planet
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.shapesize(self.radius / 10)
        self.t.color(self.color)
        self.t.penup()
        self.t.speed(0)

        # Turtle for orbit path
        self.orbit_t = turtle.Turtle()
        self.orbit_t.hideturtle()
        self.orbit_t.speed(0)
        self.orbit_t.penup()
        self.orbit_t.color("gray20")
        self.orbit_t.goto(0, -self.orbit_radius)
        self.orbit_t.pendown()
        self.orbit_t.circle(self.orbit_radius)

        # Label
        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.color("white")
        self.label.penup()

    def update(self, speed_mult):
        # Realistic orbital speed: angular velocity = 360/period
        # Earth = 1 deg/frame at 1x speed
        angular_vel = (360 / self.period) * speed_mult * 0.5
        self.angle += angular_vel

        x = self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.orbit_radius * math.sin(math.radians(self.angle))
        self.t.goto(x, y)

        # Update label
        self.label.clear()
        self.label.goto(x, y + self.radius + 5)
        self.label.write(self.name, align="center", font=("Arial", 8, "normal"))

        # Draw Saturn's rings
        if self.has_rings:
            self.draw_rings(x, y)

    def draw_rings(self, x, y):
        ring_t = turtle.Turtle()
        ring_t.hideturtle()
        ring_t.speed(0)
        ring_t.penup()
        ring_t.color("#C9B8A0")
        ring_t.width(2)
        ring_t.goto(x, y - self.radius * 1.8)
        ring_t.setheading(0)
        ring_t.pendown()
        ring_t.circle(self.radius * 1.8, 180)
        ring_t.penup()
        ring_t.goto(x, y - self.radius * 1.4)
        ring_t.pendown()
        ring_t.circle(self.radius * 1.4, 180)
        ring_t.clear()  # Prevent turtle buildup

# Draw Sun
sun = turtle.Turtle()
sun.shape("circle")
sun.shapesize(SUN_RADIUS / 10)
sun.color("yellow")
sun.penup()

# Create planets
import random
planets = [Planet(data) for data in PLANETS]

# UI for speed controls
ui = turtle.Turtle()
ui.hideturtle()
ui.color("white")
ui.penup()
ui.goto(-580, 350)

speed_display = turtle.Turtle()
speed_display.hideturtle()
speed_display.color("yellow")
speed_display.penup()

def update_ui():
    ui.clear()
    ui.write(
        f"Speed: {SPEED_MULTIPLIER:.1f}x\n"
        f"Controls: UP/DOWN = Speed | SPACE = Pause | R = Reset\n"
        f"Scale: 1 AU = {AU} pixels | Sizes exaggerated for visibility",
        align="left", font=("Arial", 12, "normal")
    )
    speed_display.clear()
    speed_display.goto(0, -370)
    speed_display.write("Solar System Simulation - Realistic Orbital Periods", 
                       align="center", font=("Arial", 16, "bold"))

update_ui()

# Speed control functions
def increase_speed():
    global SPEED_MULTIPLIER
    SPEED_MULTIPLIER = min(20, SPEED_MULTIPLIER + 0.5)
    update_ui()

def decrease_speed():
    global SPEED_MULTIPLIER
    SPEED_MULTIPLIER = max(0, SPEED_MULTIPLIER - 0.5)
    update_ui()

def toggle_pause():
    global SPEED_MULTIPLIER, paused_speed
    if SPEED_MULTIPLIER > 0:
        paused_speed = SPEED_MULTIPLIER
        SPEED_MULTIPLIER = 0
    else:
        SPEED_MULTIPLIER = paused_speed
    update_ui()

def reset():
    global SPEED_MULTIPLIER
    SPEED_MULTIPLIER = 1
    for planet in planets:
        planet.angle = random.uniform(0, 360)
    update_ui()

paused_speed = 1

# Key bindings
screen.listen()
screen.onkey(increase_speed, "Up")
screen.onkey(decrease_speed, "Down")
screen.onkey(toggle_pause, "space")
screen.onkey(reset, "r")

# Animation loop
def animate():
    for planet in planets:
        planet.update(SPEED_MULTIPLIER)
    
    screen.update()
    screen.ontimer(animate, 16)  # ~60 FPS

animate()
turtle.done()