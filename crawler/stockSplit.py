import requests
from lxml import etree
import xlwt
from datetime import datetime
from dateutil.relativedelta import relativedelta

ratioList = []
for num in range(0, 24):
    timeParam = (datetime.today().replace(day=1) - relativedelta(months=num)).strftime("%m/%d/%Y")
    print("时间：" + timeParam)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    url = 'https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=splits&begindate=' + timeParam
    page_text = requests.get(url=url, headers=headers, timeout=5).content.decode("utf-8")

    tree = etree.HTML(page_text)
    element = tree.xpath('//*[@id="messageTable4"]/tbody/tr')

    lst = []
    for tr in element:
        symbol = tr.xpath('.//td/a//text()')
        str1 = ''
        # normalize-space() 去掉/r/t等字符
        for i in tr.xpath('normalize-space(.//td/text())'):
            str1 += i
        symbol.append(str1)
        symbol = list(filter(None, symbol))
        row = []
        row += tr.xpath('.//th/a//text()')
        row += symbol
        row += tr.xpath('.//td/text()')[-4:]
        lst.append(row)
    for ls in lst:
        if (ls[2].split(":"))[0] > (ls[2].split(":"))[1]:
            ratioList.append(ls)
print("共计" + str(len(ratioList)) + "条")


def write_to_excel(filename, lst):
    try:
        # 1、创建excel表格类型文件
        work_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # 2、在excel表中创建一张sheet表单
        sheet = work_book.add_sheet("sheet1", cell_overwrite_ok=True)
        # 3、自定义表头
        col = ('Company', 'Symbol', 'Split Ratio', 'Announcement Date', 'Record Date', 'Ex-Date')
        # 4、将表头写入sheet表单中
        for x in range(0, 6):
            sheet.write(0, x, col[x])
        # 5、将数据写进sheet表单中
        for n in range(0, len(lst)):
            data = lst[n]
            for m in range(0, 6):
                sheet.write(n + 1, m, data[m])
        savePath = '../file/' + filename + '.xls'
        work_book.save(savePath)
        print("写入成功")
    except Exception:
        print("写入失败")


write_to_excel("拆股数据", ratioList)
