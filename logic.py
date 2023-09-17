import pygame
from pygame.event import Event
from typing import Callable, Self, NamedTuple, Optional
import random

from graphic import Graphic

Block = tuple[int, int]
Tetrimino = list[Block]

class Logic:
    def __init__(self, graphic: Graphic) -> None:
        self.graphic = graphic
        
        self.event_loop()

    current_tetrimino: Tetrimino = [
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0),
        (1.5, 0.5)
    ]

    def event_loop(self):
        event_loop_running = True

        movement_key_held_down: Optional[int] = None

        while event_loop_running:
            for event in pygame.event.get():
                match event:
                    case Event(type=pygame.QUIT):
                        event_loop_running = False
                    case Event(type=pygame.KEYDOWN, key=(pygame.K_DOWN | pygame.K_RIGHT | pygame.K_LEFT)):
                        movement_key_held_down = event.key
                        # self.shift_tetrimino(event.key)
                    case Event(type=pygame.KEYDOWN, key=(pygame.K_a | pygame.K_d)):
                        movement_key_held_down = event.key
                        # self.rotate_tetrimino(event.key)
                    case Event(type=pygame.KEYUP, key=(pygame.K_DOWN | pygame.K_RIGHT | pygame.K_LEFT | pygame.K_a | pygame.K_d)):
                        movement_key_held_down = None
            
            match movement_key_held_down:
                case pygame.K_DOWN | pygame.K_RIGHT | pygame.K_LEFT:
                    self.shift_tetrimino(event.key)
                case pygame.K_DOWN | pygame.K_RIGHT | pygame.K_LEFT:
                    self.shift_tetrimino(event.key)


    def sync_graphic_and_logic(self, is_movement = True):        
        self.graphic.tetrimino_blocks = [*self.current_tetrimino][:-1]
        self.graphic.draw_tetrimino(is_movement)

    movement_offsets = {
        pygame.K_DOWN: (0, 1),
        pygame.K_RIGHT: (1, 0),
        pygame.K_LEFT: (-1, 0),
        pygame.K_a: (1, -1),
        pygame.K_d: (-1, 1)
    }

    fallen_blocks: set[Block] = set()

    @staticmethod
    def move_tetrimino_decor(move_tetri_func: Callable[[Self, int], Tetrimino]):
        def decorated_move_tetri_func(self: Self, movement_key: int):
            new_tetrimino = move_tetri_func(self, movement_key)

            for (new_x, new_y) in new_tetrimino[:-1]:
                if not (0 <= new_x < 10) or new_y >= 20 or (new_x, new_y) in self.fallen_blocks:
                    if movement_key == pygame.K_DOWN:
                        self.refresh_tetrimino()
                    return 
            
            self.current_tetrimino = new_tetrimino

            self.sync_graphic_and_logic()
        
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
        print("Yuh")
        (rot_offset_x, rot_offset_y) = self.movement_offsets[movement_key]
        (pivot_x, pivot_y) = self.current_tetrimino[-1]

        pivot_adjusted_tetromino = [(x - pivot_x, y - pivot_y) for (x, y) in self.current_tetrimino[:-1]]

        rotated_tetromino = [(y * rot_offset_x, x * rot_offset_y) for (x, y) in pivot_adjusted_tetromino]

        new_tetromino = [(x + pivot_x, y + pivot_y) for (x, y) in rotated_tetromino] 

        return [*new_tetromino, (pivot_x, pivot_y)]

    tetrimino_variants: list[Tetrimino] = [
        [(0, 0),(1, 0),
        (2, 0), (3, 0),
        (1.5, 0.5)],
        [(0, 0),(1, 0),
        (0, 1), (1, 1),
        (0.5, 0.5)],
    ]

    def refresh_tetrimino(self):
        self.fallen_blocks.update(self.current_tetrimino[:-1])

        refreshed_tetrimino = random.choice(self.tetrimino_variants)
        self.current_tetrimino = refreshed_tetrimino

        self.sync_graphic_and_logic(False)
