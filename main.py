from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import re
from dotenv import load_dotenv
import os

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

load_dotenv()
username = os.getenv('LINKEDIN_USERNAME')
password = os.getenv('LINKEDIN_PASSWORD')

driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/login')
time.sleep(1)

username_field = driver.find_element(By.ID, 'username')
username_field.send_keys(username)

password_field = driver.find_element(By.ID, 'password')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

time.sleep(1)

driver.get('https://www.linkedin.com/games/queens/')

play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'ember38')))
play_button.click()

parent_div = driver.find_element(By.ID, "queens-grid")
child_divs = parent_div.find_elements(By.TAG_NAME, "div")
cell_colors = []

for child in child_divs:
    class_name = child.get_attribute("class")
    match = re.search(r'cell-color-(\d+)', class_name)
    if match:
        cell_colors.append(match.group(1))

n = int(math.sqrt(len(cell_colors)))
grid = [[0 for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        grid[i][j] = cell_colors[i * n + j]

queens = solve(grid)

actions = ActionChains(driver)
for i, j in queens:
    idx = i * n + j
    cell_button = driver.find_element(By.CSS_SELECTOR, f'div.queens-cell[data-cell-idx="{idx}"]')
    actions.double_click(cell_button).perform()

input("Press Enter to close the browser and end the script...")
driver.quit()

