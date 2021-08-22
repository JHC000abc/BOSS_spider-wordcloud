'''
BOSS爬虫
'''

from pymongo import *
import requests
from lxml import etree

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
cookies = {
    'Cookie':''
}
for i in range(0,11):
    response = requests.get('https://www.zhipin.com/c101010100/?page='+str(i)+'&ka=page-10',headers=headers,cookies=cookies)
    response.encoding='utf8'

    with open('./boss.txt','a',encoding='utf8') as fp:
        fp.write(response.text)

with open('./boss.txt',encoding='utf8') as fp:
    a = fp.read()
    # print(a)
# w_name = re.findall('\.html\" title=(.*?) target\=',a)
# print(w_name)
list = []
tree = etree.HTML(a)
lis = tree.xpath('//div[@class="job-list"]/ul/li')
for li in lis:
    c_url = li.xpath('.//span[@class="job-name"]/a/@href')
    # c_HRname = li.xpath('.//span[@class="red"]/text()')
    w_name = li.xpath('.//span[@class="job-name"]/a/text()')[0]
    money = li.xpath('.//span[@class="red"]/text()')[0]
    c_name = li.xpath('.//h3[@class="name"]/a/text()')[0]
    zhuangtai = li.xpath('.//div[@class="company-text"]/p/text()')[0]
    url = 'https://www.zhipin.com'+c_url[0]


    data =  {
        "薪资":money,
        "职位名":w_name,
        "融资状态":zhuangtai,
        "链接地址":url,
        "公司名":c_name,
    }
    list.append(data)




def insert():
    try:
        client = MongoClient(host='localhost',port=27017)
        db = client.BOSS
        db.message2.insert_many(list)


    except Exception as e:
        print(e)

if __name__ == '__main__':
    insert()
