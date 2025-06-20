import unittest
from game_elements import Board, Tetromino
from settings import GRID_WIDTH, GRID_HEIGHT, BLACK # Assuming BLACK is (0,0,0) or a similar "empty" indicator for color_grid if needed for some tests

# SHAPES and COLORS are class attributes of Tetromino
SHAPES = Tetromino.SHAPES
COLORS = Tetromino.COLORS

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board_empty(self):
        """Test if a new board's logical grid is empty (all zeros)."""
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                self.assertEqual(self.board.grid[r][c], 0, f"Cell ({r},{c}) should be empty (0)")

    def test_add_tetromino(self):
        """Add a tetromino to the board and check if the corresponding cells are marked."""
        tetromino = Tetromino('T', self.board) # 'T' shape: [[0, 1, 0], [1, 1, 1]]
        tetromino.x = 3
        tetromino.y = 5
        self.board.add_tetromino(tetromino)

        # Expected cells to be filled by a 'T' shape at (3,5)
        # Shape: [[0,1,0],[1,1,1]] (relative to tetromino's top-left)
        # (5, 3+1), (6, 3), (6, 3+1), (6, 3+2)
        expected_filled_cells = [
            (5, 4), (6, 3), (6, 4), (6, 5)
        ]
        for r_idx, row_data in enumerate(tetromino.shape):
            for c_idx, cell in enumerate(row_data):
                if cell:
                    board_r, board_c = tetromino.y + r_idx, tetromino.x + c_idx
                    self.assertEqual(self.board.grid[board_r][board_c], 1, f"Cell ({board_r},{board_c}) should be marked as filled (1)")
                    self.assertEqual(self.board.color_grid[board_r][board_c], tetromino.color, f"Cell ({board_r},{board_c}) should have tetromino color")

        # Check a few surrounding cells to ensure they are still empty
        self.assertEqual(self.board.grid[5][3], 0)
        self.assertEqual(self.board.grid[7][4], 0)


    def test_is_valid_position_empty_board(self):
        """Test if a tetromino can be placed in various valid positions on an empty board."""
        tetromino = Tetromino('L', self.board)

        # Test center
        tetromino.x = GRID_WIDTH // 2 - 1
        tetromino.y = GRID_HEIGHT // 2
        self.assertTrue(self.board.is_valid_position(tetromino), "Should be valid in center")

        # Test top-left
        tetromino.x = 0
        tetromino.y = 0
        self.assertTrue(self.board.is_valid_position(tetromino), "Should be valid at top-left")

        # Test bottom-right (considering tetromino height and width)
        shape_height = len(tetromino.shape)
        shape_width = len(tetromino.shape[0])
        tetromino.x = GRID_WIDTH - shape_width
        tetromino.y = GRID_HEIGHT - shape_height
        self.assertTrue(self.board.is_valid_position(tetromino), "Should be valid at bottom-right boundary")

    def test_is_valid_position_with_landed_blocks(self):
        """Place some blocks, then test valid and collision cases."""
        # Create a landed block (e.g., a 1x1 block)
        # For simplicity, directly modify grid. In real scenario, use add_tetromino.
        self.board.grid[5][5] = 1
        self.board.color_grid[5][5] = COLORS['I'] # Assign some color

        tetromino = Tetromino('O', self.board) # 'O' is a 2x2

        # Valid position near the landed block
        tetromino.x = 3
        tetromino.y = 3 # O-shape is at (3,3), (3,4), (4,3), (4,4) - no collision with (5,5)
        self.assertTrue(self.board.is_valid_position(tetromino), "Should be valid near landed block")

        # Collision case: Try to place 'O' directly on the landed block
        tetromino.x = 4
        tetromino.y = 4 # O-shape is at (4,4),(4,5),(5,4),(5,5). (5,5) will collide.
        self.assertFalse(self.board.is_valid_position(tetromino), "Should not be valid due to collision")

        # Collision with offset
        tetromino.x = 3
        tetromino.y = 3
        self.assertTrue(self.board.is_valid_position(tetromino)) # Valid at (3,3)
        # Try to move it onto the block at (5,5) using offset
        # O-shape: (3+dx, 3+dy), (3+dx, 4+dy), (4+dx, 3+dy), (4+dx, 4+dy)
        # We want one of these to be (5,5)
        # If dx=1, dy=1, then (4+dx, 4+dy) = (4+1, 4+1) = (5,5)
        self.assertFalse(self.board.is_valid_position(tetromino, offset_x=1, offset_y=1), "Should collide with offset")


    def test_is_valid_position_out_of_bounds(self):
        """Test placing tetrominoes partially or fully outside boundaries."""
        tetromino = Tetromino('I', self.board) # 'I' shape is [[1,1,1,1]]

        # Too far left
        tetromino.x = -1
        tetromino.y = 0
        self.assertFalse(self.board.is_valid_position(tetromino), "Should be invalid (too far left)")

        # Partially left
        tetromino.x = -2 # Shape: x-coords -2, -1, 0, 1
        tetromino.y = 0
        self.assertFalse(self.board.is_valid_position(tetromino, offset_x=1), "Should be invalid (partially left with offset)")


        # Too far right
        tetromino.x = GRID_WIDTH # Starts at col 10, shape is 4 wide, so 10,11,12,13 are out
        tetromino.y = 0
        self.assertFalse(self.board.is_valid_position(tetromino), "Should be invalid (too far right)")

        tetromino.x = GRID_WIDTH - 3 # Starts at 7, shape: 7,8,9,10. 10 is out.
        tetromino.y = 0
        self.assertFalse(self.board.is_valid_position(tetromino, offset_x=1), "Should be invalid (partially right with offset)")


        # Too far down
        tetromino.x = 0
        tetromino.y = GRID_HEIGHT # Starts at row 20 for a 1-row high piece, so it's out
        self.assertFalse(self.board.is_valid_position(tetromino), "Should be invalid (too far down)")

        tetromino.y = GRID_HEIGHT -1
        self.assertTrue(self.board.is_valid_position(tetromino)) # Valid
        self.assertFalse(self.board.is_valid_position(tetromino, offset_y=1), "Should be invalid (partially down with offset)")

        # Too far up (y < 0)
        tetromino.x = 0
        tetromino.y = -1
        self.assertFalse(self.board.is_valid_position(tetromino), "Should be invalid (too far up)")


    def test_clear_single_line(self):
        """Fill one line, complete it, and check if cleared and count is correct."""
        line_to_fill = GRID_HEIGHT - 1 # Bottom line
        for c in range(GRID_WIDTH):
            self.board.grid[line_to_fill][c] = 1
            self.board.color_grid[line_to_fill][c] = COLORS['I']

        # Add a tetromino that doesn't complete the line yet
        # (This part of test is more about setup integrity)
        # For example, place a piece above the filled line
        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 1, "Line should be cleared")

        # Check if the line is now empty (all zeros)
        for c in range(GRID_WIDTH):
            self.assertEqual(self.board.grid[line_to_fill][c], 0, f"Cell ({line_to_fill},{c}) on cleared line should be 0")

        # Check if the top line is empty (newly added row)
        for c in range(GRID_WIDTH):
            self.assertEqual(self.board.grid[0][c], 0, f"Top line cell ({0},{c}) should be 0 after clear")


    def test_clear_multiple_lines(self):
        """Fill and complete multiple lines (e.g., 2 and 4 lines) and check."""
        # Test clearing 2 lines
        for r in range(GRID_HEIGHT - 2, GRID_HEIGHT): # Fill bottom two lines
            for c in range(GRID_WIDTH):
                self.board.grid[r][c] = 1
                self.board.color_grid[r][c] = COLORS['L']

        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 2, "Should have cleared 2 lines")
        for r in range(GRID_HEIGHT - 2, GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                self.assertEqual(self.board.grid[r][c], 0, f"Cell ({r},{c}) on cleared lines should be 0")
        for c in range(GRID_WIDTH): # Check top two new lines
            self.assertEqual(self.board.grid[0][c], 0)
            self.assertEqual(self.board.grid[1][c], 0)

        # Reset board for 4-line clear test
        self.board = Board()
        for r in range(GRID_HEIGHT - 4, GRID_HEIGHT): # Fill bottom four lines
            for c in range(GRID_WIDTH):
                self.board.grid[r][c] = 1
                self.board.color_grid[r][c] = COLORS['O']

        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 4, "Should have cleared 4 lines (Tetris)")
        for r in range(GRID_HEIGHT - 4, GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                self.assertEqual(self.board.grid[r][c], 0, f"Cell ({r},{c}) on cleared lines should be 0 (4-line clear)")
        for i in range(4): # Check top four new lines
             for c in range(GRID_WIDTH):
                self.assertEqual(self.board.grid[i][c], 0)


    def test_rows_shift_down_after_line_clear(self):
        """After clearing a line, verify that rows above it shift down correctly."""
        # Setup:
        # Row H-1: Full XXXXXXXXXX (will be cleared)
        # Row H-2: Partial 00X00X00X0
        # Row H-3: Empty   0000000000

        # Fill H-1 completely
        for c in range(GRID_WIDTH):
            self.board.grid[GRID_HEIGHT - 1][c] = 1
            self.board.color_grid[GRID_HEIGHT - 1][c] = COLORS['I']

        # Fill H-2 partially
        self.board.grid[GRID_HEIGHT - 2][2] = 1; self.board.color_grid[GRID_HEIGHT - 2][2] = COLORS['L']
        self.board.grid[GRID_HEIGHT - 2][5] = 1; self.board.color_grid[GRID_HEIGHT - 2][5] = COLORS['L']
        self.board.grid[GRID_HEIGHT - 2][8] = 1; self.board.color_grid[GRID_HEIGHT - 2][8] = COLORS['L']

        original_row_h_minus_2_state = list(self.board.grid[GRID_HEIGHT - 2]) # shallow copy
        original_color_row_h_minus_2_state = list(self.board.color_grid[GRID_HEIGHT - 2])


        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 1)

        # Row H-1 (which was H-2) should now have the state of original H-2
        self.assertListEqual(list(self.board.grid[GRID_HEIGHT - 1]), original_row_h_minus_2_state, "Row H-2 did not shift to H-1 correctly (grid)")
        self.assertListEqual(list(self.board.color_grid[GRID_HEIGHT - 1]), original_color_row_h_minus_2_state, "Row H-2 did not shift to H-1 correctly (color_grid)")


        # Row H-2 (which was H-3) should be empty
        for c in range(GRID_WIDTH):
            self.assertEqual(self.board.grid[GRID_HEIGHT - 2][c], 0, "Row H-2 (new) should be empty")

        # Top row should be empty
        for c in range(GRID_WIDTH):
            self.assertEqual(self.board.grid[0][c], 0, "Top row should be empty")


    def test_no_lines_cleared(self):
        """Test that if no lines are full, clear_lines returns 0 and board is unchanged."""
        self.board.grid[GRID_HEIGHT - 1][0] = 1 # Partially fill bottom line
        self.board.grid[GRID_HEIGHT - 2][GRID_WIDTH -1] = 1 # Partially fill line above

        original_grid_state = [list(row) for row in self.board.grid] # Deep copy

        lines_cleared = self.board.clear_lines()
        self.assertEqual(lines_cleared, 0, "Should clear 0 lines")

        self.assertListEqual(self.board.grid, original_grid_state, "Board grid should be unchanged when no lines are cleared")


class TestTetromino(unittest.TestCase):
    def setUp(self):
        self.board = Board() # Tetromino constructor needs a board instance

    def test_tetromino_creation(self):
        """Check if tetrominoes are created with correct shape and initial position."""
        for shape_name, shape_matrix in SHAPES.items():
            tetromino = Tetromino(shape_name, self.board)
            self.assertEqual(tetromino.shape, shape_matrix, f"Initial shape for {shape_name} is incorrect")
            self.assertEqual(tetromino.color, COLORS[shape_name], f"Color for {shape_name} is incorrect")

            expected_x = GRID_WIDTH // 2 - len(shape_matrix[0]) // 2
            self.assertEqual(tetromino.x, expected_x, f"Initial x position for {shape_name} is incorrect")
            self.assertEqual(tetromino.y, 0, f"Initial y position for {shape_name} should be 0")

    def test_tetromino_L_shape_rotation(self):
        """Test rotation sequence for L-shape tetromino."""
        # Assuming self.board.is_valid_position will always be true for these rotations
        # or that the piece is placed far from any collision points.
        # The nudge logic in Tetromino.rotate might complicate this if not handled.
        # For this test, we primarily check the shape transformation.
        tetromino = Tetromino('L', self.board)
        tetromino.x = GRID_WIDTH // 2 # Place it somewhere it can rotate freely
        tetromino.y = 3

        # From SHAPES['L'] = [[0, 0, 1], [1, 1, 1]]
        shape_0 = [[0, 0, 1], [1, 1, 1]]
        shape_1 = [[1, 0], [1, 0], [1, 1]] # After 1 rotation
        shape_2 = [[1, 1, 1], [1, 0, 0]] # After 2 rotations
        shape_3 = [[0, 1], [0, 1], [1, 1]] # After 3 rotations (Corrected from [[1,1],[0,1],[0,1]])

        self.assertEqual(tetromino.shape, shape_0, "Initial L-shape incorrect")

        tetromino.rotate() # 1st rotation
        self.assertEqual(tetromino.shape, shape_1, "L-shape rotation 1 incorrect")

        tetromino.rotate() # 2nd rotation
        self.assertEqual(tetromino.shape, shape_2, "L-shape rotation 2 incorrect")

        tetromino.rotate() # 3rd rotation
        self.assertEqual(tetromino.shape, shape_3, "L-shape rotation 3 incorrect")

        tetromino.rotate() # 4th rotation (back to original)
        self.assertEqual(tetromino.shape, shape_0, "L-shape rotation 4 (back to original) incorrect")

    def test_tetromino_T_shape_rotation(self):
        """Test rotation sequence for T-shape tetromino."""
        tetromino = Tetromino('T', self.board)
        tetromino.x = GRID_WIDTH // 2
        tetromino.y = 3

        # From SHAPES['T'] = [[0, 1, 0], [1, 1, 1]]
        shape_0 = [[0, 1, 0], [1, 1, 1]]
        shape_1 = [[1, 0], [1, 1], [1, 0]]
        shape_2 = [[1, 1, 1], [0, 1, 0]]
        shape_3 = [[0, 1], [1, 1], [0, 1]]

        self.assertEqual(tetromino.shape, shape_0, "Initial T-shape incorrect")
        tetromino.rotate()
        self.assertEqual(tetromino.shape, shape_1, "T-shape rotation 1 incorrect")
        tetromino.rotate()
        self.assertEqual(tetromino.shape, shape_2, "T-shape rotation 2 incorrect")
        tetromino.rotate()
        self.assertEqual(tetromino.shape, shape_3, "T-shape rotation 3 incorrect")
        tetromino.rotate()
        self.assertEqual(tetromino.shape, shape_0, "T-shape rotation 4 incorrect")

    def test_tetromino_I_shape_rotation(self):
        """Test rotation sequence for I-shape tetromino."""
        tetromino = Tetromino('I', self.board)
        tetromino.x = GRID_WIDTH // 2 - 2 # I is 4 wide
        tetromino.y = 3

        # From SHAPES['I'] = [[1, 1, 1, 1]]
        shape_horizontal = [[1, 1, 1, 1]]
        shape_vertical = [[1], [1], [1], [1]]

        self.assertEqual(tetromino.shape, shape_horizontal, "Initial I-shape incorrect")

        tetromino.rotate() # 1st rotation
        self.assertEqual(tetromino.shape, shape_vertical, "I-shape rotation 1 (to vertical) incorrect")

        tetromino.rotate() # 2nd rotation
        self.assertEqual(tetromino.shape, shape_horizontal, "I-shape rotation 2 (to horizontal) incorrect")

        tetromino.rotate() # 3rd rotation
        self.assertEqual(tetromino.shape, shape_vertical, "I-shape rotation 3 (to vertical) incorrect")

        tetromino.rotate() # 4th rotation
        self.assertEqual(tetromino.shape, shape_horizontal, "I-shape rotation 4 (to horizontal) incorrect")


if __name__ == '__main__':
    unittest.main()
