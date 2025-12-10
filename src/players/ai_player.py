"""
Игрок - компьютер с разными уровнями сложности
"""

import random
from typing import Tuple, List
from .base_player import Player
from ..board import Board

class AIPlayer(Player):
    """
    Базовый класс игрока - компьютера.
    """

    def __init__(self, symbol: str, name: Optional[str] = None, difficulty: str = 'easy'):
        """
        Инициализирует игрока - компьютера. 
        """
        super().__init__(symbol, name or f"AI - {difficulty}")
        self.difficulty = difficulty

    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        Выбирает ход в зависимости от уровня сложности.
        """
        if self.difficulty == 'easy':
            return self._get_random_move(board)
        elif self.difficulty == 'medium':
            return self._get_medium_move(board)
        elif self.difficulty == 'hard':
            return self._get_hard_move(board)
        else:
            raise ValueError(f"Неизвестный уровень сложности: {self.difficulty}")
        
    def _get_random_move(self, board: Board) -> Tuple[int, int]:
        """
        Выбирает случайный ход.
        AI - легкий.
        """
        available_moves = self._get_available_moves(board)
        if not available_moves:
            raise ValueError("Ходов не осталось")
        
        # Пауза на размышления)
        import time
        time.sleep(0.5)

        return random.choice(available_moves)
    
    def _get_available_moves(self, board: Board) -> List[Tuple[int, int]]:
        """
        Возвращает список доступных ходов
        """
        moves = []
        for row in range(board.size):
            for col in range(board.size):
                if board.get_cell(row, col) == ' ':
                    moves.append((row, col))
        return moves
    
    def _get_medium_move(self, board: Board) -> Tuple[int, int]:
        """
        Игрок компьютер.
        Уровень средний.
        1 Проверяет есть ли победный ход.
        2 Блокирует победный ход противника, если он есть.
        3 Случайный ход.
        """
        # TODO
        return self._get_random_move(board)
    
    def _get_hard_move(self, board: Board) -> Tuple[int, int]:
        """
        Игрок компьютер.
        Уровень сложный.
        ...
        """
        # TODO
        return self._get_medium_move(board)
    