import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASS_GREEN = (0, 125, 0)

# Initialize Pygame
pygame.init()

images = {
    'p': pygame.image.load("white_knight.png"),
    'P': pygame.image.load("black_knight.png"),

    'a': pygame.image.load("white_alpha.png"),
    'A': pygame.image.load("black_alpha.png"),

    'r': pygame.image.load("white_rook.png"),
    'R': pygame.image.load("black_rook.png"),

    'n': pygame.image.load("white_horse.png"),
    'N': pygame.image.load("black_horse.png"),    

    'w': pygame.image.load("white_wall.png"),
    'W': pygame.image.load("black_wall.png"),    

    'b': pygame.image.load("white_bishop.png"),
    'B': pygame.image.load("black_bishop.png"),    

    'k': pygame.image.load("white_king.png"),
    'K': pygame.image.load("black_king.png"),    

    'q': pygame.image.load("white_queen.png"),
    'Q': pygame.image.load("black_queen.png"),    

    'm': pygame.image.load("move_outline.png"),
    'M': pygame.image.load("move_full.png")         
}

# Chess Board Representation
board = [
    ['P', 'N', 'B', 'Q', 'K', 'B', 'N', 'P'],
    ['R', 'P', 'P', 'P', 'P', 'P', 'P', 'R'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['r', 'p', 'p', 'p', 'p', 'p', 'p', 'r'],
    ['p', 'n', 'b', 'q', 'k', 'b', 'n', 'p']
]

#help player w possible moves
possible_moves = [[False for _ in range(8)] for _ in range(8)]

# Add the "meta layer" array to represent the walls formed by two rooks of the same color
meta_layer = [[" " for _ in range(8)] for _ in range(8)]

start_pos = None

# Add a global variable to store the color of the player whose move it is
current_player_color = 'W'  # Assume it's White's turn at the start

def find_rooks_on_same_row():
    global meta_layer
    #reset meta layer
    meta_layer = [[" " for _ in range(8)] for _ in range(8)]
    # Find positions of rooks on the same row for both colors
    white_rook_positions = find_rooks_on_same_row_by_color('W')
    black_rook_positions = find_rooks_on_same_row_by_color('B')

# Function to find the positions of rooks on the same row for both colors
def find_rooks_on_same_row_by_color(color):
    global meta_layer

    if color == 'W': wall = 'w'
    else: wall = 'W'

    rooks_positions = []
    for row in range(8):
        rooks_in_row = [(row, col) for col in range(8) if board[row][col].upper() == 'R' and board[row][col].islower() == (color == 'W')]
        if len(rooks_in_row) >= 2:
            rooks_positions.extend(rooks_in_row)
            # Update the meta layer for the wall positions
            for i in range(rooks_in_row[0][1]+1,rooks_in_row[1][1]):
                meta_layer[rooks_in_row[0][0]][i] = wall

    return rooks_positions

find_rooks_on_same_row()

# Function to check if a position is blocked by a wall of the opposing player
def is_blocked_by_wall(row, col, piece):
    return meta_layer[row][col] != ' ' and (meta_layer[row][col].isupper() != piece.isupper()) 


def is_field_occupied(row,col,piece):
    is_occupied = board[row][col] != ' ' or is_blocked_by_wall(row,col,piece)
    return is_occupied

# Function to display the board
def draw_board(screen):
    global start_pos

    for row in range(8):
        for col in range(8):
            #draw board itself
            color = WHITE if (row + col) % 2 == 0 else GRASS_GREEN # (125,125,125)
            pygame.draw.rect(screen, color, pygame.Rect(col * 80, row * 80, 80, 80))

    if start_pos != None:
        pygame.draw.rect(screen, RED, pygame.Rect(start_pos[1] * 80, start_pos[0] * 80, 80, 80))

    for row in range(8):
        for col in range(8):
            # draw wall
            wall = meta_layer[row][col]
            if wall != ' ':
                piece_rect = pygame.Rect(col * 80 - 50, row * 80 - 10, 40, 40)
                piece_rect_right = pygame.Rect(col * 80 + 30, row * 80 - 10, 40, 40)
                screen.blit(images[wall], piece_rect)  
                screen.blit(images[wall], piece_rect_right)            

            # draw pieces
            piece = board[row][col]
            font = pygame.font.Font(None, 60)
            piece_rect = pygame.Rect(col * 80, row * 80, 40, 40)
            if piece in images:
                screen.blit(images[piece], piece_rect)
            elif piece != ' ':
                text = font.render(piece, True, GRAY if piece.isupper() else RED)
                screen.blit(text, piece_rect)

            if start_pos != None:
                if possible_moves[row][col]:
                    screen.blit(images['M' if piece.isupper() else 'm'], pygame.Rect(col * 80, row * 80, 80, 80))                
    


def is_valid_move(piece, start_row, start_col, end_row, end_col):
    # Ensure the piece being moved belongs to the current player
    if piece.isupper() and board[start_row][start_col].islower():
        return False
    if piece.islower() and board[start_row][start_col].isupper():
        return False

    # Check for friendly fire
    if board[end_row][end_col] != ' ' and board[end_row][end_col].isupper() == piece.isupper():
        return False

    # Check if the path is blocked by a wall
    if is_blocked_by_wall(end_row, end_col, piece):
        return False

    # Movement logic for each piece
    piece_type = piece.upper()  # Make sure the piece is uppercase for simplicity
    if piece_type == 'R':
        # Rooks cannot take rooks
        if board[end_row][end_col].upper() == 'R':
            return False

        # Rook moves horizontally or vertically
        if start_row == end_row and start_col != end_col:
            # Check for obstructions along the row
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if is_field_occupied(start_row,col,piece):
                    return False
            return True
        elif start_col == end_col and start_row != end_row:
            # Check for obstructions along the column
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if is_field_occupied(row,start_col,piece):
                    return False
            return True
    elif piece_type == 'N':
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # moves one square in any direction
        if row_diff <= 1 and col_diff <= 1:
            return True

        # OR jumps over a piece 2 squares away
        if row_diff + col_diff <= 4 and row_diff <= 2 and col_diff <= 2:
            # Check for jumping over a neighboring piece
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            if is_field_occupied(middle_row, middle_col, piece):
                if board[middle_row][middle_col].isupper() != piece.isupper():
                    board[middle_row][middle_col] = ' '
                return True
            else: return False

        return False
    elif piece_type == 'B':
        # Bishop moves diagonally
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        # Check for obstructions along the diagonal
        step_row = 1 if start_row < end_row else -1
        step_col = 1 if start_col < end_col else -1
        row, col = start_row + step_row, start_col + step_col
        while row != end_row and col != end_col:
            if is_field_occupied(row,col,piece):
                return False
            row += step_row
            col += step_col
        return True
    elif piece_type == 'Q':
        # Queen moves one square diagonally
        return abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1
    elif piece_type == 'K':
        # King moves one square in non-diagonal directions
        return (abs(start_row - end_row) <= 1 and abs(start_col - end_col) == 0) or (abs(start_row - end_row) == 0 and abs(start_col - end_col) <= 1)        
    elif piece_type == 'P':
        # Pawn moves one square in any direction
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
    elif piece_type == 'A':
        # Alpha moves two squares in any direction
        return abs(start_row - end_row) <= 2 and abs(start_col - end_col) <= 2

    return False

# Function to update the board after a move
def make_move(move):
    global current_player_color, start_pos

    start_row, start_col = move[0]
    end_row, end_col = move[1]

    piece = board[start_row][start_col]

    print(f"Piece being moved: {piece}")  # Debug output
    if possible_moves[end_row][end_col]:
        board[start_row][start_col] = ' '

        # check for "alpha knight" conversion
        if (piece == 'p' and end_row == 0):
            piece = 'a'
        if (piece == 'P' and end_row == 7):
            piece = 'A'

        board[end_row][end_col] = piece

        # Switch the player's turn after a valid move
        current_player_color = 'W' if current_player_color == 'B' else 'B'        

        start_pos = None  # Reset start_pos after the move
    else:
        print("Invalid move! Try again.")  

    # Find positions of rooks on the same row for both colors
    find_rooks_on_same_row()    


# Function to get player's move
def get_move():
    global start_pos

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // 80, y // 80
                if start_pos is None:
                    piece = board[row][col]
                    if piece != ' ':
                        start_pos = (row, col)
                        print(f"Start position: {start_pos}")  # Debug output
                else:
                    end_pos = (row, col)
                    print(f"End position: {end_pos}")  # Debug output
                    return start_pos, end_pos


def determine_possible_moves(piece):
    global possible_moves, start_pos

    possible_moves = [[False for _ in range(8)] for _ in range(8)]

    for row in range(8):
        for col in range(8):   
            if is_valid_move(piece, start_pos[0], start_pos[1], row, col):
                possible_moves[row][col] = True

# Main game loop
def play_chess():
    global start_pos

    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Chess")

    start_pos = None  # Initialize start_pos here
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(screen)
        pygame.display.flip()

        while start_pos is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // 80, y // 80
                    piece = board[row][col]
                    if piece != ' ':
                        # Check if the piece belongs to the current player
                        if (current_player_color == 'B' and piece.islower()) or (current_player_color == 'W' and piece.isupper()):
                            print("It's the other player's turn.")
                        else:                        
                            start_pos = (row, col)
                            determine_possible_moves(piece)
                            print(f"Start position: {start_pos}")  # Debug output

        draw_board(screen)
        pygame.display.flip()

        move = get_move()
        make_move(move)
        start_pos = None
        

# Run the game
if __name__ == "__main__":
    print("Welcome to Chess!")
    play_chess()
