from time import sleep
import requests
from selenium import webdriver
from requests.auth import HTTPBasicAuth
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class ImportSolutions:
    chromedriver = r"C:/geckodriver.exe"
    options = webdriver.ChromeOptions()

    def run(self, solutions):
        self.options.add_argument("start-maximized")
        binary = FirefoxBinary('C:/geckodriver.exe')
        browser = webdriver.Firefox(executable_path=r'C:/geckodriver.exe')

        session = requests.Session()
        www_request = session.get('https://is1c.ru/bitrix/admin/',
                                  auth=HTTPBasicAuth('USER', 'PASSWORD'),
                                  allow_redirects=False)

        # add domain
        browser.get("https://is1c.ru/bitrix/admin/")

        # chrome needed to open the page before add the cookies
        cookies = session.cookies.get_dict()
        for key in cookies:
            browser.add_cookie({'name': key, 'value': cookies[key]})

        for solution in solutions:
            browser.get("https://is1c.ru/bitrix/admin/iblock_element_edit.php?IBLOCK_ID=24&type=experience&lang=ru&ID=0&find_section_section=0&IBLOCK_SECTION_ID=0")

            browser.find_element_by_name("NAME").send_keys(solution['solution'] or '')  # Название
            browser.find_element_by_name("ACTIVE_FROM").send_keys(solution['date'] or '')  # Начало активности
            browser.find_element_by_name("PROP[86][n0][VALUE]").send_keys(solution['id'] or '')  # SolutionID
            # browser.find_element_by_name("PROP[87][n0]").send_keys(solution['type'])  # Тип проекта
            browser.find_element_by_name("PROP[171][n0]").send_keys(solution['filter_solution'] or '')  # Внедренное типовое решение (для фильтра)
            browser.find_element_by_name("PROP[88][n0]").send_keys(solution['solution'] or '')  # Внедренное типовое решение
            browser.find_element_by_name("PROP[89][n0]").send_keys(solution['industry'] or '')  # Отрасли
            # browser.find_element_by_name("PROP[90][n0]").send_keys(solution['industry'])  # Область автоматизации
            browser.find_element_by_name("PROP_91__n0__VALUE__TEXT_").send_keys(';'.join(solution['functions'] or []))  # Автоматизированные функции
            browser.find_element_by_name("PROP[92][n0]").send_keys(solution['additionally'] or '')  # Сопровождение

            for _ in solution['done_works'] or []:
                browser.execute_script("BX.IBlock.Tools.addNewRow('tbd76cc124a0f5b70bfe0107004e38d354');")

            for i in range(len(solution['done_works'] or [])):
                browser.find_element_by_name("PROP[93][" + "n" + str(i) + "]").send_keys(solution['done_works'][i] or '')  # Выполненные работы

            # browser.find_element_by_name("PROP[93][n0]").send_keys(solution['done_works'] or '')  # Выполненные работы

            for _ in solution['review_img'] or []:
                browser.execute_script("BX.IBlock.Tools.addNewRow('tb56804784f96dc718e8ea14e36a9a01df');")

            for i in range(len(solution['review_img'] or [])):
                browser.find_element_by_name("PROP[100][" + "n" + str(i) + "]").send_keys(solution['review_img'][i] or '')  # Отзыв (изображение)


            browser.find_element_by_name("PROP[94][n0]").send_keys(solution['company'] or '')  # Компания
            browser.find_element_by_name("PROP[95][n0]").send_keys(solution['city'])  # Город
            browser.find_element_by_name("PROP[96][n0]").send_keys(solution['date'] or '')  # Дата
            browser.find_element_by_name("PROP[97][n0]").send_keys(solution['workplace'] or '')  # АРМ
            browser.find_element_by_name("PROP[98][n0]").send_keys(solution['option_work'] or '')  # Вариант работы
            browser.find_element_by_name("PROP_99__n0__VALUE__TEXT_").send_keys(solution['review'] or '')  # Отзыв

            please = browser.find_element_by_id('save')
            browser.execute_script('arguments[0].click()', please)
