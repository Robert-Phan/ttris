import pygame

Block = tuple[int, int]

class Graphic:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([1280, 720])
        self.draw_grid()
        self.init_block_rects()

    grid_padding_left = 10
    grid_padding_top = 10
    cell_size = 30
    cell_border = 2
    grid_width = 10
    grid_height = 20

    def draw_grid(self):
        """
        Draws the Tetris grid upon game initialization.
        """

        for i in range(0, self.grid_height):
            for j in range(0, self.grid_width):
                cell_top_pos = self.grid_padding_top + i * (self.cell_size - self.cell_border)
                cell_left_pos = self.grid_padding_left + j * (self.cell_size - self.cell_border)

                grid_cell = pygame.Rect(
                    cell_left_pos,
                    cell_top_pos,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, (200, 200, 200),
                                grid_cell, self.cell_border)

        pygame.display.flip()

    tetrimino_blocks: list[Block] = []

    tetrimino_color = (55, 155, 255)

    def init_block_rects(self):
        block_size = self.cell_size - self.cell_border * 2
        self.block_rects = [
            pygame.Rect(-self.cell_size, 0, block_size, block_size)
            for _ in range(0, 4)
        ]

    def draw_tetrimino(self, is_for_refresh: bool):
        if not is_for_refresh:
            for block_rect in self.block_rects:
                pygame.draw.rect(self.screen, (0, 0, 0), block_rect)

        for ((x, y), block_rect) in zip(self.tetrimino_blocks, self.block_rects):
            rect_x = self.grid_padding_left + x * (self.cell_size - self.cell_border) + self.cell_border
            rect_y = self.grid_padding_left + y * (self.cell_size - self.cell_border) + self.cell_border

            block_rect.update(rect_x, rect_y, 
                            block_rect.width, block_rect.height)
            pygame.draw.rect(self.screen, self.tetrimino_color, block_rect)

        pygame.display.flip()
