import pygame
import random
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 28)
big_font = pygame.font.SysFont('arial', 50)

# Colors
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
ROAD_COLOR = (50, 50, 50)

# Road dimensions
ROAD_WIDTH = 300
ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH
LANE_WIDTH = ROAD_WIDTH // 3

# Player car
CAR_WIDTH, CAR_HEIGHT = 40, 70
PLAYER_SPEED = 6

# Obstacles
OBSTACLE_SPAWN_RATE = 25  # Lower = more frequent
OBSTACLE_SPEED_INITIAL = 4

class PlayerCar:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = WIDTH // 2 - CAR_WIDTH // 2
        self.y = HEIGHT - CAR_HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > ROAD_LEFT:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED // 2
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED // 2

    def draw(self):
        # Car body
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=8)
        # Windshield
        windshield = pygame.Rect(self.rect.x + 5, self.rect.y + 10, self.width - 10, 15)
        pygame.draw.rect(screen, (150, 200, 255), windshield, border_radius=3)
        # Wheels
        pygame.draw.rect(screen, BLACK, (self.rect.x - 3, self.rect.y + 10, 6, 15))
        pygame.draw.rect(screen, BLACK, (self.rect.right - 3, self.rect.y + 10, 6, 15))
        pygame.draw.rect(screen, BLACK, (self.rect.x - 3, self.rect.bottom - 25, 6, 15))
        pygame.draw.rect(screen, BLACK, (self.rect.right - 3, self.rect.bottom - 25, 6, 15))

class Obstacle:
    def __init__(self, speed):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        # Spawn in one of 3 lanes
        lane = random.randint(0, 2)
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - CAR_WIDTH // 2
        self.y = -self.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = speed
        self.color = random.choice([RED, GREEN, (255, 165, 0), (128, 0, 128)])

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        # Car body
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        # Windshield
        windshield = pygame.Rect(self.rect.x + 5, self.rect.bottom - 25, self.width - 10, 15)
        pygame.draw.rect(screen, (150, 200, 255), windshield, border_radius=3)
        # Wheels
        pygame.draw.rect(screen, BLACK, (self.rect.x - 3, self.rect.y + 10, 6, 15))
        pygame.draw.rect(screen, BLACK, (self.rect.right - 3, self.rect.y + 10, 6, 15))
        pygame.draw.rect(screen, BLACK, (self.rect.x - 3, self.rect.bottom - 25, 6, 15))
        pygame.draw.rect(screen, BLACK, (self.rect.right - 3, self.rect.bottom - 25, 6, 15))

    def off_screen(self):
        return self.rect.top > HEIGHT

class RoadLine:
    def __init__(self, y):
        self.width = 10
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = y

    def move(self, speed):
        self.y += speed
        if self.y > HEIGHT:
            self.y = -self.height

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

def draw_road():
    # Road background
    pygame.draw.rect(screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
    # Road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5)

def draw_ui(score, speed):
    score_text = font.render(f"Score: {score}", True, WHITE)
    speed_text = font.render(f"Speed: {speed}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 45))

def game_over_screen(score):
    screen.fill(BLACK)

    game_over_text = big_font.render("CRASHED!", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart | Q to Quit", True, YELLOW)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    player = PlayerCar()
    obstacles = []
    road_lines = [RoadLine(y) for y in range(0, HEIGHT, 80)]
    
    score = 0
    obstacle_speed = OBSTACLE_SPEED_INITIAL
    spawn_timer = 0
    
    running = True
    while running:
        screen.fill(GRAY) # Grass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player input
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer >= OBSTACLE_SPAWN_RATE:
            obstacles.append(Obstacle(obstacle_speed))
            spawn_timer = 0

        # Move obstacles + remove off-screen ones
        for obstacle in obstacles[:]:
            obstacle.move()
            if obstacle.off_screen():
                obstacles.remove(obstacle)
                score += 10 # Score for dodging

        # Move road lines
        for line in road_lines:
            line.move(obstacle_speed)

        # Increasing difficulty: speed up every 100 points
        if score > 0 and score % 100 == 0:
            obstacle_speed = OBSTACLE_SPEED_INITIAL + score // 100

        # Collision detection
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                game_over_screen(score)
                return

        # Drawing
        draw_road()
        for line in road_lines:
            line.draw()
        player.draw()
        for obstacle in obstacles:
            obstacle.draw()
        draw_ui(score, obstacle_speed)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()