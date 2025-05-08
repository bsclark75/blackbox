import os
from Constants import *
from grid import Grid


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

        print(f"Ray at ({x},{y}) moving ({dx},{dy}), diag1={diag1}, diag2={diag2}, mine1={mine1}, mine2={mine2}")

        if mine1 and mine2:
            return "Reflected"
        elif mine1:
            # Diagonal to upper-right (relative to direction)
            if (dx, dy) == (0, 1):      # → (Moving right)
                dx, dy = -1, 0          # go ↑
            elif (dx, dy) == (0, -1):   # ← (Moving left)
                dx, dy = -1, 0          # go ↑
            elif (dx, dy) == (1, 0):    # ↓ (Moving down)
                dx, dy = 0, -1          # go ←
            elif (dx, dy) == (-1, 0):   # ↑ (Moving up)
                dx, dy = 0, -1          # go ←
        elif mine2:
            # Diagonal to lower-left (relative to direction)
            if (dx, dy) == (0, 1):      # → (Moving right)
                dx, dy = 1, 0           # go ↓ (down)
            elif (dx, dy) == (0, -1):   # ← (Moving left)
                dx, dy = 1, 0           # go ↓ (down)
            elif (dx, dy) == (1, 0):    # ↓ (Moving down)
                dx, dy = 0, -1          # go ← (left)
            elif (dx, dy) == (-1, 0):   # ↑ (Moving up)
                dx, dy = 0, -1          # go ← (left)

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
            trace_ray(user_input)
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
