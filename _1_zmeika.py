from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None):  # ИСПРАВЛЕНО: должно быть __init__
        """
        Инициализирует игровой объект.

        Args:
            position: Позиция объекта на игровом поле. Если None,
                     устанавливается в центр экрана.
        """
        if position is None:
            self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        else:
            self.position = position
        self.body_color = None  # ДОБАВЛЕНО: инициализация body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self):  # ИСПРАВЛЕНО: должно быть __init__
        """Инициализирует яблоко со случайной позицией и красным цветом."""
        super().__init__()  # ИСПРАВЛЕНО: правильный вызов super()
        self.body_color = APPLE_COLOR  # ДОБАВЛЕНО: установка цвета
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self):  # ИСПРАВЛЕНО: должно быть __init__
        """Инициализирует змейку с начальными параметрами."""
        super().__init__()  # ИСПРАВЛЕНО: правильный вызов super()
        self.body_color = SNAKE_COLOR  # ДОБАВЛЕНО: установка цвета
        self.reset()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]  # ДОБАВЛЕНО: инициализация positions
        self.direction = RIGHT  # ДОБАВЛЕНО: установка направления
        self.next_direction = None  # ДОБАВЛЕНО: инициализация next_direction
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову и удаляя хвост."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Проверка на столкновение с собой
        if new_position in self.positions[:-1]:
            self.reset()
            return

        # Сохраняем последнюю позицию для затирания
        if len(self.positions) >= self.length:
            self.last = self.positions[-1]

        # Добавляем новую голову
        self.positions.insert(0, new_position)

        # Удаляем хвост, если длина превышена
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):  # ИСПРАВЛЕНО: убрал лишний отступ, это метод класса
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.

    Args:
        game_object: Объект змейки, для которого обрабатываются клавиши.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Обработка действий пользователя
        handle_keys(snake)

        # Обновление направления движения змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появится на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':  # ИСПРАВЛЕНО: должно быть __name__
    main()
