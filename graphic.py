import pygame
from type_aliases import *

class Graphic:    
    grid_width = 10
    grid_height = 20

    margin_left = 10
    margin_top = 10
    cell_size = 30
    cell_border = 2

    four_cell_width = cell_size * 4 - cell_border * 3
    main_margin_left = margin_left * 2 + four_cell_width 
    main_margin_top = margin_top + (cell_size - cell_border) * 2
    block_size = cell_size - cell_border * 2

    preview_margin_left = (main_margin_left + margin_left 
                            + cell_size * grid_width 
                            - cell_border * (grid_width - 1))
    each_preview_margin_top = 3 * (cell_size - cell_border) 

    screen_width = (preview_margin_left 
                    + four_cell_width
                    + margin_left)

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([self.screen_width, 720])
        pygame.font.init()
        self.draw_preview_grid()
        self.draw_hold_grid()
        self.draw_main_grid()
        self.init_block_rects()


    def draw_main_grid(self):
        """
        Draws the Tetris grid upon game initialization.
        """

        for i in range(self.grid_height - 1, -3, -1):
            for j in range(self.grid_width):
                cell_top_pos = self.main_margin_top + i * (self.cell_size - self.cell_border)
                cell_left_pos = self.main_margin_left + j * (self.cell_size - self.cell_border)

                grid_cell = pygame.Rect(
                    cell_left_pos,
                    cell_top_pos,
                    self.cell_size,
                    self.cell_size
                )

                grid_cell_color = (230, 86, 86) if i < 0 else (200, 200, 200)

                pygame.draw.rect(self.screen, grid_cell_color,
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
    
    def draw_preview_grid(self):        
        for h in range(5):
            for i in range(2):
                for j in range(4):
                    cell_top_pos = self.main_margin_top + i * (self.cell_size - self.cell_border) \
                                    + self.each_preview_margin_top * h
                    cell_left_pos = self.preview_margin_left + j * (self.cell_size - self.cell_border)

                    grid_cell = pygame.Rect(
                        cell_left_pos,
                        cell_top_pos,
                        self.cell_size,
                        self.cell_size
                    )

                    pygame.draw.rect(self.screen, (200, 200, 200),
                                    grid_cell, self.cell_border)

    tetrimino_bag: list[ColoredTetrimino] = []
    current_tetrimino: Tetrimino = []
    held_tetrimino: ColoredTetrimino = []
    drop_position: Tetrimino = []
    tetrimino_color = (0, 0, 0)

    def init_block_rects(self):
        self.block_rects = [
            pygame.Rect(-self.cell_size, 0, self.block_size, self.block_size)
            for _ in range(0, 4)
        ]
        self.drop_pos_block_rects = [
            pygame.Rect(-self.cell_size, 0, self.block_size, self.block_size)
            for _ in range(0, 4)
        ]

    def draw_tetrimino(self, draw_tetromino_settings: DrawTetrominoSettings):
        if draw_tetromino_settings != 'move':
            self.draw_preview_tetrominoes()
        
        if draw_tetromino_settings == "hold":
            self.draw_hold_tetromino()
        
        self.draw_drop_position(draw_tetromino_settings)
        
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
                (rect_x, rect_y) = self.block_coords_to_grid_position(x, y, "hold")

                block_rect.update(rect_x, rect_y, 
                                block_rect.width, block_rect.height)
                pygame.draw.rect(self.screen, (0, 0, 0), block_rect)

        for (x, y) in self.held_tetrimino[0][:-1]:
            (rect_x, rect_y) = self.block_coords_to_grid_position(x, y, "hold")

            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
            pygame.draw.rect(self.screen, self.held_tetrimino[1], block_rect)
    
    def draw_drop_position(self, draw_tetromino_settings: DrawTetrominoSettings):
        if draw_tetromino_settings == "move" or draw_tetromino_settings == "hold":
            for block_rect in self.drop_pos_block_rects:
                pygame.draw.rect(self.screen, (0, 0, 0), block_rect)
        
        for ((x, y), block_rect) in zip(self.drop_position[:-1], self.drop_pos_block_rects):
            (rect_x, rect_y) = self.block_coords_to_grid_position(x, y)
            
            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
                    
            pygame.draw.rect(self.screen, self.tetrimino_color, block_rect, 2)
    
    def draw_preview_tetrominoes(self):
        block_rect = pygame.Rect(-1, -1, self.block_size, self.block_size)

        for (h, tetrimino) in enumerate(self.tetrimino_bag[:-6:-1]):
            for y in range(2):
                for x in range (4):
                    (rect_x, rect_y) = self.block_coords_to_grid_position(x, y, "preview")
                    rect_y += self.each_preview_margin_top * h

                    block_rect.update(rect_x, rect_y, 
                                    block_rect.width, block_rect.height)
                    pygame.draw.rect(self.screen, (0, 0, 0), block_rect)
            
            for (x, y) in tetrimino[0][:-1]:
                (rect_x, rect_y) = self.block_coords_to_grid_position(x, y, "preview")
                rect_y += self.each_preview_margin_top * h

                block_rect.update(rect_x, rect_y, 
                                block_rect.width, block_rect.height)
                pygame.draw.rect(self.screen, tetrimino[1], block_rect)
        
        # for tetrimino in self.tetrimino_bag[:5]:
        #     ...

    def block_coords_to_grid_position(self, block_x: int, block_y: int, 
                                    translationSettings: CoordinateTranslationSettings = "main"):

        margin_left = (self.main_margin_left if translationSettings == "main" 
                    else self.margin_left if translationSettings == "hold" 
                    else self.preview_margin_left)

        # margin_top = (self.margin_top if translationSettings == "preview"
        #             else self.main_margin_top)

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
