from typing import List

from bs4 import BeautifulSoup
import re
from selenium import webdriver

from cookie_engine import driver_get_with_cookies
from environment import dataset_path, driver_path, main_page
from operation_engine import goto_result
from question import Question
from question_engine import load_question_list


# 还有一些没答案的，这里没有处理

def default_load() -> List[Question]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')

    result = ""
    for item in soup.findAll("p"):
        cur_text = item.text.replace(" ", "").replace("\n", "").replace("\xa0", "")
        if len(cur_text) > 0:
            result += cur_text
    return get_questions_from_text(result)


def local_load(path) -> List[Question]:
    return load_question_list(path)


def web_load() -> List[Question]:
    driver = driver_get_with_cookies(main_page)
    try:
        goto_result(driver)
        body = driver.find_elements_by_class_name("panel-group")[0]
        result_text = body.text.replace("\n", "")
    finally:
        driver.quit()
    return get_questions_from_text(result_text)


def get_questions_from_text(raw_text) -> List[Question]:
    raw_question_list = re.findall("(?<=\d\.).*?:[0-9]\.[0-9](?=\d*\.\D|[一二三四五六])", raw_text)

    question_list = []
    for question in raw_question_list:
        stem = re.findall("^.*?(?=选项A)", question)[0]

        answers = []
        if question.find("正确答案") != -1:
            raw_answers = re.findall("(?<=选项A:).*(?=正确答案)", question)[0]
        else:
            raw_answers = re.findall("(?<=选项A:).*(?=考生答案)", question)[0]
        answers = re.split("选项.:", raw_answers)

        correct_answers = []
        raw_correct_answers = re.findall("(?<=正确答案:).*(?=考生答案)", question)
        if len(raw_correct_answers) > 0:
            raw_correct_answers = raw_correct_answers[0]
            raw_correct_answers_list = raw_correct_answers.split(",")
            correct_answers = [ord(answer.split("选项")[1]) - ord('A') for answer in raw_correct_answers_list]
            correct_answers = [answers[index] for index in correct_answers]
        question_list.append(Question(stem, answers, correct_answers))
    return question_list
