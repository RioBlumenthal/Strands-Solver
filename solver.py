from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

start_button_class = 'Feo8La_playButton'
close_button_class = 'PwGt5a_closeX'

driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/games/strands")

start_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, start_button_class)))
start_button.click()

close_button = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, close_button_class)))
close_button.click()

print(driver.title)

driver.quit()