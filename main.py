"""
Главный модуль игры "Крестики-нолики"
Запуск игры: python main.py
"""

from src.game import TicTacToeGame

def main():
    """Точка входа в игру"""
    print("=" * 40)
    print("   Добро пожаловать в Крестики-нолики!")
    print("=" * 40)
    
    game = TicTacToeGame()
    game.start()

if __name__ == "__main__":
    main()