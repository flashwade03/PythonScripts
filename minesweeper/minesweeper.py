import sys, os
from map import MAP
from game_manager import GameManager

def main():
    game_manager = GameManager()
    game_manager.run_game()

if __name__ == '__main__':
    sys.exit(main())
