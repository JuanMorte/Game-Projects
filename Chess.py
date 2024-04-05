def startBoard():
    board = [['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
             ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
             ['--', '--', '--', '--', '--', '--', '--', '--'],
             ['--', '--', '--', '--', '--', '--', '--', '--'],
             ['--', '--', '--', '--', '--', '--', '--', '--'],
             ['--', '--', '--', '--', '--', '--', '--', '--'],
             ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
             ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']]
    return board

def printboard(board):
    i = 8
    for row in board:
        print(f'{i}. ', end='')
        i -= 1
        for j in range(len(row) - 1):
            print(row[j], end = ' ')
        print(f'{row[7]}')
    print('   a. b. c. d. e. f. g. h.')

temp = input().split(' ')
move = {}
# Inputing the moves into white and black
move['white'] = []
move['black'] = []
for i in range(len(temp)):
    if i%2 == 0:
        move['white'].append(temp[i])
    else:
        move['black'].append(temp[i])

board = startBoard() 
printboard(board)
turn = 'white'
rnd = 0
columns = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5:'f', 6:'g', 7:'h'}
revCol = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h':7}
checked = {'white': False, 'black': False}
opp = {'white': 'black', 'black': 'white'}
blackPawn = [False]*8
whitePawn = [False]*8

def inCheck(currentturn):
    # Finding the location of both kings
    global checked
    global turn
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'wk':
                wking = f'{columns[j]}{8-i}'
            if board[i][j] == 'bk':
                bking = f'{columns[j]}{8-i}'

    checkerWhite = 0
    checkerBlack = 0
    # Checking if both player is in check after possible move
    for i in range(8):
        for j in range(8):
            if board[i][j][0] == 'w':
                turn = 'white'
                moveset = allMoves(board[i][j],f'{columns[j]}{8-i}')
                if bking in moveset:
                    checked['black'] = True
                    checkerBlack += 1
                turn = currentturn
            if board[i][j][0] == 'b':
                turn = 'black'
                moveset = allMoves(board[i][j],f'{columns[j]}{8-i}')
                if wking in moveset:
                    checked['white'] = True
                    checkerWhite += 1
                turn = currentturn
    if checkerWhite == 0:
        checked['white'] = False
    if checkerBlack == 0:
        checked['black'] = False

def checkmate(currentturn): # The currentturn is the one that is checked to be lost or not
    # If it's not even checked why bother
    if checked[currentturn] == False:
        return False

    # Simulate every single move
    for i in range(8):
        for j in range(8):
            if board[i][j][0] == currentturn[0]:
                moveset = allMoves(board[i][j],f'{columns[j]}{8-i}')
                for move in moveset:
                    piece = board[i][j]
                    front = board[8-int(move[1])][revCol[move[0]]]
                    simMove(piece, f'{columns[j]}{8-i}', move)
                    inCheck(currentturn)
                    # Make a piece for the possibly eaten piece
                    if checked[currentturn] == False:
                        undoMove(piece, front, move, f'{columns[j]}{8-i}')
                        return False
                    undoMove(piece, front, move, f'{columns[j]}{8-i}')
    return True

def simMove(piece, src, des):
    board[8-int(des[1])][revCol[des[0]]] = piece
    board[8-int(src[1])][revCol[src[0]]] = '--'

def undoMove(piece, front, src, des):
    board[8-int(des[1])][revCol[des[0]]] = piece
    board[8-int(src[1])][revCol[src[0]]] = front

def pawn(color, col, row):
    moves = []
    if color == 'w': mult = -1
    if color == 'b': mult = 1

    # Add the basic forward moves and the possible two steps
    new_row = row + (1*mult)
    if board[new_row][col] == '--' and new_row >= 0 and new_row < 8:
        moves.append(f'{columns[col]}{8-new_row}')
        new_row = row + (2*mult)
        # Two steps
        if color == 'w' and whitePawn[col] == False:
            if board[new_row][col] == '--':
                moves.append(f'{columns[col]}{8-new_row}')
        elif color == 'b' and blackPawn[col] == False:
            if board[new_row][col] == '--':
                moves.append(f'{columns[col]}{8-new_row}')

    # Add the taking moves
    up = row + (1*mult)
    left = col - 1
    right = col + 1
    if up >= 0 and up < 8:
        if left >= 0 and left < 8:
            if board[up][left][0] == opp[turn][0]:
                moves.append(f'{columns[left]}{8-up}')
        if right >= 0 and right < 8:
            if board[up][right][0] == opp[turn][0]:
                moves.append(f'{columns[right]}{8-up}')
    return moves

def knight(col, row):
    moves = []
    possible = [[1, 2], [1, -2], [2, 1], [2, -1], [-1, 2], [-1, -2], [-2, -1], [-2, 1]]
    for move in possible:
        new_row = row + move[1]
        new_col = col + move[0]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            # As long as it's not the same colored piece
            if board[new_row][new_col][0] != turn[0]:
                moves.append(f'{columns[new_col]}{8-new_row}')
    return moves

def bishop(col, row):
    moves = []
    directions = [[1, 1], [1, -1], [-1, -1], [-1, 1]]
    for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]
        while new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            # It's an empty space
            if board[new_row][new_col] == '--':
                moves.append(f'{columns[new_col]}{8-new_row}')
            # It's a piece of a different color
            elif board[new_row][new_col][0] == opp[turn][0]:
                moves.append(f'{columns[new_col]}{8-new_row}')
                break
            # It's a piece of the same color
            else:
                break
            new_row += direction[0]
            new_col += direction[1]
    return moves

def rook(col, row):
    # Just like bishop but just vertical and horizontal
    moves = []
    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]
        while new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            if board[new_row][new_col] == '--':
                moves.append(f'{columns[new_col]}{8-new_row}')
            elif board[new_row][new_col][0] == opp[turn][0]:
                moves.append(f'{columns[new_col]}{8-new_row}')
                break
            else:
                break
            new_row += direction[0]
            new_col += direction[1]
    return moves

def queen(col, row):
    # The queen's move is just the bishop move plus the rook's move
    moves = bishop(col, row) + rook(col, row)
    return moves

def king(col, row):
    moves = []
    possible = [[1,0],[-1,0],[0,1],[0,-1]]
    for move in possible:
        new_row = row + move[1]
        new_col = col + move[0]
        if new_row >= 0 and new_row < 8 and new_col >= 0 and new_col < 8:
            # As long as it's not the same colored piece
            if board[new_row][new_col][0] != turn[0]:
                moves.append(f'{columns[new_col]}{8-new_row}')
    return moves

def allMoves(item, src):
    color = item[0]
    piece = item[1]

    col = revCol[src[0]]
    row = int(src[1]) # This is flipped because 1 is suppose to be bottom
    row = 8 - row

    # Check if the piece is in the said spot
    if board[row][col] != item:
        return []

    moves = []
    if piece == 'p':
        moves = pawn(color, col, row)
    elif piece == 'n':
        moves = knight(col, row)
    elif piece == 'b':
        moves = bishop(col, row)
    elif piece == 'q':
        moves = queen(col, row)
    elif piece == 'k':
        moves = king(col, row)
    return moves

while True:
    if checkmate(turn):
        print(f'{opp[turn]} win!')
        break
    try:
        current = move[turn][rnd]
    except:
        break
    piece = current[:2:]
    src = f'{current[3]}{current[5]}'
    des = f'{current[8]}{current[10]}'

    # Find all possible move for the current piece
    possibleMoves = allMoves(piece, src)

    # If it's not the correct color
    if piece[0] != turn[0]:
        possibleMoves = []
        
    # If possible moves are nul, or the typed is not in possible moves, it returns errors and stops
    print(f'{turn} move: {current}')
    if possibleMoves == [] or des not in possibleMoves:
        print('error', current)
        break
    else:
        # Make the move in the board
        board[8-int(des[1])][revCol[des[0]]] = piece
        board[8-int(src[1])][revCol[src[0]]] = '--'

        # If the pawn is already moved, it can't move two steps again
        if piece[1] == 'p':
            if piece[0] == 'w':
                whitePawn[revCol[des[0]]] = True
            elif piece[0] == 'b':
                blackPawn[revCol[des[0]]] = True
        
        # If after the turn, it is in check, then break it up
        inCheck(turn)
        if checked[turn]:
            print('error', current)
            break

        printboard(board)
        if turn == 'white':
            turn = 'black'
        elif turn == 'black':
            turn = 'white'
            rnd += 1