import pygame
from settings import *

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.block_size = SCREEN_HEIGHT // GRID_HEIGHT
        # Store colors of landed blocks
        self.color_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


    def is_valid_position(self, tetromino, offset_x=0, offset_y=0):
        """Checks if the tetromino's position (with optional offset) is valid."""
        for r_idx, row in enumerate(tetromino.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    board_x = tetromino.x + c_idx + offset_x
                    board_y = tetromino.y + r_idx + offset_y
                    # Check bounds
                    if not (0 <= board_x < GRID_WIDTH and 0 <= board_y < GRID_HEIGHT):
                        return False
                    # Check collision with existing blocks
                    if self.grid[board_y][board_x] != 0:
                        return False
        return True

    def add_tetromino(self, tetromino):
        """Adds a landed tetromino to the board's grid."""
        for r_idx, row in enumerate(tetromino.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    self.grid[tetromino.y + r_idx][tetromino.x + c_idx] = 1 # Mark as filled
                    self.color_grid[tetromino.y + r_idx][tetromino.x + c_idx] = tetromino.color


    def clear_lines(self):
        """Checks for and clears completed lines, then shifts rows down."""
        lines_cleared = 0
        new_grid = []
        new_color_grid = []

        for r in range(GRID_HEIGHT -1, -1, -1): # Iterate from bottom up
            if all(self.grid[r]): # If line is full
                lines_cleared += 1
            else:
                new_grid.insert(0, self.grid[r])
                new_color_grid.insert(0, self.color_grid[r])

        # Add empty rows at the top for cleared lines
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            new_color_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])

        if lines_cleared > 0:
            self.grid = new_grid
            self.color_grid = new_color_grid

        return lines_cleared

    def draw(self, screen):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                # Draw the landed blocks with their colors
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, self.color_grid[y][x], rect)
                # Draw the grid lines
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)


class Tetromino:
    SHAPES = {
        "I": [[1, 1, 1, 1]],
        "J": [[1, 0, 0], [1, 1, 1]],
        "L": [[0, 0, 1], [1, 1, 1]],
        "O": [[1, 1], [1, 1]],
        "S": [[0, 1, 1], [1, 1, 0]],
        "T": [[0, 1, 0], [1, 1, 1]],
        "Z": [[1, 1, 0], [0, 1, 1]]
    }
    COLORS = {
        "I": (0, 255, 255),  # Cyan
        "J": (0, 0, 255),    # Blue
        "L": (255, 165, 0),  # Orange
        "O": (255, 255, 0),  # Yellow
        "S": (0, 255, 0),    # Green
        "T": (128, 0, 128),  # Purple
        "Z": (255, 0, 0)     # Red
    }

    def __init__(self, shape_name, board): # Added board reference
        self.shape_name = shape_name
        self.shape = self.SHAPES[shape_name]
        self.color = self.COLORS[shape_name]
        # Position: col (x), row (y)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.board = board # Store a reference to the board for collision checks

    def rotate(self):
        """Rotates the tetromino 90 degrees clockwise."""
        # Transpose the shape matrix
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]

        # Check if the rotated shape is valid before applying
        # This is a basic check; more complex wall kick logic might be needed
        original_shape = self.shape
        self.shape = rotated_shape
        if not self.board.is_valid_position(self):
            # If not valid, try to nudge left/right
            if self.board.is_valid_position(self, offset_x=-1):
                self.x -= 1
            elif self.board.is_valid_position(self, offset_x=1):
                self.x += 1
            elif self.board.is_valid_position(self, offset_x=-2): # For I piece
                self.x -=2
            elif self.board.is_valid_position(self, offset_x=2): # For I piece
                self.x += 2
            else: # If still not valid, revert rotation
                self.shape = original_shape
        # Ensure x is within bounds after rotation and nudge
        if self.x < 0:
            self.x = 0
        elif self.x + len(self.shape[0]) > GRID_WIDTH:
            self.x = GRID_WIDTH - len(self.shape[0])


    def draw(self, screen, block_size):
        """Draws the tetromino on the screen."""
        for r_idx, row in enumerate(self.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        ( (self.x + c_idx) * block_size, (self.y + r_idx) * block_size, block_size, block_size)
                    )

    def draw_at(self, screen, x_offset, y_offset, block_size):
        """Draws the tetromino at a specific pixel offset, used for preview."""
        for r_idx, row in enumerate(self.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        self.color,
                        (x_offset + c_idx * block_size, y_offset + r_idx * block_size, block_size, block_size)
                    )
