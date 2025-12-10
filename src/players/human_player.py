"""
Игрок против человека. Версия для консоли.
"""

from typing import Tuple
from .base_player import Player
from ..board import Board

class HumanPlayer(Player):
    """
    Игрок - человек, который вводит ходы через коноль.
    """
    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        Запрашивает ход у игрока
        """
        print(f"\nХод игрока {self.name} ({self.symbol}):")
        print(f"Введите координаты через пробел, начиная с нуля (строка, столбец):")
        
        while True:
            try:
                # Получаем ввод.
                input_str = input(">>> ").strip()

                # Проверяем не хочет ли игрок выйти.
                if input_str.lower() in ('выход', 'exit', 'quit', 'q'):
                    raise KeyboardInterrupt("Игрок прервал игру")
                
                # Разбираем координаты.
                parts = input_str.split()
                if len(parts) != 2:
                    print(f"Ошибка. Координаты должны быть от 0 до {board.size -1}")
                    continue

                row, col = map(int, parts)

                # Проверяем, что ячейка свободна.
                if board.get_cell(row, col) != ' ':
                    print(f"Ошибка! Ячейка ({row}, {col}) уже занята")
                    continue

                return row, col 

            except ValueError:
                print(f"Ошибка. Введите целые числа")
            except KeyboardInterrupt:
                print(f"\nИгра остановлена игроком")
                raise
            except Exception as e:
                print(f"Неизвестная ошибка: {e}")



                
