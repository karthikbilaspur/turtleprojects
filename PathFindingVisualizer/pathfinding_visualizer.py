import pygame
import sys
from queue import PriorityQueue, Queue

# Window setup
WIDTH = 800
HEIGHT = 850
ROWS = 40
CELL_SIZE = WIDTH // ROWS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer - A* and BFS")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0) # Start
RED = (255, 0, 0) # End
BLUE = (64, 224, 208) # Path
ORANGE = (255, 165, 0) # Open set
PURPLE = (128, 0, 128) # Closed set
YELLOW = (255, 255, 0) # Current node
LIGHT_BLUE = (173, 216, 230) # Grid

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.distance = float('inf')
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.previous = None

    def get_pos(self):
        return self.row, self.col

    def is_start(self):
        return self.color == GREEN

    def is_end(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def reset(self):
        self.color = WHITE
        self.distance = float('inf')
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.previous = None

    def make_start(self):
        self.color = GREEN

    def make_end(self):
        self.color = RED

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = PURPLE

    def make_path(self):
        self.color = BLUE

    def make_current(self):
        self.color = YELLOW

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down, Up, Right, Left
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < ROWS - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def h(p1, p2):
    # Manhattan distance heuristic for A*
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(current, start, draw):
    path = []
    while current.previous:
        path.append(current)
        current = current.previous
    path.append(start)
    path.reverse()

    # Animate path drawing
    for node in path:
        if not node.is_start() and not node.is_end():
            node.make_path()
        draw()
        pygame.time.wait(20)

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    start.g_score = 0
    start.f_score = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(end, start, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = current.g_score + 1

            if temp_g_score < neighbor.g_score:
                neighbor.previous = current
                neighbor.g_score = temp_g_score
                neighbor.f_score = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.f_score, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current!= start:
            current.make_closed()

    return False

def bfs(draw, grid, start, end):
    queue = Queue()
    queue.put(start)
    visited = {start}
    start.distance = 0

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.get()

        if current == end:
            reconstruct_path(end, start, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.previous = current
                neighbor.distance = current.distance + 1
                queue.put(neighbor)
                neighbor.make_open()

        draw()

        if current!= start:
            current.make_closed()

    return False

def make_grid():
    return [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]

def draw_grid():
    for i in range(ROWS):
        pygame.draw.line(screen, LIGHT_BLUE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(screen, LIGHT_BLUE, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

def draw(grid):
    screen.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw()
    draw_grid()
    draw_ui()
    pygame.display.update()

def draw_ui():
    font = pygame.font.SysFont('arial', 18)
    text = [
        "Left Click: Place Start, End, Walls | Right Click: Erase",
        "SPACE: Run A* | B: Run BFS | C: Clear | R: Reset Path",
        "Orange = Open Set | Purple = Visited | Blue = Final Path"
    ]
    for i, line in enumerate(text):
        text_surf = font.render(line, True, BLACK)
        screen.blit(text_surf, (10, WIDTH + 5 + i * 20))

def get_clicked_pos(pos):
    x, y = pos
    if y >= WIDTH: # Clicked in UI area
        return None, None
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

def main():
    grid = make_grid()
    start = None
    end = None
    running = True

    while running:
        draw(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]: # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if row is None:
                    continue
                node = grid[row][col]
                if not start and node!= end:
                    start = node
                    start.make_start()
                elif not end and node!= start:
                    end = node
                    end.make_end()
                elif node!= end and node!= start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                if row is None:
                    continue
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    a_star(lambda: draw(grid), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    bfs(lambda: draw(grid), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid()

                if event.key == pygame.K_r: # Reset path but keep walls
                    for row in grid:
                        for node in row:
                            if not node.is_barrier() and not node.is_start() and not node.is_end():
                                node.reset()
                                node.update_neighbors(grid)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()