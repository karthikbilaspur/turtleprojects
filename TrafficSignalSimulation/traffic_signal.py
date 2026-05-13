import pygame
import random
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Signal Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
big_font = pygame.font.SysFont('arial', 32)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
ROAD_COLOR = (60, 60, 60)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRASS = (20, 80, 20)
BUILDING = (100, 100, 120)

# Intersection setup
ROAD_WIDTH = 120
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
INTERSECTION_SIZE = ROAD_WIDTH

# Car properties
CAR_WIDTH, CAR_HEIGHT = 35, 20
CAR_SPEED = 2.5
SPAWN_RATE = 90 # Lower = more cars

# Traffic light states and timing
LIGHT_STATES = ['GREEN', 'YELLOW', 'RED']
STATE_DURATIONS = {'GREEN': 300, 'YELLOW': 60, 'RED': 360} # frames at 60 FPS: 5s, 1s, 6s

class TrafficLight:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 'NS' or 'EW'
        self.state = 'RED'
        self.timer = 0
        self.width = 30
        self.height = 70

    def update(self):
        self.timer += 1
        if self.timer >= STATE_DURATIONS[self.state]:
            self.timer = 0
            # Cycle: GREEN -> YELLOW -> RED
            if self.state == 'GREEN':
                self.state = 'YELLOW'
            elif self.state == 'YELLOW':
                self.state = 'RED'
            elif self.state == 'RED':
                self.state = 'GREEN'

    def draw(self):
        # Light housing
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

        # Lights
        lights = [
            (self.y + 10, RED),     # Top - Red
            (self.y + 30, YELLOW),  # Middle - Yellow
            (self.y + 50, GREEN)    # Bottom - Green
        ]

        for y_pos, color in lights:
            active = False
            if color == RED and self.state == 'RED':
                active = True
            elif color == YELLOW and self.state == 'YELLOW':
                active = True
            elif color == GREEN and self.state == 'GREEN':
                active = True

            if active:
                pygame.draw.circle(screen, color, (self.x + self.width // 2, y_pos), 8)
                # Glow effect
                glow = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*color, 100), (10, 10), 12)
                screen.blit(glow, (self.x + self.width // 2 - 10, y_pos - 10))
            else:
                pygame.draw.circle(screen, (40, 40, 40), (self.x + self.width // 2, y_pos), 8)

class Car:
    def __init__(self, direction):
        self.direction = direction  # 'N', 'S', 'E', 'W'
        self.color = random.choice([(200, 0, 0), (0, 0, 200), (0, 150, 0), 
                                    (200, 200, 0), (200, 0, 200), (0, 200, 200),
                                    (255, 165, 0), (128, 0, 128)])
        self.stopped = False

        # Set start position and lane based on direction
        if direction == 'N': # Going South
            self.x = CENTER_X - ROAD_WIDTH // 4
            self.y = -CAR_HEIGHT
            self.width = CAR_WIDTH
            self.height = CAR_HEIGHT
        elif direction == 'S': # Going North
            self.x = CENTER_X + ROAD_WIDTH // 4 - CAR_WIDTH
            self.y = HEIGHT
            self.width = CAR_WIDTH
            self.height = CAR_HEIGHT
        elif direction == 'E': # Going West
            self.x = WIDTH
            self.y = CENTER_Y - ROAD_WIDTH // 4 - CAR_HEIGHT
            self.width = CAR_HEIGHT # Swap for horizontal
            self.height = CAR_WIDTH
        elif direction == 'W': # Going East
            self.x = -CAR_HEIGHT
            self.y = CENTER_Y + ROAD_WIDTH // 4
            self.width = CAR_HEIGHT
            self.height = CAR_WIDTH

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, ns_light, ew_light, cars):
        self.stopped = False

        # Stop line positions
        stop_lines = {
            'N': CENTER_Y - INTERSECTION_SIZE // 2 - CAR_HEIGHT - 5,
            'S': CENTER_Y + INTERSECTION_SIZE // 2 + 5,
            'E': CENTER_X + INTERSECTION_SIZE // 2 + 5,
            'W': CENTER_X - INTERSECTION_SIZE // 2 - CAR_HEIGHT - 5
        }

        # Check traffic lights
        if self.direction in ['N', 'S']: # NS traffic
            light = ns_light
        else: # EW traffic
            light = ew_light

        stop_line = stop_lines[self.direction]

        # Check if we should stop at red/yellow light
        should_stop = False
        if light.state in ['RED', 'YELLOW']:
            if self.direction == 'N' and self.y <= stop_line and self.y + CAR_HEIGHT >= stop_line - 50:
                should_stop = True
            elif self.direction == 'S' and self.y >= stop_line and self.y <= stop_line + 50:
                should_stop = True
            elif self.direction == 'E' and self.x >= stop_line and self.x <= stop_line + 50:
                should_stop = True
            elif self.direction == 'W' and self.x <= stop_line and self.x + CAR_HEIGHT >= stop_line - 50:
                should_stop = True

        # Check for car in front
        for other in cars:
            if other == self:
                continue
            if self.direction == other.direction:
                if self.direction == 'N' and other.y > self.y and other.y - self.y < CAR_HEIGHT + 10:
                    should_stop = True
                elif self.direction == 'S' and other.y < self.y and self.y - other.y < CAR_HEIGHT + 10:
                    should_stop = True
                elif self.direction == 'E' and other.x < self.x and self.x - other.x < CAR_HEIGHT + 10:
                    should_stop = True
                elif self.direction == 'W' and other.x > self.x and other.x - self.x < CAR_HEIGHT + 10:
                    should_stop = True

        if not should_stop:
            if self.direction == 'N':
                self.y += CAR_SPEED
            elif self.direction == 'S':
                self.y -= CAR_SPEED
            elif self.direction == 'E':
                self.x -= CAR_SPEED
            elif self.direction == 'W':
                self.x += CAR_SPEED
        else:
            self.stopped = True

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        # Car body
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        
        # Windshield
        if self.direction in ['N', 'S']:
            windshield = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.width - 6, 8)
        else:
            windshield = pygame.Rect(self.rect.x + 3, self.rect.y + 3, 8, self.height - 6)
        pygame.draw.rect(screen, (150, 200, 255), windshield, border_radius=2)

        # Brake lights if stopped
        if self.stopped:
            if self.direction == 'N':
                pygame.draw.rect(screen, RED, (self.rect.x + 2, self.rect.bottom - 4, 6, 3))
                pygame.draw.rect(screen, RED, (self.rect.right - 8, self.rect.bottom - 4, 6, 3))
            elif self.direction == 'S':
                pygame.draw.rect(screen, RED, (self.rect.x + 2, self.rect.y + 1, 6, 3))
                pygame.draw.rect(screen, RED, (self.rect.right - 8, self.rect.y + 1, 6, 3))

    def off_screen(self):
        return (self.y > HEIGHT + 50 or self.y < -50 or 
                self.x > WIDTH + 50 or self.x < -50)

def draw_road_graphics():
    # Grass background
    screen.fill(GRASS)

    # Roads
    # Vertical road
    pygame.draw.rect(screen, ROAD_COLOR, 
                    (CENTER_X - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))
    # Horizontal road
    pygame.draw.rect(screen, ROAD_COLOR, 
                    (0, CENTER_Y - ROAD_WIDTH // 2, WIDTH, ROAD_WIDTH))

    # Lane dividers - dashed yellow lines
    for y in range(0, HEIGHT, 40):
        if y < CENTER_Y - INTERSECTION_SIZE // 2 or y > CENTER_Y + INTERSECTION_SIZE // 2:
            pygame.draw.rect(screen, YELLOW, (CENTER_X - 2, y, 4, 20))
    
    for x in range(0, WIDTH, 40):
        if x < CENTER_X - INTERSECTION_SIZE // 2 or x > CENTER_X + INTERSECTION_SIZE // 2:
            pygame.draw.rect(screen, YELLOW, (x, CENTER_Y - 2, 20, 4))

    # Stop lines - white
    pygame.draw.line(screen, WHITE, 
                    (CENTER_X - ROAD_WIDTH // 2, CENTER_Y - INTERSECTION_SIZE // 2 - 5),
                    (CENTER_X + ROAD_WIDTH // 2, CENTER_Y - INTERSECTION_SIZE // 2 - 5), 3)
    pygame.draw.line(screen, WHITE,
                    (CENTER_X - ROAD_WIDTH // 2, CENTER_Y + INTERSECTION_SIZE // 2 + 5),
                    (CENTER_X + ROAD_WIDTH // 2, CENTER_Y + INTERSECTION_SIZE // 2 + 5), 3)
    pygame.draw.line(screen, WHITE,
                    (CENTER_X - INTERSECTION_SIZE // 2 - 5, CENTER_Y - ROAD_WIDTH // 2),
                    (CENTER_X - INTERSECTION_SIZE // 2 - 5, CENTER_Y + ROAD_WIDTH // 2), 3)
    pygame.draw.line(screen, WHITE,
                    (CENTER_X + INTERSECTION_SIZE // 2 + 5, CENTER_Y - ROAD_WIDTH // 2),
                    (CENTER_X + INTERSECTION_SIZE // 2 + 5, CENTER_Y + ROAD_WIDTH // 2), 3)

    # Simple buildings for scenery
    buildings = [
        (50, 50, 80, 100), (200, 80, 60, 120), (WIDTH - 150, 60, 90, 110),
        (70, HEIGHT - 180, 100, 130), (WIDTH - 200, HEIGHT - 160, 120, 100)
    ]
    for bx, by, bw, bh in buildings:
        pygame.draw.rect(screen, BUILDING, (bx, by, bw, bh))
        # Windows
        for wy in range(by + 10, by + bh - 10, 20):
            for wx in range(bx + 10, bx + bw - 10, 15):
                pygame.draw.rect(screen, YELLOW, (wx, wy, 8, 12))

def main():
    # Create traffic lights - NS and EW work opposite each other
    ns_light = TrafficLight(CENTER_X - 80, CENTER_Y - 150, 'NS')
    ew_light = TrafficLight(CENTER_X + 50, CENTER_Y - 150, 'EW')
    ns_light.state = 'GREEN' # Start NS green
    ew_light.state = 'RED'   # Start EW red

    cars = []
    spawn_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update traffic lights
        ns_light.update()
        ew_light.update()

        # Sync lights: when one goes yellow, the other stays red
        # When one turns red, the other turns green after a delay
        if ns_light.state == 'YELLOW' and ns_light.timer == 0:
            ew_light.state = 'RED'
            ew_light.timer = 0
        elif ns_light.state == 'RED' and ns_light.timer == 0:
            ew_light.state = 'GREEN'
            ew_light.timer = 0
        elif ew_light.state == 'YELLOW' and ew_light.timer == 0:
            ns_light.state = 'RED'
            ns_light.timer = 0
        elif ew_light.state == 'RED' and ew_light.timer == 0:
            ns_light.state = 'GREEN'
            ns_light.timer = 0

        # Spawn cars
        spawn_timer += 1
        if spawn_timer >= SPAWN_RATE:
            direction = random.choice(['N', 'S', 'E', 'W'])
            cars.append(Car(direction))
            spawn_timer = 0

        # Update cars
        for car in cars[:]:
            car.move(ns_light, ew_light, cars)
            if car.off_screen():
                cars.remove(car)

        # Drawing
        draw_road_graphics()
        ns_light.draw()
        ew_light.draw()
        
        for car in cars:
            car.draw()

        # UI
        ns_text = font.render(f"NS Light: {ns_light.state}", True, WHITE)
        ew_text = font.render(f"EW Light: {ew_light.state}", True, WHITE)
        car_text = font.render(f"Cars: {len(cars)}", True, WHITE)
        
        screen.blit(ns_text, (10, 10))
        screen.blit(ew_text, (10, 35))
        screen.blit(car_text, (10, 60))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()