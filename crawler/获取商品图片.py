import os
import requests
from lxml import etree


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

url = 'https://list.jd.com/list.html?cat=670%2C671%2C672&page=1&s=1&click=1'
page_text = requests.get(url=url, headers=headers, timeout=5).content.decode("utf-8")
# print(page_text)

tree = etree.HTML(page_text)
element = tree.xpath('//*[@id="J_goodsList"]/ul')
imgs = []
for li in element:
    imgs += li.xpath('//*[@id="J_goodsList"]/ul/li/div/div[1]/a/img/@data-lazy-img')
i = 1
for imgUrl in imgs:
    imgUrl = "https:" + imgUrl
    # print(imgUrl)
    req = requests.get(imgUrl, headers=headers)
    if not (os.path.exists('../file/图片')):
        os.mkdir('../file/图片')
    with open("../file/图片/电脑" + str(i) + ".jpg", 'wb') as f:
        f.write(req.content)
    i += 1
