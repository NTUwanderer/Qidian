#!/usr/bin/env python3
# coding=utf-8
# author:sakuyo
#----------------------------------
import requests,sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver

class downloader(object):
    def __init__(self,target):#初始化
        self.target = target
        self.chapterNames = []
        self.chapterHrefs = []
        self.chapterNum = 0
        self.session = requests.Session()
        # options = webdriver.ChromeOptions()
        # options.binary="/usr/bin/google-chrome-stable"
        # options.add_argument('user-data-dir=/home/harvey/.config/google-chrome/Default')
        # self.browser = webdriver.Chrome(options=options)
        self.browser = webdriver.Chrome()
    def GetChapterContent(self):#獲取章節內容
        self.browser.get(self.target)
        time.sleep(3)
        html = self.browser.page_source

        bf = BeautifulSoup(html,"html.parser")

        # update the next chapter
        nextChapter = bf.find('a', id='j_chapterNext')
        self.target = 'https:'+nextChapter.get('href')
        print('target: ', self.target)

        textContent = []

        mainTextWrapDiv = bf.find('div',class_='main-text-wrap')

        # Get Charter Name
        textHeadDiv = mainTextWrapDiv.find('div',class_='text-head')
        chapterNameH = textHeadDiv.find('h3',class_='j_chapterName')
        # chatperNameSpans = textHeadDiv.find_all('span',class_='content-wrap')
        textContent.append(chapterNameH.text)

        # Get Context
        readContentDiv = mainTextWrapDiv.find('div',class_='read-content j_readContent')
        readContent = readContentDiv.find_all('span',class_='content-wrap')
        for content in readContent:
            if content.string == '':
                print('error format')
            else:
                textContent.append(content.string)
                print('content.string: ', content.string)
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
    maxLength = 3
    for i in range(maxLength):
        try:
            dlObj.writer('output.txt',dlObj.GetChapterContent())
        except Exception:
            print('下載出錯，已跳過')
            pass
        sys.stdout.write("  已下載:%.3f%%" %  float(100.0 * (i+1)/maxLength) + '\r')
        sys.stdout.flush()
    print('下載完成')
