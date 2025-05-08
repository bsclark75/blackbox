import unittest
from grid import Grid

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(size=8, mines={(1, 7), (3, 5), (6, 0)})

    def test_grid_size(self):
        self.assertEqual(self.grid.size, 8)

    def test_mine_count(self):
        self.assertEqual(len(self.grid.mines), 3)

    def test_mine_positions(self):
        self.assertIn((1, 7), self.grid.mines)
        self.assertIn((3, 5), self.grid.mines)
        self.assertIn((6, 0), self.grid.mines)

    def test_out_of_bounds_mine_check(self):
        # Assuming has_mine handles out-of-bounds checks gracefully
        if hasattr(self.grid, 'has_mine'):
            self.assertFalse(self.grid.has_mine(-1, 0))
            self.assertFalse(self.grid.has_mine(8, 8))

    def test_has_mine(self):
        if hasattr(self.grid, 'has_mine'):
            self.assertTrue(self.grid.has_mine(1, 7))
            self.assertFalse(self.grid.has_mine(2, 2))

    def test_mine_not_in_wrong_location(self):
        self.assertNotIn((0, 0), self.grid.mines)
        self.assertNotIn((7, 7), self.grid.mines)

if __name__ == '__main__':
    unittest.main()
