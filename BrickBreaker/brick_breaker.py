import pygame
import sys
import math

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 28)
big_font = pygame.font.SysFont('arial', 48)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (200, 0, 200)
CYAN = (0, 255, 255)

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
PADDLE_SPEED = 8

# Ball
BALL_RADIUS = 8
BALL_SPEED = 5

# Bricks
BRICK_WIDTH, BRICK_HEIGHT = 75, 25
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_GAP = 5

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = PADDLE_SPEED

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=5)

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.reset()
        self.speed = BALL_SPEED

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.vel_x = random.choice([-1, 1]) * BALL_SPEED
        self.vel_y = -BALL_SPEED
        self.launched = False

    def move(self):
        if self.launched:
            self.x += self.vel_x
            self.y += self.vel_y

            # Wall bounce logic
            if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
                self.vel_x *= -1
            if self.y - self.radius <= 0:
                self.vel_y *= -1

    def paddle_collision(self, paddle):
        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                                self.radius * 2, self.radius * 2)
        
        if ball_rect.colliderect(paddle.rect) and self.vel_y > 0:
            # Paddle physics: angle depends on where ball hits paddle
            hit_pos = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
            hit_pos = max(-1, min(1, hit_pos)) # Clamp between -1 and 1
            
            angle = hit_pos * math.pi / 3  # Max 60 degree angle
            speed = math.sqrt(self.vel_x**2 + self.vel_y**2)
            
            self.vel_x = speed * math.sin(angle)
            self.vel_y = -speed * math.cos(angle)
            
            # Prevent ball from getting stuck in paddle
            self.y = paddle.rect.top - self.radius

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def off_screen(self):
        return self.y - self.radius > HEIGHT

class Brick:
    def __init__(self, x, y, color, points):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.points = points
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
            pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=3)

def create_level(level):
    bricks = []
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, PURPLE]
    points = [60, 50, 40, 30, 20, 10] # Top rows worth more
    
    rows = min(BRICK_ROWS, 3 + level) # More rows as level increases
    
    for row in range(rows):
        for col in range(BRICK_COLS):
            x = 50 + col * (BRICK_WIDTH + BRICK_GAP)
            y = 60 + row * (BRICK_HEIGHT + BRICK_GAP)
            color = colors[row % len(colors)]
            point_val = points[row % len(points)]
            bricks.append(Brick(x, y, color, point_val))
    
    return bricks

def ball_brick_collision(ball, bricks):
    ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius,
                            ball.radius * 2, ball.radius * 2)
    
    for brick in bricks:
        if brick.alive and ball_rect.colliderect(brick.rect):
            brick.alive = False
            
            # Determine bounce direction based on collision side
            overlap_left = ball_rect.right - brick.rect.left
            overlap_right = brick.rect.right - ball_rect.left
            overlap_top = ball_rect.bottom - brick.rect.top
            overlap_bottom = brick.rect.bottom - ball_rect.top
            
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
            
            if min_overlap == overlap_left or min_overlap == overlap_right:
                ball.vel_x *= -1
            else:
                ball.vel_y *= -1
            
            return brick.points
    return 0

def draw_ui(score, lives, level):
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(level_text, (WIDTH // 2 - 40, 10))

def level_complete_screen(level, score):
    screen.fill(BLACK)
    complete_text = big_font.render(f"Level {level} Complete!", True, GREEN)
    score_text = font.render(f"Score: {score}", True, WHITE)
    next_text = font.render("Press SPACE for Next Level", True, YELLOW)
    
    screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2 + 60))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart | Q to Quit", True, YELLOW)
    
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
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    paddle = Paddle()
    ball = Ball()
    level = 1
    bricks = create_level(level)
    score = 0
    lives = 3
    
    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball.launched:
                    ball.launched = True
        
        # Player input
        keys = pygame.key.get_pressed()
        paddle.move(keys)
        
        # Ball follows paddle before launch
        if not ball.launched:
            ball.x = paddle.rect.centerx
            ball.y = paddle.rect.top - ball.radius
        
        ball.move()
        
        # Paddle physics: ball angle changes based on hit position
        ball.paddle_collision(paddle)
        
        # Ball bounce logic on bricks
        points = ball_brick_collision(ball, bricks)
        score += points
        
        # Ball falls off screen
        if ball.off_screen():
            lives -= 1
            if lives <= 0:
                game_over_screen(score)
                return
            else:
                ball.reset()
        
        # Check level complete
        if all(not brick.alive for brick in bricks):
            level_complete_screen(level, score)
            level += 1
            bricks = create_level(level)
            ball.reset()
            ball.speed = BALL_SPEED + level * 0.5 # Ball gets faster each level
        
        # Drawing
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
        draw_ui(score, lives, level)
        
        if not ball.launched:
            launch_text = font.render("Press SPACE to Launch", True, YELLOW)
            screen.blit(launch_text, (WIDTH // 2 - launch_text.get_width() // 2, HEIGHT - 100))
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    import random # Needed for ball.reset()
    main()