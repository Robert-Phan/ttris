import pygame
from type_aliases import *

class Graphic:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([1280, 720])
        pygame.font.init()
        self.draw_grid()
        self.draw_hold_grid()
        self.init_block_rects()

    margin_left = 10
    margin_top = 10
    cell_size = 30
    cell_border = 2

    grid_margin_left = margin_left * 2 - cell_border * 3 + cell_size * 4 
    main_margin_top = margin_top + cell_size * 2 
    block_size = cell_size - cell_border * 2

    grid_width = 10
    grid_height = 20

    def draw_grid(self):
        """
        Draws the Tetris grid upon game initialization.
        """

        for i in range(self.grid_height):
            for j in range(self.grid_width):
                cell_top_pos = self.main_margin_top + i * (self.cell_size - self.cell_border)
                cell_left_pos = self.grid_margin_left + j * (self.cell_size - self.cell_border)

                grid_cell = pygame.Rect(
                    cell_left_pos,
                    cell_top_pos,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, (200, 200, 200),
                                grid_cell, self.cell_border)

        for i in range(-2, 0):
            for j in range(self.grid_width):
                danger_cell_top_pos = self.main_margin_top + i * (self.cell_size - self.cell_border)
                danger_cell_left_pos = self.grid_margin_left + j * (self.cell_size - self.cell_border)

                grid_cell = pygame.Rect(
                    danger_cell_left_pos,
                    danger_cell_top_pos,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, (230, 86, 86),
                                grid_cell, self.cell_border)

        pygame.display.flip()
    
    def draw_hold_grid(self):
        for i in range(2):
            for j in range(4):
                cell_top_pos = self.main_margin_top + i * (self.cell_size - self.cell_border)
                cell_left_pos = self.margin_left + j * (self.cell_size - self.cell_border)

                grid_cell = pygame.Rect(
                    cell_left_pos,
                    cell_top_pos,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, (200, 200, 200),
                                grid_cell, self.cell_border)

    current_tetrimino: list[Block] = []
    held_tetrimino: ColoredTetrimino = []
    tetrimino_color = (55, 155, 255)

    def init_block_rects(self):
        self.block_rects = [
            pygame.Rect(-self.cell_size, 0, self.block_size, self.block_size)
            for _ in range(0, 4)
        ]

    def draw_tetrimino(self, draw_tetromino_settings: DrawTetrominoSettings):
        if draw_tetromino_settings == "hold":
            self.draw_hold_tetromino()

        if draw_tetromino_settings == "move" or draw_tetromino_settings == "hold":
            for block_rect in self.block_rects:
                pygame.draw.rect(self.screen, (0, 0, 0), block_rect)

        for ((x, y), block_rect) in zip(self.current_tetrimino[:-1], self.block_rects):
            (rect_x, rect_y) = self.block_coords_to_grid_position(x, y)

            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
            pygame.draw.rect(self.screen, self.tetrimino_color, block_rect)

        pygame.display.flip()
    
    def draw_hold_tetromino(self):
        block_rect = pygame.Rect(-1, -1, self.block_size, self.block_size)

        for y in range(2):
            for x in range(4):
                (rect_x, rect_y) = self.block_coords_to_grid_position(x, y, for_holding=True)

                block_rect.update(rect_x, rect_y, 
                                block_rect.width, block_rect.height)
                pygame.draw.rect(self.screen, (0, 0, 0), block_rect)

        for (x, y) in self.held_tetrimino[0][:-1]:
            (rect_x, rect_y) = self.block_coords_to_grid_position(x, y, for_holding=True)

            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
            pygame.draw.rect(self.screen, self.held_tetrimino[1], block_rect)
        
        pygame.display.flip()

    def block_coords_to_grid_position(self, block_x: int, block_y: int, for_holding = False):
        margin_left = self.margin_left if for_holding else self.grid_margin_left
        rect_x = margin_left + block_x * (self.cell_size - self.cell_border) + self.cell_border
        rect_y = self.main_margin_top + block_y * (self.cell_size - self.cell_border) + self.cell_border
        return rect_x, rect_y
    
    fallen_blocks: set[ColoredBlock] = set()

    def update_fallen_block(self, new_fallen_blocks: set[ColoredBlock], clear_line = False):
        if not clear_line:
            self.fallen_blocks = new_fallen_blocks
            return
        
        block_rect = pygame.Rect(-1, -1, self.block_size, self.block_size)

        for ((x, y), _) in self.fallen_blocks:
            (rect_x, rect_y) = self.block_coords_to_grid_position(x, y)
            
            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
            pygame.draw.rect(self.screen, (0, 0, 0), block_rect)
        
        for ((x, y), color) in new_fallen_blocks:
            (rect_x, rect_y) = self.block_coords_to_grid_position(x, y)
            
            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
            pygame.draw.rect(self.screen, color, block_rect)
        
        pygame.display.flip()

    def game_over(self):
        font = pygame.font.SysFont("jetbrainsmonoextrabold", 100)
        text = font.render("GAME OVER", True, (230, 210, 0))
        self.screen.blit(text, (20, 20))
        pygame.display.flip()
