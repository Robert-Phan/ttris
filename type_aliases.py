from typing import Literal

Block = tuple[int, int]
Tetrimino = list[Block]
Color = tuple[int, int, int]
ColoredBlock = tuple[Block, Color]
ColoredTetrimino = tuple[Tetrimino, Color]
DrawTetrominoSettings = Literal["refresh", "move", "hold"]
HoldingRefreshSettings = Literal["no hold", "new hold", "hold"]