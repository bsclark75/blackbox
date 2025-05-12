import unittest
from ray import Ray
from grid import Grid  # Assuming your grid class is in grid.py
from Constants import GRID_SIZE

class TestRay(unittest.TestCase):
    def setUp(self):
        # Basic setup that runs before each test
        self.empty_grid = Grid(GRID_SIZE)
        
    def test_initialization(self):
        """Test that Ray initializes correctly"""
        start = (0, 0)
        direction = (0, 1)  # Moving right
        ray = Ray(start, direction, self.empty_grid)
        
        self.assertEqual(ray.x, 0)
        self.assertEqual(ray.y, 0)
        self.assertEqual(ray.dx, 0)
        self.assertEqual(ray.dy, 1)
        self.assertEqual(len(ray.visited), 0)

    def test_direct_hit(self):
        """Test ray hitting a mine directly"""
        grid = Grid(GRID_SIZE)
        grid.add_mine(1, 1)
        
        ray = Ray((0, 1), (1, 0), grid)  # Moving down towards mine
        result = ray.move()
        self.assertEqual(result, "Absorbed")

    def test_exit_points(self):
        """Test ray exiting the grid from different directions"""
        test_cases = [
            ((0, 7), (0, -1), "A"),  # Exit left
            ((7, 0), (-1, 0), "0"),  # Exit top
            ((7, 0), (0, 1), "P"),   # Exit right
            ((0, 7), (1, 0), "15")    # Exit bottom
        ]
        
        for start, direction, expected in test_cases:
            with self.subTest(start=start, direction=direction):
                ray = Ray(start, direction, self.empty_grid)
                result = ray.move()
                self.assertEqual(result, expected)

    def test_deflections(self):
        """Test ray deflections from diagonal mines"""
        grid = Grid(GRID_SIZE)
        # Set up mines for a single deflection
        grid.add_mine(1, 2)  # Diagonal mine
        
        # Test right deflection
        ray = Ray((0, 1), (1, 0), grid)  # Moving down
        result = ray.move()
        self.assertEqual((ray.dx, ray.dy), (0, -1))  # Should deflect left

    def test_reflection(self):
        """Test ray reflection from two diagonal mines"""
        grid = Grid(GRID_SIZE)
        # Set up mines for reflection
        grid.add_mine(1, 2)
        grid.add_mine(1, 0)
        
        ray = Ray((0, 1), (1, 0), grid)  # Moving down
        result = ray.move()
        self.assertEqual(result, "Reflected")
    """
    def test_loop_detection(self):
        #Test detection of infinite loops
        grid = Grid(GRID_SIZE)
        # Set up mines to create a loop
        grid.add_mine(1, 2)
        grid.add_mine(2, 1)
        grid.add_mine(1, 0)
        grid.add_mine(0, 1)
        
        ray = Ray((1, 1), (0, 1), grid)  # Moving right
        result = ray.move()
        self.assertEqual(result, "Loop")
        """

 
if __name__ == '__main__':
    unittest.main()
