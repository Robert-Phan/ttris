import pygame
import graphic, logic

def main():
    pygame.init()
    game_graphic = graphic.Graphic()
    game_logic = logic.Logic(game_graphic)
    pygame.quit()


if __name__ == '__main__':
    main()