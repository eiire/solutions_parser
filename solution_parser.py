import math

from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json


class SolutionsParser:
    chromedriver = r"C:/chromedriver.exe"
    options = webdriver.ChromeOptions()

    def get_base_info_solutions(self, log=True):
        self.options.add_argument('headless')
        # self.options.add_argument("start-maximized")
        browser = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.options)
        browser.get("https://1c.ru/solutions/public/?searchModel=%7B%22itemsPerPage%22:100,%22pageNumber%22:1,%22orderBy%22:%5B%5D,%22archive%22:true,%22onlyTitle%22:true,%22fraze%22:true,%22firstSolutionsDate%22:%222021-03-15T17:00:00.000Z%22,%22findByCompanyGroup%22:true,%22regions%22:%5B%5D,%22fresh%22:true,%22grm%22:true,%22partner%22:%7B%22id%22:5689,%22commercename%22:%22%D0%98%D0%BD%D1%84%D0%BE%D0%A1%D0%BE%D1%84%D1%82%22,%22cityName%22:%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%7D%7D")
        page = browser.page_source
        soup = BeautifulSoup(page, 'html5lib')
        count_pages = int(math.ceil(int(soup.find_all('div', attrs={'mat-paginator-range-label'})[0].text.split('of')[1]) / 100))
        print(count_pages, ' count pages')

        base_solutions_res = []
        for page_numb in reversed(range(count_pages)):
            base_table_url = f"https://1c.ru/solutions/public/?searchModel=%7B%22itemsPerPage%22:100,%22pageNumber%22:{page_numb + 1},%22orderBy%22:%5B%5D,%22archive%22:true,%22onlyTitle%22:true,%22fraze%22:true,%22firstSolutionsDate%22:%222021-03-15T17:00:00.000Z%22,%22findByCompanyGroup%22:true,%22regions%22:%5B%5D,%22fresh%22:true,%22grm%22:true,%22partner%22:%7B%22id%22:5689,%22commercename%22:%22%D0%98%D0%BD%D1%84%D0%BE%D0%A1%D0%BE%D1%84%D1%82%22,%22cityName%22:%22%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D0%B8%D0%B1%D0%B8%D1%80%D1%81%D0%BA%22%7D%7D"
            browser.get(base_table_url)
            sleep(2)

            browser.execute_script(
                'function pageScroll() {window.scrollBy(0,100);scrolldelay = setTimeout(pageScroll,1);};pageScroll()'
            )
            sleep(2)

            page = browser.page_source
            soup = BeautifulSoup(page, 'html5lib')
            table = soup.findChildren('table')
            introducing = table[0]
            rows = introducing.findChildren(['tr'])

            for row in reversed(rows):
                cells = row.findChildren('td')

                try:
                    base_solutions_res.append({
                        'id': ((list(iter(cells))[1]).findChildren('a'))[0].attrs["href"].split('/')[-1],
                        'city': list(iter(cells))[0].text,
                        'solution': list(iter(cells))[1].text,
                        'date': list(iter(cells))[-1].text,
                        'detail_url': 'https://1c.ru' + ((list(iter(cells))[1]).findChildren('a'))[0].attrs["href"],
                    })
                except:
                    pass

            if log:
                print(page_numb, ' page is done parse')  # log

        return base_solutions_res

    def update_solutions_info(self, base_solutions, safe_update=False, log=True):
        # self.options.add_argument('start-maximized')
        self.options.add_argument('headless')
        # self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.options)

        for solution in base_solutions:
            if 'company' not in solution and 'detail_url' in solution:  # begin from last update
                browser.get(solution.get('detail_url'))
                sleep(2)

                browser.execute_script(
                    'function pageScroll() {window.scrollBy(0,80);scrolldelay = setTimeout(pageScroll,1);};pageScroll()'
                )
                sleep(2)

                page = browser.page_source
                soup = BeautifulSoup(page, 'html5lib')

                solution.update({
                    'company': SolutionsParser.__get_value(soup, SolutionsParser.__contains_company, 'div',
                                                           {'class': "big-1-font-size"}),
                    'filter_solution': SolutionsParser.__get_value(soup, SolutionsParser.__contains_filter_solution,
                                                                   'div', {'class': 'big-1-font-size'}),
                    'additionally': SolutionsParser.__get_value(soup, SolutionsParser.__contains_additionally,
                                                                'app-spots-tree-item', {'class': "ng-star-inserted"},
                                                                parent=True, multiple_val=True),
                    'functions': SolutionsParser.__get_value(soup, SolutionsParser.__contains_functions,
                                                             'span', {'class': 'fas fa-map-pin ng-star-inserted'},
                                                             parent=True, multiple_val=True),
                    'done_works': SolutionsParser.__get_value(soup, SolutionsParser.__contains_done_works,
                                                              'span', {'class': 'fas fa-map-pin ng-star-inserted'},
                                                              parent=True, multiple_val=True),
                    'industry': SolutionsParser.__get_value(soup, SolutionsParser.__contains_industry,
                                                            'div', {'class': 'mat-chip-ripple'},
                                                            parent=True, multiple_val=True),
                    'review': SolutionsParser.__get_value(soup, SolutionsParser.__contains_review,
                                                          'div', {'class': 'mat-expansion-panel-content'}),
                    'workplace': SolutionsParser.__get_value(soup, SolutionsParser.__contains_workplace,
                                                             'div', {'class': 'big-1-font-size'}),
                    'option_work': SolutionsParser.__get_value(soup, SolutionsParser.__contains_option_work,
                                                               'mat-card-content', {'class': 'mat-card-content'},
                                                               multiple_val=True),
                    'description': SolutionsParser.__get_value(soup, SolutionsParser.__contains_description,
                                                               'mat-card-content',
                                                               {'class': 'mat-card-content'}),
                    'review_img': SolutionsParser.__get_value(soup, SolutionsParser.__contains_review_img, None, None,
                                                              find_imgs=True),
                })

                if log:
                    print(solution)  # log

                if safe_update:
                    with open("incomplete_result.json", "w", encoding="utf-8") as file:
                        json.dump(base_solutions, file, indent=4)

        return base_solutions  # after update

    @staticmethod
    def __get_bs_objs(elem, text) -> list:
        # is an element, not text and any NavigableText child elements contain the word in text var
        return getattr(elem, 'name', None) \
               and any(text in child for child in elem.children if not getattr(child, 'name', None))

    @staticmethod
    def __get_value(soup, func, teg, attrs, parent=False, multiple_val=False, find_imgs=False):
        if find_imgs:
            return ['https://1c.ru/solutions/public/' + el.attrs['href']
                    for el in soup.find_all(func)[0].parent.parent.parent.parent.parent.find_all('a', attrs={'data-type': 'image'})] \
                if soup.find_all(func) and len(soup.find_all(func)[0].parent.parent.parent.parent.parent
                                               .find_all('a')) > 0 \
                else None

        if soup.find_all(func) and soup.find_all(func)[0].parent.parent.parent.parent.parent.find_all(teg, attrs=attrs):
            if len(soup.find_all(func)[0].parent.parent.parent.parent.parent.find_all(teg, attrs=attrs)) >= 1 \
                    and parent and multiple_val:
                return [
                    el.parent.text for el in soup.find_all(func)[0].parent.parent.parent.parent.parent
                      .find_all(teg, attrs=attrs)
                ]
            elif len(soup.find_all(func)[0].parent.parent.parent.parent.parent.find_all(teg, attrs=attrs)) >= 1 \
                    and multiple_val:
                return [
                    el.text for el in soup.find_all(func)[0].parent.parent.parent.parent.parent
                      .find_all(teg, attrs=attrs)
                ]
            elif len(soup.find_all(func)[0].parent.parent.parent.parent.parent.find_all(teg, attrs=attrs)) == 1 \
                    and not multiple_val:
                return soup.find_all(func)[0].parent.parent.parent.parent.parent.find_all(teg, attrs=attrs)[0].text
        else:
            return None

    @staticmethod
    def __contains_company(elem):
        return SolutionsParser.__get_bs_objs(elem, ' Пользователь ')

    @staticmethod
    def __contains_filter_solution(elem):
        return SolutionsParser.__get_bs_objs(elem, 'Внедренное типовое решение')

    @staticmethod
    def __contains_additionally(elem):
        return SolutionsParser.__get_bs_objs(elem, 'Сопровождение')

    @staticmethod
    def __contains_functions(elem):
        return SolutionsParser.__get_bs_objs(elem, ' Автоматизированы функции ')

    @staticmethod
    def __contains_done_works(elem):
        return SolutionsParser.__get_bs_objs(elem, ' Выполнены работы ')

    @staticmethod
    def __contains_industry(elem):
        return SolutionsParser.__get_bs_objs(elem, 'Отрасль')

    @staticmethod
    def __contains_review(elem):
        return SolutionsParser.__get_bs_objs(elem, ' Текст отзыва ')

    @staticmethod
    def __contains_workplace(elem):
        return SolutionsParser.__get_bs_objs(elem, 'Автоматизированных рабочих мест')

    @staticmethod
    def __contains_option_work(elem):
        return SolutionsParser.__get_bs_objs(elem, 'Вариант работы')

    @staticmethod
    def __contains_type(elem):
        return SolutionsParser.__get_bs_objs(elem, 'Версия 1С:Предприятия')

    @staticmethod
    def __contains_review_img(elem):
        return SolutionsParser.__get_bs_objs(elem, ' Пользователь ')

    @staticmethod
    def __contains_description(elem):
        return SolutionsParser.__get_bs_objs(elem, ' Описание ')
