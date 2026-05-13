import pygame
import math
import sys
import tkinter as tk
from tkinter import colorchooser

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spiral Art Generator")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)

# Default colors
BG_COLOR = (10, 10, 30)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
current_color_idx = 0

class SpiralGenerator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.angle = 0
        self.radius = 0
        self.points = []
        self.pattern = "archimedean" # archimedean, fermat, logarithmic, polygon
        self.sides = 5 # For polygon spiral
        self.angle_step = 5
        self.radius_step = 1
        self.drawing = False
        self.auto_rotate = True

    def pick_color(self):
        # Use tkinter color chooser
        root = tk.Tk()
        root.withdraw() # Hide main window
        color = colorchooser.askcolor(title="Pick a spiral color")[0]
        root.destroy()
        if color:
            COLORS.append((int(color[0]), int(color[1]), int(color[2])))
            global current_color_idx
            current_color_idx = len(COLORS) - 1

    def get_next_point(self):
        cx, cy = WIDTH // 2, HEIGHT // 2

        if self.pattern == "archimedean": # r = a + b*θ
            self.radius += self.radius_step * 0.1
            x = cx + self.radius * math.cos(math.radians(self.angle))
            y = cy + self.radius * math.sin(math.radians(self.angle))

        elif self.pattern == "fermat": # r = a*√θ
            self.radius = 8 * math.sqrt(self.angle)
            x = cx + self.radius * math.cos(math.radians(self.angle))
            y = cy + self.radius * math.sin(math.radians(self.angle))

        elif self.pattern == "logarithmic": # r = a*e^(b*θ)
            self.radius = 5 * math.exp(0.01 * self.angle)
            x = cx + self.radius * math.cos(math.radians(self.angle))
            y = cy + self.radius * math.sin(math.radians(self.angle))

        elif self.pattern == "polygon": # Polygon spiral
            self.radius += self.radius_step * 0.2
            poly_angle = self.angle + (360 / self.sides) * (self.angle // (360 / self.sides))
            x = cx + self.radius * math.cos(math.radians(poly_angle))
            y = cy + self.radius * math.sin(math.radians(poly_angle))

        self.angle += self.angle_step
        return (x, y)

    def draw(self):
        if len(self.points) > 1:
            color = COLORS[current_color_idx]
            for i in range(len(self.points) - 1):
                # Fade older lines for cool effect
                alpha = int(255 * (i / len(self.points)))
                faded_color = (color[0], color[1], color[2])
                pygame.draw.line(screen, faded_color, self.points[i], self.points[i + 1], 2)

            # Draw current point
            if self.points:
                pygame.draw.circle(screen, WHITE, (int(self.points[-1][0]), int(self.points[-1][1])), 3)

def draw_ui(spiral):
    # Background panel
    pygame.draw.rect(screen, (0, 0, 0, 180), (0, 0, WIDTH, 120))

    # Current settings
    pattern_text = font.render(f"Pattern: {spiral.pattern.upper()} | Sides: {spiral.sides}", True, WHITE)
    angle_text = font.render(f"Angle Step: {spiral.angle_step} | Radius Step: {spiral.radius_step}", True, WHITE)
    color_text = font.render(f"Color: {current_color_idx + 1}/{len(COLORS)}", True, COLORS[current_color_idx])

    screen.blit(pattern_text, (10, 10))
    screen.blit(angle_text, (10, 35))
    screen.blit(color_text, (10, 60))

    # Controls
    controls = [
        "SPACE: Start/Stop | C: Clear | R: Reset | T: Cycle Pattern",
        "1-6: Change Color | P: Pick Color | UP/DOWN: Angle Step | LEFT/RIGHT: Sides",
        "Q/W: Radius Step | A: Toggle Auto-draw"
    ]
    for i, text in enumerate(controls):
        control_text = font.render(text, True, YELLOW)
        screen.blit(control_text, (350, 10 + i * 25))

    # Color preview boxes
    for i, color in enumerate(COLORS[:6]):
        rect = pygame.Rect(WIDTH - 200 + i * 30, 85, 25, 25)
        pygame.draw.rect(screen, color, rect)
        if i == current_color_idx:
            pygame.draw.rect(screen, WHITE, rect, 3)

def main():
    spiral = SpiralGenerator()
    global current_color_idx

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spiral.drawing = not spiral.drawing

                elif event.key == pygame.K_c: # Clear
                    spiral.points = []

                elif event.key == pygame.K_r: # Reset
                    spiral.reset()
                    screen.fill(BG_COLOR)

                elif event.key == pygame.K_t: # Cycle pattern
                    patterns = ["archimedean", "fermat", "logarithmic", "polygon"]
                    idx = patterns.index(spiral.pattern)
                    spiral.pattern = patterns[(idx + 1) % len(patterns)]
                    spiral.points = []
                    spiral.angle = 0
                    spiral.radius = 0

                elif event.key == pygame.K_p: # Pick color
                    spiral.pick_color()

                elif event.key == pygame.K_a: # Toggle auto
                    spiral.auto_rotate = not spiral.auto_rotate

                elif event.key == pygame.K_UP:
                    spiral.angle_step = min(20, spiral.angle_step + 1)
                elif event.key == pygame.K_DOWN:
                    spiral.angle_step = max(1, spiral.angle_step - 1)

                elif event.key == pygame.K_LEFT:
                    spiral.sides = max(3, spiral.sides - 1)
                elif event.key == pygame.K_RIGHT:
                    spiral.sides = min(12, spiral.sides + 1)

                elif event.key == pygame.K_q:
                    spiral.radius_step = max(0.1, spiral.radius_step - 0.1)
                elif event.key == pygame.K_w:
                    spiral.radius_step = min(5, spiral.radius_step + 0.1)

                # Number keys for color
                elif pygame.K_1 <= event.key <= pygame.K_6:
                    idx = event.key - pygame.K_1
                    if idx < len(COLORS):
                        current_color_idx = idx

        # Generate spiral points
        if spiral.drawing and spiral.auto_rotate:
            point = spiral.get_next_point()
            # Stop if we go off screen
            if 0 <= point[0] <= WIDTH and 0 <= point[1] <= HEIGHT:
                spiral.points.append(point)
            else:
                spiral.drawing = False # Auto-stop at edges

        # Drawing
        screen.fill(BG_COLOR)
        spiral.draw()
        draw_ui(spiral)

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()