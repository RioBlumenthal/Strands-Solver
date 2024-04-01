from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from nltk.corpus import words

from trie import Trie
from trie import TrieNode

# function to print the 2d array in board form
def printBoard(board):
   for row in board:
      for letter in row:
         print(letter, end=' ')
      print()
      
# names of the elements on the webpage
start_button_class = 'Feo8La_playButton'
close_button_class = 'PwGt5a_closeX'
board_class = 'UOpmtW_board'

# dimensions of the board
ROWS = 8
COLS = 6

# launch the browser and click through start screen to get to puzzle
driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/games/strands")

start_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, start_button_class)))
start_button.click()

close_button = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, close_button_class)))
close_button.click()

# get the puzzle and store as 2d array
board_from_web = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, board_class)))
board = [[0 for x in range(COLS)] for y in range(ROWS)]
buttonAt = 0
for x in range(ROWS):
   for y in range(COLS):
      board[x][y] = board_from_web.find_element(By.ID, f'button-{buttonAt}').text[0]
      buttonAt += 1

# get a list of all english words from nltk
english_words = [word.lower() for word in words.words() if word.isalpha()]

# insert all english words into a trie
trie = Trie()
for word in english_words:
   trie.insert(word.lower())

# function to find all words in the board

def findWords(board, row, col, visited, str, trie, words):
   # mark the current cell as visited
   visited[row][col] = True
   # add the current character to the string
   str += board[row][col]
   # if the string is a word, add it to the list of words
   if trie.search(str):
      words.append(str)
   # check all 8 directions
   for i in range(-1, 2):
      for j in range(-1, 2):
         if row + i >= 0 and row + i < ROWS and col + j >= 0 and col + j < COLS and not visited[row + i][col + j]:
            findWords(board, row + i, col + j, visited, str, trie, words)
   # mark the current cell as not visited
   visited[row][col] = False

driver.quit()
