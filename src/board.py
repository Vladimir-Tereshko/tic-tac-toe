"""
Правила игры в крестики нолики
"""
class Board:
    MAX_SIZE = 8 # максимальный размер поля
    def __init__(self, size=3, win_length=None):
        """
        Создает игровое поле.
        Args:
            size - размер поля от 3х3 до 8х8. По умолчанию 3х3.
            win_length - длина линии для победы. По умолчанию size.
        Raises:
            TypeError: Если size не целое число.
            ValueError: Если size вне допустимого диапазона.
        """

        if not isinstance(size, int):
            raise TypeError(f"Размер поля должен быть целым числом, а не {type(size).__name__}")
        if size < 3 or size > self.MAX_SIZE:
            raise ValueError(f"Допустимый размер поля от 3 до {self.MAX_SIZE}, ваше значение - {size}")
        if win_length is not None:
            if not isinstance(win_length, int):
                raise TypeError(f"Длина для победы должна быть целым числом")
            if win_length < 3 or win_length > size:
                raise ValueError(f"Длина для победы должна быть от 3 до {size}")
            
        self.size = size
        self.win_length = win_length or size

        # Игровое поле
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
    
        # Для проверки победителя
        self.row_counts = [{'X': 0, 'O': 0} for _ in range(size)]
        self.col_counts = [{'X': 0, 'O': 0} for _ in range(size)]
        self.diag_counts = [{'X': 0, 'O': 0} for _ in range(2)]

        # Состояние игры
        self.winner = None
        self.winning_cells = []
        self.last_symbol = None
        self.move_count = 0

    def display(self):
        """
        Выводит поле в консоль
        """
        # Верхняя граница
        print('┌' + '─' * (self.size * 2 - 1) + '┐')

        for i, row in enumerate(self.grid):
            row_str = f'{i}│' + '│'.join(row) + '│'
            print(row_str)

            if i < self.size - 1:
                print('├' + '─' * (self.size * 2 - 1) + '┤')

        print('└' + '─' * (self.size * 2 - 1) + '┘')
        col_numbers = ' '.join(str(i) for i in range(self.size))
        print(' ' + col_numbers)

        if self.winner:
            print(f"Победил - {self.winner}")
            print(f"Выигрышная комбинация - {self.winning_cells}")
        elif self.is_full():
            print("Ничья!")
    
    def normalize_symbol(self, symbol):
        """
        Приводит символ к стандарному виду.
        Return: Х или О в верхнем регистре.
        Raises:
            ValueError: если символ недопустим.
        """
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError(f"Символ может быть Х или О. Введено: {symbol}")
        
        symbol = symbol.upper()

        if symbol not in ('X', 'O'):
            raise ValueError(f"Символ может быть Х или О (англ.). Введено: {symbol}")

        return symbol

    def make_move(self, row, col, symbol):
        """
        Выполняет ход на поле
        """
        try:
            symbol = self.normalize_symbol(symbol)

            # Проверяем границы поля.
            if not (0 <= row < self.size and 0 <= col < self.size):
                print(f"Введенные координаты находятся вне поля. Доступное поле: {self.size}x{self.size}")
                return False, False
        
            # Проверяем занятость клетки
            if self.grid[row][col] != ' ':
                print(f"Ячейка ({row}x{col}) уже занята символом '{self.grid[row][col]}'")
                return False, False
        
            # Если уже есть победитель
            if self.winner:
                print(f"Игра закончена. Победил {self.winner}")
                return False, False
            
            # Проверка чередования ходов
            if self.move_count > 0 and symbol == self.last_symbol:
                other_symbol = 'O' if symbol == 'X' else 'X'
                print(f"Сейчас не Ваш ход, ходить должен '{other_symbol}'")
                return False, False
            
            # Выполняем ход
            self.grid[row][col] = symbol
            self.last_symbol = symbol
            self.move_count += 1

            # Обновляем счетчик
            self.update_counters(row, col, symbol)

            # Проверяем не привел ли ход к победе
            is_winning = self.check_winner_after_move(row, col, symbol)

            print(f"{symbol} установлен на ({row}x{col})")
            return True, is_winning
        
        except ValueError as e:
            print(f"Ошибка: {e}")
            return False, False
        except Exception as e:
            print(f"Неизвестная ошибка {e}")
            return False, False
        
    def update_counters(self, row, col, symbol):
        """
        Обновляет счетчики для быстрой проверки победителя
        """
        self.row_counts[row][symbol] += 1
        self.col_counts[col][symbol] += 1

        if row == col:
            self.diag_counts[0][symbol] += 1
        
        if row + col == self.size - 1:
            self.diag_counts[1][symbol] += 1

    def check_winner_after_move(self, row, col, symbol):
        """
        Быстрая проверка, стал ли ход выигршным.
        """
        if self.check_line('row', row, symbol):
            return True
        
        if self.check_line('col', col, symbol):
            return True
        
        if row == col and self.check_line('diag', 0, symbol):
            return True
        
        if row + col == self.size - 1 and self.check_line ('diag', 1, symbol):
            return True
        return False
    
    def check_line(self, line_type, index, symbol):
        """
        Проверяет, заполнена ли линия.
        """
        if line_type == 'row':
            count = self.row_counts[index][symbol]
            if count == self.win_length:
                self.winning_cells = [(index, col) for col in range(self.size)]
                self.winner = symbol
                return True
            
        elif line_type == 'col':
            count = self.col_counts[index][symbol]
            if count == self.win_length:
                self.winning_cells = [(row, index) for row in range(self.size)]
                self.winner = symbol
                return True
            
        elif line_type == 'diag':
            count = self.diag_counts[index][symbol]
            if count == self.win_length:
                if index == 0:
                    self.winning_cells = [(i, i) for i in range(self.size)]
                else:
                    self.winning_cells = [(i, self.size - 1 - i) for i in range(self.size)]
                self.winner = symbol
                return True
        return False

    def is_full(self):
        """
        Проверяет заполнено ли поле
        """
        for row in self.grid:
            if ' ' in row:
                return False
        return True
    
    def get_cell(self, row, col):
        """
        Возвращает символ в указанной ячейке
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None
    
    def reset(self):
        """
        Сбрасывает поле
        """
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.row_counts = [{'X':0, 'O': 0} for _ in range(self.size)]
        self.col_counts = [{'X':0, 'O': 0} for _ in range(self.size)]
        self.diag_counts = [{'X':0, 'O': 0} for _ in range(2)]
        self.winner = None
        self.winning_cells = []
        self.last_symbol = None
        self.move_count = 0

    def get_state (self):
        """
        Возвращает текущее состояние игры
        """
        return {
            'size' : self.size,
            'win_length' : self.win_length,
            'grid' : [row.copy() for row in self.grid],
            'winner' : self.winner,
            'winning_cells' : self.winning_cells.copy(),
            'last_symbol' : self.last_symbol,
            'move_count' : self.move_count,
            'is_full' : self.is_full()
            }

    def __str__(self):
        return f"Board({self.size}x{self.size}, win={self.win_length}, moves={self.move_count})"
    
