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
    'Cookie':'lastCity=101010100; wt2=DouFExoGr5TuQOsZSm6KAEt59AENyy_2CnYYvpO00rDdykfrcj8FlHZYUUyqhB23-81p3pF82DXDsbeExkYnXng~~; _bl_uid=e4k7ks7zj2vqO4vkU78a802mb56F; acw_tc=0bccaf0a16294495715668530e31c3fa046df29dc71225df9a4c47b69d8a24; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1629427135,1629449572; __c=1629449572; __l=l=%2Fwww.zhipin.com%2Fc101010100%2F&r=&g=&s=3&friend_source=0&s=3&friend_source=0; __a=28334969.1629427135.1629427135.1629449572.26.2.3.26; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1629449578; __zp_stoken__=c15bcJGw3ckFJblMaUHkfTFdiVDEIRhdhAzp5SB9uPl49HjspEEsNUE4tDwESJSQjfV1HRQJLcgJBYRZlekkqJh9lByUuck5fAWAqd0JPOzcJUQlMSGABKjdEaDwVGz8cTX5XeH1EBnY8Nk1F; __zp_sseed__=rbaK/BX8cib2qPYhdiJ+wmPnSM2TB49Z83E2rbLvtlE=; __zp_sname__=b3e753c4; __zp_sts__=1629449595180'
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
