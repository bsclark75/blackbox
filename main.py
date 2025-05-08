import os
from game import Game

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Welcome to text Blackbox!")
    game = Game()
    game.start()
    

if __name__ == "__main__":
    main()
