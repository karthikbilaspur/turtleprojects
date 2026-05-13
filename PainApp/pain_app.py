import pygame
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Canvas setup
canvas = pygame.Surface((WIDTH, HEIGHT - 100))
canvas.fill(WHITE)

# Default brush settings
brush_color = BLACK
brush_size = 5
drawing = False
last_pos = None

# Color palette
COLORS = [
    BLACK, (127, 127, 127), (136, 0, 21), RED := (237, 28, 36), (255, 127, 39),
    YELLOW := (255, 242, 0), (34, 177, 76), (0, 162, 232), (63, 72, 204), (163, 73, 164),
    WHITE, (195, 195, 195), (185, 122, 87), (255, 174, 201), (255, 201, 14),
    (239, 228, 176), (181, 230, 29), (153, 217, 234), (112, 146, 190), (200, 191, 231)
]

class Button:
    def __init__(self, x, y, w, h, text, color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self):
        color = DARK_GRAY if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(centerHere’s a full **Paint App** in Python with mouse drawing, color picker, and adjustable brush size. Uses `pygame`.

### **paint_app.py**
```python
import pygame
import sys

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Canvas - this is what we actually draw on
canvas = pygame.Surface((WIDTH, HEIGHT - 100))
canvas.fill(WHITE)

# Default settings
current_color = BLACK
brush_size = 5
drawing = False
last_pos = None

# Predefined color palette
COLORS = [
    (0, 0, 0), # Black
    (255, 255, 255), # White
    (255, 0, 0), # Red
    (0, 255, 0), # Green
    (0, 0, 255), # Blue
    (255, 255, 0), # Yellow
    (255, 0, 255), # Magenta
    (0, 255, 255), # Cyan
    (255, 165, 0), # Orange
    (128, 0, 128), # Purple
    (165, 42, 42), # Brown
    (128, 128, 128) # Gray
]

# UI elements
color_rects = []
for i, color in enumerate(COLORS):
    rect = pygame.Rect(10 + i * 35, HEIGHT - 90, 30, 30)
    color_rects.append((rect, color))

# Buttons
clear_button = pygame.Rect(WIDTH - 120, HEIGHT - 90, 100, 30)
save_button = pygame.Rect(WIDTH - 120, HEIGHT - 50, 100, 30)

font = pygame.font.SysFont('arial', 18)

def draw_ui():
    # Toolbar background
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - 100, WIDTH, 100))
    pygame.draw.line(screen, BLACK, (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)

    # Color picker - show all colors
    for rect, color in color_rects:
        pygame.draw.rect(screen, color, rect)
        # Highlight selected color
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 3)
        else:
            pygame.draw.rect(screen, BLACK, rect, 1)

    # Brush size display
    brush_text = font.render(f"Brush: {brush_size}", True, BLACK)
    screen.blit(brush_text, (10, HEIGHT - 50))

    # Brush size preview
    pygame.draw.circle(screen, current_color, (120, HEIGHT - 45), brush_size)
    pygame.draw.circle(screen, BLACK, (120, HEIGHT - 45), brush_size, 1)

    # Size controls
    pygame.draw.rect(screen, DARK_GRAY, (160, HEIGHT - 60, 30, 30))
    pygame.draw.rect(screen, DARK_GRAY, (200, HEIGHT - 60, 30, 30))
    minus_text = font.render("-", True, WHITE)
    plus_text = font.render("+", True, WHITE)
    screen.blit(minus_text, (172, HEIGHT - 58))
    screen.blit(plus_text, (212, HEIGHT - 58))

    # Clear button
    pygame.draw.rect(screen, DARK_GRAY, clear_button)
    clear_text = font.render("Clear", True, WHITE)
    screen.blit(clear_text, (clear_button.x + 30, clear_button.y + 5))

    # Save button
    pygame.draw.rect(screen, DARK_GRAY, save_button)
    save_text = font.render("Save", True, WHITE)
    screen.blit(save_text, (save_button.x + 30, save_button.y + 5))

    # Instructions
    inst_text = font.render("Left Click: Draw | Scroll: Brush Size | E: Eraser", True, BLACK)
    screen.blit(inst_text, (260, HEIGHT - 55))

def draw_line(start, end, color, size):
    # Draw smooth line between two points
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    for i in range(distance):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(canvas, color, (x, y), size)

def main():
    global current_color, brush_size, drawing, last_pos

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    if mouse_pos[1] < HEIGHT - 100: # Drawing on canvas
                        drawing = True
                        last_pos = (mouse_pos[0], mouse_pos[1])
                        # Draw a dot for single clicks
                        pygame.draw.circle(canvas, current_color, last_pos, brush_size)
                    else: # UI interaction
                        # Color picker
                        for rect, color in color_rects:
                            if rect.collidepoint(mouse_pos):
                                current_color = color

                        # Brush size buttons
                        if pygame.Rect(160, HEIGHT - 60, 30, 30).collidepoint(mouse_pos):
                            brush_size = max(1, brush_size - 1)
                        elif pygame.Rect(200, HEIGHT - 60, 30, 30).collidepoint(mouse_pos):
                            brush_size = min(50, brush_size + 1)

                        # Clear button
                        if clear_button.collidepoint(mouse_pos):
                            canvas.fill(WHITE)

                        # Save button
                        if save_button.collidepoint(mouse_pos):
                            pygame.image.save(canvas, "painting.png")
                            print("Saved as painting.png")

                elif event.button == 4: # Scroll up
                    brush_size = min(50, brush_size + 1)
                elif event.button == 5: # Scroll down
                    brush_size = max(1, brush_size - 1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    last_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if drawing and mouse_pos[1] < HEIGHT - 100:
                    if last_pos:
                        draw_line(last_pos, mouse_pos, current_color, brush_size)
                    last_pos = mouse_pos

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: # Eraser
                    current_color = WHITE
                elif event.key == pygame.K_c: # Clear
                    canvas.fill(WHITE)

        # Draw everything
        screen.fill(WHITE)
        screen.blit(canvas, (0, 0))
        draw_ui()

        # Show brush preview at cursor when over canvas
        if mouse_pos[1] < HEIGHT - 100:
            pygame.draw.circle(screen, current_color, mouse_pos, brush_size, 1)

        pygame.display.update()
        clock.tick(120) # High FPS for smooth drawing

if __name__ == "__main__":
    main()