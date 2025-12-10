"""
Класс управяющий игровым процессом
"""

from typing import List, Optional, Dict, Any
from .board import Board
from .players import Player

class Game:
    """
    Управляет игровым процессом.
    Arg:
        - Игровое поле
        - Игроки
        - Индекс текущего игрока
        - Флаг завершения игры
        - История ходов
    """

    def __init__(self, player1: Player, player2: Player, board_size: int = 3):
        """
        Инициализирует новую игру
        """
        if player1.symbol == player2.symbol:
            raise ValueError("У игроков должны быть разные символы")
        
        self.board = Board(size=board_size)
        self.players = [player1, player2]
        self.current_player_index = 0
        self.game_over = False
        self.winner: Optional[Player] = None
        self.history: List[Dict[str, Any]] = []

        print(f"\nНачалась новая игра!")
        print(f"Игрок 1: {player1}")
        print(f"Игрок 2: {player2}")
        print(f"Размер поля: {board_size}x{board_size}")

    @property
    def current_player(self) -> Player:
        """
        Возвращает текущего игрока
        """
        return self.players[self.current_player_index]
    
    def play_turn(self) -> bool:
        """
        Выполняет ход игрока и делает проверку
        True, если игра продалжается
        False, если игра закончена
        """
        if self.game_over:
            print("Игра закончена")
            return False
        
        player = self.current_player
        print(f"\nХод игрока {player.name} ({player.symbol}):")

        try:
            # Получаем ход от игрока
            row, col = player.get_move(self.board)

            # Выполняем ход на поле
            success, is_winning = self.board.make_move(row, col, player.symbol)

            if not success:
                print(f"Ход не удался, попробуйсте снова")
                return self.play_turn() # Рекурсивно пробуем снова

            # Записываем ход в историю
            self.history.append({
                'player': player.name,
                'symbol': player.symbol,
                'position': (row, col),
                'turn_number': len(self.history) +1
            })

            print(f"{player.symbol} поставлен на ({row}, {col})")

            # Проверям победу
            if is_winning:
                self.game_over = True
                self.winner = player
                player.record_win()
                self._get_other_player().record_loss()

                print(f"\n{'='*50}")
                print(f"Победил: {player.name} ({player.symbol}!)")
                print(f"Выигрышная комбинация: {self.board.winning_cells}")
                print(f"{'='*50}")

                self.board.display()
                return False
            
            # Проверяем ничью
            if self.board.is_full():
                self.game_over = True
                for p in self.players:
                    p.record_draw()

                print(f"\n{'='*50}")
                print(f"Ничья. Ходов больше не осталось")
                print(f"{'='*50}")

                self.board.display()
                return False
            # Переход хода
            self.current_player_index = (self.current_player_index + 1) % 2

            return True
        
        except KeyboardInterrupt:
            print("\n\n Игра прервана пользователем.")
            self.game_over = True
            return False
        except Exception as e:
            print(f"Ошибка во вреся хода:{e}")
            return False
        
    def _get_other_player(self) -> Player:
        """
        Возвращает игорока, который сечас не ходит
        """
        return self.players[(self.current_player_index + 1) % 2]
    
    def play_full_game(self):
        """
        Играет полную игру до завершения.
        """
        print(f"\n{'='*50}")
        print(f"Начало игры")
        print(f"{'='*50}")

        self.board.display()

        while not self.game_over:
            should_continue = self.play_turn()

            if not should_continue:
                break

            # Показываем поле, после успешного хода
            if not self.game_over:
                self.board.display()

        self._show_game_summary()

    def _show_game_summary(self):
        """
        Показываем игоги игры.
        """
        print(f"\n{'='*50}")
        print(f"Итоги игры")
        print(f"{'='*50}")

        print(f"Всего ходов: {len(self.history)}")
        print(f"Победитель: {self.winner.name if self.winner else 'Ничья'}")

        print(f"\nИстория ходов")
        for move in self.history:
            print(f"Ход {move['turn_number']}: {move['player']} ({move['symbol']}) -> {move['position']}")

        print(f"\nСтатистика игроков")
        for player in self.players:
            stats = player.get_stats()
            print(f"{player.name}: {stats['wins']} побед, {stats['win_rate']:.1f}%")

    def reset(self):
        """
        Обнуляем игру
        """
        self.board.reset()
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        self.history.clear()
        print("\nИгра сброшена, для нового раунда")

def create_game_from_config(config: Dict[str, Any]) -> Game:
    """
    Создает игру из конфигурационного словаря.
    config: {
        'player_type': 'human' or 'ai',
        'player1_name': str,
        'player1_symbol': 'X' or 'O',
        'player2_name': str,
        'player2_symbol': 'X' or 'O',
        'board_size': int,
        'ai_difficulty': str ('easy', 'medium', 'hard')
        }
    """
    from .players import HumanPlayer, AIPlayer
    # Создаем первого игрока
    if config.get('player1_type', 'human') == 'ai':
        player1 = AIPlayer(
            symbol=config['player1_symbol'],
            name=config.get('player1_name'),
            difficulty=config.get('ai_difficulty', 'easy')
        )
    else:
        player1 = HumanPlayer(
            symbol=config['player1_symbol'],
            name=config.get('player1_name', 'Игрок 1')
        )

    # Создаем второго игрока
    if config.get('player2_type', 'human') == 'ai':
        player2 = AIPlayer(
            symbol=config['player2_symbol'],
            name=config.get('player2_name'),
            difficulty=config.get('ai_difficulty', 'easy')
        )
    else:
        player2 = HumanPlayer(
            symbol=config['player2_symbol'],
            name=config.get('player2_name', 'Игрок 2')
        )
        
    return Game(
        player1=player1,
        player2=player2,
        board_size=config.get('board_size', 3)
    )
    