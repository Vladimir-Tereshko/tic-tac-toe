"""
Пакет players - содержит классы игроков
"""

from .base_player import Player
from .human_player import HumanPlayer
from .ai_player import AIPlayer

__all__ = ['Player', 'HumanPlayer', 'AIPlayer']
