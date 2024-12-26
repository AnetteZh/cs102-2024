import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        height, width = screen.getmaxyx()
        for i, row in enumerate(self.life.curr_generation):
            for j, val in enumerate(row):
                if 0 < i < height - 1 and 0 < j < width - 1:
                    ch = " "
                    if val == 1:
                        ch = "1"
                    screen.addch(i, j, ch)

    def run(self) -> None:
        screen = curses.initscr()
        screen.nodelay(True)
        while True:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            # screen.addstr(self.life.rows + 3, 0, "Press [Q] to quit")
            # Выполняем один шаг игры если еще не получена устойчивая комбинация и не превышено заданное число поколений
            if not self.life.is_max_generations_exceeded and self.life.is_changing:
                self.life.step()

            try:
                key = screen.getkey()
            except Exception:
                key = None
            if key and key.lower() == "q":
                break

            time.sleep(0.1)
            screen.refresh()


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=50)
    ui = Console(life)
    ui.run()
