from Constants import GRID_SIZE,LETTERS

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
