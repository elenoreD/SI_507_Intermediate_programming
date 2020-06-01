
# CONSTANTS
PLAYER_NAMES = ["Nobody", "X", "O"] 


# FUNCTIONS
def player_name(player_id):
    '''return the name of a player with a specified ID

    Looks up the name in the PLAYER_NAMES global list

    Parameters
    ----------
    player_id: int
        player's id, which is an index into PLAYER_NAMES

    Returns
    -------
    string
        the player's name

    '''
    return PLAYER_NAMES[player_id]


def display_board(board):
    '''display the current state of the board

    board layout:
    1 | 2 | 3
    4 | 5 | 6
    7 | 8 | 9

    Numbers are replaced by players' names once they move. 
    Iterate through the board and choose the right thing
    to display for each cell.

    Parameters
    ----------
    board: list
        the playing board

    Returns
    -------
    None
    '''

    board_to_show = "" # string that will display the board, starts empty
    for i in range(len(board)):
        if board[i] == 0: # 0 means unoccupied
            # displayed numbers are one greater than the board index
            board_to_show += str(i + 1) # display cell number
        else:
            board_to_show += player_name(board[i]) # display player's mark
        if (i + 1) % 3 == 0: # every 3 cells, start a new row
            board_to_show += "\n"
        else:
            board_to_show += " | " # within a row, divide the cells
    print()
    print(board_to_show)


def make_move(player, board):
    '''allows a player to make a move in the game

    displays who's move it is (X or O)
    prompts the user to enter a number 1-9
    validates input, repeats until valid input is entered
    checks move is valid (space is unoccupied), repeats until valid move
    is entered

    Parameters
    ----------
    player: int
        the id of the player to move (1 = X, 2 = O)

    board: list
        the board upon which to move
        the board is modified in place when a valid move is entered
    '''
    current_player=player_name(player)
    print('current player is ', current_player)
    
    while True:
        every_move=input('enter a number 1-9: ')
        if every_move.isnumeric() and int(every_move) in range (1,10): # validate input
            board_index=int(every_move)-1 #Since python start counting from 0
            if board[board_index] == 0: # When player makes a valid move, board is displayed with their player name in the correct cell.  
                board[board_index]=player
                break
            else:
                print('the board postion is already taken, please correct your input: ') # Program rejects moves into occupied spaces and prompts user for a different move.
        else:
            print('please correct your input') # Program rejects invalid inputs (non-numerics and numbers < 1 or > 9)


def check_win_horizontal(board):
    '''check if the horizontal values are identical

    check every row, and if the 3 values are same, it will return the player's name, or it will return 0, means 0 winners in horizontal level yet.

    Parameters
    ----------
    board: list
        the board upon which to move
        the board is modified in place when a valid move is entered

    Returns
    -------
    string or integer
        the player's name or 0

    '''
    if (board[0] != 0 and 
        board[0] == board[1] and 
        board[0] == board[2]):
        return board[0]
    if (board[3] != 0 and
        board[3] == board[4] and 
        board[3] == board[5]):
        return board[3]
    if (board[6] != 0 and
        board[6] == board[7] and 
        board[6] == board[8]):
        return board[6]
    return 0


def check_win_vertical(board):
    '''check if the vertical values are identical

    check every column, and if the 3 values are same, it will return the player's name, or it will return 0, means 0 winners in vertical level yet.

    Parameters
    ----------
    board: list
        the board upon which to move
        the board is modified in place when a valid move is entered

    Returns
    -------
    string or integer
        the player's name or 0

    '''
    if (board[0] != 0 and 
        board[0] == board[3] and 
        board[0] == board[6]):
        return board[0]
    if (board[1] != 0 and
        board[1] == board[4] and 
        board[1] == board[7]):
        return board[1]
    if (board[2] != 0 and
        board[2] == board[5] and 
        board[2] == board[8]):
        return board[2]
    return 0


def check_win_diagonal(board):
    '''check if the diagonal values are identical

    check every diagonal rows, and if the 3 values are same, it will return the player's name, or it will return 0, means 0 winners in diagonal level yet.

    Parameters
    ----------
    board: list
        the board upon which to move
        the board is modified in place when a valid move is entered

    Returns
    -------
    string or integer
        the player's name or 0

    '''
    if (board[0] != 0 and 
        board[0] == board[4] and 
        board[0] == board[8]):
        return board[0]
    if (board[3] != 0 and
        board[3] == board[4] and 
        board[3] == board[6]):
        return board[3]
    return 0


def check_win(board):
    '''checks a board to see if there's a winner

    delegates to functions that check horizontally, vertically, and 
    diagonally to see if there is a winner. Returns the first winner
    found in the case of multiple winners.

    Parameters
    ----------        
    board: list
        the board to check

    Returns
    -------
    int
        the player ID of the winner. 0 means no winner found.
    '''

    winner = check_win_horizontal(board)
    if (winner != 0):
        return winner
    
    winner = check_win_vertical(board)
    if (winner != 0):
        return winner
    
    winner = check_win_diagonal(board)
    if (winner != 0):
        return winner

    else:
        return 0


def next_player(current_player):
    '''determines who goes next

    given the current player ID, returns the player who should 
    go next

    Parameters
    ----------        
    current_player: int
        the id of the player who's turn it is now

    Returns
    -------
    int
        the id of the player to go next
    '''
    if current_player == 1:
        return 2 
    if current_player == 2:
        return 1
    else:
        return 0

# MAIN PROGRAM (INDENT LEVEL 0)

# GLOBAL VARIABLES
board = [0, 0, 0,   # top row:    indices 0, 1, 2
         0, 0, 0,   # middle row: indices 3, 4, 5
         0, 0, 0]   # bottom row: indices 6, 7, 8

player = 1          # X goes first
moves_left = 9      # number of moves so far 
winner = 0          # "Nobody" is winning to start



while (moves_left > 0 and winner == 0):
    display_board(board)
    make_move(player, board)
    winner = check_win(board)
    player = next_player(player)
    moves_left -= 1

display_board(board)

if winner==0:
    print('Game over, no one wins')

if winner !=0:
    print('Congraduations!', player_name(winner), 'You win!')
