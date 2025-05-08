from functions import coord_to_label

class Ray:
    def __init__(self, start, direction, grid):
        self.x, self.y = start
        self.dx, self.dy = direction
        self.grid = grid
        self.visited = set()

    def move(self):
        while True:
            if not (0 <= self.x < self.grid.size and 0 <= self.y < self.grid.size):
                return coord_to_label((self.x, self.y))  # Exit point

            if (self.x, self.y) in self.grid.mines:
                return "Absorbed"

            # Check diagonals relative to current position
            diag1 = (self.x + self.dy, self.y - self.dx)
            diag2 = (self.x - self.dy, self.y + self.dx)

            mine1 = diag1 in self.grid.mines
            mine2 = diag2 in self.grid.mines

            print(f"Ray at ({self.x},{self.y}) moving ({self.dx},{self.dy}), diag1={diag1}, diag2={diag2}, mine1={mine1}, mine2={mine2}")

            if mine1 and mine2:
                return "Reflected"
            elif mine1:
                self.deflect_left()
            elif mine2:
                self.deflect_right()

            if (self.x, self.y, self.dx, self.dy) in self.visited:
                return "Loop"
            self.visited.add((self.x, self.y, self.dx, self.dy))

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
