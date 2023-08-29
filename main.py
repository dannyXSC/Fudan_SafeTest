import selenium
from selenium import webdriver

from dataset_loader import default_load
from environment import driver_path

# driver = webdriver.Chrome(executable_path=driver_path)
# input()
# driver.quit()
result = default_load()
print(len(result))