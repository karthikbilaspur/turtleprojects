import pygame
import random
import sys
import time

# Initialize
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
big_font = pygame.font.SysFont('arial', 32)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 50, 50) # Comparing
GREEN = (50, 255, 50) # Sorted
BLUE = (50, 150, 255) # Default
YELLOW = (255, 255, 50) # Pivot/key element
PURPLE = (200, 50, 255) # Merge sections

# Array settings
ARRAY_SIZE = 80
BAR_WIDTH = WIDTH // ARRAY_SIZE
SPEED = 60 # FPS, controls animation speed

class SortingVisualizer:
    def __init__(self):
        self.array = []
        self.reset_array()
        self.sorting = False
        self.algorithm = "Bubble Sort"
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0

    def reset_array(self):
        self.array = [random.randint(10, HEIGHT - 100) for _ in range(ARRAY_SIZE)]
        self.comparisons = 0
        self.swaps = 0
        self.sorting = False

    def draw_array(self, color_positions={}):
        screen.fill(BLACK)

        for i, height in enumerate(self.array):
            color = BLUE
            if i in color_positions:
                color = color_positions[i]

            x = i * BAR_WIDTH
            y = HEIGHT - height - 50
            pygame.draw.rect(screen, color, (x, y, BAR_WIDTH - 2, height))

        self.draw_ui()
        pygame.display.update()

    def draw_ui(self):
        # Title and stats
        title = big_font.render(f"{self.algorithm}", True, WHITE)
        screen.blit(title, (10, 10))

        comp_text = font.render(f"Comparisons: {self.comparisons}", True, WHITE)
        swap_text = font.render(f"Swaps: {self.swaps}", True, WHITE)

        if self.sorting:
            elapsed = time.time() - self.start_time
            time_text = font.render(f"Time: {elapsed:.2f}s", True, WHITE)
        else:
            time_text = font.render("Time: 0.00s", True, WHITE)

        screen.blit(comp_text, (10, 50))
        screen.blit(swap_text, (10, 75))
        screen.blit(time_text, (10, 100))

        # Controls
        controls = [
            "SPACE: Start | R: Reset | 1: Bubble | 2: Merge | 3: Quick",
            "UP/DOWN: Speed | Q: Quit",
            f"Speed: {SPEED} FPS"
        ]
        for i, text in enumerate(controls):
            ctrl_text = font.render(text, True, YELLOW)
            screen.blit(ctrl_text, (WIDTH - 400, 10 + i * 25))

    def bubble_sort(self):
        self.sorting = True
        self.start_time = time.time()
        n = len(self.array)

        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparisons += 1

                # Visualize comparison
                self.draw_array({j: RED, j + 1: RED})
                clock.tick(SPEED)
                self.handle_events()

                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.swaps += 1

                    # Visualize swap
                    self.draw_array({j: GREEN, j + 1: GREEN})
                    clock.tick(SPEED)
                    self.handle_events()

            # Mark as sorted
            self.draw_array({n - i - 1: GREEN})
            clock.tick(SPEED // 2)

        self.sorting = False
        self.draw_array({i: GREEN for i in range(n)})

    def merge_sort(self, arr=None, left=0, right=None):
        if arr is None:
            self.sorting = True
            self.start_time = time.time()
            arr = self.array
            right = len(arr) - 1

        if left >= right:
            return

        mid = (left + right) // 2
        self.merge_sort(arr, left, mid)
        self.merge_sort(arr, mid + 1, right)
        self.merge(arr, left, mid, right)

        if left == 0 and right == len(self.array) - 1:
            self.sorting = False
            self.draw_array({i: GREEN for i in range(len(self.array))})

    def merge(self, arr, left, mid, right):
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            self.comparisons += 1

            # Visualize merge sections
            color_map = {left + i: PURPLE, mid + 1 + j: PURPLE, k: YELLOW}
            self.draw_array(color_map)
            clock.tick(SPEED)
            self.handle_events()

            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1
            self.swaps += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
            self.swaps += 1
            self.draw_array({k - 1: YELLOW})
            clock.tick(SPEED)

        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
            self.swaps += 1
            self.draw_array({k - 1: YELLOW})
            clock.tick(SPEED)

    def quick_sort(self, low=0, high=None):
        if high is None:
            self.sorting = True
            self.start_time = time.time()
            high = len(self.array) - 1

        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)

        if low == 0 and high == len(self.array) - 1:
            self.sorting = False
            self.draw_array({i: GREEN for i in range(len(self.array))})

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            self.comparisons += 1

            # Visualize: pivot=yellow, current=red, swap candidate=blue
            color_map = {high: YELLOW, j: RED}
            if i >= low:
                color_map[i] = BLUE
            self.draw_array(color_map)
            clock.tick(SPEED)
            self.handle_events()

            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.swaps += 1

        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.swaps += 1

        # Show partition result
        self.draw_array({i + 1: GREEN})
        clock.tick(SPEED)

        return i + 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r and not self.sorting:
                    self.reset_array()

def main():
    global SPEED
    viz = SortingVisualizer()

    running = True
    while running:
        viz.draw_array()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r and not viz.sorting:
                    viz.reset_array()
                elif event.key == pygame.K_SPACE and not viz.sorting:
                    if viz.algorithm == "Bubble Sort":
                        viz.bubble_sort()
                    elif viz.algorithm == "Merge Sort":
                        viz.merge_sort()
                    elif viz.algorithm == "Quick Sort":
                        viz.quick_sort()
                elif event.key == pygame.K_1 and not viz.sorting:
                    viz.algorithm = "Bubble Sort"
                elif event.key == pygame.K_2 and not viz.sorting:
                    viz.algorithm = "Merge Sort"
                elif event.key == pygame.K_3 and not viz.sorting:
                    viz.algorithm = "Quick Sort"
                elif event.key == pygame.K_UP:
                    SPEED = min(240, SPEED + 10)
                elif event.key == pygame.K_DOWN:
                    SPEED = max(10, SPEED - 10)

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()