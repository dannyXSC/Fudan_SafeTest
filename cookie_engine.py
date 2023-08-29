import json
import os
import time
from selenium import webdriver

from environment import cookie_path, input_wait_time, auth_url, driver_path, if_load_cookie, main_page


def load_cookies(log_url, browser, path=cookie_path):
    """
    获取cookies保存至本地
    """
    browser.get(log_url)
    time.sleep(input_wait_time)
    dictCookies = browser.get_cookies()  # 获取list的cookies
    jsonCookies = json.dumps(dictCookies)  # 转换成字符串保存

    with open(path, 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')


def get_cookies(browser, path=cookie_path):
    with open(path, 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        browser.add_cookie(cookie)


def driver_get_with_cookies(url, path=cookie_path):
    browser = webdriver.Chrome(executable_path=driver_path)

    if not os.path.exists(path) or if_load_cookie:
        try:
            load_cookies(auth_url, browser, path)
        finally:
            browser.quit()
            browser = webdriver.Chrome(executable_path=driver_path)

    browser.get(url)
    get_cookies(browser, path)
    browser.refresh()
    time.sleep(5)
    return browser


if __name__ == "__main__":
    driver = driver_get_with_cookies(main_page)
    input()
    driver.quit()
