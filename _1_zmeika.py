import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (RGB)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Speed (FPS)
SPEED = 20

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Base class for game objects."""

    def __init__(self):
        """Initialize position at screen center."""
        self.position = (
            (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
            (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        )
        self.body_color = None

    def draw(self, surface):
        """Abstract draw method. Override in subclasses."""
        pass


class Apple(GameObject):
    """Apple that the snake can eat."""

    def __init__(self):
        """Initialize apple with red color and random position."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Set random position within the grid."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Draw the apple as a filled rectangle."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Player-controlled snake."""

    def __init__(self):
        """Initialize snake at center, length 1, moving right."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Update direction if a new one is queued."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move the snake one cell in the current direction."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self, surface):
        """Draw the snake and erase the tail trail."""
        # Draw head
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Draw body
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Erase tail
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Return the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Reset snake to initial state."""
        self.length = 1
        self.positions = [
            (
                (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
                (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
            )
        ]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(current_direction):
    """Handle key presses and return new direction."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and current_direction != DOWN:
                return UP
            if event.key == pygame.K_DOWN and current_direction != UP:
                return DOWN
            if event.key == pygame.K_LEFT and current_direction != RIGHT:
                return LEFT
            if event.key == pygame.K_RIGHT and current_direction != LEFT:
                return RIGHT
    return current_direction


def main():
    """Main game loop."""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Python Snake')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        # Handle input
        snake.next_direction = handle_keys(snake.direction)

        # Update game state
        snake.update_direction()
        snake.move()

        # Check if apple is eaten
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        # Check self-collision
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        # Redraw screen
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()

        # Control speed
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
