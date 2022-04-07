from sys import argv
from random import randint, choices


class Cell:
    __slots__ = ('opened', 'stat', 'ma')

    def __init__(self):
        self.opened = False
        self.stat = 0  # stat have 4 statements: empty (0), bomb (1), flag(correct) (2), flag(not correct) (3)
        self.ma = 0  # ma - mines around

    def __str__(self):
        if self.stat in (2, 3):
            return 'F'
        elif self.opened:
            return str(self.ma)
        else:
            return '_'


# check is the cell is valid function
def is_valid(x: int, y: int, w: int, h: int) -> bool:
    return bool((0 <= x < w) and (0 <= y < h))


# function that generates game matrix
def generate_matrix(_h: int, _w: int, _m: int) -> list:
    game_matrix = [[Cell() for _ in range(_w)] for _ in range(_h)]
    cnt = 0
    while cnt < _m:
        x, y = randint(0, _w - 1), randint(0, _h - 1)
        if game_matrix[y][x].stat != 1:
            for _x in range(x - 1, x + 2):
                for _y in range(y - 1, y + 2):
                    if is_valid(_x, _y, _w, _h):
                        game_matrix[_y][_x].ma += 1
            game_matrix[y][x].stat = 1
            cnt += 1
    return game_matrix


# function that makes matrix print correct
def print_matrix(matrix: list, remain_flags: int):
    print('\n' * 6)
    print(f'\tRemain flags: {remain_flags}\n')
    w = len(matrix[0])
    h = len(matrix)
    padding = ' ' if w < 10 else '  '
    print('\t', 'G', '  ' if h >= 10 else ' ', padding.join([str(i + 1) for i in range(min(w, 9))]), padding, padding[:-1].join([str(i + 1) for i in range(9, w)]), sep='')
    for n, i in enumerate(matrix):
        print('\t', n + 1, '  ' if n + 1 < 10 and h >= 10 else ' ', *[str(j) + padding for j in i], sep='')
    print('\n' * 2)


# function that open one cell
def open_cell(matrix: list, x: int, y: int):
    if matrix[y][x].stat == 1:
        print('\n' * 2)
        print('\tYou lose!')
        exit(0)
    if matrix[y][x].stat in (2, 3):
        print('\n' * 2)
        print('\tFlag here! Cannot open!')
        return
    matrix[y][x].opened = True
    open_cells(matrix, x, y)


# recursive function that open a lot of cells with no mines on them
def open_cells(matrix: list, x: int, y: int):
    matrix[y][x].opened = True
    if matrix[y][x].ma == 0:
        for _x in range(x - 1, x + 2):
            for _y in range(y - 1, y + 2):
                if is_valid(_x, _y, matrix.__len__(), matrix[0].__len__()):
                    if not matrix[_y][_x].opened:
                        open_cells(matrix, _x, _y)


# functions for placing flags
def place_flag(matrix: list, x: int, y: int):
    if matrix[y][x].stat == 0:
        matrix[y][x].stat = 3
        return
    if matrix[y][x].stat == 1:
        matrix[y][x].stat = 2
        return
    if matrix[y][x].stat == 3:
        matrix[y][x].stat = 0
        return
    if matrix[y][x].stat == 2:
        matrix[y][x].stat = 1
        return


# functions that check player win
def check_win(matrix: list) -> bool:
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x].stat == 1 or matrix[y][x] == 3:
                return False
    return True


# main function
def main():

    remain_flags = 5
    h, w, m = 5, 5, 5

    if '--help' in argv:
        print('''
        Sapper game made by Denis with Python 3.8
        
        Input parameters:
        
            --help will show help monolog
            -h [number] for set height of game field
            -w [number] for set width of game field
            -m [mine number] for set mines Counter
            -e for escape from program and do nothing
            other parameters will be ignored
            
        In-game commands:
        
            -o [x] [y] open selected cell
            -f [x] [y] mark/unmark selected cell with flag
            -e exit and go programming
        ''')

        exit(0)

    try:
        if '-h' in argv:
            h = int(argv[argv.index('-h') + 1])
        if '-w' in argv:
            w = int(argv[argv.index('-w') + 1])
        if '-m' in argv:
            m = int(argv[argv.index('-m') + 1])
            remain_flags = m
        if '-e' in argv:
            exit(0)
        if m > h * w:
            print('\tToo much mines!')
            exit(0)
        w = 99 if w > 99 else w
        h = 99 if h > 99 else h
    except ValueError:
        print(f'\tValue Error! Lox!')
    except IndexError:
        print(f'\tIndex Error! Lox!')

    game_matrix = generate_matrix(h, w, m)

    while not False:
        print_matrix(game_matrix, remain_flags)
        prompt = input('>>> ')
        if '-e' in prompt:
            exit(0)
        prompt_list = prompt.split()
        try:
            command, x, y = prompt_list
        except Exception as e:
            print(e)
            continue
        if command == '-o':
            open_cell(game_matrix, int(x) - 1, int(y) - 1)
        if command == '-f':
            if game_matrix[int(y) - 1][int(x) - 1].opened:
                print('\n' * 2, "\tNo! You can't place flag on opened cells!", '\n' * 2)
            elif remain_flags <= 0:
                print('\n' * 2, "\tNo! You have no more flags!", '\n' * 2)
            else:
                place_flag(game_matrix, int(x) - 1, int(y) - 1)
                remain_flags -= 1
        if check_win(game_matrix):
            print('\n' * 3, '    Congratulations! You won!', '\n' * 2)
            exit(0)


if __name__ == '__main__':
    main()
