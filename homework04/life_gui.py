import pygame
from pygame.constants import K_SPACE, KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_q
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.running = True
        self.paused = False
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

    def draw_lines(self) -> None:
        """
        Рисуем разметку
        """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Рисуем клетки
        """
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                pygame.draw.rect(
                    self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        """
        Запускаем игру
        """
        pygame.init()
        clock = pygame.time.Clock()
        self.screen.fill(pygame.Color("white"))
        self.life.curr_generation = self.life.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:  # Пауза по пробелу
                        self.paused = not self.paused
                    elif event.key == K_q:  # Выход по клавише 'q'
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.paused:
                        x, y = event.pos
                        # ячейка, внутри которой был клик
                        x //= self.cell_size
                        y //= self.cell_size
                        self.life.curr_generation[y][x] = not self.life.curr_generation[y][x]
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()

            if not self.paused:
                self.life.step()  # Выполнение шага игры, если не на паузе

            self.draw_lines()
            self.draw_grid()
            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((30, 30))
    game = GUI(life)
    game.run()
