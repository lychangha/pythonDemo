from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests
from lxml import etree
import time

url = 'https://www.jd.com/'
driver = webdriver.Chrome()
driver.get(url)

driver.find_element(By.ID, 'key').send_keys('笔记本')

driver.find_element(By.TAG_NAME, 'button').click()

time.sleep(5)

driver.execute_script("window.scrollTo(window.pageXOffset, document.body.scrollHeight)")

time.sleep(5)

html = driver.page_source


def getimage(html):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }

    tree = etree.HTML(html)

    element = tree.xpath('//*[@id="J_goodsList"]/ul')
    imgs = []

    for li in element:
        for x in range(1, len(li) + 1):
            if li.xpath('//*[@id="J_goodsList"]/ul/li[' + str(x) + ']/div/div[1]/a/img/@data-lazy-img') == ['done']:
                imgs += li.xpath('//*[@id="J_goodsList"]/ul/li[' + str(x) + ']/div/div[1]/a/img/@src')
            else:
                imgs += li.xpath('//*[@id="J_goodsList"]/ul/li[' + str(x) + ']/div/div[1]/a/img/@data-lazy-img')
    print(len(imgs))

    i = 1
    for imgUrl in imgs:
        imgUrl = "https:" + imgUrl
        print(imgUrl)
        req = requests.get(imgUrl, headers=headers)
        if not (os.path.exists('./file/图片')):
            os.mkdir('./file/图片')
        with open("./file/图片/电脑" + str(i) + ".jpg", 'wb') as f:
            f.write(req.content)
        i += 1

    driver.find_element(By.CLASS_NAME, 'pn-next').click()

    time.sleep(5)


getimage(html)
