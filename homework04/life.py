import pathlib
import random
import typing as tp

from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1
        self.size = size

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создаем список клеток
        """
        grid = [[0] * self.cols for i in range(self.rows)]
        if randomize:
            for i, row in enumerate(grid):
                for j, _ in enumerate(row):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Получаем соседей интересующей нас клетки
        """
        neighbours = []
        pos_row, pos_col = cell
        for i in range(pos_row - 1, pos_row + 2):
            for j in range(pos_col - 1, pos_col + 2):
                if 0 <= i < self.rows and 0 <= j < self.cols and (pos_row, pos_col) != (i, j):
                    neighbours.append(self.curr_generation[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Делаем выводы о судьбе клеток на следующем шаге
        """
        next_generation = self.create_grid()
        for i, row in enumerate(next_generation):
            for j, _ in enumerate(row):
                neighbours = self.get_neighbours((i, j))
                sum_neigh = sum(neighbours)
                if self.curr_generation[i][j] == 1:
                    if sum_neigh == 2 or sum_neigh == 3:
                        next_generation[i][j] = 1
                    else:
                        next_generation[i][j] = 0
                else:
                    if sum_neigh == 3:
                        next_generation[i][j] = 1
        return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded and self.is_changing:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations is not None and self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with filename.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    row = [int(char) for char in line]
                    grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w") as f:
            for row in self.curr_generation:
                f.write("".join(map(str, row)) + "\n")
