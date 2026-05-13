import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20 # Size of snake segments and food
FPS_INITIAL = 8 # Starting speed

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 25)
big_font = pygame.font.SysFont('arial', 40)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (BLOCK_SIZE, 0) # Start moving right
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_dir):
        # Prevent snake from reversing into itself
        if (new_dir[0] * -1, new_dir[1] * -1)!= self.direction:
            self.direction = new_dir

    def check_collision(self):
        head_x, head_y = self.body[0]

        # Wall collision
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True

        # Self collision
        if (head_x, head_y) in self.body[1:]:
            return True

        return False

    def draw(self):
        for i, segment in enumerate(self.body):
            color = GREEN if i == 0 else DARK_GREEN # Head brighter than body
            pygame.draw.rect(screen, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE), 1)

class Food:
    def __init__(self, snake_body):
        self.position = self.spawn_food(snake_body)

    def spawn_food(self, snake_body):
        while True:
            x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_speed(speed):
    speed_text = font.render(f"Speed: {speed - FPS_INITIAL + 1}", True, WHITE)
    screen.blit(speed_text, (10, 40))

def game_over_screen(score):
    screen.fill(BLACK)

    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, GRAY)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))

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
                    main() # Restart
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    snake = Snake()
    food = Food(snake.body)
    score = 0
    current_fps = FPS_INITIAL

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -BLOCK_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, BLOCK_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-BLOCK_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((BLOCK_SIZE, 0))

        snake.move()

        # Food collision
        if snake.body[0] == food.position:
            snake.grow = True
            score += 10
            food = Food(snake.body)

            # Increasing speed every 50 points
            if score % 50 == 0:
                current_fps += 1

        # Check collisions
        if snake.check_collision():
            game_over_screen(score)
            return

        # Drawing
        screen.fill(BLACK)
        snake.draw()
        food.draw()
        draw_score(score)
        draw_speed(current_fps)

        # Draw grid lines for better visibility
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(screen, (20, 20, 20), (0, y), (WIDTH, y))

        pygame.display.update()
        clock.tick(current_fps)

if __name__ == "__main__":
    main()