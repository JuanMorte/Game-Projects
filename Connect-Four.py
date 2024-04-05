def createBoard():
    # Remember 6 floors, 7 towers
    r, c = 6, 7
    if 'n' == input('Standard game? (y/n): '):
        r, c = int(input('r? (2 - 20): ')), int(input('c? (2 - 20): '))
    # Creates a list 'board' with r many items, and in each items there are c many items.
    return [['·'] * c for i in range(r)]

def printBoard(board):
    r, c = len(board), len(board[0])
    spaces = 1
    if r>9 or c>9: spaces = 2 #bigBoard
    x = ''
    for row in range(r-1,-1, -1):
        # Aligning right with spaces
        x += f'{row:>{spaces}}'
        ss = ' '
        if spaces==2: ss = '  '
        for col in range(c):
            x += ss+board[row][col]
        x += ' \n'
    x += ' ' + ' '*spaces
    for col in range(c): x += f'{col:>{spaces}}'+' '
    print(x)

def makeMove(board, player, col):
    r = len(board)
    for row in range(r):
        if board[row][col]!='·' and board[row+1][col]=='·':
            board[row+1][col] = player
            break
        elif board[row][col]=='·':
            board[row][col] = player
            break

def valid(board, move):
    toReturn = True
    if board[len(board) - 1][int(move)] != '·':
        toReturn = False
    return toReturn

def check_win(board):
    X, O = ['X', 'X', 'X', 'X'], ['O', 'O', 'O', 'O']
    r, c = len(board), len(board[0])
    # Check for the win vertically
    for col in range(c):
        check = []
        for row in range(r): 
            if board[row][col] == 'X':
                check.append('X')
            elif board[row][col] == 'O':
                check.append('O')
            if check == X or check == O:
                return True

    # Check for the win horizontally
    for row in range(r):
        check = []
        for col in range(c): 
            if board[row][col] == 'X':
                check.append('X')
            elif board[row][col] == 'O':
                check.append('O')
            if check == X or check == O:
                return True
    
    # Make a diagonal list of items
    for col in range(c - 4):
        for row in range(r - 4):
            for k in range(4):
                check = []
                if board[row + k][col + k] == 'X':
                    check += ['X']
                elif board[row + k][col + k] == 'O':
                    check += ['O']
                if check == X or check == O:
                    return True
        for row in range(3, r - 1):
            for k in range(4):
                check = []
                if board[row - k][col + k] == 'X':
                    check += ['X']
                elif board[row - k][col + k] == 'O':
                    check += ['O']
                if check == X or check == O:
                    return True
    return False

def check_tie(board):
    for i in board:
        for j in i:
            if j == '·':
                return False
    return True

board = createBoard()
printBoard(board)
player = 'X'
while True:
    move = input('player'+player+' (col #): ')
    if move == 'e': break
    while board[len(board) - 1][int(move)] != '·':
        printBoard(board)
        move = input('player'+player+' (col #): ')
        if move == 'e': break
    if move == 'e': break
    makeMove(board, player, int(move))
    printBoard(board)
    if check_win(board):
        print(f'Player {player} has won!')
        break
    if check_tie(board):
        print("Draw!")
        break
    # Alternates between players
    if player == 'X': player = 'O'
    else: player = 'X'
print('bye')