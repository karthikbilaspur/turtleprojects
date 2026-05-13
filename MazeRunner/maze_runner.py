import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
MAZE_WIDTH, MAZE_HEIGHT = 25, 19 # Odd numbers work best for maze gen
CELL_SIZE = 30
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255) # Player
GREEN = (0, 255, 0) # Goal
GRAY = (40, 40, 40) # Walls
YELLOW = (255, 255, 0) # Timer/Path
RED = (255, 0, 0) # Timer warning

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 30)
big_font = pygame.font.SysFont('arial', 50)

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)] # 1 = wall, 0 = path
        self.generate_maze(1, 1)

    def generate_maze(self, x, y):
        # Randomized DFS maze generation
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        self.grid[y][x] = 0 # Mark current cell as path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and self.grid[ny][nx] == 1:
                # Remove wall between cells
                self.grid[y + dy // 2][x + dx // 2] = 0
                self.generate_maze(nx, ny)

    def draw(self, offset_x, offset_y):
        for y in range(self.height):
            for x in range(self.width):
                rect = (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[y][x] == 1: # Wall
                    pygame.draw.rect(screen, GRAY, rect)
                else: # Path
                    pygame.draw.rect(screen, BLACK, rect)
                    pygame.draw.rect(screen, (20, 20, 20), rect, 1)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y

    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        # Check bounds and walls
        if 0 <= new_x < maze.width and 0 <= new_y < maze.height:
            if maze.grid[new_y][new_x] == 0: # 0 = path
                self.x = new_x
                self.y = new_y

    def draw(self, offset_x, offset_y):
        center_x = offset_x + self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = offset_y + self.y * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(screen, BLUE, (center_x, center_y), CELL_SIZE // 2 - 3)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y

def draw_timer(start_time, maze_x, maze_y):
    elapsed = time.time() - start_time
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)
    timer_color = YELLOW if secs < 50 else RED

    timer_text = font.render(f"Time: {mins:02d}:{secs:02d}", True, timer_color)
    screen.blit(timer_text, (maze_x, 10))
    return elapsed

def win_screen(elapsed_time):
    screen.fill(BLACK)

    win_text = big_font.render("YOU ESCAPED!", True, GREEN)
    time_text = font.render(f"Final Time: {int(elapsed_time // 60):02d}:{int(elapsed_time % 60):02d}", True, WHITE)
    restart_text = font.render("Press R for New Maze | Q to Quit", True, YELLOW)

    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2))
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
                    main() # New maze
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    # Center the maze on screen
    maze_pixel_width = MAZE_WIDTH * CELL_SIZE
    maze_pixel_height = MAZE_HEIGHT * CELL_SIZE
    offset_x = (WIDTH - maze_pixel_width) // 2
    offset_y = (HEIGHT - maze_pixel_height) // 2 + 20

    maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
    player = Player(1, 1) # Start position
    goal_x, goal_y = MAZE_WIDTH - 2, MAZE_HEIGHT - 2 # End position

    # Make sure goal is on a path
    maze.grid[goal_y][goal_x] = 0

    start_time = time.time()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move(0, 1, maze)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move(1, 0, maze)
                elif event.key == pygame.K_r: # Reset maze
                    main()
                    return

        # Check win condition
        if player.x == goal_x and player.y == goal_y:
            elapsed = time.time() - start_time
            win_screen(elapsed)
            return

        # Drawing
        screen.fill(BLACK)
        maze.draw(offset_x, offset_y)

        # Draw goal
        goal_rect = (offset_x + goal_x * CELL_SIZE + 3, offset_y + goal_y * CELL_SIZE + 3,
                     CELL_SIZE - 6, CELL_SIZE - 6)
        pygame.draw.rect(screen, GREEN, goal_rect)

        player.draw(offset_x, offset_y)
        draw_timer(start_time, offset_x, offset_y)

        # Instructions
        inst_text = font.render("WASD/Arrows to Move | R to Reset", True, WHITE)
        screen.blit(inst_text, (WIDTH // 2 - inst_text.get_width() // 2, HEIGHT - 40))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()