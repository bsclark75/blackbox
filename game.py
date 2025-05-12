from Constants import GAME_INSTRUCTIONS, LETTERS
from grid import Grid
from ray import Ray
from functions import label_to_coord_and_dir

class Game:
    def __init__(self):
        self.grid = Grid(8, {(2, 5), (6, 3), (1, 7)})
        self.game_over = False

    def start(self):
        self.show_instructions()
        self.play_game()

    def show_instructions(self):
        print(GAME_INSTRUCTIONS)

    def play_game(self):
        while not self.game_over:
            self.grid.display()
            user_input = input("Enter command (A–P, 0–15, HELP, S, Q): ").strip().upper()

            if user_input == "HELP":
                self.show_instructions()
            elif user_input == "S":
                self.grid.reveal_mines()
                self.game_over = True
            elif user_input == "Q":
                print("Quitting game.")
                self.game_over = True
            elif user_input in LETTERS or user_input.isdigit():
                self.trace_ray(user_input)
            elif len(user_input) == 2 and user_input[0] in LETTERS and user_input[1].isdigit():
                self.guess_atom(user_input)
            else:
                print("Invalid input.")

    def trace_ray(self, entry_label):
        start, direction = label_to_coord_and_dir(entry_label)
        #print(f"start is {start} moving in {direction} direction")
        if not start:
            print("Invalid entry label.")
            return

        ray = Ray(start, direction, self.grid)
        result = ray.move()
        print(f"{entry_label} → {result}")

    def guess_atom(self, label):
        x = LETTERS.index(label[0])
        y = int(label[1])
        self.grid.grid[x][y] = "?"
        print(f"Marked {label} as guessed atom.")
