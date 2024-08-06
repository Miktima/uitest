#!/usr/bin/python3
# -*- encoding=utf8 -*-
#
import sys
sys.path.append('../')

from pages.base import WebPage
import time, re


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import allure


from eaeunion_tests.eaeu_base import Base


class Test(Base):
    project = 'Check Eurasian Econimic Union: Legal Portal'

    def init(self, web_browser):
        self.base_init()
        self.main_page = WebPage(web_browser, self.urlsite)
        self.driver = self.main_page._web_driver
        self.wait = WebDriverWait(self.driver, 10)
    
    @allure.feature('Проверка списка на портале евразийского экономического союза')
    @allure.description("Проверка списка документов по общественным обсуждениям и оценкам регулирующего воздействия\
                        на портале евразийского экономического союза")    
    @allure.story('Проверка списка на портале евразийского экономического союза')
    def test_eaeucheck(self, web_browser):
        # pytest.skip("Временный скип для написания тестовых наборов")
        self.init(web_browser)
        time.sleep(5)

        # Получаем список документов
        trlist_eae = self.driver.find_elements(By.XPATH, "//div[@class='discussionsAndRIA-panel']/table/tbody/tr")
        # В одну строку должны попадать два элемента <tr>
        ntr = 1
        red = re.compile(r"(\d{2}.\d{2}.\d{4}) - (\d{2}.\d{2}.\d{4}) ([\w ]+)")
        for l in trlist_eae:
            if ntr == 2:
                # Проверяем, что указан ответственный департамент
                assert "Ответственный департамент:" in l.text
                # Проверяем подпись после даты
                
            else:
                # Проверяем этам разработки
                assert "Общественное обсуждение" in l.text or "Оценка регулирующего воздействия" in l.text
                ntr = 2


