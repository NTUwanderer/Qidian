#!/usr/bin/env python3
# coding=utf-8
# author:sakuyo
#----------------------------------
import requests,sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def GetContext(browser):
    html = browser.page_source
    bf = BeautifulSoup(html,"html.parser")

    mainTextWrapDiv = bf.find('div',class_='main-text-wrap')
    readContentDiv = mainTextWrapDiv.find('div',class_='read-content j_readContent')
    return readContentDiv.find_all('span',class_='content-wrap')

class downloader(object):
    def __init__(self,target):#初始化
        self.target = target

        # executor_url = ''
        # session_id = ''
        # self.browser = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        # self.browser.session_id = session_id
        self.browser = webdriver.Chrome()
        try:
            self.SwitchTC()
        except Exception:
            print('Failed to switch to TC')

    def SwitchTC(self):
        self.browser.get('https://qidian.com')
        tc_element = self.browser.find_element_by_id('switchEl')
        tc_element.click()
        print('executor_url: ', self.browser.command_executor._url)
        print('session_id: ', self.browser.session_id)

    def GetChapterContent(self):#獲取章節內容
        self.browser.get(self.target)
        WebDriverWait(self.browser, timeout=10).until(GetContext)

        html = self.browser.page_source

        bf = BeautifulSoup(html,"html.parser")

        # update the next chapter
        nextChapter = bf.find('a', id='j_chapterNext')
        self.target = 'https:'+nextChapter.get('href')

        textContent = []

        mainTextWrapDiv = bf.find('div',class_='main-text-wrap')

        # Get Charter Name
        textHeadDiv = mainTextWrapDiv.find('div',class_='text-head')
        chapterNameH = textHeadDiv.find('h3',class_='j_chapterName')
        index = chapterNameH.text.find('\n', 1)
        textContent.append(chapterNameH.text[1:index])

        # Get Context
        readContentDiv = mainTextWrapDiv.find('div',class_='read-content j_readContent')
        readContent = readContentDiv.find_all('span',class_='content-wrap')
        for content in readContent:
            if content.string == '':
                print('error format')
            else:
                textContent.append(content.string)
        return textContent
    def writer(self, path, content=[]):
        write_flag = True
        with open(path, 'a', 1024) as f: # a: append
            for line in content:
                f.write(line)
                f.write('\n\n')

            f.write('\n')

if __name__ == '__main__':#執行層
    target = 'https://read.qidian.com/chapter/3Q__bQt6cZEVDwQbBL_r1g2/GSlTBhSdiqP4p8iEw--PPw2'
    dlObj = downloader(target)

    print('開始下載：')
    maxLength = 130
    for i in range(maxLength):
        dlObj.writer('output.txt',dlObj.GetChapterContent())
        # try:
        #     dlObj.writer('output.txt',dlObj.GetChapterContent())
        # except Exception:
        #     print('下載出錯，已跳過')
        #     pass
        sys.stdout.write("  已下載:%.3f%%" %  float(100.0 * (i+1)/maxLength) + '\r')
        sys.stdout.flush()
    print('下載完成')
