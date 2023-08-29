import time

from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from fuzzywuzzy import process


def take_exam(driver: WebDriver):
    # 进行实验室安全在线校级卷
    # 进入选择考场界面
    page1_enter_list = driver.find_elements_by_class_name("fl")
    for candidate in page1_enter_list:
        if candidate.text.replace(" ", "") == "在线考试":
            candidate.click()
            break
    time.sleep(2)
    # 确认
    check_btn_list = driver.find_elements_by_tag_name("button")
    for candidate in check_btn_list:
        if candidate.text.replace(" ", "") == "确认":
            candidate.click()
            break
    # 进入考场
    page2_enter_list = driver.find_elements_by_class_name("fl")
    for candidate in page2_enter_list:
        if candidate.text.find("实验室安全在线校级卷") != -1:
            enter_btn = candidate.find_element_by_id("intoExamRoom")
            enter_btn.click()
            break
    time.sleep(2)
    # 开始考试
    begin_btn = driver.find_element_by_id("examOnlineStrat")
    begin_btn.click()


def goto_result(driver: WebDriver):
    page1_enter_list = driver.find_elements_by_class_name("fl")
    for candidate in page1_enter_list:
        if candidate.text.replace(" ", "") == "考试成绩查询及合格证打印":
            candidate.click()
            break
    time.sleep(2)

    # 进入错题界面
    # 点击最近一次的错题
    driver.find_elements_by_class_name("odd")[0].find_elements_by_tag_name("a")[0].click()
    time.sleep(5)

    # 切换窗口
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])


def goto_next_question(driver: WebDriver):
    btns = driver.find_elements_by_tag_name("button")
    for btn in btns:
        if btn.text == "下一题":
            btn.click()
            break


def answer_question(driver: WebDriver, question_dict: dict):
    question_stem_list = list(question_dict.keys())
    question_area = driver.find_elements_by_class_name("exams")[0]

    stem = question_area.find_elements_by_tag_name("p")[0].text
    match_question_stem = process.extract(stem, question_stem_list, limit=1)[0][0]
    match_question = question_dict[match_question_stem]
    correct_answers = match_question.correct_answers_set
    print("匹配问题：{}".format(match_question.to_dict()))

    cnt = 0
    answers = question_area.find_elements_by_id("radiolist")
    for answer in answers:
        answer_text = answer.text[2:]
        if answer_text in correct_answers:
            answer.find_elements_by_tag_name("div")[0].click()
            cnt += 1
    return cnt


def answer_all_question(driver: WebDriver, question_dict: dict):
    cnt = 0
    while cnt < 100:
        answer_question(driver, question_dict)
        goto_next_question(driver)
        cnt += 1
        time.sleep(5)
