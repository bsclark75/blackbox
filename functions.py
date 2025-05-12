from Constants import GRID_SIZE,LETTERS
import random

def randomize_mines(grid_size=8, mine_count=10):
    """Randomly generate unique mine locations on a grid."""
    if mine_count > grid_size ** 2:
        raise ValueError("Too many mines for the given grid size.")

    all_positions = [(row, col) for row in range(grid_size) for col in range(grid_size)]
    random.shuffle(all_positions)
    return all_positions[:mine_count]


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

def label_to_coord_and_dir(label):
    if label in LETTERS:
        i = LETTERS.index(label)
        if i < GRID_SIZE:
            return (i, -1), (0, 1)  # LEFT → RIGHT
        else:
            return (i - GRID_SIZE, GRID_SIZE), (0, -1)  # RIGHT → LEFT
    elif label.isdigit():
        i = int(label)
        if i < GRID_SIZE:
            return (-1, i), (1, 0)  # TOP → DOWN
        elif i < GRID_SIZE * 2:
            return (GRID_SIZE, i - GRID_SIZE), (-1, 0)  # BOTTOM → UP
    return None, None
