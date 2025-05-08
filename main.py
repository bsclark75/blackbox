import os
from Constants import *
from grid import Grid
from ray import Ray


mines = {(2, 5), (6, 3), (1, 7)}  # Example hidden atoms

def guess_atom(label,grid):
    x = LETTERS.index(label[0])
    y = int(label[1])
    grid[x][y] = "?"
    print(f"Marked {label} as guessed atom.")

def label_to_coord_and_dir(label):
    if label in LETTERS:
        i = LETTERS.index(label)
        if i < GRID_SIZE:
            return (i, 0), (0, 1)  # LEFT → RIGHT
        else:
            return (i - GRID_SIZE, GRID_SIZE - 1), (0, -1)  # RIGHT → LEFT
    elif label.isdigit():
        i = int(label)
        if i < GRID_SIZE:
            return (0, i), (1, 0)  # TOP → DOWN
        elif i < GRID_SIZE * 2:
            return (GRID_SIZE - 1, i - GRID_SIZE), (-1, 0)  # BOTTOM → UP
    return None, None

def coord_to_label(pos):
    x, y = pos
    if x < 0:
        return str(y)
    elif x >= GRID_SIZE:
        return str(y + GRID_SIZE)
    elif y < 0:
        return LETTERS[x]
    elif y >= GRID_SIZE:
        return LETTERS[x + GRID_SIZE]
    return "?"


def trace_ray(entry_label,grid):
    start, direction = label_to_coord_and_dir(entry_label)
    if not start:
        print("Invalid entry label.")
        return

    ray = Ray(start,direction,grid)
    result = ray.move()
    print(f"{entry_label} → {result}")

def play_game():
    grid = Grid(8, {(2, 5), (6, 3), (1, 7)})
    while True:
        grid.display()
        user_input = input("Enter command (A–P, 0–15, HELP, S, Q): ").strip().upper()

        if user_input == "HELP":
            print(GAME_INSTRUCTIONS)
        elif user_input == "S":
            grid.reveal_mines()
            break
        elif user_input == "Q":
            print("Quitting game.")
            break
        elif user_input in LETTERS or user_input.isdigit():
            trace_ray(user_input,grid)
        elif len(user_input) == 2 and user_input[0] in LETTERS and user_input[1].isdigit():
            guess_atom(user_input, grid)
        else:
            print("Invalid input.")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Welcome to text Blackbox!")
    print(GAME_INSTRUCTIONS)
    play_game()

if __name__ == "__main__":
    main()
