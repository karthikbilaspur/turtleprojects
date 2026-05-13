import pygame
import random
import sys
import math

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks Animation")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
NIGHT_BLUE = (5, 5, 20)

# Physics
GRAVITY = 0.15
FRICTION = 0.98

class Particle:
    def __init__(self, x, y, color, velocity, life, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.life = life
        self.max_life = life
        self.size = size
        self.trail = [] # For particle trails

    def update(self):
        # Store trail positions
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 5: # Trail length
            self.trail.pop(0)

        # Gravity simulation
        self.vy += GRAVITY

        # Apply friction/air resistance
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Decrease life
        self.life -= 1

    def draw(self):
        # Fade out based on remaining life
        alpha = int(255 * (self.life / self.max_life))
        if alpha <= 0:
            return

        # Draw trail with fading effect
        for i, pos in enumerate(self.trail):
            trail_alpha = int(alpha * (i / len(self.trail)) * 0.5)
            if trail_alpha > 0:
                trail_color = (*self.color, trail_alpha)
                trail_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                pygame.draw.circle(trail_surf, trail_color, (self.size // 2, self.size // 2), self.size // 2)
                screen.blit(trail_surf, pos)

        # Draw main particle with glow
        particle_color = (*self.color, alpha)
        glow_surf = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color, alpha // 3),
                          (self.size * 3 // 2, self.size * 3 // 2), self.size)
        screen.blit(glow_surf, (int(self.x - self.size), int(self.y - self.size)))

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)

    def is_dead(self):
        return self.life <= 0

class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.target_y = random.randint(100, HEIGHT // 2)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-12, -8)
        self.color = (255, 255, 255)
        self.exploded = False
        self.particles = []
        self.trail = []

    def update(self):
        if not self.exploded:
            # Trail for rocket
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > 8:
                self.trail.pop(0)

            # Rocket physics
            self.vy += GRAVITY * 0.5 # Less gravity on rockets
            self.x += self.vx
            self.y += self.vy

            # Explode at peak or random chance
            if self.vy >= 0 or self.y <= self.target_y:
                self.explode()
        else:
            # Update all explosion particles
            for particle in self.particles[:]:
                particle.update()
                if particle.is_dead():
                    self.particles.remove(particle)

    def explode(self):
        self.exploded = True
        num_particles = random.randint(80, 150)
        explosion_color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )

        # Random explosion patterns
        pattern = random.choice(['circle', 'star', 'random'])

        for i in range(num_particles):
            if pattern == 'circle':
                angle = (i / num_particles) * 2 * math.pi
                speed = random.uniform(2, 6)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
            elif pattern == 'star':
                angle = (i / num_particles) * 2 * math.pi
                speed = random.uniform(1, 7) if i % 2 == 0 else random.uniform(3, 5)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
            else: # random
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 7)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed

            # Some particles with different colors for variety
            particle_color = explosion_color
            if random.random() < 0.3:
                particle_color = (
                    min(255, explosion_color[0] + random.randint(-50, 50)),
                    min(255, explosion_color[1] + random.randint(-50, 50)),
                    min(255, explosion_color[2] + random.randint(-50, 50))
                )

            life = random.randint(40, 80)
            size = random.randint(2, 5)
            self.particles.append(Particle(self.x, self.y, particle_color, (vx, vy), life, size))

    def draw(self):
        if not self.exploded:
            # Draw rocket trail
            for i, pos in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)) * 0.6)
                if alpha > 0:
                    trail_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surf, (255, 200, 100, alpha), (2, 2), 2)
                    screen.blit(trail_surf, pos)

            # Draw rocket
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
            pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 1)
        else:
            # Draw all particles
            for particle in self.particles:
                particle.draw()

    def is_dead(self):
        return self.exploded and len(self.particles) == 0

def draw_stars():
    # Static background stars
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 2)
        brightness = random.randint(100, 200)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

def main():
    fireworks = []
    stars_drawn = False
    font = pygame.font.SysFont('arial', 20)

    running = True
    while running:
        # Draw night sky background
        screen.fill(NIGHT_BLUE)

        # Draw stars once
        if not stars_drawn:
            draw_stars()
            stars_drawn = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Manual firework launch
                    fireworks.append(Firework())
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Random explosions - launch new fireworks randomly
        if random.random() < 0.04: # 4% chance per frame
            fireworks.append(Firework())

        # Update and draw all fireworks
        for firework in fireworks[:]:
            firework.update()
            firework.draw()
            if firework.is_dead():
                fireworks.remove(firework)

        # Instructions
        text1 = font.render("SPACE - Launch Firework", True, (200, 200, 200))
        text2 = font.render("Q - Quit", True, (200, 200, 200))
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 35))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    YELLOW = (255, 255, 0) # Define here for rocket glow
    main()