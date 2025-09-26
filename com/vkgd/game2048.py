import random
# The following import is removed to comply with the request:
# from typing import List, Tuple, Optional, Dict, Any 

class Game2048:
    """
    Implements the core game logic for 2048, including movement, merging, 
    and tracking the movement and merge sources of all resulting tiles.
    """
    move_left = 'left'
    move_right = 'right'
    move_up = 'up'
    move_down = 'down'
    def __init__(self, size: int = 4):
        """Initializes the game board and adds the first two tiles."""
        if size < 2:
            raise ValueError("Board size must be at least 2.")
        self.size = size
        # The board is a list of lists representing the grid.
        self.board = []
        for r in range(size):
            row = []
            for c in range(size):
                row.append(0)
            self.board.append(row)
        self.score = 0
        self.game_over = False
        
        # Start the game with two initial tiles
        self.add_random_tile()
        self.add_random_tile()

    # Original type hint removed: -> Optional[Tuple[int, int, int]]
    def add_random_tile(self):
        """
        Adds a new tile (2 or 4) to a random empty spot.
        Returns the (row, col, value) of the new tile, or None if no empty spots.
        """
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))
        
        if not empty_cells:
            self.game_over = self._check_game_over()
            return None
        
        r, c = random.choice(empty_cells)
        # 90% chance for 2, 10% chance for 4
        value = 2 if random.random() < 0.9 else 4
        self.board[r][c] = value
        return (r, c, value)

    # Original type hint removed: (self, line_data: list[tuple[int, tuple[int, int]]]) -> tuple[List[int], int, list[dict]]
    def _slide_and_merge_line_with_tracking(self, line_data):
        """
        Performs the slide and merge operation on a single line, tracking the source 
        coordinates of all resulting tiles.
        
        Args:
            line_data: List of (value, (r, c)) tuples for the current line, ordered
                       from the starting edge of the slide (e.g., left or up).
            
        Returns:
            (new_line_values, score_added, move_actions):
            - new_line_values: The processed list of tile values.
            - score_added: Score gained in this line.
            - move_actions: List of dicts describing 'move' or 'merge' operations. 
              {type, value, final_index, (source/sources)}
        """
        # Filter out zeros, keeping only active tiles with their original coordinates
        active_tiles = [data for data in line_data if data[0] != 0]
        
        new_line_values = []
        move_actions = []
        score_added = 0
        i = 0
        
        while i < len(active_tiles):
            current_val, current_start_coord = active_tiles[i]
            
            # Check for merge opportunity with the next tile
            if i + 1 < len(active_tiles) and current_val == active_tiles[i + 1][0]:
                # MERGE operation
                merged_val = current_val * 2
                score_added += merged_val
                
                source1 = current_start_coord
                source2 = active_tiles[i + 1][1]
                
                final_index_in_line = len(new_line_values)
                
                move_actions.append({
                    'type': 'merge',
                    'value': merged_val,
                    'sources': [source1, source2], 
                    'final_index': final_index_in_line 
                })
                
                new_line_values.append(merged_val)
                i += 2 # Skip the next tile
            else:
                # SIMPLE MOVE operation (or no move if already at the front)
                final_index_in_line = len(new_line_values)
                
                move_actions.append({
                    'type': 'move',
                    'value': current_val,
                    'source': current_start_coord,
                    'final_index': final_index_in_line
                })
                
                new_line_values.append(current_val)
                i += 1
                
        # Pad with zeros
        for x in range(self.size - len(new_line_values)):
            new_line_values.append(0)
        
        return new_line_values, score_added, move_actions

    # Original type hint removed: -> Tuple[bool, int, List[Dict[str, Any]], Optional[Tuple[int, int, int]]]
    def move(self, direction: str):
        """
        Performs a move in the given direction and tracks all resulting tile movements and merges.
        
        Args:
            direction: 'up', 'down', 'left', or 'right'.
            
        Returns:
            (moved, score_added, move_details, new_tile_info):
            - moved (bool): True if the board state changed.
            - score_added (int): The total score added in this move.
            - move_details (list of dicts): List of 'move', 'merge', or 'new_tile' actions.
            - new_tile_info (tuple | None): (r, c, value) of the newly added tile.
        """
        if self.game_over:
            return False, 0, [], None

        original_board = [row[:] for row in self.board]
        total_score_added = 0
        all_move_details = []
        
        if direction in ('left', 'right'):
            # Iterate over rows
            
            # 'left' slide starts at index 0, 'right' slide starts at index size-1
            line_order = range(self.size) if direction == 'left' else range(self.size - 1, -1, -1)
            # This maps the final logical index (0, 1, 2, 3) back to the physical column index
            final_map = range(self.size) if direction == 'left' else range(self.size - 1, -1, -1)

            for r in range(self.size):
                # 1. Prepare data: (value, (r, c)) tuples in the order of the slide
                line_data = [(self.board[r][c], (r, c)) for c in line_order]

                # 2. Slide and Merge with tracking
                new_line_values, score_added, move_actions = self._slide_and_merge_line_with_tracking(line_data)
                total_score_added += score_added

                # 3. Map move_actions to final (r, c) coordinates and update board row
                # final_row = [0] * self.size
                final_row = [0 for _ in range(self.size)]

                for action in move_actions:
                    # 'final_index' is the logical position (0-3) in the resulting compacted line.
                    final_r = r
                    final_c = final_map[action['final_index']]
                    
                    action['end'] = (final_r, final_c)
                    final_row[final_c] = action['value']
                    
                    # Clean up temporary key: 'final_index' is only used internally for mapping.
                    # 'source'/'sources' must be kept.
                    del action['final_index']
                    
                    all_move_details.append(action)

                self.board[r] = final_row
                
        elif direction in ('up', 'down'):
            # Iterate over columns
            
            # 'up' slide starts at index 0, 'down' slide starts at index size-1
            line_order = range(self.size) if direction == 'up' else range(self.size - 1, -1, -1)
            # This maps the final logical index (0, 1, 2, 3) back to the physical row index
            final_map = range(self.size) if direction == 'up' else range(self.size - 1, -1, -1)

            for c in range(self.size):
                # 1. Prepare data: (value, (r, c)) tuples in the order of the slide (along the column)
                line_data = [(self.board[r][c], (r, c)) for r in line_order]

                # 2. Slide and Merge with tracking
                new_line_values, score_added, move_actions = self._slide_and_merge_line_with_tracking(line_data)
                total_score_added += score_added
                
                # 3. Map move_actions to final (r, c) coordinates and update board column
                # final_col = [0] * self.size
                final_col = [0 for _ in range(self.size)]
                
                for action in move_actions:
                    # 'final_index' is the logical position (0-3) in the resulting compacted column.
                    final_r = final_map[action['final_index']]
                    final_c = c
                    
                    action['end'] = (final_r, final_c)
                    final_col[final_r] = action['value'] 
                    
                    # Clean up temporary key: 'final_index' is only used internally for mapping.
                    # 'source'/'sources' must be kept.
                    del action['final_index']

                    all_move_details.append(action)

                # Now, update the actual board column
                for r_update in range(self.size):
                    self.board[r_update][c] = final_col[r_update]

        else:
            raise ValueError(f"Invalid direction: {direction}")


        # 4. Check for changes and add new tile
        moved = self.board != original_board
        new_tile_info = None
        
        if moved:
            # new_tile_info = self.add_random_tile()
            self.score += total_score_added
            
            # Append the new tile action to the move details
            if new_tile_info:
                r, c, value = new_tile_info
                all_move_details.append({
                    'type': 'new_tile',
                    'end': (r, c),
                    'value': value
                })
            
            return moved, total_score_added, all_move_details, new_tile_info
        else:
            # If no move was made, check for game over possibility
            self.game_over = self._check_game_over()
            return moved, 0, [], None

    # Original type hint removed: -> bool
    def _check_game_over(self):
        """Checks if there are any valid moves left."""
        # 1. Check for empty cells 
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return False
        
        # 2. Check for adjacent identical tiles (possible merges)
        for r in range(self.size):
            for c in range(self.size):
                value = self.board[r][c]
                # Check right
                if c + 1 < self.size and self.board[r][c + 1] == value:
                    return False
                # Check down
                if r + 1 < self.size and self.board[r + 1][c] == value:
                    return False
                    
        return True # No empty cells and no possible merges

    def display_board(self):
        """Prints the current state of the board."""
        print("-" * (self.size * 5 + 1))
        for row in self.board:
            print("|" + "|".join(f"{val:4}" if val != 0 else "    " for val in row) + "|")
            print("-" * (self.size * 5 + 1))
        print(f"Score: {self.score}\n")

# --- Example Usage ---
if __name__ == '__main__':
    game = Game2048(size=4)
    print("--- Game Start ---")
    game.display_board()

    # Simple command loop for demonstration
    while not game.game_over:
        print("Enter move (w/a/s/d):")
        move_input = input().lower()
        
        if move_input == 'q':
            break

        direction_map = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}
        direction = direction_map.get(move_input)
        
        if not direction:
            print("Invalid input. Use w, a, s, or d.")
            continue
            
        moved, score_added, move_details, new_tile_info = game.move(direction)
        
        if moved:
            print(f"\n--- Move '{direction}' executed! ---")
            print(f"Score added: {score_added}")
            
            if move_details:
                print("\n--- Move Details ---")
                for detail in move_details:
                    if detail['type'] == 'move':
                        # We use .get('source') here as 'source' is not present for 'merge' actions
                        print(f"  > Move: {detail['value']} from {detail.get('source')} to {detail['end']}")
                    elif detail['type'] == 'merge':
                        print(f"  > MERGE: {detail['sources']} combined into {detail['value']} at {detail['end']}")
                    elif detail['type'] == 'new_tile':
                        print(f"  > NEW TILE: {detail['value']} placed at {detail['end']}")

            
            game.display_board()
        else:
            print("No tiles moved or merged. Try a different direction.")
            game.game_over = game._check_game_over()
        
        if game.game_over:
            print("GAME OVER! Final Score:", game.score)
