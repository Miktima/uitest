#!/usr/bin/python3
# -*- encoding=utf8 -*-
#
import sys
sys.path.append('../')

from pages.base import WebPage
import time, re
from datetime import date


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
                flist = red.findall(l.text)
                sstartdate = (flist[0][0]).split(".")
                startdate = date(sstartdate[2], sstartdate[1], sstartdate[0])
                senddate = (flist[0][1]).split(".")
                enddate = date(senddate[2], senddate[1], senddate[0])
                td = date.today()
                if td == startdate:
                    assert "Создан" in flist[0][2]
                elif td > startdate and td <= enddate:
                    assert "Идет обсуждение" in flist[0][2]
                elif td > enddate:
                    assert "Обсуждение завершено" in flist[0][2]
                else:
                    assert False # Непонятная дата обсуждения
            else:
                # Проверяем этап разработки
                assert "Общественное обсуждение" in l.text or "Оценка регулирующего воздействия" in l.text
                ntr = 2

    @allure.feature('Проверка списка на портале евразийского экономического союза')
    @allure.description("Проверка списка документов по общественным обсуждениям и оценкам регулирующего воздействия\
                        на портале евразийского экономического союза")    
    @allure.story('Проверка фильтра по ответственному департаменту')
    def test_eaeucheckdep(self, web_browser):
        # pytest.skip("Временный скип для написания тестовых наборов")
        self.init(web_browser)
        time.sleep(5)
        self.driver.find_element(By.XPATH, "//div[@class='cr-col-left']/div[@class='filters']\
                                 /div[@data-name='npbdiscussiondepartmentresponsibletaxId']/a").click()
        time.sleep(5)
        iframe_el = self.driver.find_element(By.XPATH, "//div[@class='ms-dlgFrameContainer']/iframe")
        self.driver.switch_to.frame(iframe_el)
        divlist_el = self.driver.find_elements(By.XPATH, "//div[@id='ctl00_PlaceHolderMain_DeltaApplication1__scopeid']/div[@class='tree']/\
                                               div/div")
        for nel in range(1, len(divlist_el) + 1):
            lbl = self.driver.find_element(By.XPATH, "//div[@id='ctl00_PlaceHolderMain_DeltaApplication1__scopeid']/div[@class='tree']/\
                                               div/div[" + str(nel) + "]/label")
            if "Департамент конкурентной политики и политики в области государственных закупок" in lbl.text:
                lbl.click()
                self.driver.find_element(By.XPATH, "//div[@id='ctl00_PlaceHolderMain_DeltaApplication1__scopeid']/div[@class='buttons']\
                                               /button").click()
                break
        time.sleep(5)
        trlist_eae = self.driver.find_elements(By.XPATH, "//div[@class='discussionsAndRIA-panel']/table/tbody/tr")
        # В одну строку должны попадать два элемента <tr>
        ntr = 1
        for l in trlist_eae:
            if ntr == 2:
                # Проверяем, что указан ответственный департамент
                assert "Ответственный департамент: Департамент конкурентной политики и политики в области государственных закупок" in l.text
            else:
                ntr = 2


