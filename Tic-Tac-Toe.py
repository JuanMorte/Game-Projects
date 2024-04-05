def board(value, lenght):
    for i in range(size**2):
        numlenght = 1
        if value[i] != "X" and value[i] != "O": 
            numlenght = len(str(i))
        if numlenght < lenght or value[i] == "X" or value[i] == "O":
            print(" "*(lenght-numlenght), end = "")        
        if (i+1)%size == 0:
            print(value[i])
        else:
            print(value[i], end=" ")

def check_win(size, value):
    row, col, X, O = list(_ for _ in range(0, size**2, size)), list(_ for _ in range(0, size)), list(ele for ele in "X"*size), list(ele for ele in "O"*size)
    for i in row:
        for j in col:
            if value[i:i+size:] == X or value[i:i+size:] == O or value[j:size**2:size] == X or value[j:size**2:size] == O:
                return True
    if value[0::size+1] == X or value[0::size+1] == O or value[size-1:(size**2)-size+1:size-1] == X or value[size-1:(size**2)-size+1:size-1] == O:
        return True
    else: return False

size = int(input("Size--> "))
lenght = len(str(size**2 + 1))
value = list(i for i in range(size**2))
rotation, players = 0, ["X", "O"]
board(value, lenght)
while check_win(size, value) == False and rotation < size**2:
    answer = int(input(f'{players[rotation%2]}--> '))
    value[answer] = players[rotation%2]
    rotation += 1
    board(value, lenght)

if rotation == size**2 and check_win(size, value) == False:
    print("Winner: None")
elif check_win(size, value):
    print(f"Winner: {players[(rotation+1)%2]}")