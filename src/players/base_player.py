"""
Базовый класс для всех игроков.
Определяет интерфейс, для каждого игрока.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional
from ..board import Board

class Player(ABC):
    """
    Абстрактный класс игрока.
    Arg:
    symbol: "X" или "O".
    name: Имя игрока.
    wins: Счетчик побед
    """

    def __init__(self, symbol: str, name: Optional[str] = None):
        """
        Инициализация игрока
        """
        if symbol.upper() not in ('X', 'O'):
            raise ValueError(f"Символ должен быть 'X' или 'O' (англ.), введен {symbol}")
        
        self.symbol = symbol.upper()
        self.name = name or self.__class__.__name__
        self.wins = 0
        self.total_games = 0

    @abstractmethod
    def get_move(self, board: Board) -> Tuple[int, int]:
        """
        Получает ход от игрока.
        Возвращает координаты хода.
        """
        pass

    def record_win(self):
        """
        Записывает победу игрока
        """
        self.wins += 1
        self.total_games +=1

    def record_loss(self):
        """
        Записывает проигрыш игрока
        """
        self.total_games +=1

    def record_draw(self):
        """
        Записывает ничью в игре
        """
        self.total_games +=1

    @property
    def win_rate(self) -> float:
        """
        Возвращает процент побед
        """
        if self.total_games == 0:
            return 0.0
        return (self.wins / self.total_games) * 100
    def reset_stats(self):
        """
        Сбрасывает статистику игрока
        """
        self.wins = 0
        self.total_games = 0

    def __str__(self) -> str:
        """
        Представление игрока в виде строки.
        """
        return f"{self.name} ({self.symbol})"
    
    def get_stats (self):
        """
        Возвращает статистику игрока
        """
        return{
            'name': self.name,
            'symbol': self.symbol,
            'wins': self.wins,
            'total_games': self.total_games,
            'win_rate': self.win_rate
        }

