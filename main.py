import os
import time

import selenium
from selenium import webdriver

from cookie_engine import get_cookies, driver_get_with_cookies
from dataset_loader import default_load, local_load, web_load
from environment import driver_path, main_page, question_path,  cookie_path
from operation_engine import take_exam, answer_question, answer_all_question
from question_engine import question_list_merge, save_question_list, load_question_list

question_result = load_question_list(question_path)

driver = driver_get_with_cookies(main_page, cookie_path)
try:
    take_exam(driver)
    time.sleep(2)
    answer_all_question(driver, {question.stem: question for question in question_result})
finally:
    driver.quit()
