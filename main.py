import random
import string
import os

GRID_SIZE = 8
LETTERS = "ABCDEFGHIJKLMNOP"
GAME_INSTRUCTIONS = """
Enter a letter (A–P) or number (0–15) to fire a shot.
Enter something like B4 to guess an atom.
Enter S to show the answer grid and quit.
Enter HELP to see instructions.
"""

grid = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
mines = {(2, 3), (5, 5), (6, 1)}  # Example hidden atoms

def display_grid():
    # Print top column numbers
    col_labels_top = "   " + " ".join(f"{i:>2}" for i in range(GRID_SIZE))
    print(col_labels_top)

    # Print rows with left and right side labels
    for i in range(GRID_SIZE):
        row_label_left = LETTERS[i]
        row_label_right = LETTERS[i + GRID_SIZE]
        row_cells = " ".join(f"{cell:>2}" for cell in grid[i])
        print(f"{row_label_left} |{row_cells}| {row_label_right}")

    # Print bottom column numbers
    col_labels_bottom = "   " + " ".join(f"{i + GRID_SIZE:>2}" for i in range(GRID_SIZE))
    print(col_labels_bottom)


def show_answers():
    for x, y in mines:
        grid[x][y] = "*"
    display_grid()
    print("Atoms revealed.")

def guess_atom(label):
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

def follow_ray(start, direction):
    x, y = start
    dx, dy = direction
    visited = set()

    while True:
        # If we're about to step outside, this is the exit point
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return coord_to_label((x, y))

        # Direct hit
        if (x, y) in mines:
            return "Absorbed"

        # Check diagonal influence BEFORE moving
        # Compute next cell (where ray is headed)
        next_x = x + dx
        next_y = y + dy

        # Check diagonals from the *next* cell
        diag1 = (next_x + dy, next_y - dx)  # top-right
        diag2 = (next_x - dy, next_y + dx)  # bottom-left

        mine1 = diag1 in mines
        mine2 = diag2 in mines

        print(f"Ray at ({x},{y}) moving ({dx},{dy})")

        if mine1 and mine2:
            return "Reflected"
        elif mine1:
            # Diagonal to upper-right (relative to direction)
            if (dx, dy) == (0, 1):      # →
                dx, dy = -1, 0          # go ↑
            elif (dx, dy) == (0, -1):   # ←
                dx, dy = -1, 0          # go ↑
            elif (dx, dy) == (1, 0):    # ↓
                dx, dy = 0, -1          # go ←
            elif (dx, dy) == (-1, 0):   # ↑
                dx, dy = 0, -1          # go ←
        elif mine2:
            # Diagonal to lower-left (relative to direction)
            if (dx, dy) == (0, 1):      # →
                dx, dy = 1, 0           # go ↓
            elif (dx, dy) == (0, -1):   # ←
                dx, dy = 1, 0           # go ↓
            elif (dx, dy) == (1, 0):    # ↓
                dx, dy = 0, 1           # go →
            elif (dx, dy) == (-1, 0):   # ↑
                dx, dy = 0, 1           # go →


        # Detect potential infinite loop
        if (x, y, dx, dy) in visited:
            return "Loop"
        visited.add((x, y, dx, dy))

        # Now move
        x += dx
        y += dy

def trace_ray(entry_label):
    start, direction = label_to_coord_and_dir(entry_label)
    if not start:
        print("Invalid entry label.")
        return

    result = follow_ray(start, direction)
    print(f"{entry_label} → {result}")


def play_game():
    while True:
        display_grid()
        user_input = input("Enter command (A–P, 0–15, HELP, S, Q): ").strip().upper()

        if user_input == "HELP":
            print(GAME_INSTRUCTIONS)
        elif user_input == "S":
            show_answers()
            break
        elif user_input == "Q":
            print("Quitting game.")
            break
        elif user_input in LETTERS or user_input.isdigit():
            trace_ray(user_input)
        elif len(user_input) == 2 and user_input[0] in LETTERS and user_input[1].isdigit():
            guess_atom(user_input)
        else:
            print("Invalid input.")

def main():
    os.system('clear')
    print("Welcome to text Blackbox!")
    print(GAME_INSTRUCTIONS)
    play_game()

if __name__ == "__main__":
    main()

