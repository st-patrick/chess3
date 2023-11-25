import pygame
import sys

# TODOs
# multiplayer
# write rulebook / instructions / video > ask chatgpt to extract custom rules from code
# AI
# create a funtion that applies a given function on all the fields and returns their (chained) return values
# create function to get field clicked on (right now duplicate in get piece in main loop and get_move)
# winning scenario art n stuff
# animations
# ---- DONEs ----
# winning condition
# pawn can't take alpha
# new bishop movement (anywhere + pawn attack range) DONE

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRASS_GREEN = (0, 125, 0)

# Initialize Pygame
pygame.init()

board_bg = pygame.image.load("board.png")
board_bg = pygame.transform.scale(board_bg, (640, 640))
active_bg = pygame.image.load("active_bg.png")
active_bg = pygame.transform.scale(active_bg, (80, 80))
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

#images["P"] = pygame.image.load('alpha.png').convert(24)
#images["P"].set_alpha(128)

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

#for showing debug helpers
debug_layer = [[" " for _ in range(8)] for _ in range(8)]

start_pos = None
screen = None
game_won = False

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

# check if you can jump over this field
def is_crossing_wall(row, col, piece):
    # when jumping / traveling, can't cross wall OR rook (used in horse "N")
    return is_blocked_by_wall(row,col, piece) or (board[row][col].upper() == 'R' and board[row][col].isupper() != piece.isupper())


def is_field_occupied(row,col,piece):
    return is_field_occupied_by_piece(row,col,piece) or is_blocked_by_wall(row,col,piece)

def is_field_occupied_by_piece(row,col,piece):
    return board[row][col] != ' '

# determine whether the game is won by one player and if so, which color
def is_game_won():
    global board
    white_lost = True
    black_lost = True

    for row in range(8):
        for col in range(8):
            #DEBUGHELPER
            if board[row][col] == "q" or board[row][col] == "k": white_lost = False
            elif board[row][col] == "Q" or board[row][col] == "K": black_lost = False

    if white_lost: return "black"
    if black_lost: return "white"
    return white_lost or black_lost

def set_debug_layer(row,col):
    debug_layer[row][col] = "y"

#because you draw it with col as x coordinate which can be confusing, col coming first
def draw_square_at(row,col,color):
    global screen
    pygame.draw.rect(screen, color, pygame.Rect(col * 80, row * 80, 80, 80))

# Function to display the board
def draw_board(screen):
    global start_pos, board_bg

    screen.blit(board_bg, (0,0))

    if start_pos != None:
        screen.blit(active_bg, (start_pos[1] * 80, start_pos[0] * 80))

    for row in range(8):
        for col in range(8):
            #DEBUGHELPER
            if debug_layer[row][col] != " ":
                draw_square_at(row,col,RED)

            # draw wall
            #wall = meta_layer[row][col]
            #if wall != ' ':
            #    piece_rect = pygame.Rect(col * 80 - 50, row * 80 - 10, 40, 40)
            #    piece_rect_right = pygame.Rect(col * 80 + 30, row * 80 - 10, 40, 40)
            #    screen.blit(images[wall], piece_rect)  
            #    screen.blit(images[wall], piece_rect_right)   

            piece_at_square = board[row][col]

            #draw valid move positions
            if start_pos != None:
                target = piece_at_square
                piece = board[start_pos[0]][start_pos[1]]
                if possible_moves[row][col]:
                    if target != " ":
                        screen.blit(images['M'], pygame.Rect(col * 80, row * 80, 80, 80))                
                    else:
                        screen.blit(images['m'], pygame.Rect(col * 80, row * 80, 80, 80))

            # draw pieces
            font = pygame.font.Font(None, 60)
            piece_rect = pygame.Rect(col * 80, row * 80, 40, 40)
            if piece_at_square in images:
                screen.blit(images[piece_at_square], piece_rect)
            elif piece_at_square != ' ':
                text = font.render(piece_at_square, True, GRAY if piece_at_square.isupper() else RED)
                screen.blit(text, piece_rect)
  
# Function to display ui elements
def draw_ui_message(screen, message):
    pygame.draw.rect(screen, GREEN, (80,150,480,200), 5)

    font = pygame.font.Font(None, 100)
    text = font.render(message, True, BLACK)
    text2 = font.render(message, True, WHITE)
    screen.blit(text, (125,205,100,100))
    screen.blit(text2, (130,200,100,100))
    
  


# check whether the given piece can move from its start to its end position by applying custom game logic
def is_valid_move(piece, start_row, start_col, end_row, end_col):
    target = board[end_row][end_col]

    # Check for friendly fire
    if target != ' ' and target.isupper() == piece.isupper():
        return False

    # Check if the path is blocked by a wall
    if is_blocked_by_wall(end_row, end_col, piece):
        return False

    # Movement logic for each piece
    piece_type = piece.upper()  # Make sure the piece is uppercase for simplicity
    if piece_type == 'R':
        # Rooks cannot take rooks
        if target.upper() == 'R':
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

        # move in L shape
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):

            #check for wall in between            
            for i in range(start_row if start_row < end_row else end_row, end_row if start_row < end_row else start_row):
                for j in range(start_col if start_col < end_col else end_col, end_col if start_col < end_col else start_col):
                    if is_crossing_wall(i,j,piece): return False
            return True

        # OR jumps over a piece 2 squares away
        if (row_diff + col_diff == 4 or row_diff + col_diff == 2) and (row_diff == 2 or col_diff == 2):
            # Check for jumping over a neighboring piece
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            if is_field_occupied(middle_row, middle_col, piece) and not is_blocked_by_wall(middle_row, middle_col, piece):
                return True
            else: return False

        return False
    # the BISHOP can move anywhere unoccupied but only attack like a pawn
    elif piece_type == 'B':
        if is_field_occupied(end_row,end_col,piece):
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
        return True
    elif piece_type == 'Q':
        # Queen moves one square diagonally
        return abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1
    elif piece_type == 'K':
        # King moves one square in non-diagonal directions
        return (abs(start_row - end_row) <= 1 and abs(start_col - end_col) == 0) or (abs(start_row - end_row) == 0 and abs(start_col - end_col) <= 1)        
    elif piece_type == 'P':
        # pawn can't take alpha
        if target.upper() == 'A': return False

        # Pawn moves one square in any direction
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
    elif piece_type == 'A':
        # Alpha moves two squares in any direction
        return abs(start_row - end_row) <= 3 and abs(start_col - end_col) <= 3

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
        elif (piece == 'P' and end_row == 7):
            piece = 'A'
        # horse can eliminate the piece he jumps over
        elif piece.upper() == 'N':
            row_diff = abs(start_row - end_row)
            col_diff = abs(start_col - end_col)

            # jumps over a piece, only allow taking a piece on the way when jumping in line or diagonally, not L shape
            if (row_diff + col_diff == 4 or row_diff + col_diff == 2) and (row_diff == 2 or col_diff == 2):
                # Check for jumping over a neighboring piece
                middle_row = (start_row + end_row) // 2
                middle_col = (start_col + end_col) // 2
                if is_field_occupied(middle_row, middle_col, piece) and board[middle_row][middle_col].isupper() != piece.isupper():
                    board[middle_row][middle_col] = " "

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
    global start_pos, screen, game_won

    screen = pygame.display.set_mode((640, 640))
    pygame.display.set_caption("Chess")

    start_pos = None  # Initialize start_pos here
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(screen)

        game_won = is_game_won()
        if game_won != False: 
            print(game_won + " wins!")
            draw_ui_message(screen, game_won + " wins!")

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
