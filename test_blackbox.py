import unittest

# Import your functions and set up your grid context
from main import follow_ray, label_to_coord_and_dir, mines, coord_to_label

class TestRayLogic(unittest.TestCase):
    def setUp(self):
        # Set fixed mine locations for predictable tests
        self.mines = {(2, 3), (5, 5), (6, 1)}
        mines.clear()
        mines.update(self.mines)

    def trace(self, label):
        start, direction = label_to_coord_and_dir(label)
        return follow_ray(start, direction)

    def test_absorbed_direct_hit(self):
        self.assertEqual(self.trace("3"), "Absorbed")  # Down from top to (2,3)

    def test_reflection(self):
        # Ray passes between (2,3) and another mine at (3,2) (if we had one)
        mines.clear()
        mines.update({(2, 3), (0, 3)})
        self.assertEqual(self.trace("B"), "Reflected")

    def test_deflect_up(self):
        # Should deflect up due to (2,3) being diagonally down-right
        mines.clear()
        mines.add((2, 3))
        self.assertEqual(self.trace("B"), "2")

    def test_deflect_down(self):
        # Should deflect down due to mine diagonally up-right
        mines.clear()
        mines.add((0, 3))  # Above-right from (1,2) going right
        self.assertEqual(self.trace("B"), "10")

    """
    def test_loop(self):
        # Create a loop trap
        mines.clear()
        mines.update({(1,2), (2,3), (3,2), (2,1)})
        self.assertEqual(self.trace("B"), "Loop") 
    """

    def test_clear_pass_through(self):
        # No deflections or hits
        mines.clear()
        self.assertEqual(self.trace("0"), "8")  # From top (0,0) straight down

    def test_exit_bottom(self):
        mines.clear()
        self.assertEqual(self.trace("2"), "10")  # From top column 2 to bottom column 10

    def test_exit_left(self):
        # Enter from bottom edge and pass upward without hitting anything
        mines.clear()
        self.assertEqual(self.trace("10"), "2")  # Enters from (7,2), should go up to top edge

if __name__ == '__main__':
    unittest.main()
