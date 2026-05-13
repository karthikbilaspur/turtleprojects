import pygame
import random
import math
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Night Sky Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 18)

# Colors
BLACK = (0, 0, 0)
NIGHT_BLUE = (5, 5, 25)
DARK_BLUE = (10, 10, 40)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 200)
MOON_COLOR = (240, 240, 220)

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT - 150) # Keep stars above ground
        self.size = random.choice([1, 1, 1, 2, 2, 3]) # Most stars small
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_offset = random.uniform(0, 2 * math.pi)

    def draw(self, time):
        # Twinkling effect using sine wave
        twinkle = math.sin(time * self.twinkle_speed + self.twinkle_offset)
        current_brightness = self.brightness + twinkle * 0.3
        current_brightness = max(0.1, min(1.0, current_brightness))

        color_val = int(255 * current_brightness)
        color = (color_val, color_val, color_val)

        # Draw star with glow for brighter ones
        if self.size >= 2 and current_brightness > 0.7:
            glow_surf = pygame.Surface((self.size * 6, self.size * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, 50),
                             (self.size * 3, self.size * 3), self.size * 2)
            screen.blit(glow_surf, (self.x - self.size * 3, self.y - self.size * 3))

        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

class Moon:
    def __init__(self):
        self.angle = 0 # Position in sky
        self.radius = WIDTH // 2 - 100
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT + 100 # Moon arc center below screen
        self.size = 40
        self.phase = 0 # 0 to 2π for moon phases

    def update(self):
        self.angle += 0.001 # Slow movement across sky
        self.phase += 0.005 # Slow phase change
        if self.angle > math.pi:
            self.angle = 0

    def get_position(self):
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y - self.radius * math.sin(self.angle)
        return int(x), int(y)

    def draw(self):
        x, y = self.get_position()

        # Only draw if above horizon
        if y < HEIGHT - 100:
            # Moon glow
            glow_surf = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*MOON_COLOR, 30),
                             (self.size * 2, self.size * 2), self.size * 1.5)
            screen.blit(glow_surf, (x - self.size * 2, y - self.size * 2))

            # Full moon base
            pygame.draw.circle(screen, MOON_COLOR, (x, y), self.size)

            # Moon phase shadow - creates crescent/new moon effect
            phase_shift = math.cos(self.phase) * self.size
            shadow_x = x + int(phase_shift)

            if abs(phase_shift) < self.size * 2:
                shadow_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.circle(shadow_surf, NIGHT_BLUE, (self.size, self.size), self.size)
                screen.blit(shadow_surf, (shadow_x - self.size, y - self.size))

            # Moon craters for detail
            pygame.draw.circle(screen, (200, 200, 190), (x - 10, y - 5), 5)
            pygame.draw.circle(screen, (200, 200, 190), (x + 12, y + 8), 4)
            pygame.draw.circle(screen, (200, 200, 190), (x + 5, y - 15), 3)

class ShootingStar:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT // 3)
        angle = random.uniform(math.pi / 4, 3 * math.pi / 4) # Downward angles
        speed = random.uniform(8, 15)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(30, 60)
        self.max_life = self.life
        self.trail = []
        self.active = False
        self.cooldown = random.randint(100, 300) # Time between shooting stars

    def update(self):
        if not self.active:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.active = True
                self.reset()
                self.active = True
            return

        # Store trail
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 15:
            self.trail.pop(0)

        # Move
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

        # Reset when dead or off screen
        if self.life <= 0 or self.x < 0 or self.x > WIDTH or self.y > HEIGHT:
            self.active = False
            self.cooldown = random.randint(100, 400)

    def draw(self):
        if not self.active:
            return

        # Draw trail with gradient
        for i in range(len(self.trail) - 1):
            alpha = int(255 * (i / len(self.trail)))
            start_pos = self.trail[i]
            end_pos = self.trail[i + 1]

            # Color shifts from white to yellow to orange in trail
            t = i / len(self.trail)
            r = 255
            g = int(255 - t * 100)
            b = int(200 - t * 200)

            pygame.draw.line(screen, (r, g, b), start_pos, end_pos, 2)

        # Draw bright head
        if self.trail:
            pygame.draw.circle(screen, WHITE, self.trail[-1], 3)
            pygame.draw.circle(screen, YELLOW, self.trail[-1], 2)

def draw_ground():
    # Simple ground silhouette
    ground_points = [(0, HEIGHT - 100)]
    for x in range(0, WIDTH + 20, 20):
        y = HEIGHT - 100 + random.randint(-5, 5) + math.sin(x * 0.01) * 10
        ground_points.append((x, y))
    ground_points.append((WIDTH, HEIGHT))
    ground_points.append((0, HEIGHT))
    pygame.draw.polygon(screen, (0, 0, 0), ground_points)

def draw_ui(num_stars):
    text1 = font.render(f"Stars: {num_stars} | SPACE: Shooting Star | Q: Quit", True, (150, 150, 150))
    screen.blit(text1, (10, HEIGHT - 30))

def main():
    stars = [Star() for _ in range(200)]
    moon = Moon()
    shooting_stars = [ShootingStar() for _ in range(3)]

    time_elapsed = 0
    running = True

    while running:
        time_elapsed += 1

        # Gradient sky background
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(NIGHT_BLUE[0] + (DARK_BLUE[0] - NIGHT_BLUE[0]) * ratio)
            g = int(NIGHT_BLUE[1] + (DARK_BLUE[1] - NIGHT_BLUE[1]) * ratio)
            b = int(NIGHT_BLUE[2] + (DARK_BLUE[2] - NIGHT_BLUE[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Force a shooting star
                    for ss in shooting_stars:
                        if not ss.active:
                            ss.active = True
                            ss.reset()
                            ss.active = True
                            break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Update moon
        moon.update()

        # Draw all stars with twinkling
        for star in stars:
            star.draw(time_elapsed)

        # Draw moon
        moon.draw()

        # Update and draw shooting stars
        for ss in shooting_stars:
            ss.update()
            ss.draw()

        # Draw ground
        draw_ground()
        draw_ui(len(stars))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()