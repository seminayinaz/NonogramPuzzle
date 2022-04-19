# Nonogram Puzzle

# Projenin calistirilmasi :
# nonogram.py dosyasini calistirarak geyik.txt ya da balina.txt 
# dosya adlarini verip nonogram bulmacayi gorebilirsiniz.

from ast import literal_eval

class Nonogram:
    def __init__(self, row, blok, rowIndex, blokIndex):
        self.row = row
        self.blok = blok
        self.rowIndex = rowIndex
        self.blokIndex = blokIndex

def pr_row(row, blok):
    # Satirlari renklendirmek icin olasiliklarin listesini verir.

    if (not blok):
        blok = [-1]

    if (not row):
        return []

    coloredCell= sum(blok)  
    if (coloredCell > len(row) - row.count(0)) or (len(row) < coloredCell + len(blok)-1):
        return []

    return vrs_row(row, blok, 0, 0, 0)


def vrs_row(row, blok, rowIndex, blokIndex, sequence):
    # Kisitlari izleyen bir satiri renklendirmek icin olasiliklarin listesini verir.

    list = []
    for i in range(rowIndex, len(row)):
        if (row[i] == -1):
            row[i] = 0  
            list += vrs_row(row[:], blok, i, blokIndex, sequence)
            row[i] = 1  
            list += vrs_row(row[:], blok, i, blokIndex, sequence)
            row[i] = -1 

            return list

        if ((row[i] == 1) and (blok[blokIndex] > sequence)):
            sequence += 1  

        elif ((row[i] == 0) and (0 < sequence < blok[blokIndex])):
            return []

        elif (blok[blokIndex] == sequence):
            if row[i] == 1: 
                return []

            if (blokIndex != len(blok) - 1): 
                blokIndex += 1 
                sequence = 0 

    if ((sequence >= blok[blokIndex]) and (blokIndex == len(blok) - 1)):
        list.append(row)  

    return list


def intersection_row(rows):
    # Verilen tum satirlar arasinda bir kesisim satiri dondurur.

    if (not rows):
        return []

    i_row = [] 

    for i, val in enumerate(rows[0]):
        i_row.append(-1)
        if (val != -1):
            value = True

            for j in range(1, len(rows)):
                if (rows[j][i] != val):
                    value = False 
                    break 

            if (value):
                i_row[i] = val

    return i_row


def constraint(board, constraints):
    # Hangi hucrelerin renkli olmasi gerektigini kontrol eder ve tahtayi buna gore degistirir.

    if  (not constraints[0]) or (not board) or (not constraints[1]):
        return 

    newResult = True
    while newResult: 
        rows_constraints(board, constraints[0])

        trpBoard = []
        for i in range(len(board[0])):
            trp = []
            for j in range(len(board)):
                trp.append(board[j][i])
            trpBoard.append(trp)

        newResult = rows_constraints(trpBoard, constraints[1])

        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j] = trpBoard[j][i]


def rows_constraints(rows, constraints):
    # Hangi hücrelerin renklendirilip renklendirilmeyecegini kontrol eder ve satirlari degistirir.

    change = False

    for i, row in enumerate(rows):
        if (-1 in row):  
            varRow = pr_row(row, constraints[i])
            if (varRow): 
                newRow = intersection_row(varRow)
                if (row != newRow):
                    rows[i] = newRow
                    change = True

    return change


def solveNonogram(board, constraints, rowIndex):
    # Nonogram tahtasini cozer ve cozumlerin listesini dondurur.

    board_game = createBoard(constraints)
    constraint(board_game, constraints)
    board = board_game
    board = copyBoard(board_game)
    constraint(board, constraints)
    rowIndex, colIndex = emptyCells(board, rowIndex)

    if (rowIndex == -1): 
        return [board] 

    ans = []  

    # Backtracking
    nextRow = rowIndex
    if (colIndex == len(board[0]) - 1): 
        nextRow += 1

    board[rowIndex][colIndex] = 1
    ans += solveNonogram(board, constraints, nextRow)
    
    board[rowIndex][colIndex] = 0
    ans += solveNonogram(board, constraints, nextRow)

    return ans


def emptyCells(board, rowIndex):
    # Bos hucreyi arar ve indexini dondurur.

    for i in range(rowIndex, len(board)):
        for j, value in enumerate(board[i]):
            if (value == -1):
                return i, j

    return -1, -1


def createBoard(constraints):
    # Kisitlara gore board yaratir.

    board = []
    for i in range(len(constraints[0])):
        board.append([-1] * len(constraints[1]))
    return board


def copyBoard(board):

    copy = []
    for row in board:
        copy.append(row[:])
    return copy


table = {1: '■', 0: '·', -1: '?'}


def printBoard(board):

    board_str = ""
    for line in board:
        for sq in line:
            board_str += table[sq] + " "
        board_str += "\n"

    print()
    print(board_str, end="")
    print()

filename = input("Please enter the file name.\n")
file = open(filename, "r")
content = file.read()
dict = literal_eval(content)


if __name__ == "__main__":
    
    for name, const in dict.items():
        print("\nStarting to solve",name)
        board_game = createBoard(const)
        constraint(board_game, const)
        board = board_game
        printBoard(board)
        
