import pygame
import random
import math
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fractal Tree Generator")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

# Tree parameters
START_X = WIDTH // 2
START_Y = HEIGHT - 50
START_LENGTH = 120
START_ANGLE = -90  # Pointing up
MIN_LENGTH = 5
ANGLE_VARIATION = 25
LENGTH_FACTOR = 0.75

def random_color():
    """Generate vibrant random colors"""
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def random_autumn_color():
    """Generate autumn-like colors for leaves"""
    return random.choice([
        (255, 165, 0),   # Orange
        (255, 140, 0),   # Dark orange
        (255, 69, 0),    # Red orange
        (255, 215, 0),   # Gold
        (218, 165, 32),  # Goldenrod
        (210, 105, 30),  # Chocolate
        (178, 34, 34),   # Firebrick
        (220, 20, 60)    # Crimson
    ])

def draw_branch(x1, y1, angle, length, depth, max_depth):
    """
    Recursively draw tree branches
    
    x1, y1: starting position
    angle: branch angle in degrees
    length: branch length
    depth: current recursion depth
    max_depth: maximum recursion depth
    """
    if length < MIN_LENGTH or depth > max_depth:
        # Draw leaves at the end of branches
        if depth > max_depth - 2:
            leaf_color = random_autumn_color()
            leaf_size = random.randint(3, 7)
            pygame.draw.circle(screen, leaf_color, (int(x1), int(y1)), leaf_size)
        return

    # Calculate end position of branch
    x2 = x1 + math.cos(math.radians(angle)) * length
    y2 = y1 + math.sin(math.radians(angle)) * length

    # Branch thickness decreases with depth
    thickness = max(1, int(length / 12))
    
    # Color: trunk = brown, branches = random colors
    if depth < 2:
        color = BROWN
    else:
        color = random_color()

    # Draw the branch
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)

    # Recursive calls for left and right branches
    new_length = length * LENGTH_FACTOR
    
    # Add some randomness to angles for natural look
    left_angle = angle - ANGLE_VARIATION + random.uniform(-5, 5)
    right_angle = angle + ANGLE_VARIATION + random.uniform(-5, 5)
    
    # Sometimes add a third middle branch for fuller trees
    draw_branch(x2, y2, left_angle, new_length, depth + 1, max_depth)
    draw_branch(x2, y2, right_angle, new_length, depth + 1, max_depth)
    
    # 30% chance for a middle branch
    if random.random() < 0.3:
        mid_angle = angle + random.uniform(-8, 8)
        draw_branch(x2, y2, mid_angle, new_length * 0.9, depth + 1, max_depth)

def draw_instructions():
    text1 = font.render("Press SPACE for new tree | UP/DOWN: depth | LEFT/RIGHT: angle", True, WHITE)
    text2 = font.render("Press C to clear | ESC to quit", True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 35))

def draw_params(depth, angle_var):
    param_text = font.render(f"Depth: {depth} | Angle: {angle_var}°", True, WHITE)
    screen.blit(param_text, (WIDTH - 220, 10))

def main():
    global ANGLE_VARIATION
    max_depth = 10
    
    running = True
    regenerate = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    regenerate = True
                elif event.key == pygame.K_c:
                    screen.fill(BLACK)
                    pygame.display.update()
                elif event.key == pygame.K_UP:
                    max_depth = min(14, max_depth + 1)
                    regenerate = True
                elif event.key == pygame.K_DOWN:
                    max_depth = max(5, max_depth - 1)
                    regenerate = True
                elif event.key == pygame.K_LEFT:
                    ANGLE_VARIATION = max(10, ANGLE_VARIATION - 2)
                    regenerate = True
                elif event.key == pygame.K_RIGHT:
                    ANGLE_VARIATION = min(45, ANGLE_VARIATION + 2)
                    regenerate = True

        if regenerate:
            screen.fill(BLACK)
            
            # Draw ground
            pygame.draw.rect(screen, (20, 40, 20), (0, HEIGHT - 50, WIDTH, 50))
            
            # Generate new tree
            random.seed()  # New random seed each time
            draw_branch(START_X, START_Y, START_ANGLE, START_LENGTH, 0, max_depth)
            
            regenerate = False

        draw_instructions()
        draw_params(max_depth, ANGLE_VARIATION)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()