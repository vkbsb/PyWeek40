import random

class Game2048:
    move_left = 'left'
    move_right = 'right'
    move_up = 'up'
    move_down = 'down'
    
    def __init__(self, size=4):
        self.size = size
        self.grid = []
        
        # Create the outer list (rows)
        for row in range(size):
            # Create a new row filled with zeros
            new_row = []
            for column in range(size):
                new_row.append(0)
            # Add the completed row to the grid
            self.grid.append(new_row)

        self.spawn_block()
        self.spawn_block()

    def spawn_block(self):
        empty_positions = [(r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0]
        if not empty_positions:
            return False
        print(empty_positions)
        r, c = random.choice(empty_positions)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
        return True

    def is_game_finished(self):
        # Any empty cell means not finished
        for row in self.grid:
            if 0 in row:
                return False
        # Any horizontal merge possible?
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        # Any vertical merge possible?
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

    def merge_line(self, line):
        # Slide non-zeros
        # new_line = [i for i in line if i != 0]
        
        # Traditional loop approach
        new_line = []
        for i in line:
            if i != 0:
                new_line.append(i)

        merged_line = []
        skip = False
        for i in range(len(new_line)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
                merged_line.append(new_line[i] * 2)
                skip = True
            else:
                merged_line.append(new_line[i])
        # Pad with zeros
        # merged_line.extend([0] * (self.size - len(merged_line)))
        # Calculate how many zeros we need
        remaining_spaces = self.size - len(merged_line)

        # Create a list of zeros
        zeros_to_add = []
        for i in range(remaining_spaces):
            zeros_to_add.append(0)

        # Add all zeros to the merged_line
        for zero in zeros_to_add:
            merged_line.append(zero)

        return merged_line

    def move(self, direction):
        moved = False
        if direction == 'left':
            for r in range(self.size):
                merged = self.merge_line(self.grid[r])
                if merged != self.grid[r]:
                    moved = True
                    self.grid[r] = merged
        elif direction == 'right':
            for r in range(self.size):
                merged = self.merge_line(self.grid[r][::-1])[::-1]
                if merged != self.grid[r]:
                    moved = True
                    self.grid[r] = merged
        elif direction == 'up':
            for c in range(self.size):
                col = [self.grid[r][c] for r in range(self.size)]
                merged = self.merge_line(col)
                if merged != col:
                    moved = True
                for r in range(self.size):
                    self.grid[r][c] = merged[r]
        elif direction == 'down':
            for c in range(self.size):
                col = [self.grid[r][c] for r in range(self.size)][::-1]
                merged = self.merge_line(col)[::-1]
                if merged != [self.grid[r][c] for r in range(self.size)]:
                    moved = True
                for r in range(self.size):
                    self.grid[r][c] = merged[r]
        return moved

    def print_board(self):
        width = max(len(str(num)) for row in self.grid for num in row) or 1
        sep = '+' + '+'.join(['-' * (width + 2) for _ in range(self.size)]) + '+'
        print(sep)
        for row in self.grid:
            line = '| ' + ' | '.join(f"{num:{width}d}" if num != 0 else ' ' * width for num in row) + ' |'
            print(line)
            print(sep)

# if __name__ == '__main__':
#     game = Game2048(size=4)
#     controls = {
#         'w': 'up',
#         'a': 'left',
#         's': 'down',
#         'd': 'right',
#         'q': 'quit'
#     }
#     print("Controls: w=up, a=left, s=down, d=right, q=quit")
#     while True:
#         game.print_board()
#         if game.is_game_finished():
#             print("Game over!")
#             break
#         cmd = input('Move (w/a/s/d or q): ').strip().lower()
#         if cmd == 'q':
#             print('Bye!')
#             break
#         if cmd not in controls:
#             print('Invalid input.')
#             continue
#         moved = game.move(controls[cmd])
#         if moved:
#             game.spawn_block()
#         else:
#             print('No move possible in that direction.')
