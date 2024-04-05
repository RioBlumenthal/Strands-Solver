from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import re
import PySimpleGUI as sg

from trie import Trie

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

# path to chromedriver
CHROMEDRIVER_PATH = "C:/Users/Rio/OneDrive/Documents/Python happies/chromedriver-win64/chromedriver.exe"

# min/max length of words
MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 12


# launch the browser and click through start screen to get to puzzle 
service = Service(executable_path=CHROMEDRIVER_PATH)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-third-party-cookies')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(service=service,
options=options)
driver.get("https://www.nytimes.com/games/strands")

start_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, start_button_class)))
start_button.click() 

close_button = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, close_button_class)))
close_button.click()

p_elements = driver.find_elements(By.TAG_NAME, "p")

# regex pattern
pattern = r"0 of (\d+) theme words found."
num_words = 0
for p_element in p_elements:
   # Get the text
   text = p_element.text

   matches = re.match(pattern, text)
   if matches:
      num_words = matches.group(1)
      break

print(f"Number of theme words: {num_words}")

# get the puzzle and store as 2d array
board_from_web = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, board_class)))
board = [[0 for x in range(COLS)] for y in range(ROWS)]
buttonAt = 0
for x in range(ROWS):
   for y in range(COLS):
      board[x][y] = board_from_web.find_element(By.ID, f'button-{buttonAt}').text[0].lower()
      buttonAt += 1

# close the web browser
driver.quit()

def is_lowercase(word):
    return bool(re.match(r'^[a-z]+$', word))

printBoard(board)

# insert all english words into a trie
trie = Trie()
with open("30k.txt", "r", encoding="utf-8") as file:
   for line in file:

      # make sure the word is within the min/max length and is alphabetical
      line = line.strip().lower()
      if (len(line) >= MIN_WORD_LENGTH) and (len(line) <= MAX_WORD_LENGTH) and is_lowercase(line):
         try:
            trie.insert(line)
         except IndexError:
            print(f"Error with: {line}")
            raise  # Re-raise the exception to stop further processing

# function to find all words in the board and return 
# a list of the 48 bit representations of the words
# where each bit represents a letter in the board
# with 1 being the letter is used and 0 being the letter is not used in the word
   
def arrayToBinary(array):
   binary = 0
   for x in range(ROWS):
      for y in range(COLS):
         binary <<= 1
         binary += array[x][y]
   return binary

def findWords(board, trie):
   words = []
   wordsArray = []

   # for each letter on the board, call the helper function to find all the words
   # that start with that letter
   for x in range(ROWS):
      for y in range(COLS):
         visited = [[False for i in range(COLS)] for j in range(ROWS)]
         wordLocationArray = [[0 for i in range(COLS)] for j in range(ROWS)]
         findWordsHelper(board, trie, x, y, visited, board[x][y], words, wordLocationArray, wordsArray)
   return words, wordsArray

# helper function to find all words that start with a given letter on the board
def findWordsHelper(board, trie, x, y, visited, word, words, wordLocationArray, wordsArray):
   visited[x][y] = True
   wordLocationArray[x][y] = 1

   # check if the current thing is a word
   if trie.search(word):
      words.append(word)
      wordsArray.append(arrayToBinary(wordLocationArray))

   # check all the words branching off of that letter
   if trie.startsWith(word):
      for i in range(-1, 2):
         for j in range(-1, 2):
            if x + i >= 0 and x + i < ROWS and y + j >= 0 and y + j < COLS and not visited[x + i][y + j]:
               wordLocationArray[x + i][y + j] = 1
               findWordsHelper(board, trie, x + i, y + j, visited, word + board[x + i][y + j], words, wordLocationArray, wordsArray)
   visited[x][y] = False 
   wordLocationArray[x][y] = 0

def count_ones(binary_number):
    count = 0
    while binary_number:
        count += binary_number & 1
        binary_number >>= 1
    return count

# find all words in the board 
words, wordsInBinary = findWords(board, trie)
count = 0
for i in range(len(wordsInBinary)):
   for j in range(i + 1, len(wordsInBinary)):
      if wordsInBinary[i] & wordsInBinary[j] == 0:
         thingToConsider = wordsInBinary[i] | wordsInBinary[j]
         for k in range(j + 1, len(wordsInBinary)):
            if thingToConsider & wordsInBinary[k] == 0:
               thingsToConsider = thingToConsider | wordsInBinary[k]
               for l in range(k + 1, len(wordsInBinary)):
                  if thingsToConsider & wordsInBinary[l] == 0:
                     thingsToConsider = thingsToConsider | wordsInBinary[l]
                     for m in range(l + 1, len(wordsInBinary)):
                        if thingsToConsider & wordsInBinary[m] == 0:
                           thingsToConsider = thingsToConsider | wordsInBinary[m]
                           if count_ones(thingsToConsider) >= 36:
                              count += 1
                              if(count % 1000 == 0):
                                 print(count)
                              #print(words[i], words[j], words[k], words[l], words[m])

print(count)
# generate a GUI to show the board
layout = [[sg.Button(board[x][y], size=(3, 3), pad=(1, 1), button_color=('white', 'black'), key=(x, y)) for y in range(COLS)] for x in range(ROWS)]
window = sg.Window("Strands Solver", layout)

while True:
   event, values = window.read()
   if event == sg.WINDOW_CLOSED:
      break

window.close()