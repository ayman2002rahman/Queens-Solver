import cv2
import pyautogui
import pygetwindow as gw
import keyboard
import time
import numpy as np
from PIL import Image, ImageDraw

# the vision window is always fixed, so cell size depends on this fixed size divided by n
WINDOW_SIZE = 1000 # some constant

def capture_window(window_title, x, y, width, height, file_name):
    for i in range(3):
        print(3 - i)
        time.sleep(1)
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot.save(f'{file_name}.png')

STROKE_BORDER = 3
DIVIDER = 1
def computer_vision_model(img_path): # returns a nxn grid of colors distinguised by their corresponding integer
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 149, 255, None)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    n = int(np.sqrt(len(contours)-2))

    grid = []
    img = Image.open(img_path)
    cell_size = (398 - 2*STROKE_BORDER - n + 1) // n
    width, height = img.size
    colors = {}
    curr = 0
    for i in range(n):
        y = STROKE_BORDER + cell_size * i + cell_size // 2 + DIVIDER * i
        row = []
        for j in range(n):
            x = STROKE_BORDER + cell_size * j + cell_size // 2 + DIVIDER * j
            r, g, b, a = img.getpixel((x, y))
            color = (r, g, b)
            if color not in colors:
                colors[color] = curr
                curr += 1
            row.append(colors[color])
        grid.append(row)
    
    return grid

def solve(grid):
    n = len(grid)

    queens = set()
    colored_queens = set()
    column_queens = set()
    
    def dfs(i):
        if i == n:
            return len(colored_queens) == n
        
        for j in range(n):
            if j not in column_queens and grid[i][j] not in colored_queens and (i-1, j-1) not in queens and (i-1, j+1) not in queens:
                queens.add((i, j))
                colored_queens.add(grid[i][j])
                column_queens.add(j)
                if dfs(i+1):
                    return True
                queens.remove((i, j))
                colored_queens.remove(grid[i][j])
                column_queens.remove(j)
        return False

    dfs(0)
    return list(queens)

def control_mouse(queens, window_x, window_y):
    n = len(queens)
    cell_size = (398 - 2*STROKE_BORDER - n + 1) // n

    for i, j in queens:
        y = STROKE_BORDER + cell_size * i + cell_size // 2 + DIVIDER * i + window_y
        x = STROKE_BORDER + cell_size * j + cell_size // 2 + DIVIDER * j + window_x
        pyautogui.moveTo(x, y)
        pyautogui.doubleClick()

# ==== MAIN PROGRAM TO SOLVE QUEENS BOARD GAME ==== 
window_title = 'Your Window Title'
WINDOW_X = 557
WINDOW_Y = 324
WINDOW_SIZE = 398

print('Program started:')
key = input()
capture_window(window_title, WINDOW_X, WINDOW_Y, WINDOW_SIZE, WINDOW_SIZE, 'current_queens_game')
grid = computer_vision_model('current_queens_game.png')
queens = solve(grid)
control_mouse(queens, WINDOW_X, WINDOW_Y)