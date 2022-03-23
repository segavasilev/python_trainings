empty = '_________'
matrix = [[empty[i], empty[i+1], empty[i+2]] for i in range(0, len(empty), 3)]

def printer(matrix):
    print('---------')
    for i in matrix:
        print('| ' + ' '.join(i) + ' |')
    print('---------')

def win_lose(matrix):
    arr = [j for i in matrix for j in i]
    x = arr.count('X')
    o = arr.count('O')
    u = arr.count('_')
    s = arr.count(' ')
    line = [arr[i:i + 3] for i in range(0, len(arr), 3)]
    col = [arr[i:len(arr):3] for i in range(0, 3, 1)]
    diag = [''.join([arr[i] for i in range(0, len(arr), 2) if i % 2 == 0][0::2]),
            ''.join([arr[i] for i in range(0, len(arr), 2) if i % 2 == 0][1:4:1])]
    results = [''.join(item) for sublist in [line, col, diag] for item in sublist]

    if abs(x - o) > 1 or results.count('XXX') == results.count('OOO') != 0:
        print('Impossible')
        return 0
    elif results.count('XXX') == 1:
        print('X wins')
        return 1
    elif results.count('OOO') == 1:
        print('O wins')
        return 2
    elif  abs(x - o) <= 1 and u == s == 0 and all(True for i in results if results not in ['XXX', 'OOO']):
        print('Draw')
        return 3
    else:
        print('Game not finished')
        return 4

printer(matrix)

step = ['X']

while True:
    coords = input('Enter the coordinates: ').replace(' ', '')
    if coords[0].isdigit() and coords[1].isdigit():
        if int(coords[0]) in [1, 2, 3] and int(coords[1]) in [1, 2, 3]:
            if matrix[int(coords[0])-1][int(coords[1])-1] in ('_', ' '):
                matrix[int(coords[0])-1][int(coords[1])-1] = step[0]
                printer(matrix)
                step = ['O' if step[0] == 'X' else 'X']
                if win_lose(matrix) in [0, 1, 2, 3]:
                    break
                else:
                    pass
            else:
                print('This cell is occupied! Choose another one!')
        else:
            print('Coordinates should be from 1 to 3!')
    else:
        print('You should enter numbers!')
