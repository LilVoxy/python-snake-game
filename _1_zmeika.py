import random
import time
import os


class GameObject:
    """Base class for all game objects."""

    def __init__(self, position=None):
        self.position = position if position else (10, 10)

    def draw(self):
        pass


class Apple(GameObject):
    """Apple object that snake can eat."""

    def __init__(self, grid_width=20, grid_height=15):
        super().__init__()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.randomize_position()

    def randomize_position(self):
        x = random.randint(0, self.grid_width - 1)
        y = random.randint(0, self.grid_height - 1)
        self.position = (x, y)

    def draw(self, grid):
        x, y = self.position
        grid[y][x] = 'A'


class Snake(GameObject):
    """Snake object controlled by player."""

    def __init__(self, grid_width=20, grid_height=15):
        super().__init__()
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)  # Right
        self.next_direction = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_x = (head_x + dx) % self.grid_width
        new_y = (head_y + dy) % self.grid_height
        new_head = (new_x, new_y)

        # Check collision with self
        if new_head in self.positions[1:]:
            return False

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

        return True

    def reset(self):
        self.length = 1
        self.positions = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = (1, 0)
        self.next_direction = None

    def draw(self, grid):
        for i, (x, y) in enumerate(self.positions):
            if i == 0:  # Head
                grid[y][x] = 'O'
            else:  # Body
                grid[y][x] = '*'


class Game:
    """Main game class."""

    def __init__(self, width=20, height=15):
        self.width = width
        self.height = height
        self.snake = Snake(width, height)
        self.apple = Apple(width, height)
        self.score = 0
        self.game_over = False

    def handle_input(self):
        """Handle keyboard input."""
        try:
            key = input("Direction (w/a/s/d - q to quit): ").lower()
            if key == 'w' and self.snake.direction != (0, 1):
                self.snake.next_direction = (0, -1)
            elif key == 's' and self.snake.direction != (0, -1):
                self.snake.next_direction = (0, 1)
            elif key == 'a' and self.snake.direction != (1, 0):
                self.snake.next_direction = (-1, 0)
            elif key == 'd' and self.snake.direction != (-1, 0):
                self.snake.next_direction = (1, 0)
            elif key == 'q':
                return False
        except (EOFError, KeyboardInterrupt):
            return False
        return True

    def update(self):
        """Update game state."""
        self.snake.update_direction()

        if not self.snake.move():
            self.game_over = True
            return

        # Check if snake ate apple
        if self.snake.get_head_position() == self.apple.position:
            self.snake.length += 1
            self.score += 10
            self.apple.randomize_position()
            # Make sure apple doesn't spawn on snake
            while self.apple.position in self.snake.positions:
                self.apple.randomize_position()

    def draw(self):
        """Draw game state."""
        os.system('cls' if os.name == 'nt' else 'clear')

        # Create empty grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # Draw borders
        for i in range(self.height):
            grid[i][0] = '|'
            grid[i][-1] = '|'
        for j in range(self.width):
            grid[0][j] = '-'
            grid[-1][j] = '-'

        # Draw game objects
        self.snake.draw(grid)
        self.apple.draw(grid)

        # Print grid
        for row in grid:
            print(''.join(row))

        print(f"Score: {self.score}")
        print("Controls: w=up, a=left, s=down, d=right, q=quit")

    def run(self):
        """Main game loop."""
        while not self.game_over:
            self.draw()
            if not self.handle_input():
                break
            self.update()
            time.sleep(0.2)

        print(f"Game Over! Final Score: {self.score}")


if __name__ == "__main__":
    game = Game()
    game.run()
