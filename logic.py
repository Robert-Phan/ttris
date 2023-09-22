import pygame
from pygame.event import Event
from typing import Callable, Self, Optional
import random

from graphic import Graphic
from type_aliases import *

class Logic:
    def __init__(self, graphic: Graphic) -> None:
        self.graphic = graphic
        self.refresh_tetrimino()
        self.event_loop()

    current_tetrimino: Tetrimino = []
    held_tetrimino: ColoredTetrimino = ()
    movement_event_key: Optional[int] = None
    movement_event: Optional[Event] = None
    
    MOVEKEYHELD = pygame.USEREVENT + 1
    TETROMINOFALL = pygame.USEREVENT + 2
    GAMEOVER = pygame.USEREVENT + 3

    def event_loop(self):
        event_loop_running = True
        game_over = False

        self.tetromino_fall_loop()

        while event_loop_running:
            if len(pygame.event.get(pygame.QUIT)) > 0:
                event_loop_running = False

            if game_over:
                continue

            for event in pygame.event.get():
                match event:
                    case Event(type=pygame.QUIT):
                        event_loop_running = False
                    case Event(type=self.GAMEOVER):
                        self.graphic.game_over()
                        game_over = True

                    case Event(type=self.TETROMINOFALL):
                        self.shift_tetrimino(pygame.K_DOWN)
                    
                    case Event(type=pygame.KEYDOWN, key=(pygame.K_DOWN | pygame.K_RIGHT | pygame.K_LEFT)):
                        self.movement_event_key = event.key
                        self.shift_tetrimino(event.key)
                    case Event(type=pygame.KEYDOWN, key=(pygame.K_a | pygame.K_d)):
                        self.movement_event_key = event.key
                        self.rotate_tetrimino(event.key)
                    case Event(type=pygame.KEYUP, key=(pygame.K_DOWN | pygame.K_RIGHT | pygame.K_LEFT | pygame.K_a | pygame.K_d)):
                        self.movement_event_key = None
                    
                    case Event(type=self.MOVEKEYHELD):
                        if self.movement_event != None:
                            pygame.time.set_timer(self.movement_event, 80)
                    
                    case Event(type=pygame.KEYDOWN, key=pygame.K_s):
                        self.hold_tetrimino()
                    
            self.handle_held_movement_key()

    def handle_held_movement_key(self):
        if self.movement_event_key and not self.movement_event:
            self.movement_event = Event(pygame.KEYDOWN, key=self.movement_event_key)
            pygame.time.set_timer(Event(self.MOVEKEYHELD), 200, 1)
        elif not self.movement_event_key and self.movement_event:
            pygame.time.set_timer(self.movement_event, 0)
            self.movement_event = None
        
    def tetromino_fall_loop(self):
        pygame.time.set_timer(self.TETROMINOFALL, 1000)

    def sync_graphic_and_logic(self, draw_tetromino_settings: DrawTetrominoSettings, rows_removed: bool = False):        
        self.graphic.current_tetrimino = [*self.current_tetrimino]
        self.graphic.draw_tetrimino(draw_tetromino_settings)
        self.graphic.update_fallen_block(self.fallen_blocks, rows_removed)

    movement_offsets = {
        pygame.K_DOWN: (0, 1),
        pygame.K_RIGHT: (1, 0),
        pygame.K_LEFT: (-1, 0),
        pygame.K_a: (1, -1),
        pygame.K_d: (-1, 1)
    }

    fallen_blocks: set[ColoredBlock] = set()

    @staticmethod
    def move_tetrimino_decor(move_tetri_func: Callable[[Self, int], Tetrimino]):
        def decorated_move_tetri_func(self: Self, movement_key: int):
            fallen_blocks: set[Block] = {(x, y) for ((x, y), _) in self.fallen_blocks}
            new_tetrimino = move_tetri_func(self, movement_key)

            for (new_x, new_y) in new_tetrimino[:-1]:
                if not (0 <= new_x < 10) or new_y >= 20 or (new_x, new_y) in fallen_blocks:
                    if movement_key == pygame.K_DOWN:
                        self.refresh_tetrimino()
                    return 
            
            self.current_tetrimino = new_tetrimino

            self.sync_graphic_and_logic('move')
        
        return decorated_move_tetri_func
    
    @move_tetrimino_decor
    def shift_tetrimino(self, movement_key: int):
        (offset_x, offset_y) = self.movement_offsets[movement_key]

        new_tetrimino: Tetrimino = [
            ((x + offset_x), (y + offset_y))
            for (x, y) in self.current_tetrimino
        ]

        return new_tetrimino

    @move_tetrimino_decor
    def rotate_tetrimino(self, movement_key: int):
        (rot_offset_x, rot_offset_y) = self.movement_offsets[movement_key]
        (pivot_x, pivot_y) = self.current_tetrimino[-1]

        pivot_adjusted_tetromino = [(x - pivot_x, y - pivot_y) for (x, y) in self.current_tetrimino[:-1]]

        rotated_tetromino = [(y * rot_offset_x, x * rot_offset_y) for (x, y) in pivot_adjusted_tetromino]

        new_tetromino = [(x + pivot_x, y + pivot_y) for (x, y) in rotated_tetromino] 

        return [*new_tetromino, (pivot_x, pivot_y)]
    
    tetrimino_variants: list[ColoredTetrimino] = [
        # I piece
        ([(0, 0),(1, 0),
        (2, 0), (3, 0),
        (1.5, 0.5)], (0, 240, 240)),
        # O piece
        ([(0, 0),(1, 0),
        (0, 1), (1, 1),
        (0.5, 0.5)], (240, 240, 0)),
        # T piece
        ([(0, 0),(1, 0),
        (2, 0), (1, 1),
        (1, 0)], (161, 0, 240)),
        # J piece
        ([(0, 0),(0, 1),
        (1, 1), (2, 1),
        (1, 1)], (0, 0, 240)),
        # L piece
        ([(2, 0),(0, 1),
        (1, 1), (2, 1),
        (1, 1)], (240, 161, 0)),
        # S piece
        ([(1, 0),(2, 0),
        (0, 1), (1, 1),
        (1, 1)], (0, 240, 0)),
        # Z piece
        ([(0, 0),(1, 0),
        (1, 1), (2, 1),
        (1, 1)], (240, 0, 0)),
    ]

    def tetrimino_starting_position(self, tetrimino: Tetrimino):
        start_pos_tetrimino: Tetrimino = [(x + 3, y - 2) for (x, y) in tetrimino]
        return start_pos_tetrimino

    def hold_tetrimino(self):
        old_held_tetrimino = self.held_tetrimino
        self.held_tetrimino = [col_tetrimino for col_tetrimino in self.tetrimino_variants
                            if col_tetrimino[1] == self.graphic.tetrimino_color][0]
        self.graphic.held_tetrimino = self.held_tetrimino

        if old_held_tetrimino == ():
            self.refresh_tetrimino(for_holding='new hold')
        else:
            self.current_tetrimino = self.tetrimino_starting_position(old_held_tetrimino[0])
            self.graphic.tetrimino_color = old_held_tetrimino[1]
            self.sync_graphic_and_logic('hold')

    tetromino_bag: list[ColoredTetrimino] = []

    def refresh_tetrimino(self, for_holding: HoldingRefreshSettings = 'no hold'):
        if for_holding == "no hold":
            new_fallen_blocks = [(x, self.graphic.tetrimino_color) for x in self.current_tetrimino[:-1]]
            self.fallen_blocks.update(new_fallen_blocks)

        rows_removed = self.remove_rows()

        if self.check_failure():
            pygame.event.post(Event(self.GAMEOVER))
            return

        if not self.tetromino_bag:
            self.tetromino_bag = random.sample(self.tetrimino_variants, len(self.tetrimino_variants))

        refreshed_tetrimino = self.tetromino_bag.pop()
        self.current_tetrimino = self.tetrimino_starting_position(refreshed_tetrimino[0])
        self.graphic.tetrimino_color = refreshed_tetrimino[1]

        self.sync_graphic_and_logic('refresh' if for_holding == "no hold" else 'hold', rows_removed)
    
    def remove_rows(self):
        blocks_num_for_every_row: dict[int, int] = {}

        for block in self.fallen_blocks:
            ((_, block_row), _) = block

            if block_row not in blocks_num_for_every_row.keys():
                blocks_num_for_every_row[block_row] = 0
            
            blocks_num_for_every_row[block_row] += 1
        
        rows_to_remove = [row for (row, blocks_num) in blocks_num_for_every_row.items()
                        if blocks_num == 10]

        if len(rows_to_remove) == 0: 
            return False

        new_fallen_blocks = set()
        
        for ((x, y), color) in self.fallen_blocks:
            if y in rows_to_remove:
                continue
            
            num_rows_below = len([row for row in rows_to_remove if row > y])
            new_fallen_blocks.add(((x, y + num_rows_below), color))

        self.fallen_blocks = new_fallen_blocks

        return True

    def check_failure(self):
        return any(y < 0 for ((_, y), _) in self.fallen_blocks)