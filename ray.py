from functions import coord_to_label
from Constants import GRID_SIZE
class Ray:
    def __init__(self, start, direction, grid):
        self.x, self.y = start
        self.dx, self.dy = direction
        self.grid = grid
        self.visited = set()

    def move(self):
       while True:
        # If we're about to step outside, this is the exit point
        if not (0 <= self.x < GRID_SIZE and 0 <= self.y < GRID_SIZE):
            return coord_to_label((self.x, self.y))

        # Direct hit
        if (self.x, self.y) in self.grid.mines:
            return "Absorbed"

        # Check diagonal influence BEFORE moving
        # Compute next cell (where ray is headed)
        next_x = self.x + self.dx
        next_y = self.y + self.dy

        # Check diagonals from the *next* cell
        diag1 = (next_x + self.dy, next_y - self.dx)  # top-right
        diag2 = (next_x - self.dy, next_y + self.dx)  # bottom-left

        mine1 = diag1 in self.grid.mines
        mine2 = diag2 in self.grid.mines

        print(f"Ray at ({self.x},{self.y}) moving ({self.dx},{self.dy}), diag1={diag1}, diag2={diag2}, mine1={mine1}, mine2={mine2}")

        if mine1 and mine2:
            return "Reflected"
        elif mine1:
            # Diagonal to upper-right (relative to direction)
            if (self.dx, self.dy) == (0, 1):      # → (Moving right)
                self.dx, self.dy = -1, 0          # go ↑
            elif (self.dx, self.dy) == (0, -1):   # ← (Moving left)
                self.dx, self.dy = -1, 0          # go ↑
            elif (self.dx, self.dy) == (1, 0):    # ↓ (Moving down)
                self.dx, self.dy = 0, -1          # go ←
            elif (self.dx, self.dy) == (-1, 0):   # ↑ (Moving up)
                self.dx, self.dy = 0, -1          # go ←
        elif mine2:
            # Diagonal to lower-left (relative to direction)
            if (self.dx, self.dy) == (0, 1):      # → (Moving right)
                self.dx, self.dy = 1, 0           # go ↓ (down)
            elif (self.dx, self.dy) == (0, -1):   # ← (Moving left)
                self.dx, self.dy = 1, 0           # go ↓ (down)
            elif (self.dx, self.dy) == (1, 0):    # ↓ (Moving down)
                self.dx, self.dy = 0, -1          # go ← (left)
            elif (self.dx, self.dy) == (-1, 0):   # ↑ (Moving up)
                self.dx, self.dy = 0, -1          # go ← (left)

        # Detect potential infinite loop
        if (self.x, self.y, self.dx, self.dy) in self.visited:
            return "Loop"
        self.visited.add((self.x, self.y, self.dx, self.dy))

        # Now move
        self.x += self.dx
        self.y += self.dy

    def deflect_left(self):
        if (self.dx, self.dy) == (0, 1):      # →
            self.dx, self.dy = -1, 0          # ↑
        elif (self.dx, self.dy) == (0, -1):   # ←
            self.dx, self.dy = 1, 0           # ↓
        elif (self.dx, self.dy) == (1, 0):    # ↓
            self.dx, self.dy = 0, -1          # ←
        elif (self.dx, self.dy) == (-1, 0):   # ↑
            self.dx, self.dy = 0, 1           # →

    def deflect_right(self):
        if (self.dx, self.dy) == (0, 1):      # →
            self.dx, self.dy = 1, 0           # ↓
        elif (self.dx, self.dy) == (0, -1):   # ←
            self.dx, self.dy = -1, 0          # ↑
        elif (self.dx, self.dy) == (1, 0):    # ↓
            self.dx, self.dy = 0, 1           # →
        elif (self.dx, self.dy) == (-1, 0):   # ↑
            self.dx, self.dy = 0, -1          # ←
