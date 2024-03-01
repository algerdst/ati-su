from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import re

import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")


def login_func(browser):
    """
    Авторизация
    """
    browser.get('https://id.ati.su/login/')
    # login_field = browser.find_element(By.CLASS_NAME, 'ati-core-login-wrapper').find_element(By.CSS_SELECTOR, 'input')
    # password_field = browser.find_element(By.CLASS_NAME, 'password-wrapper').find_element(By.CSS_SELECTOR, 'input')
    # login_field.send_keys('krendelyangarik@mail.ru')
    # password_field.send_keys('rTYyUi4D1ri(')
    # button = browser.find_element(By.CLASS_NAME, 'ati-core-button')
    # button.click()
    # time.sleep(20)
    # pickle.dump(browser.get_cookies(), open("cookies", 'wb'))
    for cookie in pickle.load(open('cookies', 'rb')):
        browser.add_cookie(cookie)
    browser.refresh()


def fing_cargos(browser):
    """
    Найти грузы
    """
    browser.get('https://loads.ati.su/?utm_source=header&utm_campaign=new_header')
    from_input = browser.find_elements(By.CLASS_NAME, 'input-wrapper_JaqEh')[0].find_element(By.TAG_NAME, 'input')
    where_input = browser.find_elements(By.CLASS_NAME, 'input-wrapper_JaqEh')[1].find_element(By.TAG_NAME, 'input')
    weight_input = browser.find_element(By.CLASS_NAME, 'MinMax_minInput__DEdbP').find_element(By.TAG_NAME, 'input')
    find_cargo = browser.find_element(By.CLASS_NAME, 'dropdown-button-wrapper_vTb-d').find_element(By.TAG_NAME,
                                                                                                   'button')
    from_input.click()
    from_input.clear()
    from_input.send_keys('самара')
    time.sleep(1)
    browser.find_element(By.CLASS_NAME, 'Geo_suggestion__FxHag').click()
    where_input.click()
    where_input.clear()
    where_input.send_keys('москва')
    time.sleep(1)
    browser.find_element(By.CLASS_NAME, 'Geo_suggestion__FxHag').click()
    weight_input.click()
    weight_input.clear()
    weight_input.send_keys(10)
    find_cargo.click()
    time.sleep(5)


with webdriver.Chrome(options) as browser:
    login_func(browser)
    fing_cargos(browser)
    time.sleep(5)
    try:
        max_page = int(browser.find_element(By.CLASS_NAME, 'total-index_kjYkG').text)
    except:
        max_page = 1
    next_page = browser.find_element(By.CSS_SELECTOR, 'button.next_FJXnH')
    count = 0
    for page in range(max_page):
        if page == 0:
            continue
        blocks = browser.find_elements(By.CSS_SELECTOR, 'div.fOZ4h')
        for block in blocks:
            try:
                block.find_element(By.CLASS_NAME, 'glz-button').click()
            except:
                pass
            items = [
                m.group()
                for m in re.finditer(r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", block.text)
            ]
            number=''
            for i in items:
                if i[0] == '+':
                    number+=i
                    number+=' '
            print(number)
            count+=1
        next_page.click()
        time.sleep(2)
print(count)
