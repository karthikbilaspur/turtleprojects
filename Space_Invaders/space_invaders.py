import pygame
import random
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)
big_font = pygame.font.SysFont('arial', 48)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)

# Player
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 30
PLAYER_SPEED = 5
BULLET_SPEED = 7
PLAYER_COOLDOWN = 300  # ms between shots

# Enemy
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30
ENEMY_ROWS, ENEMY_COLS = 4, 8
ENEMY_X_GAP, ENEMY_Y_GAP = 60, 50
ENEMY_SPEED = 1
ENEMY_DROP = 20
ENEMY_BULLET_SPEED = 4
ENEMY_SHOOT_CHANCE = 0.002  # Per frame per enemy

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, 
                                HEIGHT - PLAYER_HEIGHT - 10, 
                                PLAYER_WIDTH, PLAYER_HEIGHT)
        self.last_shot = 0
        self.lives = 3

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > PLAYER_COOLDOWN:
            self.last_shot = now
            return Bullet(self.rect.centerx, self.rect.top, -BULLET_SPEED, GREEN)
        return None

    def draw(self):
        # Simple triangle ship
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(screen, BLUE, points)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, RED, self.rect)
            # Eyes
            pygame.draw.rect(screen, WHITE, (self.rect.x + 8, self.rect.y + 8, 6, 6))
            pygame.draw.rect(screen, WHITE, (self.rect.right - 14, self.rect.y + 8, 6, 6))

class Bullet:
    def __init__(self, x, y, speed, color):
        self.rect = pygame.Rect(x - 2, y, 4, 12)
        self.speed = speed
        self.color = color

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def off_screen(self):
        return self.rect.bottom < 0 or self.rect.top > HEIGHT

class EnemyGroup:
    def __init__(self):
        self.enemies = []
        self.direction = 1  # 1 = right, -1 = left
        self.create_enemies()

    def create_enemies(self):
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                x = 80 + col * ENEMY_X_GAP
                y = 50 + row * ENEMY_Y_GAP
                self.enemies.append(Enemy(x, y))

    def move(self):
        # Check if any enemy hits screen edge
        move_down = False
        for enemy in self.enemies:
            if enemy.alive:
                if (enemy.rect.right >= WIDTH and self.direction == 1) or \
                   (enemy.rect.left <= 0 and self.direction == -1):
                    move_down = True
                    break

        if move_down:
            self.direction *= -1
            for enemy in self.enemies:
                if enemy.alive:
                    enemy.rect.y += ENEMY_DROP
        else:
            for enemy in self.enemies:
                if enemy.alive:
                    enemy.rect.x += ENEMY_SPEED * self.direction

    def shoot(self):
        bullets = []
        for enemy in self.enemies:
            if enemy.alive and random.random() < ENEMY_SHOOT_CHANCE:
                bullets.append(Bullet(enemy.rect.centerx, enemy.rect.bottom, 
                                    ENEMY_BULLET_SPEED, YELLOW))
        return bullets

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

    def all_dead(self):
        return all(not e.alive for e in self.enemies)

    def reached_bottom(self):
        for enemy in self.enemies:
            if enemy.alive and enemy.rect.bottom >= HEIGHT - 60:
                return True
        return False

def draw_ui(score, lives):
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

def game_over_screen(score, win):
    screen.fill(BLACK)
    
    if win:
        title_text = big_font.render("YOU WIN!", True, GREEN)
    else:
        title_text = big_font.render("GAME OVER", True, RED)
        
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 60))
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
    player = Player()
    enemy_group = EnemyGroup()
    player_bullets = []
    enemy_bullets = []
    score = 0

    running = True
    while running:
        screen.fill(BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player input
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE]:
            bullet = player.shoot()
            if bullet:
                player_bullets.append(bullet)

        # Move enemies + enemy shooting
        enemy_group.move()
        enemy_bullets.extend(enemy_group.shoot())

        # Move bullets
        for bullet in player_bullets[:]:
            bullet.move()
            if bullet.off_screen():
                player_bullets.remove(bullet)

        for bullet in enemy_bullets[:]:
            bullet.move()
            if bullet.off_screen():
                enemy_bullets.remove(bullet)

        # Bullet collision: Player bullets vs Enemies
        for bullet in player_bullets[:]:
            for enemy in enemy_group.enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.alive = False
                    player_bullets.remove(bullet)
                    score += 10
                    break

        # Bullet collision: Enemy bullets vs Player
        for bullet in enemy_bullets[:]:
            if bullet.rect.colliderect(player.rect):
                enemy_bullets.remove(bullet)
                player.lives -= 1
                if player.lives <= 0:
                    game_over_screen(score, win=False)
                    return

        # Win condition
        if enemy_group.all_dead():
            game_over_screen(score, win=True)
            return

        # Lose condition: enemies reach bottom
        if enemy_group.reached_bottom():
            game_over_screen(score, win=False)
            return

        # Draw everything
        player.draw()
        enemy_group.draw()
        for bullet in player_bullets:
            bullet.draw()
        for bullet in enemy_bullets:
            bullet.draw()
        draw_ui(score, player.lives)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()