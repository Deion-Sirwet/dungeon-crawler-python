import pygame
import game
import sys

if __name__ == '__main__':
    current_game = game.Game()
    current_game.intro_screen()
    current_game.new()
    while current_game.running:
        current_game.main() 
        current_game.game_over()

pygame.quit()
sys.exit()