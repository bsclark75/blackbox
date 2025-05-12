from Constants import LETTERS, MINE_COUNT

class Grid:
    def __init__(self, size=8, mines=None):
        self.size = size
        self.grid = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.mines = set()
        self.mark_count = MINE_COUNT
    
        if mines is not None:
            for mine in mines:
                x, y = mine
                self.add_mine(x, y)


    def add_mine(self, x, y):
        self.mines.add((x, y))

    def display(self):
        print(f"Mines left to mark: {self.mark_count}")
        col_labels_top = "   " + " ".join(f"{i:>2}" for i in range(self.size))
        print(col_labels_top)

        for i in range(self.size):
            row_label_left = LETTERS[i]
            row_label_right = LETTERS[i + self.size]
            row_cells = " ".join(f"{cell:>2}" for cell in self.grid[i])
            print(f"{row_label_left} |{row_cells}| {row_label_right}")

        col_labels_bottom = "   " + " ".join(f"{i + self.size:>2}" for i in range(self.size))
        print(col_labels_bottom)

    def reveal_mines(self):
        correct_guess = 0
        for x, y in self.mines:
            if self.grid[x][y] == "?":
                correct_guess += 1
            self.grid[x][y] = "*"
        self.display()
        print(f"You guessed {correct_guess} out of {MINE_COUNT}.")
