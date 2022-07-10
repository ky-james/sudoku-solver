# import statements
import pygame as pg
import numpy as np
import time
import random

# globals  
BG_COLOUR = (137, 107, 73)
ACCENT_COLOUR = (176, 144 ,107)
NUM_COLOUR = (50, 50, 50)
DIM = (1100, 731)
START_TIME = time.time()
solving = False
board_ind = 0
step_boards = []
step_boards_ind = 0
solve_time = 0

def load_games(file_name):
    # opens and parses file
    file = open(file_name)
    games = []
    line = '?'

    for line in file:
        line = line.split(',')
        games.append(line[0])

    return games

def load_sudoku(index):
    # loads sudoku game into a np array
    board = np.zeros((9,9))

    for num in range(len(sudoku_games[index])):

        if num < 9:
            sudoku_number = int(sudoku_games[index][num])  
            board[0][num] = sudoku_number

        else:
            sudoku_number = int(sudoku_games[index][num])
            board[num//9][num  - (9 * (num // 9))] = sudoku_number

    return board

def find_unfilled(board):
    # finds and returns an unfilled square
    for row in range(9):
        for col in range(9):

            if board[row][col]< 1:
                return (row, col)

    return None

def valid(bo, num, pos):
    # checks if sudoku entry is valid
    for i in range(9):

        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(9):

        if bo[i][pos[1]] == num and pos[0] != 1:
            return False
    
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):

            if bo[i][j] == num and (i,j) != pos:
                return False

    return True

def clone(bo):
    # clones a board np array
    clone = np.zeros((9,9))

    for row in range(9):
        for col in range(9):
            clone[row][col] = bo[row][col]

    return clone

def solve(bo):
    # recursive function that solves a board
    square = find_unfilled(bo)

    if not square:
        return True
    else:
        row, col = square
    
    for i in range(1,10):
        step_boards.append(((row, col), i))
        
        if valid(bo, i, (row,col)):
            bo[row][col] = i

            if solve(bo):
                return True
            
            bo[row][col] = 0
            step_boards.append(((row,col), 0))
        step_boards.append(((row,col), 0))

    return False

def draw_nums(window, font, board):
    # draws all sudoku entries on window
    for row in range(9):
        for col in range(9):
            num = int(board[row][col])

            if num < 1:
                value = font.render(str(num), True, (NUM_COLOUR))
                window.blit(value, (22 + 20 + 75*row, 22 + 75*col))
                
            else:
                value = font.render(str(num), True, (0,0,0))
                window.blit(value, (22 + 20 + 75*row, 22 + 75*col))

def draw_board(window, font):
    # draws the board/grid on window
    pg.draw.rect(window, ACCENT_COLOUR, [22, 22, 678, 678])

    for i in range(10):

        if i %3 == 0:
            pg.draw.line(window, (0,0,0), (22+ 75*i, 22), (22 + 75*i, 697), 5)
            pg.draw.line(window, (0,0,0), (22, 22 + 75*i), (697, 22 + 75*i), 5)

        else:
            pg.draw.line(window, (0,0,0), (22+ 75*i, 22), (22 + 75*i, 697), 3)
            pg.draw.line(window, (0,0,0), (22, 22 + 75*i), (697, 22 + 75*i), 3)
    
    signature = font.render("Programmed with Pride by Ky James", True, (0,0,0))
    window.blit(signature, (735, 700))

def draw_buttons(window):
    # draws the outlines of buttons
    pg.draw.rect(window, ACCENT_COLOUR, [722, 139, 353, 150])
    pg.draw.rect(window, ACCENT_COLOUR, [722, 439, 353, 150])

    pg.draw.line(window, (0,0,0), (722, 139), (722, 289), 5)
    pg.draw.line(window, (0,0,0), (1075, 139), (1075, 289), 5)
    pg.draw.line(window, (0,0,0), (722, 139), (1075, 139), 5)
    pg.draw.line(window, (0,0,0), (722, 289), (1075, 289), 5)
    pg.draw.line(window, (0,0,0), (722, 439), (1075, 439), 5)
    pg.draw.line(window, (0,0,0), (722, 589), (1075, 589), 5)
    pg.draw.line(window, (0,0,0), (722, 439), (722, 589), 5)
    pg.draw.line(window, (0,0,0), (1075, 439), (1075, 589), 5)
    
def draw_solving(window, font):
    # draws text over buttons when the program is solving
    solving_text1 = font.render("Solve Time: ", True, (0,0,0))
    solving_text2 = font.render(str(solve_time)[0:7] + "s", True, (0,0,0))
    solving_text3 = font.render("Cancel", True, (115, 12, 40))

    window.blit(solving_text1, (785, 150))
    window.blit(solving_text2, (820, 215))
    window.blit(solving_text3, (840, 485))

def draw_static(window, font):
     # draws text over buttons when the program is NOT solving

    static_text1 = font.render("Generate a New", True, (0,0,0))
    static_text2 = font.render("Sudoku Board", True, (0,0,0))
    static_text3 = font.render("Solve this Board!", True, (13,125,28))

    window.blit(static_text1, (745, 150))
    window.blit(static_text2, (770, 215))
    window.blit(static_text3, (740, 485))

def clear_side(window):
    # clears the buttons 
    pg.draw.rect(window, BG_COLOUR, [720, 135, 370, 565])

def draw_new(window, num, pos, font):
    # draws new number on window
    row = pos[0]
    col = pos[1]

    pg.draw.rect(window, ACCENT_COLOUR, [27 + 75*row, 27 + 75*col, 67, 67])
    value = font.render(str(num), True, (NUM_COLOUR))
    window.blit(value, (22 + 20 + 75*row, 22 + 75*col))

def main():
    # globals used in main
    global window 
    global grid_font 
    global step_boards
    global step_boards_ind
    global start_board
    global solving
    global solve_time
    global start_time 
    global end_time

    # window set up
    pg.init()
    window = pg.display.set_mode((DIM[0],DIM[1]))
    window.fill(BG_COLOUR)
    pg.display.set_caption("Sudoku Solver")
    grid_font = pg.font.SysFont('Comic Sans Ms', 60)
    button_font = pg.font.SysFont('Comic Sans Ms', 40)
    signature_font = pg.font.SysFont('Comic Sans Ms', 20)
    
    # intial window drawing
    draw_board(window, signature_font)
    draw_nums(window, grid_font, start_board)
    draw_buttons(window)
    draw_static(window, button_font)

    cur_time = time.time()
    while True:

        if solving:
            if time.time() > cur_time + 0.01:
                if step_boards_ind != len(step_boards):

                    # solving animation
                    draw_new(window, step_boards[step_boards_ind][1], step_boards[step_boards_ind][0], grid_font)
                    cur_time = time.time()
                    step_boards_ind += 1

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:

                pg.quit()
                return

            elif event.type == pg.MOUSEBUTTONDOWN:

                coordinates = pg.mouse.get_pos()
                x = coordinates[0]
                y = coordinates[1]

                # top button
                if x < 1075 and x > 724 and y < 288 and y > 142:

                    # generate new sudoku board
                    if not solving:
                        step_boards = []
                        step_boards_ind = 0
                        board_ind = random.randint(0, len(sudoku_games) - 1)
                        board = load_sudoku(board_ind)
                        start_board = clone(board)
                        window.fill(BG_COLOUR)
                        start_time = time.time()
                        solve(board)
                        end_time = time.time()
                        solve_time = end_time - start_time
                        draw_board(window, signature_font)
                        draw_nums(window, grid_font, start_board)
                        draw_buttons(window)
                        draw_static(window, button_font)
                
                # bottom button
                elif x < 1075 and x > 724 and y < 590 and y > 440:
                    # cancel
                    if solving:
                        clear_side(window)
                        draw_buttons(window)
                        draw_static(window, button_font)
                        solving = False
                    # solve this board
                    else:
                        clear_side(window)
                        draw_buttons(window)
                        draw_solving(window, button_font)
                        solving = True

# MAIN LINE  
sudoku_games = load_games("sudoku.csv")
board = load_sudoku(board_ind)
start_board = clone(board)
vis = clone(board)
start_time = time.time()
solve(board)
end_time = time.time()
solve_time = end_time - start_time 
main()