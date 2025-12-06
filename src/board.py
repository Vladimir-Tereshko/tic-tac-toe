class Board:
    def __init__(self, size=3):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
    
    def display(self):
        for row in self.grid:
            print('|' + '|'.join(row) + '|')
    
    def make_move(self, row, col, symbol):
        if not (0 <= row < self.size and 0 <= col < self.size):
            print(f"АУТ!")
            return False
        
        if self.grid[row][col] == ' ':
           self.grid[row][col] = symbol
           return True
        else:
            print(f"Занято!")
            return False
    
    def is_full(self):
        for row in self.grid:
            for cell in row:
                if cell == ' ':
                    return False
        return True
    
    def get_cell(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None
    
    def reset(self):
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
