from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://google.com")

print(driver.title)